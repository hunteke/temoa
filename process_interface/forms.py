from collections import defaultdict
from operator import itemgetter as iget
import math, re

from django import forms as F
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from models import (
  Analysis,
  AnalysisCommodity,
  Commodity,
  CommodityType,
  Param_CapacityToActivity,
  Param_CostFixed,
  Param_CostVariable,
  Param_Efficiency,
  Param_GrowthRate,
  Param_LifetimeTech,
  Param_LifetimeTechLoan,
  Process,
  Set_tech_baseload,
  Set_tech_storage,
  Technology,
  Vintage,
)


class LoginForm ( F.Form ):
	username = F.CharField( label=_('Username'), max_length=254 )
	password = F.CharField( label=_('Password'), widget=F.PasswordInput() )


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



vintage_help = """ A comma separated list of integers, to be the vintages of this analysis.  Note that the last integer will serve as a sentinel year for the model to calculate the length of the periods.  See the <a href='http://temoaproject.org/docs/#sets' title='Explanation of Temoa&rsquo;s understanding of time'>Temoa Documentation</a> for more information."""
class VintagesForm ( F.Form ):
	vintages = F.CharField(
	  label=_('Vintages'),
	  help_text=vintage_help,
	)

	def __init__ ( self, *args, **kwargs ):
		analysis = kwargs.pop( 'analysis' )
		super( VintagesForm, self ).__init__( *args, **kwargs )

		self.analysis = analysis

		vintages = Vintage.objects.filter( analysis=analysis )
		vintages = sorted( i.vintage for i in vintages )
		vintages = ', '.join( str(v) for v in vintages )
		self.fields['vintages'].initial = vintages


	def clean_vintages ( self ):
		data = self.cleaned_data['vintages']

		data = data.strip().strip(',').split(',')
		if not data:
			raise F.ValidationError( 'There are no vintages.' )

		new_data = []
		try:
			num = 'Not a Number'
			for i in data:
				if not i: continue
				num = i
				new_data.append( int( i ))
		except ValueError:
			msg = 'Unable to convert "{}" to an integer'
			raise F.ValidationError( msg.format( num ))

		return set( new_data )


	def save ( self ):
		a = self.analysis

		vintages = Vintage.objects.filter( analysis=a )
		old_vintages = set( v.vintage for v in vintages )
		new_vintages = self.cleaned_data['vintages']

		# ensure any associated data with last_period is also dropped
		last_period = max( new_vintages );
		to_remove = old_vintages - new_vintages
		to_remove.add( last_period )
		Vintage.objects.filter(analysis=a, vintage__in=to_remove).delete()

		for v in (new_vintages - old_vintages):
			Vintage( analysis=a, vintage=v ).save()



class TechnologyForm ( F.ModelForm ):
	class Meta:
		model = Technology
		fields = ('name', 'capacity_to_activity', 'description')



class SegFracForm ( F.Form ):
	# All fields on the model are required.  However, the UI may only send what
	# has changed, so the Form fields are _not_ required.  The DB layer will
	# throw an error if not all fields have been set.
	season      = F.RegexField( required=False, label=_('Season'), regex=r'^[A-z_]\w*$' )
	time_of_day = F.RegexField( required=False, label=_('Time of Day'), regex=r'^[A-z_]\w*$' )
	value       = F.FloatField( required=False, label=_('Fraction') )

	def __init__ ( self, *args, **kwargs ):
		self.instance = kwargs.pop( 'instance' )
		super( SegFracForm, self ).__init__( *args, **kwargs )


	def clean_value ( self ):
		cd = self.cleaned_data

		if ( 'value' in cd and cd['value'] is not None ):
			if not ( 0 < cd['value'] and cd['value'] <= 1 ):
				msg = 'Please specify a value in the range (0, 1].'
				raise F.ValidationError( msg )

		else:
			if not self.instance.value:
				msg = 'Please specify a value in the range (0, 1].'
				raise F.ValidationError( msg )

		return 'value' in cd and cd['value'] or None


	def save ( self ):
		sf = self.instance
		cd = self.cleaned_data

		for field in ('season', 'time_of_day', 'value'):
			if field in cd and cd[ field ]:
				setattr( sf, field, cd[ field ] )

		# convenience for UI, in case of error
		cd['name'] = u'{}, {}'.format( sf.season, sf.time_of_day )

		sf.save()



