__all__ = (
  'Analysis',
  'AnalysisCommodity',
  'Commodity',
  'CommodityType',
  'Param_CapacityToActivity',
  'Param_CostFixed',
  'Param_CostVariable',
  'Param_Demand',
  'Param_DemandDefaultDistribution',
  'Param_DemandSpecificDistribution',
  'Param_Efficiency',
  'Param_EmissionActivity',
  'Param_EmissionLimit',
  'Param_GrowthRate',
  'Param_LifetimeTech',
  'Param_LifetimeTechLoan',
  'Param_MaxCapacity',
  'Param_MinCapacity',
  'Param_ResourceBound',
  'Param_SegFrac',
  'Param_TechInputSplit',
  'Param_TechOutputSplit',
  'PeriodCostParameter',
  'Process',
  'Set_tech_baseload',
  'Set_tech_storage',
  'Technology',
  'TechnologySetMember',
  'Vintage'
)

import math, re

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models as DM   # Django Models
from django.utils.translation import ugettext_lazy as _

# One glaring deficiency with Django: lack of database level check constraints.
# Django has the basics like, > 0, not null, and unique/unique_together, but it
# is not able to check things like "field 1 < field 2".  There is a _lot_ of
# data interdependency in Temoa, so we will have to code these checks into the
# Django views.  We can add most of these checks at the DB level with some
# hand-written SQL, but means that if something /does/ get through (god-forbid,
# someone accesses the DB directly or through another frontend), then data
# integrity might become an issue.  For now, the /only/ supported interaction
# will be through Django.

help_analysis_name = _("""A "short" name for this analysis.  This will likely be how you reference this data set in conversation or publications, so choose it wisely.  For example, "XPL2003" might be a poor choice.  Note that spaces and "special" characters <em>are</em> allowed.""")
help_analysis_desc = _("""Include here any "meta" information pertinent to this analysis.  You might include a general description of the analysis, links to relevant publications, other analyses, and so on.  Anything that would be helpful to another person trying to understand what you have done.  (Which may be you, 2 years later!)  Please use only text in this field: HTML entities will be escaped.  (To see the effect if this, log out and view the description field of this analysis.)""")
help_analysis_per0 = _("""The start year of the analysis.  Years prior to this will be the "Existing Capacity" vintages, and years following will be in optimization horizon.  For more information, see the discussion of <a href='http://temoaproject.org/docs/index.html#sets' title='Set documentation section on temoaproject.org/'>P<sup>e</sup> and P<sup>f</sup></a> in the Temoa documentation.""")
help_analysis_gdr  = _("""Also used as a fallback for process discount rates.  A typical value is 0.05 (5%).  See the Temoa documentation for more information about the <a href='http://temoaproject.org/docs/#globaldiscountrate' title='GDR explanation on temoaproject.org/'>GDR</a>.""")

class Analysis ( DM.Model ):
	user        = DM.ForeignKey( User )
	name        = DM.CharField( max_length=32767, help_text=help_analysis_name )
	description = DM.TextField('Background Information', help_text=help_analysis_desc)
	period_0    = DM.IntegerField( help_text=help_analysis_per0 )
	global_discount_rate = DM.FloatField( 'Global Discount Rate', help_text=help_analysis_gdr )


	class Meta:
		unique_together = ('user', 'name')


	def __unicode__ ( self ):
		return u'{} - {}'.format( self.user.username, self.name )



class Vintage ( DM.Model ):
	analysis = DM.ForeignKey( Analysis )
	vintage  = DM.IntegerField()

	class Meta:
		unique_together = ('analysis', 'vintage')
		ordering = ('analysis', 'vintage')


	def __unicode__ ( self ):
		return '({}) {}'.format( self.analysis, self.vintage )



