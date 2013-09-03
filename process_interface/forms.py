from collections import defaultdict
from operator import itemgetter as iget
import re

from django import forms as F
from django.db.models import Max
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from models import (
  Process,
  Vintage,
  Param_CostFixed,
  Param_CostVariable,
  Param_Efficiency,
  Param_LifetimeTech,
  Param_LifetimeTechLoan,
  Set_commodity_emission,
  Set_commodity_physical,
  Set_commodity_output
)

from IPython import embed as II


class ProcessForm ( F.Form ):
	"""
	Given a process, this form will automatically provide the appropriate
	"""
	discountrate = F.FloatField( required=False, label=_('Discount Rate') )
	lifetime     = F.FloatField( required=False, label=_('Lifetime') )
	loanlife     = F.FloatField( required=False, label=_('Loan Lifetime') )

	def __init__ ( self, process, *args, **kwargs ):
		cur_cfr, all_cfr = kwargs.pop( 'CostFixedRows',    ((), ()) )
		cur_cvr, all_cvr = kwargs.pop( 'CostVariableRows', ((), ()) )
		cur_effr = kwargs.pop( 'EfficiencyRows',       () )
		cur_emar = kwargs.pop( 'EmissionActivityRows', () )
		super(ProcessForm, self).__init__(*args, **kwargs)
		prefix = kwargs.get( 'prefix', '' )

		p = self.process = process
		t = p.technology
		a = p.analysis
		flds = self.fields

		t_life = Param_LifetimeTech.objects.filter(analysis=a, technology=t)
		l_life = Param_LifetimeTechLoan.objects.filter(analysis=a, technology=t)
		t_life = t_life and t_life[0].value or None
		l_life = l_life and l_life[0].value or None

		def setUpField ( name, default=None, fmt='{}' ):
			value = getattr(p, name, None)
			if value:
				flds[ name ].initial = value
			if default:
				flds[ name ].widget.attrs.update({
				  'placeholder' : fmt.format( default ) })

		setUpField( 'discountrate', a.global_discount_rate, '{} (GDR)' )
		setUpField( 'lifetime', t_life, '{} (class)' )
		setUpField( 'loanlife', l_life, '{} (class)' )

		if p.vintage.vintage < a.period_0:
			flds['existingcapacity'] = F.FloatField(
			  required=False,
			  label=_('Existing Capacity')
			)
			setUpField('existingcapacity')
		else:
			flds['costinvest'] = F.FloatField(
			  required=False,
			  label=_('Investment Cost')
			)
			setUpField('costinvest')


	def clean_lifetime ( self ):
		life = self.cleaned_data['lifetime']
		p = self.process
		a = p.analysis

		if not life:
			return life

		# Ensure that value reaches to at least the first period from process
		# vintage.  Note that this is _not_ done at the DB level because a model
		# may be in flux (i.e. a modeler is changing the structure of the data).
		# Meanwhile, this check *will* be performed when downloading the complete
		# dat file.
		if life + p.vintage.vintage <= a.period_0:
			msg = ('Process lifetime guarantees no use in model optimization.  '
			  'Consider extending the lifetime, or changing the analysis start '
			  'year.'
			)
			raise F.ValidationError( msg )

		return life



