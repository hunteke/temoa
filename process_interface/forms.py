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
  Param_LifetimeTech,
  Param_LifetimeTechLoan,
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

		costfixed = []
		periods_available = set( (p.vintage, p.vintage) for p in all_cfr )
		dkey = 'id_{}costfixed_datalist'.format( str(prefix) + '-' )
		for per, val in cur_cfr:
			pkey, vkey = (
			  'costfixed_{}_period'.format(per),
			  'costfixed_{}_value'.format(per)
			)
			flds[ pkey ] = F.ChoiceField(
			  label=_('Period'),
			  widget=F.TextInput,
			  required=False )
			flds[ vkey ] = F.FloatField(
			  label=_('Fixed Cost'),
			  required=False )

			if per and val:
				forced_choice = set( ((per, per),) )
				flds[ pkey ].widget.attrs['readonly'] = True
				flds[ pkey ].choices = forced_choice
				flds[ pkey ].initial = per
				flds[ vkey ].initial = val

				periods_available -= forced_choice
			else:
				new_key = pkey

			costfixed.append( (self[pkey], self[vkey]) )

		if periods_available:
			periods_available = sorted( periods_available )
			self.costfixed_datalist = [ i[0] for i in periods_available ]
			self.costfixed_datalist_id = dkey

			# And, for completeness ...
			flds[ new_key ].choices = periods_available
			flds[ new_key ].widget.attrs.update({ 'list' : dkey })

		costvariable = []
		periods_available = set( (p.vintage, p.vintage) for p in all_cfr )
		dkey = 'id_{}costvariable_datalist'.format( str(prefix) + '-' )
		for per, val in cur_cvr:
			pkey, vkey = (
			  'costvariable_{}_period'.format(per),
			  'costvariable_{}_value'.format(per)
			)
			flds[ pkey ] = F.ChoiceField(
			  label=_('Period'),
			  initial=per if per else '',
			  widget=F.TextInput,
			  required=False )
			flds[ vkey ] = F.FloatField(
			  label=_('Variable Cost'),
			  required=False )

			if per and val:
				forced_choice = set( ((per, per),) )
				flds[ pkey ].widget.attrs['readonly'] = True
				flds[ pkey ].choices = forced_choice
				flds[ vkey ].initial = val

				periods_available -= forced_choice
			else:
				new_key = pkey

			costvariable.append( (self[pkey], self[vkey]) )

		if periods_available:
			periods_available = sorted( periods_available )
			self.costvariable_datalist = [ i[0] for i in periods_available ]
			self.costvariable_datalist_id = dkey

			# And, for completeness ...
			flds[ new_key ].choices = periods_available
			flds[ new_key ].widget.attrs.update({ 'list' : dkey })

		efficiency = []
		inp_choices = [
		  (cp.commodity.name, cp.commodity.name)

		  for cp in Set_commodity_physical.objects.filter(analysis=a)
		]
		out_choices = [
		  (cp.commodity.name, cp.commodity.name)

		  for cp in Set_commodity_output.objects.filter(analysis=a)
		]
		for epk, (inp, out, val) in cur_effr:
			ikey, okey, vkey = (
			  'efficiency_{}_input'.format(  epk ),
			  'efficiency_{}_output'.format( epk ),
			  'efficiency_{}_value'.format(  epk )
			)
			flds[ ikey ] = F.ChoiceField(
			  label=_('Input'),
			  choices=inp_choices,
			  widget=F.TextInput,
			  required=False )
			flds[ okey ] = F.ChoiceField(
			  label=_('Output'),
			  choices=out_choices,
			  widget=F.TextInput,
			  required=False )
			flds[ vkey ] = F.FloatField(
			  label=_('Percent'),
			  required=False )

			if inp and out and val:
				flds[ ikey ].widget.attrs['readonly'] = True
				flds[ okey ].widget.attrs['readonly'] = True
				flds[ ikey ].initial = inp
				flds[ okey ].initial = out
				flds[ vkey ].initial = val
			else:
				new_keys = (ikey, okey, vkey)

			efficiency.append( (self[ikey], self[okey], self[vkey]) )

		self.efficiency   = efficiency
		self.costfixed    = costfixed
		self.costvariable = costvariable


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