class Param_SegFrac ( DM.Model ):
	analysis    = DM.ForeignKey( Analysis )
	season      = DM.CharField( max_length=100 )
	time_of_day = DM.CharField( max_length=100 )
	value       = DM.FloatField()

	class Meta:
		unique_together = ('analysis', 'season', 'time_of_day')

	def __unicode__ ( self ):
		return u'({}) {}, {}: {}'.format(
		   self.analysis, self.season, self.time_of_day, self.value )


	def save ( self, *args, **kwargs ):
		name_re = re.compile( r'^[A-z_]\w*$' )
		if not name_re.match( self.season ):
			msg = ('Season name is not valid.  Use only alphanumeric (A-z, 0-9, '
			  'and underscore [_]) characters and begin with a letter.')
			raise ValidationError( msg )

		if not name_re.match( self.time_of_day ):
			msg = ('"Time of Day" name is not valid.  Use only alphanumeric '
			  '(A-z, 0-9, and underscore [_]) characters and begin with a '
			  'letter.')
			raise ValidationError( msg )

		if self.value and not (0 < self.value and self.value <= 1):
			msg = 'Time slice must be a fractional value between 0 and 1.'
			raise ValidationError( msg )

		super( Param_SegFrac, self ).save( *args, **kwargs )



class Technology ( DM.Model ):
	# There's no need for a limit on the name size, other than practical usage.
	# I can't think of a context that would use more than 100 characters for
	# name, so I think 1024 characters (2**10) is more than adequate storage --
	# overkill, just in case.
	user        = DM.ForeignKey( User )
	name        = DM.CharField( max_length=1024 )
	description = DM.TextField()

	# may be overridden, but must be defined by something
	capacity_to_activity = DM.FloatField( null=True )

	class Meta:
		unique_together = ('user', 'name')
		ordering = ('name',)


	def __unicode__ ( self ):
		return unicode( self.name )


	def clean ( self ):
		self.name = self.name.replace('\r', '').strip()
		self.description = self.description.replace('\r', '').strip()

		if not self.name:
			raise ValidationError( 'Technologies must have a name.' )

		if not self.description:
			raise ValidationError( 'Technologies must have a description.' )



class Commodity ( DM.Model ):
	name        = DM.CharField( max_length=32767, unique=True )
	description = DM.TextField('Backround information')

	def __unicode__ ( self ):
		return unicode( self.name )



class TechnologySetMember ( DM.Model ):
	analysis   = DM.ForeignKey( Analysis )
	technology = DM.ForeignKey( Technology )

	class Meta:
		abstract = True
		ordering = ('analysis', 'technology')
		unique_together = ('analysis', 'technology',)

	def __unicode__ ( self ):
		return u'({}) {}'.format( self.analysis, self.technology )



class Set_tech_baseload ( TechnologySetMember ): pass
class Set_tech_storage  ( TechnologySetMember ): pass