class DemandDefaultDistributionForm ( F.Form ):
	value = F.FloatField( label=_('Value') )

	def __init__ ( self, *args, **kwargs ):
		self.instance = kwargs.pop( 'instance' )
		super( DemandDefaultDistributionForm, self ).__init__( *args, **kwargs )


	def clean_value ( self ):
		cd = self.cleaned_data

		if not self.instance.value and (
		   'value' not in cd or math.isnan( cd['value'] )
		):
			raise F.ValidationError('Please specify a value in the range (0, 1].')

		elif 'value' in cd and not ( 0 < cd['value'] and cd['value'] <= 1 ):
			raise F.ValidationError('Please specify a value in the range (0, 1].')

		return 'value' in cd and cd['value'] or float('nan')


	def save ( self ):
		ddd = self.instance
		cd = self.cleaned_data

		if 'value' in cd and cd[ 'value' ]:
			ddd.value = cd[ 'value' ]

		# convenience for UI, in case of error
		cd['name'] = u'{}, {}'.format(
		  ddd.timeslice.season, ddd.timeslice.time_of_day )

		ddd.save()



class DemandForm ( F.Form ):
	value = F.FloatField( label=_('Value') )

	def __init__ ( self, *args, **kwargs ):
		self.instance = kwargs.pop( 'instance' )
		super( DemandForm, self ).__init__( *args, **kwargs )


	def save ( self ):
		dem = self.instance
		cd = self.cleaned_data

		dem.value = cd['value']

		# convenience
		cd['name'] = '{}, {}'.format(
		  dem.demand.commodity.name, dem.period.vintage )

		dem.save()



class AnalysisCommodityForm ( F.Form ):
	name = F.RegexField( label=_('Name'), regex=r'^[A-z_]\w*$' )

	def __init__ ( self, *args, **kwargs ):
		self.instance = kwargs.pop('instance')
		super( AnalysisCommodityForm, self ).__init__( *args, **kwargs )


	def save ( self ):
		i = self.instance
		com, created = Commodity.objects.get_or_create(
		  name=self.cleaned_data['name'] )

		i.commodity = com
		i.save()


class CommodityOutputForm ( F.Form ):
	name = F.RegexField( label=_('Name'), regex=r'^[A-z_]\w*$')

	def __init__ ( self, *args, **kwargs ):
		self.instance = kwargs.pop('instance')
		super( CommodityOutputForm, self ).__init__( *args, **kwargs )


	def save ( self ):
		i = self.instance
		com, created = Commodity.objects.get_or_create(
		  name=self.cleaned_data['name'] )

		i.save( com )