class EfficiencyForm ( F.Form ):
	inp    = F.ChoiceField( label=_('Input'),  widget=F.TextInput )
	out    = F.ChoiceField( label=_('Output'), widget=F.TextInput )
	eff    = F.FloatField( required=False, label=_('Percent') )

	def __init__( self, *args, **kwargs ):
		analysis = kwargs.pop( 'analysis' )
		pk  = kwargs.pop( 'pk',  None )
		inp = kwargs.pop( 'inp', None )
		out = kwargs.pop( 'out', None )
		eff = kwargs.pop( 'eff', None )
		inp_choices = kwargs.pop( 'inp_choices', None )
		out_choices = kwargs.pop( 'out_choices', None )

		if not inp_choices:
			inp_choices = EfficiencyForm.getInputChoices( analysis )
		if not out_choices:
			out_choices = EfficiencyForm.getOutputChoices( analysis )

		super( EfficiencyForm, self ).__init__( *args, **kwargs )

		flds = self.fields
		flds['inp'].initial = inp
		flds['out'].initial = out
		flds['eff'].initial = eff

		flds['inp'].choices = inp_choices
		flds['out'].choices = out_choices

		if pk:
			flds['inp'].widget.attrs.update( readonly=True )
			flds['out'].widget.attrs.update( readonly=True )

		self.pk = pk


	@classmethod
	def getInputChoices ( cls, analysis ):
		choices = [ (cp.commodity.name, cp.commodity.name)
		  for cp in Set_commodity_physical.objects.filter(analysis=analysis)
		]

		return choices

	@classmethod
	def getOutputChoices ( cls, analysis ):
		choices = [ (cp.commodity.name, cp.commodity.name)
		  for cp in Set_commodity_output.objects.filter(analysis=analysis)
		]

		return choices



def getEfficiencyForm ( analysis, efficiency, *args, **kwargs ):
	kwargs.update(
	  analysis=analysis,
	  pk=efficiency.pk,
	  inp=efficiency.inp_commodity.commodity,
	  out=efficiency.out_commodity.commodity,
	  eff=efficiency.value
	)

	return EfficiencyForm( *args, **kwargs )


def getEfficiencyForms ( analysis, efficiencies, *args, **kwargs ):
	forms = []
	if not efficiencies:
		return forms

	inp_choices = EfficiencyForm.getInputChoices( analysis )
	out_choices = EfficiencyForm.getOutputChoices( analysis )

	kwargs.update(
	  analysis=analysis,
	  inp_choices=inp_choices,
	  out_choices=out_choices
	)
	for pk, (inp, out, eff) in sorted( efficiencies.iteritems(), key=iget(1) ):
		kwargs.update( pk=pk, inp=inp, out=out, eff=eff )
		forms.append( EfficiencyForm( *args, **kwargs ))

	return forms


def getFormCostRows ( param_type, process ):
	cls = { 'fixed' : Param_CostFixed, 'variable' : Param_CostVariable }
	param = cls[ param_type ]

	p    = process
	v    = p.vintage.vintage    # cannot be null
	a    = p.analysis           # cannot be null
	life = p.lifetime           # /could/ be null,
	p_0  = a.period_0

	if not life:
		t = p.technology
		plt = Param_LifetimeTech.objects.filter( analysis=a, technology=t )
		if plt:
			life = plt[0].value
		else:
			return []

	final_year = Vintage.objects.filter( analysis=a )
	final_year = final_year.aggregate( Max('vintage') )['vintage__max']

	active_periods = Vintage.objects.filter(
	  analysis=a,
	  vintage__gte=max(v, p_0),
	  vintage__lt=min(v + life, final_year)
	).distinct().order_by('vintage')

	cq = param.objects.filter(process=p, period__in=active_periods)
	cq = cq.order_by('period__vintage')

	rows = [ (c.period.vintage, c.value) for c in cq ]
	if len( rows ) < len( active_periods ):
		rows.insert( 0, (None, None) )

	return rows, active_periods


def getFormEfficiencyRows ( efficiencies ):
	if efficiencies:
		eff = [
		  (pk, (inp, out, val))

		  for pk, (inp, out, val) in efficiencies.iteritems()
		  ]
	else:
		eff = []

	eff.sort( key=iget(1) )
	eff.insert( 0, (None, (None, None, None)) )

	return eff


def getFormEmissionActivityRows ( emactivities, process ):
	if emactivities:
		ems = [
		  (pk, (pol, inp, out, val))

		  for pk, (pol, inp, out, val) in emactivities.iteritems()
		]
	else:
		ems = []

	effs = Param_Efficiency.objects.filter( process=process )
	if len( effs ) > len( ems ):
		ems.insert( 0, (None, (None, None, None, None)) )

	return ems