class Process ( DM.Model ):
	analysis         = DM.ForeignKey( Analysis )
	technology       = DM.ForeignKey( Technology )
	vintage          = DM.ForeignKey( Vintage )
	lifetime         = DM.FloatField( null=True )
	loanlife         = DM.FloatField( null=True )
	costinvest       = DM.FloatField( null=True )
	discountrate     = DM.FloatField( null=True )
	existingcapacity = DM.FloatField( null=True )

	class Meta:
		ordering = ('analysis', 'technology', 'vintage')
		unique_together = ('analysis', 'technology', 'vintage')

	def __unicode__ ( self ):
		a = self.analysis if self.analysis_id else 'NoAnalysis'
		t = self.technology if self.technology_id else 'NoTechnology'
		v = self.vintage.vintage if self.vintage_id else 'NoVintage'
		return u'({}) {}, {}'.format( a, t, v )


	@property
	def name ( self ):
		return u'{}, {}'.format( self.technology.name, self.vintage.vintage )


	@classmethod
	def new_with_data ( cls, *args, **kwargs ):
		a   = kwargs['analysis']
		t   = kwargs['technology']
		v   = kwargs['vintage']

		  # the optional parameters
		lifetime         = kwargs.get( 'lifetime', None )
		loanlife         = kwargs.get( 'loanlife', None )
		costinvest       = kwargs.get( 'costinvest', None )
		discountrate     = kwargs.get( 'discountrate', None )
		existingcapacity = kwargs.get( 'existingcapacity', None )

		try:
			v = Vintage.objects.get( analysis=a, vintage=v )
		except ObjectDoesNotExist as e:
			raise ValidationError('Specified vintage does not exist in analysis.')

		obj = cls( analysis=a, vintage=v, technology=t )
		obj.lifetime         = lifetime
		obj.loanlife         = loanlife
		obj.costinvest       = costinvest
		obj.discountrate     = discountrate
		obj.existingcapacity = existingcapacity
		obj.clean()
		obj.save()

		return obj


	def update_with_data ( self, data ):
		for attr in ('lifetime', 'loanlife', 'costinvest', 'discountrate',
		  'existingcapacity'
		):
			if attr in data and data[attr]:
				setattr( self, attr, data[attr] )
			elif attr in data:
				setattr( self, attr, None )

		self.save()


	def save ( self ):
		try:
			v = self.vintage.vintage
		except ObjectDoesNotExist as e:
			raise ValidationError('Process must have a vintage.')

		# Is the vintage valid for this analysis?
		vintages = Vintage.objects.filter( analysis=self.analysis )
		if not vintages.filter( vintage=v ):
			raise ValidationError('Vintage does not exist in this analysis')

		# Is the vintage a vintage year as opposed the final year?
		if v == max( i.vintage for i in vintages ):
			msg = ('The final year in the analysis vintages is not actually a '
			  'vintage.  It is a marker for calculation of the last period '
			  'length, and is therefore not a valid vintage.')
			raise ValidationError( msg )

		e = self.existingcapacity
		l = self.lifetime
		try:
			p0 = self.analysis.period_0
		except ObjectDoesNotExist as e:
			msg = ('Unexpected database error.  Does the analysis need a start '
			  'period (Period 0)?')
			raise ValidationError( msg )

		if v >= p0:
			if e is not None:
				msg = ('Vintage is in optimization horizon: cannot specify '
				  'existing capacity.')
				raise ValidationError( msg )

		else:
			if e is not None and e <= 0:
				msg = 'Existing capacity must be greater than 0.'
				raise ValidationError( msg )

			if self.costinvest is not None:
				msg = ('Cannot specify investment cost: existing capacity is '
				  'already installed and therefore has no investment cost.')
				raise ValidationError( msg )

		if l:
			if l <= 0:
				msg = ('Invalid lifetime: either do not specify a lifetime, or '
				  'specify one greater than 0.')
				raise ValidationError( msg )

			if v + l <= p0:
				msg = ('Invalid lifetime: vintage would not be used in analysis: '
				  '{} + {} <= {}')
				raise ValidationError( msg.format( v, l, p0 ))

		super( Process, self ).save()



class LifetimeParameter ( DM.Model ):
	analysis   = DM.ForeignKey( Analysis )
	technology = DM.ForeignKey( Technology )
	value      = DM.FloatField()

	class Meta:
		abstract = True
		ordering = ('analysis', 'technology')
		unique_together = ('analysis', 'technology')

	def __unicode__ ( self ):
		return u'({}) {}: {}'.format(
		  self.analysis, self.technology.name, self.value )


class Param_LifetimeTech     ( LifetimeParameter ): pass
class Param_LifetimeTechLoan ( LifetimeParameter ): pass



class CommodityType ( DM.Model ):
	name = DM.CharField( max_length=64, unique=True )

	def __unicode__ ( self ):
		return u'{}'.format( self.name )



class AnalysisCommodity ( DM.Model ):
	analysis       = DM.ForeignKey( Analysis )
	commodity_type = DM.ForeignKey( CommodityType )
	commodity      = DM.ForeignKey( Commodity )


	class Meta:
		ordering = ('analysis', 'commodity_type', 'commodity')
		unique_together = ('analysis', 'commodity')


	def __unicode__ ( self ):
		a = self.analysis if self.analysis_id else 'NoAnalysis'
		t = self.commodity_type if self.commodity_type_id else 'NoType'
		c = self.commodity if self.commodity_id else 'NoCommodity'
		return u'({}) [{}] {}'.format( a, t, c )