class ProcessForm ( F.Form ):
	name         = F.RegexField( required=True, label=_('name'), regex=r'^[A-z_]\w*, *-?\d+$')
	discountrate = F.FloatField( required=False, label=_('Discount Rate') )
	lifetime     = F.FloatField( required=False, label=_('Lifetime') )
	loanlife     = F.FloatField( required=False, label=_('Loan Lifetime') )
	costinvest   = F.FloatField( required=False, label=_('Investment Cost') )
	existingcapacity = F.FloatField( required=False, label=_('Existing Capacity') )

	def __init__ ( self, *args, **kwargs ):
		p = self.process = kwargs.pop( 'instance' )
		super( ProcessForm, self ).__init__( *args, **kwargs )

		if p.pk:
			# process in DB, and name is not mutable here: remove the field
			del self.fields['name']
			if p.vintage.vintage < p.analysis.period_0:
				del self.fields['costinvest']
				del self.fields['loanlife']
				del self.fields['discountrate']
			else:
				del self.fields['existingcapacity']


	def clean_name ( self ):
		cd = self.cleaned_data
		p  = self.process

		tname, vintage = cd['name'].split(',')
		vintage = int( vintage )

		vintages = Vintage.objects.filter( analysis=p.analysis )
		if vintage not in (i.vintage for i in vintages):
			msg = '{} is not a valid vintage in this analysis.'
			raise F.ValidationError( msg.format( vintage ))
		elif vintage == max( i.vintage for i in vintages ):
			msg = 'The final year in "vintages" is not a valid vintage.'
			raise F.ValidationError( msg )
		vintage = [i for i in vintages if vintage == i.vintage][0]

		tech = None
		techs = Technology.objects.filter( name=tname )
		if not techs:
			msg = "'{}' is not a valid technology name.  Do you need to create it?"
			raise F.ValidationError( msg.format( tname ))
		elif len( techs ) > 1:
			for t in techs:
				if t.user == self.analysis.user:
					tech = t
					break
			if not tech:
				msg = ("'{}' is not a unique technology name in the database.  If "
				  'you would like to use this name, you will need to create this '
				  'technology under your account.')
				raise F.ValidationError( msg.format( tname ))

		if not tech:
			tech = techs[0]

		# store the work already done for save() method
		cd['technology'] = tech
		cd['vintage'] = vintage

		return '{}, {}'.format( tname, vintage )


	def clean_lifetime ( self ):
		life = self.cleaned_data['lifetime']
		if life is None:
			return life

		p = self.process

		# Ensure that value reaches to at least the first period from process
		# vintage.  Note that this is _not_ done at the DB level because a model
		# may be in flux (i.e. a modeler is changing the structure of the data).
		# Meanwhile, this check *will* be performed when downloading the complete
		# dat file.
		if life + p.vintage.vintage <= p.analysis.period_0:
			msg = ('Process lifetime guarantees no use in model optimization.  '
			  'Either extend the lifetime, or change the analysis start year.')
			raise F.ValidationError( msg )

		if life <= 0:
			msg = ('Either do not specify a lifetime, or specify one greater than '
			  '0.')
			raise F.ValidationError( msg )

		return life


	def clean_loanlife ( self ):
		cd = self.cleaned_data

		life = cd['loanlife']
		if life is None:
			return life

		p = self.process
		v = cd['vintage'].vintage if 'vintage' in cd else p.vintage.vintage

		if v < p.analysis.period_0:
			msg = ('Existing capacity cannot have a loan and therefore no loan '
			  'life.')
			raise F.ValidationError( msg )

		if life <= 0:
			msg = ('Either do not specify a loan lifetime, or specify one greater '
			  'than 0.')
			raise F.ValidationError( msg )

		return life


	def clean_existingcapacity ( self ):
		cd = self.cleaned_data
		ecap = cd['existingcapacity']
		p = self.process

		if ecap and not p.pk:
			if cd['vintage'].vintage >= p.analysis.period_0:
				msg = ('Cannot have existing capacity for a vintage in the '
				  'optimization horizon (Period 0 or larger).')
				raise F.ValidationError( msg )

		if ecap is None:
			return ecap

		if ecap <= 0:
			msg = ('Existing capacity must be greater than 0.')
			raise F.ValidationError( msg )

		return ecap


	def clean_costinvest ( self ):
		cd = self.cleaned_data
		ci = cd['costinvest']
		p = self.process

		if ci and not p.pk:
			if cd['vintage'].vintage < p.analysis.period_0:
				msg = ('Cannot specify an investment cost for a vintage that '
				  'exists prior to the optimization horizon (before Period 0).')
				raise F.ValidationError( msg )

		if ci is None:
			return ci

		return ci


	def save ( self ):
		p = self.process
		cd = self.cleaned_data
		for attr in ('technology', 'vintage', 'existingcapacity', 'costinvest',
		             'lifetime', 'loanlife', 'discountrate'):
			if attr in cd:
				setattr( p, attr, cd[ attr ] )

		p.save()



