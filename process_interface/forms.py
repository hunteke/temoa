from collections import defaultdict
from operator import itemgetter as iget
import re

from django import forms as F
from django.db.models import Max
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from models import (
  Analysis,
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

class CachedChoiceField ( F.ModelChoiceField ):
	""" By default, Django assumes queryset, and utilizes queryset.all().  This
	can be a problem if the field needs a dynamic set of choices that does not
	easily fit within a SQL query.  This subclass allows the form to prepopulate
	a field cache. """
	def __init__ ( self, *args, **kwargs ):
		# If choice_cache is already populuated, then utilize it.  Otherwise,
		# fallback to the normal handling.
		cache = kwargs.pop( 'cache', None )
		super( CachedChoiceField, self ).__init__( *args, **kwargs )

		if cache:
			self.cache_choices = True
			self.choice_cache = [ self.choice(c) for c in cache ]


	def choice ( self, obj ):
		return ( self.prepare_value(obj), self.label_from_instance(obj) )



class VintageField ( CachedChoiceField ):
	def label_from_instance ( self, obj ):
		return u'{}'.format( obj.vintage )



class AnalysisForm ( F.ModelForm ):
	class Meta:
		model = Analysis
		fields = ('name', 'description', 'period_0', 'global_discount_rate')


	def clean_name ( self ):
		data = self.cleaned_data['name']
		data = re.sub(r'\r\n', '', data).strip()
		return data


	def clean_description ( self ):
		data = self.cleaned_data['description']
		data = re.sub(r'\r', '', data).strip()
		return data



class NewProcessForm ( F.ModelForm ):
	class Meta:
		model = Process
		fields = ('technology', 'vintage')

	def __init__ ( self, *args, **kwargs ):
		analysis = kwargs.pop( 'analysis' )
		super( NewProcessForm, self ).__init__( *args, **kwargs )

		flds = self.fields
		query = Vintage.objects.filter( analysis=analysis ).order_by('vintage')
		flds['vintage'] = VintageField( query, cache=list(query)[:-1] )



class ProcessForm ( F.Form ):
	"""
	Given a process, this form will automatically provide the appropriate
	"""
	discountrate = F.FloatField( required=False, label=_('Discount Rate') )
	lifetime     = F.FloatField( required=False, label=_('Lifetime') )
	loanlife     = F.FloatField( required=False, label=_('Loan Lifetime') )

	def __init__ ( self, process, *args, **kwargs ):
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
	inp    = F.ChoiceField( label=_('Input') )
	out    = F.ChoiceField( label=_('Output') )
	eff    = F.FloatField( required=False, label=_('Percent') )

	def __init__( self, *args, **kwargs ):
		analysis = kwargs.pop( 'analysis' )
		pk  = kwargs.pop( 'pk',  None )
		inp = kwargs.pop( 'inp', None )
		out = kwargs.pop( 'out', None )
		eff = kwargs.pop( 'eff', None )
		inp_choices = kwargs.pop( 'inp_choices', None )
		out_choices = kwargs.pop( 'out_choices', None )

		if pk:
			inp_choices = ((inp, inp),)
			out_choices = ((out, out),)

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
			flds['inp'].widget = F.TextInput()
			flds['out'].widget = F.TextInput()
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


class EmissionActivityForm ( F.Form ):
	pol = F.ChoiceField( label=_('Pollutant') )
	eff = F.ChoiceField( label=_('Efficiency') )
	val = F.FloatField( required=False, label=_('Percent') )

	def __init__( self, *args, **kwargs ):
		process = kwargs.pop( 'process' )
		pk  = kwargs.pop( 'pk',  None )
		pol = kwargs.pop( 'pol', None )
		eff = kwargs.pop( 'eff', None )
		val = kwargs.pop( 'val', None )
		pol_choices = kwargs.pop( 'pol_choices', None )
		eff_choices = kwargs.pop( 'eff_choices', None )

		analysis = process.analysis

		if pk:
			pol_choices = ((pol, pol),)
			eff_choices = ((eff, eff),)

		if not eff_choices:
			pol_choices = EmissionActivityForm.getPollutantChoices( analysis )
		if not eff_choices:
			eff_choices = EmissionActivityForm.getEfficiencyChoices( process )

		super( EmissionActivityForm, self ).__init__( *args, **kwargs )

		flds = self.fields
		flds['pol'].initial = pol
		flds['eff'].initial = eff
		flds['val'].initial = val

		flds['pol'].choices = pol_choices
		flds['eff'].choices = eff_choices

		if pk:
			flds['pol'].widget = F.TextInput()
			flds['eff'].widget = F.TextInput()
			flds['pol'].widget.attrs.update( readonly=True )
			flds['eff'].widget.attrs.update( readonly=True )

		self.pk = pk


	@classmethod
	def getPollutantChoices ( cls, analysis ):
		choices = [ (cp.commodity.name, cp.commodity.name)
		  for cp in Set_commodity_emission.objects.filter(analysis=analysis)
		]

		return choices


	@classmethod
	def getEfficiencyChoices ( cls, process ):
		choices = []
		for eff in Param_Efficiency.objects.filter(process=process):
			inp = eff.inp_commodity.commodity.name
			out = eff.out_commodity.commodity.name
			choice = '{}, {}'.format( inp, out )
			choices.append( (choice, choice) )

		return choices


def getEmissionActivityForm ( emactivity, *args, **kwargs ):
	inp = emactivity.efficiency.inp_commodity.commodity.name
	out = emactivity.efficiency.out_commodity.commodity.name
	eff = '{}, {}'.format( inp, out )

	kwargs.update(
	  pk=emactivity.pk,
	  pol=emactivity.emission.commodity.name,
	  eff=eff,
	  val=emactivity.value
	)

	return EmissionActivityForm( *args, **kwargs )


def getEmissionActivityForms ( emactivities, *args, **kwargs ):
	forms = []
	if not emactivities:
		return forms

	process = kwargs['process']
	analysis = process.analysis
	pol_choices = EmissionActivityForm.getPollutantChoices( analysis )
	eff_choices = EmissionActivityForm.getEfficiencyChoices( process )

	kwargs.update(
	  pol_choices=pol_choices,
	  eff_choices=eff_choices
	)
	for pk, (pol, inp, out, val) in sorted( emactivities.iteritems(), key=iget(1) ):
		eff = '{}, {}'.format( inp, out )
		kwargs.update( pk=pk, pol=pol, eff=eff, val=val )
		forms.append( EmissionActivityForm( *args, **kwargs ))

	return forms


class CostForm ( F.Form ):
	per = F.ChoiceField( label=_('Period') )
	val = F.FloatField( required=False, label=_('Percent') )

	class Meta:
		abstract = True

	def __init__( self, *args, **kwargs ):
		process = kwargs.pop( 'process' )
		pk  = kwargs.pop( 'pk',  None )
		per = kwargs.pop( 'per', None )
		val = kwargs.pop( 'val', None )
		per_choices = kwargs.pop( 'per_choices', None )

		analysis = process.analysis

		if pk:
			per_choices = ((per, per),)

		if not per_choices:
			per_choices = CostForm.getPeriodChoices( process )

		super( CostForm, self ).__init__( *args, **kwargs )

		flds = self.fields
		flds['per'].initial = per
		flds['val'].initial = val

		flds['per'].choices = per_choices

		if pk:
			flds['per'].widget = F.TextInput()
			flds['per'].widget.attrs.update( readonly=True )

		self.pk = pk

	@classmethod
	def getPeriodChoices ( cls, process ):
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
				return (('Specify Lifetime','Specify Lifetime'),)

		final_year = Vintage.objects.filter( analysis=a )
		final_year = final_year.aggregate( Max('vintage') )['vintage__max']

		active_periods = Vintage.objects.filter(
		  analysis=a,
		  vintage__gte=max(v, p_0),
		  vintage__lt=min(v + life, final_year)
		).distinct()

		choices = sorted( (v.vintage, v.vintage) for v in active_periods )
		return choices



class CostFixedForm ( CostForm ): pass
class CostVariableForm ( CostForm ): pass



def getCostFixedForm ( costfixed, *args, **kwargs ):
	kwargs.update(
	  pk=costfixed.pk,
	  per=costfixed.period.vintage,
	  val=costfixed.value
	)

	return CostFixedForm( *args, **kwargs )


def getCostFixedForms ( costfixed, *args, **kwargs ):
	forms = []
	if not costfixed:
		return forms

	process = kwargs['process']
	per_choices = CostForm.getPeriodChoices( process )

	kwargs.update( per_choices=per_choices )
	for pk, (per, val) in sorted( costfixed.iteritems(), key=iget(1) ):
		kwargs.update( pk=pk, per=per, val=val )
		forms.append( CostFixedForm( *args, **kwargs ))

	return forms


def getCostVariableForm ( costvariable, *args, **kwargs ):
	kwargs.update(
	  pk=costvariable.pk,
	  per=costvariable.period.vintage,
	  val=costvariable.value
	)

	return CostVariableForm( *args, **kwargs )


def getCostVariableForms ( costvariable, *args, **kwargs ):
	forms = []
	if not costvariable:
		return forms

	process = kwargs['process']
	per_choices = CostForm.getPeriodChoices( process )

	kwargs.update( per_choices=per_choices )
	for pk, (per, val) in sorted( costvariable.iteritems(), key=iget(1) ):
		kwargs.update( pk=pk, per=per, val=val )
		forms.append( CostVariableForm( *args, **kwargs ))

	return forms