class Param_CapacityToActivity ( DM.Model ):
	analysis   = DM.ForeignKey( Analysis )
	technology = DM.ForeignKey( Technology )
	value      = DM.FloatField()

	class Meta:
		unique_together = ('analysis', 'technology')


	def __unicode__ ( self ):
		a = self.analysis if self.analysis_id else 'NoAnalysis'
		t = self.technology if self.technology_id else 'NoTechnology'
		return '({}) {}: {}'.format( a, t, self.value )


	def save ( self, *args, **kwargs ):
		if self.value <= 0:
			msg = 'CapacityToActivity value must be a positive value'
			raise ValidationError( msg )

		super( Param_CapacityToActivity, self ).save( *args, **kwargs )



class Param_DemandDefaultDistribution ( DM.Model ):
	timeslice = DM.ForeignKey( Param_SegFrac, unique=True )
	value     = DM.FloatField()


	def __unicode__ ( self ):
		analysis    = self.timeslice.analysis
		season      = self.timeslice.season
		time_of_day = self.timeslice.time_of_day

		return u'({}) {}, {}: {}'.format(
		  analysis, season, time_of_day, self.value )


	def save ( self, *args, **kwargs ):
		if not ( 0 < self.value and self.value <= 1 ):
			raise ValidationError( 'Distribution value must be in range (0, 1].' )

		super( Param_DemandDefaultDistribution, self ).save( *args, **kwargs )



class Param_DemandSpecificDistribution ( DM.Model ):
	timeslice = DM.ForeignKey( Param_SegFrac )
	demand    = DM.ForeignKey( AnalysisCommodity )
	value     = DM.FloatField()

	class Meta:
		unique_together = ('timeslice', 'demand')


	def __unicode__ ( self ):
		a = self.timeslice.analysis    if self.timeslice_id else 'NoTimeslice'
		s = self.timeslice.season      if self.timeslice_id else 'NoTimeslice'
		d = self.timeslice.time_of_day if self.timeslice_id else 'NoTimeslice'
		dem = self.demand if self.demand_id else 'NoDemand'

		return u'({}) {}, {}, {}: {}'.format( a, s, d, dem, self.value )


	def save ( self, *args, **kwargs ):
		if self.demand.commodity_type.name != 'demand':
			msg = 'Distribution commodity must be a type "demand".'
			raise ValidationError( msg )

		if not ( 0 < self.value and self.value <= 1 ):
			raise ValidationError( 'Distribution value must be in range (0, 1].' )

		super( Param_DemandSpecificDistribution, self ).save( *args, **kwargs )



class Param_Demand ( DM.Model ):
	# The check that period is >= Period_0 and is a valid analysis vintage
	# happens in valid()
	period = DM.ForeignKey( Vintage )
	demand = DM.ForeignKey( AnalysisCommodity )
	value  = DM.FloatField()


	class Meta:
		unique_together = ('period', 'demand')


	def __unicode__ ( self ):
		analysis  = self.demand.analysis
		commodity = self.demand.commodity

		return u'({}) {}, {}: {}'.format(
		  analysis, commodity, self.period, self.value )


	def save ( self ):
		if self.demand.commodity_type.name != 'demand':
			msg = 'Demand value must be tied to a commodity of type "demand".'
			raise ValidationError( msg )

		super( Param_Demand, self ).save()



class Param_ResourceBound ( DM.Model ):
	# The check that period is >= Period_0 and is a valid analysis vintage
	# happens in valid()
	period   = DM.ForeignKey( Vintage )
	resource = DM.ForeignKey( AnalysisCommodity )
	value    = DM.FloatField()


	class Meta:
		unique_together = ('period', 'resource')


	def __unicode__ ( self ):
		analysis  = self.resource.analysis
		period    = self.period.vintage
		commodity = self.resource.commodity

		return u'({}) {}, {}: {}'.format(
		  analysis, period, commodity, self.value )


	def save ( self ):
		if self.resource.commodity_type != 'physical':
			msg = 'Resource commodity must be of type "physical".'
			raise ValidationError( msg )

		super( Param_ResourceBound, self ).save()