class EfficiencyForm ( F.Form ):
	inp = F.ChoiceField( label=_('Input') )
	out = F.ChoiceField( label=_('Output') )
	value = F.FloatField( required=False, label=_('Percent') )

	def __init__( self, *args, **kwargs ):
		eff = kwargs.pop( 'instance' )

		super( EfficiencyForm, self ).__init__( *args, **kwargs )

		self.efficiency = eff
		if eff.pk:
			# Remove possibility of changing input or output.  The workflow is
			# to delete one efficiency and make a new one if needed to change.
			del self.fields['inp'], self.fields['out']
			self.fields['value'].initial = eff.value
		else:
			inp_choices = EfficiencyForm.getInputChoices( eff.process.analysis )
			out_choices = EfficiencyForm.getOutputChoices( eff.process.analysis )

			self.fields['inp'].choices = inp_choices
			self.fields['out'].choices = out_choices


	@classmethod
	def getInputChoices ( cls, analysis ):
		ctype = CommodityType.objects.filter( name='physical' )
		return [ (c.commodity.name, c.commodity.name)
		  for c in AnalysisCommodity.objects.filter(
		    analysis=analysis, commodity_type__in=ctype )
		]


	@classmethod
	def getOutputChoices ( cls, analysis ):
		ctype = CommodityType.objects.filter( name__in=('physical', 'demand') )
		return [ (c.commodity.name, c.commodity.name)
		  for c in AnalysisCommodity.objects.filter(
		    analysis=analysis, commodity_type__in=ctype )
		]


	def clean_value ( self ):
		epsilon = 1e-9    # something really small

		v = self.cleaned_data['value']  # guaranteed a float or None
		if v is None or abs(v) < epsilon:
			msg = ('Process efficiency must not be 0, or it is a useless entry.  '
			  'Consider removing the efficiency instead of marking it 0.')
			raise F.ValidationError( msg )

		return v


	def clean_inp ( self ):
		# though this field is already limited by its choices, we use it here to
		# simultaneously check that it's valid and populate cleaned_data with
		# an AnalysisCommodity object rather than a string.
		inp = self.cleaned_data['inp']
		eff = self.efficiency

		try:
			inp = AnalysisCommodity.objects.get(
			  analysis=eff.process.analysis,
			  commodity_type__name__in=('physical',),
			  commodity__name=inp
			)
		except ObjectDoesNotExist as e:
			msg = ('Specified input does not exist in analysis, or is not a '
			  'physical commodity.')
			raise F.ValidationError( msg )

		return inp  # note that it is no longer a string


	def clean_out ( self ):
		# though this field is already limited by its choices, we use it here to
		# simultaneously check that it's valid and populate cleaned_data with
		# an AnalysisCommodity object rather than a string.
		out = self.cleaned_data['out']
		eff = self.efficiency

		try:
			out = AnalysisCommodity.objects.get(
			  analysis=eff.process.analysis,
			  commodity_type__name__in=('physical', 'demand'),
			  commodity__name=out
			)
		except ObjectDoesNotExist as e:
			msg = 'Specified output does not exist in analysis.'
			raise F.ValidationError( msg )

		return out  # note that it is no longer a string


	def save ( self ):
		cd = self.cleaned_data
		eff = self.efficiency

		if 'inp' in cd:
			eff.inp_commodity = cd[ 'inp' ]
		if 'out' in cd:
			eff.out_commodity = cd[ 'out' ]
		if 'value' in cd:
			eff.value = cd[ 'value' ]

		eff.save()



