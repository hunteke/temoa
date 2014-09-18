# vim:sw=3:ts=3:fileencoding=utf-8:list:listchars=tab\:»·,trail\:·:noexpandtab:
# :encoding=utf-8:indentSize=3:tabSize=3:noTabs=false:

__all__ = (
  'Analysis',
  'AnalysisCommodity',
  'Commodity',
  'CommodityType',
  'Param_CapacityFactorProcess',
  'Param_CapacityFactorTech',
  'Param_CostFixed',
  'Param_CostVariable',
  'Param_Demand',
  'Param_DemandSpecificDistribution',
  'Param_Efficiency',
  'Param_EmissionActivity',
  'Param_EmissionLimit',
  'Param_MaxMinCapacity',
  'Param_ResourceBound',
  'Param_SegFrac',
  'Param_TechInputSplit',
  'Param_TechOutputSplit',
  'PeriodCostParameter',
  'Process',
  'Technology',
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


	def __str__ ( self ):
		u, n = 'NoUser', '\r\nNoNameGiven\0\n'
		  # impossible name, if saved normally
		if self.user_id:
			u = self.user.username
		if self.name is not None:
			n = self.name

		return u'{} - {}'.format( u, n )


	def save ( self, *args, **kwargs ):
		self.clean_fields()
		super( Analysis, self ).save( *args, **kwargs )



class Vintage ( DM.Model ):
	analysis = DM.ForeignKey( Analysis )
	vintage  = DM.IntegerField()

	class Meta:
		unique_together = ('analysis', 'vintage')
		ordering = ('analysis', 'vintage')


	def __str__ ( self ):
		a, v = 'NoAnalysis', 'NoVintage'
		if self.analysis_id:
			a = self.analysis
		if self.vintage is not None:
			v = self.vintage
		return '({}) {}'.format( a, v )


	def save ( self, *args, **kwargs ):
		self.clean_fields()
		super( Vintage, self ).save( *args, **kwargs )



class Param_SegFrac ( DM.Model ):
	analysis    = DM.ForeignKey( Analysis )
	season      = DM.CharField( max_length=100 )
	time_of_day = DM.CharField( max_length=100 )
	value       = DM.FloatField()
	demanddefaultdistribution = DM.FloatField( null=True )

	class Meta:
		unique_together = ('analysis', 'season', 'time_of_day')

	def __str__ ( self ):
		a, s, d, val = 'NoAnalysis', 'NoSeason', 'NoTimeOfDay', 'NoValue'
		if self.analysis_id:
			a = self.analysis
		if self.season:
			s = self.season
		if self.time_of_day:
			d = self.time_of_day
		if self.value is not None:
			val = self.value

		return u'({}) {}, {}: {}'.format( a, s, d, val )


	def clean_season ( self ):
		name_re = re.compile( r'^[A-z_]\w*$' )
		if not name_re.match( self.season ):
			msg = ('Season name is not valid.  Use only alphanumeric (A-z, 0-9, '
			  'and underscore [_]) characters and begin with a letter.')
			raise ValidationError( msg )


	def clean_time_of_day ( self ):
		name_re = re.compile( r'^[A-z_]\w*$' )
		if not name_re.match( self.time_of_day ):
			msg = ('"Time of Day" name is not valid.  Use only alphanumeric '
			  '(A-z, 0-9, and underscore [_]) characters and begin with a '
			  'letter.')
			raise ValidationError( msg )


	def clean_value ( self ):
		v = self.value

		if v is None:
			raise ValidationError( 'Must specify time slice value.' )

		try:
			v = float(v)
		except ValueError as ve:
			raise ValidationError( 'Time slice value is not a valid number.' )

		if not (0 < v and v <= 1):
			msg = 'Time slice must be a fractional value between 0 and 1.'
			raise ValidationError( msg )


	def clean_demanddefaultdistribution ( self ):
		ddd = self.demanddefaultdistribution
		if ddd is None:
			return

		try:
			ddd = float(ddd)
		except ValueError as ve:
			msg = 'DemandDefaultDistribution value is not a valid number.'
			raise ValidationError( msg )

		if not (0 < ddd and ddd <= 1):
			msg = ('DemandDefaultDistribution must be a fractional value between '
			  '0 and 1.')
			raise ValidationError( msg )


	def clean ( self ):
		self.clean_season()
		self.clean_time_of_day()
		self.clean_value()
		self.clean_demanddefaultdistribution()


	def save ( self, *args, **kwargs ):
		self.clean()
		super( Param_SegFrac, self ).save( *args, **kwargs )



class Technology ( DM.Model ):
	# There's no need for a limit on the name size, other than practical usage.
	# I can't think of a context that would use more than 100 characters for
	# name, so I think 1024 characters (2**10) is more than adequate storage --
	# overkill, just in case.
	analysis    = DM.ForeignKey( Analysis )
	baseload    = DM.BooleanField( default=False )
	capacitytoactivity = DM.FloatField( null=True )
	description = DM.TextField()
	lifetime    = DM.FloatField( null=True )
	loanlife    = DM.FloatField( null=True )
	name        = DM.CharField( max_length=1024 )
	ratelimit   = DM.FloatField( null=True )
	rateseed    = DM.FloatField( null=True )
	storage     = DM.BooleanField( default=False )

	class Meta:
		unique_together = ('analysis', 'name')
		ordering = ('name',)


	def __str__ ( self ):
		a, n = 'NoAnalysis', '\r\nNoNameGiven\0\n'
		  # impossible name, if saved normally

		if self.analysis_id:
			a = self.analysis
		if self.name is not None:
			n = self.name

		return u'({}) {}'.format( a, n )


	def clean_name ( self ):
		if self.name:
			self.name = re.sub(r'[\s\r\n\v\0]', '', self.name).strip()

		if not self.name:
			raise ValidationError( 'Technologies must have a name.' )


	def clean_description ( self ):
		if self.description:
			self.description = re.sub(r'[\r\v\0]', '', self.description).strip()

		if not self.description:
			raise ValidationError( 'Technologies must have a description.' )


	def clean_life ( self, name='lifetime' ):
		v = getattr( self, name )
		if not v:
			setattr( self, name, None )
			return

		try:
			v = float(v)
		except ValueError as ve:
			msg = 'Technology {} is not a valid number.'
			raise ValidationError( msg.format( name ))

		if v < 0:
			msg = 'Technology {} must not exist or must be a positive value.'
			raise ValidationError( msg.format( name ))

		if v < 1e-9:
			# most likely redundant, given the setattr above, but a small chance
			msg = 'Technology {} must not exist or must be a positive value.'
			raise ValidationError( msg.format( name ))


	def clean_loanlife ( self, name='loanlife' ):
		self.clean_life( name=name )


	def clean_baseload ( self ):
		self.baseload = self.baseload and True or False


	def clean_storage ( self ):
		self.storage = self.storage and True or False


	def clean_capacitytoactivity ( self ):
		c2a = self.capacitytoactivity
		if not c2a:
			self.capacitytoactivity = None
			return

		try:
			c2a = float(c2a)
		except ValueError as ve:
			raise ValidationError( 'CapacityToActivity is not a valid number.' )

		if c2a < 0:
			msg = ('CapacityToActivity must not be specifed or must be a '
			  'positive number.')
			raise ValidationError( msg )

		if c2a < 1e-9:
			msg = ('CapacityToActivity must not be specifed or must be a '
			  'positive number.')
			raise ValidationError( msg )


	def clean_growth_rate ( self ):
		r = self.ratelimit
		s = self.rateseed

		if r is None and s is None:
			return

		if (r is None and s is not None) or (r is not None and s is None):
			msg = ('Either leave the growth rate and seed fields empty, or must '
			  'specify them both.')
			raise ValidationError( msg )

		msg = '{} is not a valid number.'
		try:
			r = float(r)
		except ValueError as ve:
			raise ValidationError( msg.format( 'Rate limit' ))

		try:
			s = float(s)
		except ValueError as ve:
			raise ValidationError( msg.format( 'Rate seed' ))


	def clean ( self ):
		self.clean_name()
		self.clean_description()
		self.clean_life()
		self.clean_loanlife()
		self.clean_baseload()
		self.clean_capacitytoactivity()
		self.clean_storage()
		self.clean_growth_rate()


	def save ( self, *args, **kwargs ):
		self.clean()
		super( Technology, self ).save( *args, **kwargs )



class Commodity ( DM.Model ):
	name        = DM.CharField( max_length=32767, unique=True )
	description = DM.TextField('Backround information')

	def __str__ ( self ):
		n = '\r\nNoNameGiven\0\n'  # impossible name, if saved normally
		if self.name is not None:
			n = self.name

		return str( n )



class Process ( DM.Model ):
	technology       = DM.ForeignKey( Technology )
	vintage          = DM.ForeignKey( Vintage )
	lifetime         = DM.FloatField( null=True )
	loanlife         = DM.FloatField( null=True )
	costinvest       = DM.FloatField( null=True )
	discountrate     = DM.FloatField( null=True )
	existingcapacity = DM.FloatField( null=True )

	class Meta:
		ordering = ('technology__analysis', 'technology', 'vintage')
		unique_together = ('technology', 'vintage')

	def __str__ ( self ):
		a, t, v = 'NoAnalysis', 'NoTechnology', 'NoVintage'
		if self.technology_id:
			t = self.technology.name
			a = self.technology.analysis
		if self.vintage_id:
			v = self.vintage.vintage

		return u'({}) {}, {}'.format( a, t, v )


	@property
	def name ( self ):
		return u'{}, {}'.format( self.technology.name, self.vintage.vintage )


	def update_with_data ( self, data ):
		for attr in ('lifetime', 'loanlife', 'costinvest', 'discountrate',
		  'existingcapacity'
		):
			if attr in data and data[attr]:
				setattr( self, attr, data[attr] )
			elif attr in data:
				setattr( self, attr, None )

		self.save()


	def clean_valid_vintage ( self ):
		vintages = Vintage.objects.filter( analysis=self.technology.analysis
		  ).order_by( '-vintage' )

		try:
			if self.vintage not in vintages:
				raise ValidationError('Vintage does not exist in this analysis.')
		except ObjectDoesNotExist as e:
			raise ValidationError('Process must have a vintage.')
		# Is the vintage valid for this analysis?

		# Is the vintage a vintage year as opposed the final year?
		if self.vintage == vintages.first():
			msg = ('The final year in the analysis vintages is not actually a '
			  'vintage.  It is a marker for calculation of the last period '
			  'length, and is therefore not a valid vintage.')
			raise ValidationError( msg )


	def clean_valid_lifetime ( self ):
		"""
		All we know for sure at this stage is that lifetime can only be None or
		positive.  Given that data sets are expected to be constantly in flux, so
		save the larger validation for the UI, and dat download.
		"""
		if self.lifetime is None:
			return

		if self.lifetime <= 0:
			msg = ('Either specify a positive integer or nothing at all.')
			raise ValidationError( msg )


	def clean_valid_existingcapacity ( self ):
		"""
		All we know for sure at this stage is that existingcapacity can only be
		None or positive.  Given that data sets are expected to be constantly in
		flux, so save the larger validation for the UI, and dat download.
		"""
		if self.existingcapacity is None:
			return

		if self.existingcapacity <= 0:
			msg = ('Either specify a positive integer or nothing at all.')
			raise ValidationError( msg )


	def clean ( self ):
		self.clean_valid_vintage()
		self.clean_valid_lifetime()
		self.clean_valid_existingcapacity()


	def save ( self, *args, **kwargs ):
		self.clean()
		super( Process, self ).save( *args, **kwargs )



class CommodityType ( DM.Model ):
	name = DM.CharField( max_length=64, unique=True )

	def __str__ ( self ):
		return u'{}'.format( self.name )


	def clean ( self ):
		self.name = re.sub(ur'[\n\r\v\t\0]', '', self.name).strip()

		if not self.name:
			raise ValidationError( 'No name specified for CommodityType.' )


	def save ( self, *args, **kwargs ):
		self.clean()
		super( CommodityType, self ).save( *args, **kwargs )



class AnalysisCommodity ( DM.Model ):
	analysis       = DM.ForeignKey( Analysis )
	commodity_type = DM.ForeignKey( CommodityType )
	commodity      = DM.ForeignKey( Commodity )


	class Meta:
		ordering = ('analysis', 'commodity_type', 'commodity')
		unique_together = ('analysis', 'commodity')


	def __str__ ( self ):
		a, ty, c = 'NoAnalysis', 'NoType', 'NoCommodity'
		if self.analysis_id:
			a = self.analysis
		if self.commodity_type_id:
			ty = self.commodity_type
		if self.commodity_id:
			c = self.commodity

		return u'({}) [{}] {}'.format( a, ty, c )



class Param_DemandSpecificDistribution ( DM.Model ):
	timeslice = DM.ForeignKey( Param_SegFrac )
	demand    = DM.ForeignKey( AnalysisCommodity )
	value     = DM.FloatField()

	class Meta:
		unique_together = ('timeslice', 'demand')


	def __str__ ( self ):
		a, s, d, dem = 'NoTimeslice', 'NoTimeslice', 'NoTimeslice', 'NoDemand'
		val = 'NoValue'
		if self.timeslice_id:
			a = self.timeslice.analysis
			s = self.timeslice.season
			d = self.timeslice.time_of_day
		if self.demand_id:
			dem = self.demand.commodity.name
		if self.value is not None:
			val = self.value

		return u'({}) {}, {}, {}: {}'.format( a, s, d, dem, val )


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


	def __str__ ( self ):
		a, c, p, val = 'NoDemand', 'NoDemand', 'NoPeriod', 'NoValue'
		if self.demand_id:
			a = self.demand.analysis
			c = self.demand.commodity
		if self.period_id:
			p = self.period.vintage
		if self.value is not None:
			val = self.value

		return u'({}) {}, {}: {}'.format( a, c, p, val )


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


	def __str__ ( self ):
		a, p, c, val = 'NoResource', 'NoPeriod', 'NoResource', 'NoValue'
		if self.resource_id:
			a = self.resource.analysis
			c = self.resource.commodity
		if self.period_id:
			p = self.period.vintage
		if self.value is not None:
			val = self.value

		return u'({}) {}, {}: {}'.format( a, p, c, val )


	def save ( self ):
		if self.resource.commodity_type.name != 'physical':
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
		ordering = (
		  'process__technology__analysis',
		  'process__technology',
		  'process__vintage',
		  'period'
		)


	def __str__ ( self ):
		a, p, t, v = 'NoProcess', 'NoPeriod', 'NoProcess', 'NoProcess'
		val = 'NoValue'
		if self.process_id:
			t = self.process.technology.name
			a = self.process.technology.analysis
			v = self.process.vintage.vintage
		if self.period_id:
			p = self.period.vintage
		if self.value is not None:
			val = self.value

		return u'({}) {}, {}, {}: {}'.format( a, p, t, v, val )


	def clean ( self ):
		per = self.period
		p   = self.process
		val = self.value

		epsilon = 1e-9
		if abs(val) < epsilon and -abs(val) > -epsilon:
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


	def __str__ ( self ):
		a, i, t, f = 'NoAnalysis', 'NoInput', 'NoTechnology', 'NoValue'
		if self.technology_id:
			t = self.technology.name
			a = self.technology.analysis
		if self.inp_commodity_id:
			i = self.inp_commodity.commodity.name
		if self.fraction is not None:
			f = self.fraction

		return u'({}) {}, {}: {}'.format( a, i, t, f )


	def clean ( self ):
		if self.inp_commodity.commodity_type.name != 'physical':
			msg = 'TechInputSplit commodity must be of type "physical".'
			raise ValidationError( msg )

		if not (0 < self.fraction and self.fraction < 1):
			msg = ('Fraction must greater than 0 and less than 1, else it is a '
			  'useless specification.')
			raise ValidationError( msg )

		analysis = self.inp_commodity.analysis
		techs = Technology.objects.filter( analysis=analysis ).distinct()
		if self.technology not in techs:
			msg = ("Technology class '{}' is not used in any processes of "
			  'Analysis {}')
			raise ValidationError( msg.format( self.technology, analysis ))


	def save ( self, *args, **kwargs ):
		self.clean()
		super( Param_TechInputSplit, self ).save( *args, **kwargs )


class Param_TechOutputSplit ( DM.Model ):
	# The check that technology is valid for this analysis is in valid()
	technology    = DM.ForeignKey( Technology )
	out_commodity = DM.ForeignKey( AnalysisCommodity )
	fraction      = DM.FloatField()


	class Meta:
		unique_together = ('technology', 'out_commodity',)


	def __str__ ( self ):
		t, o, val = '(NoAnalysis) NoTechnology', 'NoOutput', 'NoValue'
		if self.technology_id:
			t = self.technology
		if self.out_commodity_id:
			o = self.out_commodity.commodity
		if self.fraction is not None:
			val = self.fraction

		return u'{}, {}: {}'.format( t, o, val )


	def clean ( self ):
		if self.out_commodity.commodity_type.name not in ('demand', 'physical'):
			msg = ('TechOutputSplit commodity must be of type "demand" or '
			  '"physical".')
			raise ValidationError( msg )

		if not (0 < self.fraction and self.fraction < 1):
			msg = ('Fraction must greater than 0 and less than 1, else it is a '
			  'useless specification.')
			raise ValidationError( msg )

		analysis = self.out_commodity.analysis
		techs = Technology.objects.filter( analysis=analysis ).distinct()
		if self.technology not in techs:
			msg = ("Technology class '{}' is not used in any processes of "
			  'Analysis {}')
			raise ValidationError( msg.format( self.technology, analysis ))


	def save ( self, *args, **kwargs ):
		self.clean()
		super( Param_TechOutputSplit, self ).save( *args, **kwargs )



class Param_MaxMinCapacity ( DM.Model ):
	# The check that period is >= Period_0 and is a valid analysis vintage
	# happens in clean()
	period     = DM.ForeignKey( Vintage )
	technology = DM.ForeignKey( Technology )
	maximum    = DM.FloatField( null=True )
	minimum    = DM.FloatField( null=True )

	class Meta:
		unique_together = ('period', 'technology')
		ordering = ( 'technology__name', 'period__vintage' )

	def __str__ ( self ):
		a, p, t, mx, mn = 'NoPeriod', 'NoPeriod', 'NoTechnology', 'NoMax', 'NoMin'
		if self.period_id:
			a = self.period.analysis
			p = self.period.vintage
		if self.technology_id:
			t = self.technology.name
		if self.maximum is not None:
			mx = self.maximum
		if self.minimum is not None:
			mn = self.minimum

		return u'({}) {}, {}: [{}, {}]'.format( a, p, t, mn, mx )


	def clean_period_and_technology ( self ):
		a = self.period.analysis
		p = self.period.vintage
		p0 = a.period_0
		t = self.technology

		if p < p0:
			msg = 'Specified capacity not in optimization horizon'
			raise ValidationError( msg )

		if t not in Technology.objects.filter( analysis=a ):
			msg = 'Specified technology not in period analysis'
			raise ValidationError( msg )


	def clean_minimum ( self ):
		mn = self.minimum
		if mn is None:
			return

		try:
			mn = float(mn)
		except ValueError as ve:
			raise ValidationError('Minimum capacity is not a valid number.')

		if mn < 0:
			raise ValidationError('Minimum capacity cannot be negative.')

		if mn < 1e-9:
			msg = 'Minimum capacity must not be specified, or must be positive.'
			raise ValidationError( msg )


	def clean_maximum ( self ):
		mx = self.maximum
		if mx is None:
			return

		try:
			mx = float(mx)
		except ValueError as ve:
			raise ValidationError('Maximum capacity is not a valid number.')

		if mx < 0:
			raise ValidationError('Maximum capacity cannot be negative.')

		# intentionally no mx == 0 check: maximum capacity /could/ be 0.


	def clean_max_and_min ( self ):
		mn, mx = self.minimum, self.maximum

		if mn is None and mx is None:
			msg = ('Pointless attempt to unset both minimum and maximum '
			  'period-technology capacities.  Remove the entry instead.')
			raise ValidationError( msg )


	def clean ( self ):
		self.clean_period_and_technology()
		self.clean_minimum()
		self.clean_maximum()
		self.clean_max_and_min()


	def save ( self, *args, **kwargs ):
		self.clean()
		super( Param_MaxMinCapacity, self ).save( *args, **kwargs )



class Param_EmissionLimit ( DM.Model ):
	# The check that period is >= Period_0 and is a valid analysis vintage
	# happens in valid()
	period   = DM.ForeignKey( Vintage )
	emission = DM.ForeignKey( AnalysisCommodity )
	value    = DM.FloatField()


	class Meta:
		unique_together = ('period', 'emission')


	def __str__ ( self ):
		a, p, e, val = 'NoPeriod', 'NoPeriod', 'NoEmission', 'NoValue'
		if self.period_id:
			a = self.period.analysis
			p = self.period.vintage
		if self.emission_id:
			e = self.emission.commodity.name
		if self.value is not None:
			val = self.value

		return u'({}) {}, {}: {}'.format( a, p, e, val )


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


	def __str__ ( self ):
		a, t, v = 'NoProcess', 'NoProcess', 'NoProcess'
		i, o = 'NoInput', 'NoOutput'
		val = 'NoValue'
		if self.process_id:
			a = self.process.technology.analysis
			t = self.process.technology.name
			v = self.process.vintage.vintage
		if self.inp_commodity_id:
			i = self.inp_commodity.commodity.name
		if self.out_commodity_id:
			o = self.out_commodity.commodity.name
		if self.value is not None:
			val = self.value

		return u'({}) {} - {}, {} - {}: {}'.format( a, i, t, v, o, val )


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
		analysis = self.process.technology.analysis
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


	def __str__ ( self ):
		a, i, t, v, o = ('NoEfficiency',) * 5
		e, val = 'NoEmission', 'NoValue'
		if self.efficiency_id:
			a = self.efficiency.process.technology.analysis
			i = self.efficiency.inp_commodity.commodity.name
			t = self.efficiency.process.technology.name
			v = self.efficiency.process.vintage.vintage
			o = self.efficiency.out_commodity.commodity.name
		if self.emission_id:
			e = self.emission.commodity.name
		if self.value is not None:
			val = self.value

		return u'({}) {} - {} {} - {}: {} {}'.format( a, i, t, v, o, e, val )


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



class Param_CapacityFactorTech ( DM.Model ):
	timeslice  = DM.ForeignKey( Param_SegFrac )
	technology = DM.ForeignKey( Technology )
	value      = DM.FloatField()

	class Meta:
		unique_together = ('timeslice', 'technology')
		ordering = (
		  'technology__name',
		  'timeslice__season',
		  'timeslice__time_of_day'
		 )


	def __str__ ( self ):
		a, s, d = ('NoTimeslice',) * 3
		t, val = 'NoTechnology', 'NoValue'
		if self.timeslice_id:
			a = self.timeslice.analysis
			s = self.timeslice.season
			d = self.timeslice.time_of_day
		if self.technology_id:
			t = self.technology.name
		if self.value is not None:
			val = self.value

		return u'({}) {} - {}, {}: {}'.format( a, t, s, d, val )


	def save ( self ):
		epsilon = 1e-9   # something really small

		a = self.timeslice.analysis
		t = self.technology

		# Check that the linked analysis utilizes this technology.
		if not t.pk:
			msg = ('CapacityFactorTech must reference an existing technology.  '
			  'Do you need to create a technology?')
			raise ValidationError( msg )

		if t not in Technology.objects.filter( name=t.name, process__analysis=a ):
			msg = 'Technology does not exist in this analysis.'
			raise ValidationError( msg )

		if abs(self.value) < epsilon or math.isnan( self.value ):
			msg = ('CapacityFactorTech must be between 0 and 1.'
			  '\nAttempted value: {}')
			raise ValidationError( msg.format( self.value ))

		super( Param_CapacityFactorTech, self).save()



class Param_CapacityFactorProcess ( DM.Model ):
	# check that Analysis ids match is in save()
	timeslice = DM.ForeignKey( Param_SegFrac )
	process   = DM.ForeignKey( Process )
	value     = DM.FloatField()

	class Meta:
		unique_together = ('timeslice', 'process')
		ordering = (
		  'process__technology',
		  'process__vintage',
		  'timeslice__season',
		  'timeslice__time_of_day',
		)


	def __str__ ( self ):
		a, t, v = ('NoProcess',) * 3
		s, d = ('NoTimeslice',) * 2
		val = 'NoValue'
		if self.process_id:
			a = self.process.technology.analysis
			t = self.process.technology.name
			v = self.process.vintage.vintage
		if self.timeslice_id:
			s = self.timeslice.season
			d = self.timeslice.time_of_day
		if self.value is not None:
			val = self.value

		return u'({}) {}, {} - {}, {}: {}'.format( a, t, v, s, d, val )


	def save ( self ):
		epsilon = 1e-9   # something really small

		if self.timeslice.analysis != self.process.technology.analysis:
			msg = ('Inconsistent analyses!  CapacityFactorProcess timeslice and '
			  'process reference different analyses.')
			raise ValidationError( msg )

		if math.isnan( self.value ) or not ( 0 < self.value and self.value <= 1):
			msg = ('CapacityFactorProcess must be between 0 and 1.'
			  '\nAttempted value: {}')
			raise ValidationError( msg.format( self.value ))

		super( Param_CapacityFactorProcess, self).save()