class PeriodCostParameter ( DM.Model ):
	# The check that period is >= Period_0 and is a valid analysis vintage
	# happens in clean()
	period  = DM.ForeignKey( Vintage )
	process = DM.ForeignKey( Process )
	value   = DM.FloatField()

	class Meta:
		abstract = True
		unique_together = ('period', 'process')


	def __unicode__ ( self ):
		try:
			analysis = self.process.analysis
			period   = self.period.vintage
			tech     = self.process.technology
			vintage  = self.process.vintage.vintage
		except:
			return u'(new - no period or process)'

		return u'({}) {}, {}, {}: {}'.format(
		  analysis, period, tech, vintage, self.value )


	def clean ( self ):
		per = self.period
		p   = self.process
		val = self.value

		if val == 0:
			msg = ('Cost must not be 0, or it is a useless entry.  Consider '
			  'removing the row instead of marking it 0.')
			raise ValidationError( msg )

		if per.vintage < p.analysis.period_0:
			msg = ('Process cannot have a cost before the optimization starts.  '
			  '(period) {} < (start year) {}')
			raise ValidationError( msg.format( per.vintage, p.analysis.period_0 ))

		if per.vintage < p.vintage.vintage:
			msg = ('Process cannot have a cost before it is built.  '
			  '(period) {} < (vintage) {}')
			raise ValidationError( msg.format( per.vintage, p.vintage.vintage ))

		if per.analysis != p.analysis:
			msg = ('Inconsistent analyses!  Attempted to connect a period from '
			  "analysis '{}' to a process from analysis '{}'.  Either add period "
			  "'{}' to analysis '{}' or add the process '{}' to "
			  "analysis '{}'.")
			raise ValidationError( msg.format(
			  vint_analysis, analysis,
			  self.period.vintage, analysis,
			  self.process, vint_analysis
			))


	@classmethod
	def new_with_data ( cls, *args, **kwargs ):
		a   = kwargs['analysis']
		per = kwargs['period']
		p   = kwargs['process']
		val = kwargs['value']

		try:
			per = Vintage.objects.get(analysis=a, vintage=per)
		except ObjectDoesNotExist as e:
			raise ValidationError('Specified vintage does not exist in analysis.')

		obj = cls()
		obj.period  = per
		obj.process = p
		obj.value   = val
		obj.clean()
		obj.save()

		return obj



class Param_CostFixed ( PeriodCostParameter ): pass
class Param_CostVariable ( PeriodCostParameter ): pass



class Param_TechInputSplit ( DM.Model ):
	# The check that technology is valid for this analysis is in valid()
	inp_commodity = DM.ForeignKey( AnalysisCommodity )
	technology    = DM.ForeignKey( Technology )
	fraction      = DM.FloatField()


	class Meta:
		unique_together = ('inp_commodity', 'technology')


	def __unicode__ ( self ):
		analysis = self.inp_commodity.analysis
		inp      = self.inp_commodity.commodity
		tech     = self.technology

		return u'({}) {}, {}: {}'.format( analysis, inp, tech, self.fraction )


	def save ( self ):
		if self.inp_commodity.commodity_type.name != 'physical':
			msg = 'TechInputSplit commodity must be of type "physical".'
			raise ValidationError( msg )

		if not (0 < self.fraction and self.fraction < 1):
			msg = ('Fraction must greater than 0 and less than 1, else it is a '
			  'useless specification.')
			raise ValidationError( msg )

		analysis = self.inp_commodity.analysis
		analysis_techs = Technology.objects.filter(
		  process__analysis=analysis ).distinct()
		if self.technology not in analysis_techs:
			msg = ("Technology class '{}' is not used in any processes of "
			  'Analysis {}')
			raise ValidationError( msg.format( self.technology, analysis ))

		super( Param_TechInputSplit, self ).save()