class EmissionActivityForm ( F.Form ):
	pol = F.ChoiceField( label=_('Pollutant') )
	eff = F.RegexField( label=_('Efficiency'), regex=r'^[A-z_]\w*, *[A-z_]\w*$')
	value = F.FloatField( label=_('Value') )

	def __init__( self, *args, **kwargs ):
		ema = kwargs.pop( 'instance' )
		process = kwargs.pop( 'process' )

		super( EmissionActivityForm, self ).__init__( *args, **kwargs )

		self.emissionactivity = ema
		self.process = process
		analysis = process.analysis
		if ema.pk:
			# already exists; only allow updating value
			del self.fields['pol'], self.fields['eff']
		else:
			pol_choices = EmissionActivityForm.getPollutantChoices( analysis )
			self.fields['pol'].choices = pol_choices


	@classmethod
	def getPollutantChoices ( cls, analysis ):
		ctype = CommodityType.objects.get( name='emission' )
		return [ (ce.commodity.name, ce.commodity.name)
		  for ce in AnalysisCommodity.objects.filter(
		    analysis=analysis, commodity_type=ctype )
		]


	@classmethod
	def getEfficiencyChoices ( cls, process ):
		choices = []
		for eff in Param_Efficiency.objects.filter( process=process ):
			inp = eff.inp_commodity.commodity.name
			out = eff.out_commodity.commodity.name
			choice = '{}, {}'.format( inp, out )
			choices.append( (choice, choice) )

		return choices


	def clean_value ( self ):
		epsilon = 1e-9    # something really small

		v = self.cleaned_data['value']  # guaranteed a float or None
		if v is None or abs(v) < epsilon:
			msg = ('Process emission activity must not be 0, or it is a useless '
			  'entry.  Consider removing the activity instead of marking it 0.')
			raise F.ValidationError( msg )

		return v


	def clean_pol ( self ):
		# though this field is already limited by its choices, we use it here to
		# simultaneously check that it's valid and populate cleaned_data with
		# an AnalysisCommodity object rather than a string.
		pol = self.cleaned_data['pol']

		try:
			pol = AnalysisCommodity.objects.get(
			  analysis=self.process.analysis,
			  commodity_type__name='emission',
			  commodity__name=pol
			)
		except ObjectDoesNotExist as e:
			msg = 'Specified pollutant does not exist in analysis.'
			raise F.ValidationError( msg )

		return pol  # note that it is no longer a string


	def clean_eff ( self ):
		# Because the UI is text-based rather than drop-down list, this field
		# is a regex.  We /could/ limit by choices, but that would put undue
		# burden on the user to correctly format the field.  Using the regex
		# allows for a slightly more flexible input mechanism.

		# Note also, that when this function is done, eff will not be a string
		# but a Param_Efficiency object.
		inp, out = self.cleaned_data['eff'].split(',')
		out = out.strip()

		try:
			eff = Param_Efficiency.objects.get(
			  inp_commodity__commodity__name = inp,
			  process = self.process,
			  out_commodity__commodity__name = out
			)
		except ObjectDoesNotExist as e:
			msg = 'Specified efficiency does not exist in this analysis.'
			raise F.ValidationError( msg )

		return eff  # note that it is no longer a string


	def save ( self ):
		ema = self.emissionactivity
		cd = self.cleaned_data

		if 'pol' in cd:
			ema.emission = cd[ 'pol' ]
		if 'eff' in cd:
			ema.efficiency = cd[ 'eff' ]
		if 'value' in cd:
			ema.value = cd[ 'value' ]

		ema.save()