class Param_TechOutputSplit ( DM.Model ):
	# The check that technology is valid for this analysis is in valid()
	technology    = DM.ForeignKey( Technology )
	out_commodity = DM.ForeignKey( AnalysisCommodity )
	fraction      = DM.FloatField()


	class Meta:
		unique_together = ('technology', 'out_commodity',)


	def __unicode__ ( self ):
		analysis = self.out_commodity.analysis
		out      = self.out_commodity.commodity
		tech     = self.technology

		return u'({}) {}, {}: {}'.format( analysis, tech, out, self.fraction )


	def save ( self ):
		if self.out_commodity.commodity_type.name not in ('demand', 'physical'):
			msg = ('TechOutputSplit commodity must be of type "demand" or '
			  '"physical".')
			raise ValidationError( msg )

		if not (0 < self.fraction and self.fraction < 1):
			msg = ('Fraction must greater than 0 and less than 1, else it is a '
			  'useless specification.')
			raise ValidationError( msg )

		analysis = self.out_commodity.analysis
		analysis_techs = Technology.objects.filter(
		  process__analysis=analysis ).distinct()
		if self.technology not in analysis_techs:
			msg = ("Technology class '{}' is not used in any processes of "
			  'Analysis {}')
			raise ValidationError( msg.format( self.technology, analysis ))

		super( Param_TechOutputSplit, self).save()



class MinMaxParameter ( DM.Model ):
	# The check that period is >= Period_0 and is a valid analysis vintage
	# happens in clean()
	period     = DM.ForeignKey( Vintage )
	technology = DM.ForeignKey( Technology )
	value      = DM.FloatField()

	class Meta:
		abstract = True
		unique_together = ('period', 'technology')

	def __unicode__ ( self ):
		analysis = self.period.analysis
		period   = self.period.vintage
		tech     = self.technology

		return u'({}) {}, {}: {}'.format( analysis, period, tech, self.value )


	def clean ( self ):
		a = self.period.analysis
		p = self.period.vintage
		p0 = a.period_0
		t = self.technology

		if p < p0:
			msg = 'Specified capacity not in optimization horizon'
			raise ValidationError( msg )

		if t not in Technology.objects.filter( process__analysis=a ):
			msg = 'Specified technology not in period analysis'
			raise ValidationError( msg )


class Param_MinCapacity ( MinMaxParameter ): pass
class Param_MaxCapacity ( MinMaxParameter ): pass



class Param_EmissionLimit ( DM.Model ):
	# The check that period is >= Period_0 and is a valid analysis vintage
	# happens in valid()
	period   = DM.ForeignKey( Vintage )
	emission = DM.ForeignKey( AnalysisCommodity )
	value    = DM.FloatField()


	class Meta:
		unique_together = ('period', 'emission')


	def __unicode__ ( self ):
		analysis = self.period.analysis
		period   = self.period.vintage
		emission = self.emission.commodity

		return u'({}) {}, {}: {}'.format(
		  analysis, period, emission, self.value )


	def save ( self ):
		if self.emission.commodity_type.name != 'emission':
			msg = 'EmissionLimit commodity must be of type "emission".'
			raise ValidationError( msg )

		super( Param_EmissionLimit, self).save()



class Param_Efficiency ( DM.Model ):
	# check that Analysis ids match is in clean()
	inp_commodity = DM.ForeignKey( AnalysisCommodity, related_name='EfficiencyInput' )
	process       = DM.ForeignKey( Process )
	out_commodity = DM.ForeignKey( AnalysisCommodity, related_name='EfficiencyOutput' )
	value         = DM.FloatField()

	class Meta:
		unique_together = ('inp_commodity', 'process', 'out_commodity')
		ordering = (
		  'process__technology',
		  'inp_commodity',
		  'out_commodity',
		  'process__vintage'
		)


	def __unicode__ ( self ):
		try:
			analysis = self.process.analysis
			inp      = self.inp_commodity.commodity
			tech     = self.process.technology
			vintage  = self.process.vintage.vintage
			out      = self.out_commodity.commodity
		except:
			return u'(new - unsaved)'

		return u'({}) {} - {}, {} - {}: {}'.format(
		  analysis, inp, tech, vintage, out, self.value )


	def save ( self ):
		epsilon = 1e-9   # something really small

		if self.inp_commodity.commodity_type.name != 'physical':
			msg = 'Efficiency input commodity must be of type "physical".'
			raise ValidationError( msg )

		if self.out_commodity.commodity_type.name not in ('demand', 'physical'):
			msg = ('Efficiency output commodity must be of type "demand" or '
			  '"physical".')
			raise ValidationError( msg )

		if abs(self.value) < epsilon or math.isnan( self.value ):
			msg = ('Process efficiency must not be 0, or it is a useless entry.  '
			  'Consider removing the efficiency instead of marking it 0.'
			  '\nAttempted value: {}')
			raise ValidationError( msg.format( self.value ))

		inp_analysis = self.inp_commodity.analysis
		analysis = self.process.analysis
		out_analysis = self.out_commodity.analysis
		if inp_analysis != analysis or analysis != out_analysis:
			msg = ('Inconsistent analyses!  (input, process, output) analyses '
			  'passed: {}, {}, {}')
			raise ValidationError( msg.format(
			  inp_analysis, analysis, out_analysis ))

		super( Param_Efficiency, self).save()



class Param_EmissionActivity ( DM.Model ):
	emission   = DM.ForeignKey( AnalysisCommodity )
	efficiency = DM.ForeignKey( Param_Efficiency )
	value      = DM.FloatField()


	class Meta:
		unique_together = ( 'emission', 'efficiency' )


	def __unicode__ ( self ):
		if self.efficiency_id:
			analysis = self.efficiency.process.analysis
			inp      = self.efficiency.inp_commodity.commodity
			tech     = self.efficiency.process.technology
			vint     = self.efficiency.process.vintage.vintage
			out      = self.efficiency.out_commodity.commodity
		else:
			analysis = 'NoAnalysis'
			inp  = 'NoInput'
			tech = 'NoTechnology'
			vint = 'NoVintage'
			out  = 'NoOutput'

		if self.emission_id:
			emission = self.emission.commodity
		else:
			emission = 'NoEmission'

		return u'({}) {} {} {} {}: {} {}'.format(
		  analysis, inp, tech, vint, out, emission, self.value )


	def clean ( self ):
		if self.value == 0:
			msg = ('EmissionActivity must not be 0, or it is a useless entry.  '
			  'Consider removing the activity instead of marking it 0.'
			  '\nAttempted value: {}')
			raise ValidationError( msg.format( self.value ))

		emission_analysis = self.emission.analysis
		analysis = self.efficiency.process.analysis
		if emission_analysis != analysis:
			msg = ('Inconsistent analyses!  Attempted to connect a pollutant '
			  "commodity from analysis '{}' to a process from analysis '{}'.  "
			  "Either add the input commodity '{}' to analysis '{}' or add the "
			  "process '{}' to analysis '{}'.")
			raise ValidationError( msg.format(
			  emission_analysis, analysis,
			  self.inp_commodity, analysis,
			  self.efficiency.process, emission_analysis
			))


	def save ( self ):
		if self.emission.commodity_type.name != 'emission':
			msg = 'EmissionActivity commodity must be of type "emission".'
			raise ValidationError( msg )

		super( Param_EmissionActivity, self).save()



class Param_GrowthRate ( DM.Model ):
	analysis   = DM.ForeignKey( Analysis )
	technology = DM.ForeignKey( Technology )
	ratelimit  = DM.FloatField()
	seed       = DM.FloatField()


	class Meta:
		unique_together = ('analysis', 'technology')


	def __unicode__ ( self ):
		analysis = self.analysis_id and self.analysis or 'NoAnalysis'
		tech     = self.technology_id and self.technology or 'NoTechnology'

		return u'({}) {}: {}'.format( analysis, tech, self.ratelimit, self.seed )