class CostForm ( F.Form ):
	per   = F.ChoiceField( label=_('Period') )
	value = F.FloatField( label=_('Cost') )

	def __init__( self, *args, **kwargs ):
		self.cost = cost = kwargs.pop('instance')

		super( CostForm, self ).__init__( *args, **kwargs )

		if cost.pk:
			del self.fields['per']

		else:
			per_choices = CostForm.getPeriodChoices( cost.process )
			self.fields['per'].choices = per_choices

			msg = 'Invalid period (%(value)s).  Valid periods are: {}'
			pers = ', '.join( unicode(i[0]) for i in per_choices )
			em = self.fields['per'].error_messages
			em['invalid_choice'] = _(msg.format( pers ))


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

		periods = sorted( i.vintage for i in
		  Vintage.objects.filter( analysis=a, vintage__gte=p_0 ))[:-1]
		periods = set( per for per in periods  if per >= v  if per < v + life )

		return sorted( (per, per) for per in periods )


	def clean_per ( self ):
		per = self.cleaned_data['per']
		a = self.cost.process.analysis

		try:
			per = Vintage.objects.get( analysis=a, vintage=per )
		except ObjectDoesNotExist as e:
			msg = 'Specified period ({}) does not exist in this analysis.'
			raise F.ValidationError( msg.format( per ) )

		return per  # note that it's now a Vintage object, not a string/num


	def save ( self ):
		cost = self.cost
		cd = self.cleaned_data


		if 'per' in cd:
			cost.period = cd[ 'per' ]
		if 'value' in cd:
			cost.value = cd[ 'value' ]

		cost.save()



class AnalysisTechnologyForm ( F.Form ):
	baseload = F.BooleanField( required=False, label=_('Baseload') )
	storage  = F.BooleanField( required=False, label=_('Storage') )
	lifetime = F.FloatField( required=False, label=_('Default Lifetime') )
	loanlife = F.FloatField( required=False, label=_('Default Loan Lifetime') )
	capacitytoactivity = F.FloatField( required=False, label=_('Capacity to Activity') )
	growthratelimit = F.FloatField( required=False, label=_('Max Growth Rate') )
	growthrateseed  = F.FloatField( required=False, label=_('Growth Seed') )

	def __init__ ( self, *args, **kwargs ):
		self.analysis = kwargs.pop('analysis')
		self.technology = kwargs.pop('technology')
		super( AnalysisTechnologyForm, self ).__init__( *args, **kwargs )


	def clean_growthratelimit ( self ):
		if 'growthratelimit' in self.data or 'growthrateseed' in self.data:
			if not ('growthratelimit' in self.data and 'growthrateseed' in self.data):
				msg = ('Please specify or remove both Growth Rate fields.  They '
				  'always go in unison.')
				raise F.ValidationError( msg )

		return self.cleaned_data['growthratelimit']


	def clean_growthrateseed ( self ):
		if 'growthratelimit' in self.data or 'growthrateseed' in self.data:
			if not ('growthratelimit' in self.data and 'growthrateseed' in self.data):
				msg = ('Please specify or remove both Growth Rate fields.  They '
				  'always go in unison.')
				raise F.ValidationError( msg )

		return self.cleaned_data['growthrateseed']


	def numerical_clean ( self, key, validation_msg ):
		epsilon = 1e-9    # something really small

		v = self.cleaned_data[ key ]  # guaranteed a float or None
		if v is None:
			pass
		elif v < epsilon:
			raise F.ValidationError( validation_msg )
		elif math.isnan( v ):
			v = None

		return v


	def clean_lifetime ( self ):
		msg = ('Technology lifetime must either be a positive number or not '
			  'exist.  To remove it, empty the field instead of marking it 0.')
		return self.numerical_clean( 'lifetime', msg )


	def clean_loanlife ( self ):
		msg = ('Technology loan life must either be a positive number or not '
		  'exist.  To remove it, empty the field instead of marking it 0.')
		return self.numerical_clean( 'loanlife', msg )


	def clean_capacitytoactivity ( self ):
		msg = ('Technology CapacityToActivity parameter must either be a '
		  'positive number or not exist.  To remove it, empty the field instead '
		  'of marking it 0.')
		return self.numerical_clean( 'capacitytoactivity', msg )


	def save ( self ):
		a  = self.analysis
		t  = self.technology
		cd = self.cleaned_data

		if 'baseload' in self.data:
			if cd['baseload']:
				obj, created = Set_tech_baseload.objects.get_or_create(
				  analysis=a, technology=t )
			else:
				Set_tech_baseload.objects.filter(
				  analysis=a, technology=t ).delete()

		if 'storage' in self.data:
			if cd['storage']:
				obj, created = Set_tech_storage.objects.get_or_create(
				  analysis=a, technology=t )
			else:
				Set_tech_storage.objects.filter(
				  analysis=a, technology=t ).delete()

		if 'capacitytoactivity' in self.data:
			c2a = cd['capacitytoactivity']
			if c2a:
				obj, created = Param_CapacityToActivity.objects.get_or_create(
				  analysis=a, technology=t, defaults={'value': c2a} )
				if not created:
					obj.value = c2a
					obj.save()
			else:
				Param_CapacityToActivity.objects.filter(
				  analysis=a, technology=t ).delete()

		if 'lifetime' in self.data:
			lifetime = cd['lifetime']
			if lifetime:
				obj, created = Param_LifetimeTech.objects.get_or_create(
				  analysis=a, technology=t, defaults={'value': lifetime} )
				if not created:
					obj.value = lifetime
					obj.save()
			else:
				Param_LifetimeTech.objects.filter(
				  analysis=a, technology=t ).delete()

		if 'loanlife' in self.data:
			loanlife = cd['loanlife']
			if loanlife:
				obj, created = Param_LifetimeTechLoan.objects.get_or_create(
				  analysis=a, technology=t, defaults={'value': loanlife} )
				if not created:
					obj.value = loanlife
					obj.save()
			else:
				Param_LifetimeTech.objects.filter(
				  analysis=a, technology=t ).delete()

		if 'growthratelimit' in self.data:
			ratelimit = cd['growthratelimit']
			seed      = cd['growthrateseed']
			if ratelimit:
				obj, created = Param_GrowthRate.objects.get_or_create(
				  analysis=a,
				  technology=t,
				  defaults={'ratelimit': ratelimit, 'seed': seed}
				)
				if not created:
					obj.ratelimit = ratelimit
					obj.seed = seed
					obj.save()
			else:
				Param_GrowthRate.objects.filter(
				  analysis=a, technology=t ).delete()



class TechInputSplitForm ( F.Form ):
	inp   = F.ChoiceField( label=_('Input') )
	value = F.FloatField( label=_('Percentage') )

	def __init__( self, *args, **kwargs ):
		self.techinputsplit = tis = kwargs.pop('instance')
		self.analysis = analysis = kwargs.pop('analysis')

		super( TechInputSplitForm, self ).__init__( *args, **kwargs )

		if tis.pk:
			del self.fields['inp']

		else:
			inp_choices = TechInputSplitForm.getInputChoices( analysis )
			self.fields['inp'].choices = inp_choices

			msg = 'Invalid input commodity (%(value)s).  Valid choices are: {}'
			pers = ', '.join( unicode(i[0]) for i in inp_choices )
			em = self.fields['inp'].error_messages
			em['invalid_choice'] = _(msg.format( pers ))


	@classmethod
	def getInputChoices ( cls, analysis ):
		inps = AnalysisCommodity.objects.filter(
		  analysis=analysis, commodity_type__name='physical' )
		return sorted(
		  set(( ac.commodity.name, ac.commodity.name) for ac in inps )
		)


	def clean_inp ( self ):
		inp = self.cleaned_data['inp']
		a = self.analysis

		try:
			inp = AnalysisCommodity.objects.get(
			  analysis=a, commodity_type__name='physical', commodity__name=inp )
		except ObjectDoesNotExist as e:
			msg = 'Specified input commodity ({}) does not exist in this analysis.'
			raise F.ValidationError( msg.format( inp ) )

		return inp  # note that it's now a Commodity _object_, not a string/num


	def clean_value ( self ):
		epsilon = 1e-9
		v = self.cleaned_data['value']

		if v is None:
			msg = ('Please specify a percentage.  To remove this split, push the '
			  '"Shift" key and click on the corresponding red button.')
			raise F.ValidationError( msg )

		elif math.isnan( v ):
			msg = ('Received NaN ("Not A Number").  Please specify a decimal '
			  'value between 0 and 1.')
			raise F.ValidationError( msg )

		elif v < epsilon:
			msg = ('Zero is a useless entry.  Please either remove this row, or '
			  'pick a value in the range (0, 1).')
			raise F.ValidationError( msg )

		elif v >= 1:
			msg ('One (100%) is a useless entry.  Please either remove this row, '
			  'or pick a value in the range (0, 1).')
			raise F.ValidationError( msg )

		return v


	def save ( self ):
		tis = self.techinputsplit
		cd = self.cleaned_data

		if 'inp' in cd:
			tis.inp_commodity = cd[ 'inp' ]
		if 'value' in cd:
			tis.fraction = cd[ 'value' ]

		tis.save()



class TechOutputSplitForm ( F.Form ):
	out   = F.ChoiceField( label=_('Output') )
	value = F.FloatField( label=_('Percentage') )

	def __init__( self, *args, **kwargs ):
		self.techoutputsplit = ois = kwargs.pop('instance')
		self.analysis = analysis = kwargs.pop('analysis')

		super( TechOutputSplitForm, self ).__init__( *args, **kwargs )

		if ois.pk:
			del self.fields['out']

		else:
			out_choices = TechOutputSplitForm.getOutputChoices( analysis )
			self.fields['out'].choices = out_choices

			msg = 'Invalid output commodity (%(value)s).  Valid choices are: {}'
			pers = ', '.join( unicode(i[0]) for i in out_choices )
			em = self.fields['out'].error_messages
			em['invalid_choice'] = _(msg.format( pers ))


	@classmethod
	def getOutputChoices ( cls, analysis ):
		outs = AnalysisCommodity.objects.filter(
		  analysis=analysis, commodity_type__name__in=('physical', 'demand') )
		return sorted(
		  set(( ac.commodity.name, ac.commodity.name) for ac in outs)
		)


	def clean_out ( self ):
		out = self.cleaned_data['out']
		a = self.analysis

		try:
			out = AnalysisCommodity.objects.get(
			  analysis=a,
			  commodity_type__name__in=('demand', 'physical'),
			  commodity__name=out
			)
		except ObjectDoesNotExist as e:
			msg = ('Specified output commodity ({}) does not exist in this '
			  'analysis.')
			raise F.ValidationError( msg.format( out ) )

		return out  # note that it's now a Commodity _object_, not a string/num


	def clean_value ( self ):
		epsilon = 1e-9
		v = self.cleaned_data['value']

		if v is None:
			msg = ('Please specify a percentage.  To remove this split, push the '
			  '"Shift" key and click on the corresponding red button.')
			raise F.ValidationError( msg )

		elif math.isnan( v ):
			msg = ('Received NaN ("Not A Number").  Please specify a decimal '
			  'value between 0 and 1.')
			raise F.ValidationError( msg )

		elif v < epsilon:
			msg = ('Zero is a useless entry.  Please either remove this row, or '
			  'pick a value in the range (0, 1).')
			raise F.ValidationError( msg )

		elif v >= 1:
			msg ('One (100%) is a useless entry.  Please either remove this row, '
			  'or pick a value in the range (0, 1).')
			raise F.ValidationError( msg )

		return v


	def save ( self ):
		ois = self.techoutputsplit
		cd = self.cleaned_data

		if 'out' in cd:
			ois.out_commodity = cd[ 'out' ]
		if 'value' in cd:
			ois.fraction = cd[ 'value' ]

		ois.save()

