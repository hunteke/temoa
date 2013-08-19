from django.contrib.auth.models import User
from django.db import models as DM   # Django Models


# One glaring deficiency with Django: lack of database level check constraints.
# Django has the basic like, > 0, not null, and unique/unique_together, but it
# is not able to check things like "field 1 < field 2".  There is a _lot_ of
# data interdependency in Temoa, so we will have to code these checks into the
# Django views.  We can add most of these checks at the DB level with some
# hand-written SQL, but means that if something /does/ get through (god-forbid,
# someone accesses the DB directly or through another frontend), then data
# integrity might become an issue.  For now, the /only/ supported interaction
# will be through Django.

class Analysis ( DM.Model ):
	user        = DM.ForeignKey( User )
	name        = DM.CharField( max_length=32767 )
	description = DM.TextField('Backround information')
	period_0    = DM.IntegerField()
	global_discount_rate = DM.FloatField()


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



class Technology ( DM.Model ):
	name        = DM.CharField( max_length=32767, unique=True )
	description = DM.TextField()

	# may be overridden, but must be defined by something
	capacity_to_activity = DM.FloatField( null=True )

	class Meta:
		ordering = ('name',)

	def __unicode__ ( self ):
		return unicode( self.name )



class Commodity ( DM.Model ):
	name        = DM.CharField( max_length=32767, unique=True )
	description = DM.TextField('Backround information')

	def __unicode__ ( self ):
		return unicode( self.name )



class Set_tech_baseload ( DM.Model ):
	analysis   = DM.ForeignKey( Analysis )
	technology = DM.ForeignKey( Technology )

	class Meta:
		unique_together = ('analysis', 'technology',)

	def __unicode__ ( self ):
		return u'({}) {}'.format( self.analysis, self.technology )



class Set_tech_storage ( DM.Model ):
	analysis = DM.ForeignKey( Analysis )
	technology  = DM.ForeignKey( Technology )

	class Meta:
		ordering = ('analysis', 'technology')
		unique_together = ('analysis', 'technology',)

	def __unicode__ ( self ):
		return u'({}) {}'.format( self.analysis, self.technology )



class Process ( DM.Model ):
	analysis   = DM.ForeignKey( Analysis )
	technology = DM.ForeignKey( Technology )
	vintage    = DM.ForeignKey( Vintage )

	class Meta:
		ordering = ('analysis', 'technology', 'vintage')
		unique_together = ('analysis', 'technology', 'vintage')

	def __unicode__ ( self ):
		return u'({}) {}, {}'.format(
		  self.analysis, self.technology, self.vintage )


	@property
	def name ( self ):
		return u'{}, {}'.format( self.technology.name, self.vintage.vintage )



class Param_LifetimeTech ( DM.Model ):
	analysis   = DM.ForeignKey( Analysis )
	technology = DM.ForeignKey( Technology )
	value      = DM.FloatField()

	def __unicode__ ( self ):
		return u'({}) {}: {}'.format(
		  self.analysis, self.technology.name, self.value )



class Param_LifetimeProcess ( DM.Model ):
	process = DM.ForeignKey( Process, unique=True )
	value   = DM.FloatField()

	def __unicode__ ( self ):
		return u'{}: {}'.format( self.process, self.value )



class Param_LifetimeTechLoan ( DM.Model ):
	analysis   = DM.ForeignKey( Analysis )
	technology = DM.ForeignKey( Technology )
	value      = DM.FloatField()

	def __unicode__ ( self ):
		return u'({}) {}: {}'.format(
		  self.analysis, self.technology, self.value )



class Param_LifetimeProcessLoan ( DM.Model ):
	process  = DM.ForeignKey( Process, unique=True )
	value    = DM.FloatField()

	def __unicode__ ( self ):
		return u'{}: {}'.format( self.process, self.value )



class Param_ExistingCapacity ( DM.Model ):
	process = DM.ForeignKey( Process, unique=True )
	value   = DM.FloatField()

	class Meta:
		ordering = ('process',)

	def __unicode__ ( self ):
		return u'{}: {}'.format( self.process, self.value )


	def clean ( self ):
		from django.core.exceptions import ValidationError
		if not (self.value > 0):
			msg = ('Process existing capacity must be greater than 0.'
			  '\nAttempted value: {}')
			raise ValidationError( msg.format( self.value))



class Set_commodity_emission ( DM.Model ):
	analysis  = DM.ForeignKey( Analysis )
	commodity = DM.ForeignKey( Commodity )

	class Meta:
		unique_together = ('analysis', 'commodity',)

	def __unicode__ ( self ):
		return u'({}) {}'.format( self.analysis, self.commodity )



class Set_commodity_demand ( DM.Model ):
	analysis  = DM.ForeignKey( Analysis )
	commodity = DM.ForeignKey( Commodity )

	class Meta:
		unique_together = ('analysis', 'commodity',)

	def __unicode__ ( self ):
		return u'({}) {}'.format( self.analysis, self.commodity )



class Set_commodity_physical ( DM.Model ):
	analysis  = DM.ForeignKey( Analysis )
	commodity = DM.ForeignKey( Commodity )

	class Meta:
		unique_together = ('analysis', 'commodity',)

	def __unicode__ ( self ):
		return u'({}) {}'.format( self.analysis, self.commodity )



class Param_CapacityToActivity ( DM.Model ):
	analysis   = DM.ForeignKey( Analysis )
	technology = DM.ForeignKey( Technology )
	value      = DM.FloatField( null=True )

	class Meta:
		unique_together = ('analysis', 'technology')


	def __unicode__ ( self ):
		if self.value:
			return '({}) {}: {} (non-default value)'.format(
			  self.analysis, self.technology, self.value )

		return u'({}) {}: {}'.format(
			  self.analysis, self.technology, self.value )



class Param_DemandDefaultDistribution ( DM.Model ):
	timeslice = DM.ForeignKey( Param_SegFrac, unique=True )
	fraction  = DM.FloatField()


	def __unicode__ ( self ):
		analysis    = self.timeslice.analysis
		season      = self.timeslice.season
		time_of_day = self.timeslice.time_of_day

		return u'({}) {}, {}: {}'.format(
		  analysis, season, time_of_day, self.fraction )



class Param_DemandSpecificDistribution ( DM.Model ):
	timeslice = DM.ForeignKey( Param_SegFrac )
	demand    = DM.ForeignKey( Set_commodity_demand )
	fraction  = DM.FloatField()

	class Meta:
		unique_together = ('timeslice', 'demand')


	def __unicode__ ( self ):
		analysis    = self.timeslice.analysis
		season      = self.timeslice.season
		time_of_day = self.timeslice.time_of_day

		return u'({}) {}, {}, {}: {}'.format(
		  analysis, season, time_of_day, self.demand, self.fraction )



class Param_Demand ( DM.Model ):
	# The check that period is >= Period_0 and is a valid analysis vintage
	# happens in valid()
	period = DM.ForeignKey( Vintage )
	demand = DM.ForeignKey( Set_commodity_demand )
	value  = DM.FloatField()


	class Meta:
		unique_together = ('period', 'demand')


	def __unicode__ ( self ):
		analysis  = self.demand.analysis
		commodity = self.demand.commodity

		return u'({}) {}, {}: {}'.format(
		  analysis, commodity, self.period, self.value )



class Param_ResourceBound ( DM.Model ):
	# The check that period is >= Period_0 and is a valid analysis vintage
	# happens in valid()
	period   = DM.ForeignKey( Vintage )
	resource = DM.ForeignKey( Set_commodity_physical )
	value    = DM.FloatField()


	class Meta:
		unique_together = ('period', 'resource')


	def __unicode__ ( self ):
		analysis  = self.resource.analysis
		period    = self.period.vintage
		commodity = self.resource.commodity

		return u'({}) {}, {}: {}'.format(
		  analysis, period, commodity, self.value )



class Param_CostFixed ( DM.Model ):
	# The check that period is >= Period_0 and is a valid analysis vintage
	# happens in valid()
	period  = DM.ForeignKey( Vintage )
	process = DM.ForeignKey( Process )
	value   = DM.FloatField()


	class Meta:
		unique_together = ('period', 'process')


	def __unicode__ ( self ):
		period   = self.period.vintage
		analysis = self.process.analysis
		tech     = self.process.technology
		vintage  = self.process.vintage


		return u'({}) {}, {}, {}: {}'.format(
		  analysis, period, tech, vintage, self.value )


	def clean ( self ):
		from django.core.exceptions import ValidationError
		if self.value == 0:
			msg = ('Process fixed cost must not be 0, or it is a useless entry.  '
			  'Consider removing the row instead of marking it 0.'
			  '\nAttempted value: {}')
			raise ValidationError( msg.format( self.value ))

		vint_analysis = self.period.analysis
		analysis = self.process.analysis
		if vint_analysis != analysis:
			msg = ('Inconsistent analyses!  Attempted to connect a period from '
			  "analysis '{}' to a process from analysis '{}'.  Either add period "
			  "'{}' to analysis '{}' or add the process '{}' to "
			  "analysis '{}'.")
			raise ValidationError( msg.format(
			  vint_analysis, analysis,
			  self.period.vintage, analysis,
			  self.process, vint_analysis
			))




class Param_CostVariable ( DM.Model ):
	# The check that period is >= Period_0 and is a valid analysis vintage
	# happens in valid()
	period  = DM.ForeignKey( Vintage )
	process = DM.ForeignKey( Process )
	value   = DM.FloatField()


	class Meta:
		unique_together = ('period', 'process')


	def __unicode__ ( self ):
		period   = self.period.vintage
		analysis = self.process.analysis
		tech     = self.process.technology
		vintage  = self.process.vintage


		return u'({}) {}, {}, {}: {}'.format(
		  analysis, period, tech, vintage, self.value )


	def clean ( self ):
		from django.core.exceptions import ValidationError
		if self.value == 0:
			msg = ('Process fixed cost must not be 0, or it is a useless entry.  '
			  'Consider removing the row instead of marking it 0.'
			  '\nAttempted value: {}')
			raise ValidationError( msg.format( self.value ))

		vint_analysis = self.period.analysis
		analysis = self.process.analysis
		if vint_analysis != analysis:
			msg = ('Inconsistent analyses!  Attempted to connect a period from '
			  "analysis '{}' to a process from analysis '{}'.  Either add period "
			  "'{}' to analysis '{}' or add the process '{}' to "
			  "analysis '{}'.")
			raise ValidationError( msg.format(
			  vint_analysis, analysis,
			  self.period.vintage, analysis,
			  self.process, vint_analysis
			))



class Param_CostInvest ( DM.Model ):
	process = DM.ForeignKey( Process, unique=True )
	value   = DM.FloatField()


	def __unicode__ ( self ):
		analysis = self.process.analysis
		tech     = self.process.technology
		vintage  = self.process.vintage

		return u'({}) {}, {}: {}'.format(
		  analysis, tech, vintage, self.value )

	def clean ( self ):
		from django.core.exceptions import ValidationError
		if self.value == 0:
			raise ValidationError( 'Process investment cost must not be 0.' )



class Param_DiscountRate ( DM.Model ):
	process = DM.ForeignKey( Process, unique=True )
	value   = DM.FloatField()

	def __unicode__ ( self ):
		analysis = self.process.analysis
		tech     = self.process.process.technology
		vintage  = self.process.process.vintage

		return u'({}) {}, {}: {}'.format(
		  analysis, tech, vintage, self.value )



class Param_TechInputSplit ( DM.Model ):
	# The check that technology and out_commodity are valid happens in valid()
	inp_commodity = DM.ForeignKey( Set_commodity_physical )
	technology    = DM.ForeignKey( Technology )
	out_commodity = DM.ForeignKey( Commodity )
	fraction      = DM.FloatField()


	class Meta:
		unique_together = ('inp_commodity', 'technology', 'out_commodity')


	def __unicode__ ( self ):
		analysis = self.inp_commodity.analysis
		inp      = self.inp_commodity.commodity
		tech     = self.technology
		out      = self.out_commodity

		return u'({}) {}, {}, {}: {}'.format(
		  analysis, inp, tech, out, self.value )



class Param_TechOutputSplit ( DM.Model ):
	# The check that technology and out_commodity are valid happens in valid()
	inp_commodity = DM.ForeignKey( Set_commodity_physical )
	technology    = DM.ForeignKey( Technology )
	out_commodity = DM.ForeignKey( Commodity )
	fraction      = DM.FloatField()


	class Meta:
		unique_together = ('inp_commodity', 'technology', 'out_commodity')


	def __unicode__ ( self ):
		analysis = self.inp_commodity.analysis
		inp      = self.inp_commodity.commodity
		tech     = self.technology
		out      = self.out_commodity

		return u'({}) {}, {}, {}: {}'.format(
		  analysis, inp, tech, out, self.fraction )



class Param_MinCapacity ( DM.Model ):
	# The check that period is >= Period_0 and is a valid analysis vintage
	# happens in valid()
	period     = DM.ForeignKey( Vintage )
	technology = DM.ForeignKey( Technology )
	value      = DM.FloatField()


	class Meta:
		unique_together = ('period', 'technology')


	def __unicode__ ( self ):
		analysis = self.period.analysis
		period   = self.period.vintage
		tech     = self.technology

		return u'({}) {}, {}: {}'.format( analysis, period, tech, self.value )



class Param_MaxCapacity ( DM.Model ):
	# The check that period is >= Period_0, is a valid analysis vintage, and
	# technology is a valid analysis technology happens in valid()
	period     = DM.ForeignKey( Vintage )
	technology = DM.ForeignKey( Technology )
	value      = DM.FloatField()


	class Meta:
		unique_together = ('period', 'technology')


	def __unicode__ ( self ):
		return u'{}, {}: {}'.format( self.period, self.technology, self.value )



class Param_EmissionLimit ( DM.Model ):
	# The check that period is >= Period_0 and is a valid analysis vintage
	# happens in valid()
	period     = DM.ForeignKey( Vintage )
	emission   = DM.ForeignKey( Set_commodity_emission )
	value      = DM.FloatField()


	class Meta:
		unique_together = ('period', 'emission')


	def __unicode__ ( self ):
		analysis = self.period.analysis
		period   = self.period.vintage
		emission = self.emission.commodity

		return u'({}) {}, {}: {}'.format(
		  analysis, period, emission, self.value )



class Param_Efficiency ( DM.Model ):
	# check that Analysis ids match is in clean(), as is that out_commodity
	# is valid.
	inp_commodity = DM.ForeignKey( Set_commodity_physical )
	process       = DM.ForeignKey( Process )
	out_commodity = DM.ForeignKey( Commodity )
	value         = DM.FloatField()

	class Meta:
		unique_together = ('inp_commodity', 'process', 'out_commodity')


	def __unicode__ ( self ):
		analysis = self.process.analysis
		inp      = self.inp_commodity.commodity
		tech     = self.process.technology
		vintage  = self.process.vintage
		out      = self.out_commodity

		return u'({}) {} {} {} {}: {}'.format(
		  analysis, inp, tech, vintage, out, self.value )


	def clean ( self ):
		from django.core.exceptions import ValidationError
		if self.value == 0:
			msg = ('Process efficiency must not be 0, or it is a useless entry.  '
			  'Consider removing the efficiency instead of marking it 0.'
			  '\nAttempted value: {}')
			raise ValidationError( msg.format( self.value ))

		inp_analysis = self.inp_commodity.analysis
		analysis = self.process.analysis
		if inp_analysis != analysis:
			msg = ('Inconsistent analyses!  Attempted to connect an input '
			  "commodity from analysis '{}' to a process from analysis '{}'.  "
			  "Either add the input commodity '{}' to analysis '{}' or add the "
			  "process '{}' to analysis '{}'.")
			raise ValidationError( msg.format(
			  inp_analysis, analysis,
			  self.inp_commodity, analysis,
			  self.process, inp_analysis
			))

		valid_demands = Set_commodity_demand.objects.filter( analysis=analysis )
		valid_physical = Set_commodity_physical.objects.filter( analysis=analysis )

		valid_outputs = (   set( i.commodity for i in valid_demands )
		                  | set( i.commodity for i in valid_physical ))

		if self.out_commodity not in valid_outputs:
			msg = (u'Unable to connect process <{}> to invalid output commodity '
			  "'{}'.  Do you need to add the commodity to this analysis ({})?")
			raise ValidationError( msg.format(
			  self.process.name, self.out_commodity, analysis.name ))



class Param_EmissionActivity ( DM.Model ):
	# The check that out_commodity is the union set happens in valid()
	emission   = DM.ForeignKey( Set_commodity_emission )
	efficiency = DM.ForeignKey( Param_Efficiency )
	value      = DM.FloatField()


	class Meta:
		unique_together = ( 'emission', 'efficiency' )


	def __unicode__ ( self ):
		analysis = self.efficiency.process.analysis
		emission = self.emission.commodity
		inp      = self.efficiency.inp_commodity.commodity
		tech     = self.efficiency.process.technology
		vintage  = self.efficiency.process.vintage
		out      = self.efficiency.out_commodity

		return u'({}) {} {} {} {}: {} {} '.format(
		  analysis, inp, tech, vintage, out, emission, self.value )



	def clean ( self ):
		from django.core.exceptions import ValidationError
		if self.value == 0:
			msg = ('EmissionActivity must not be 0, or it is a useless entry.  '
			  'Consider removing the activity instead of marking it 0.'
			  '\nAttempted value: {}')
			raise ValidationError( msg.format( self.value ))

		emission_analysis = self.emission.analysis
		analysis = self.efficiency.process.analysis
		if emission_analysis != analysis:
			msg = ('Inconsistent analyses!  Attempted to connect an pollutant '
			  "commodity from analysis '{}' to a process from analysis '{}'.  "
			  "Either add the input commodity '{}' to analysis '{}' or add the "
			  "process '{}' to analysis '{}'.")
			raise ValidationError( msg.format(
			  emission_analysis, analysis,
			  self.inp_commodity, analysis,
			  self.efficiency.process, emission_analysis
			))



class Param_GrowthRateMax ( DM.Model ):
	analysis   = DM.ForeignKey( Analysis )
	technology = DM.ForeignKey( Technology )
	value      = DM.FloatField()

	class Meta:
		unique_together = ('analysis', 'technology')

	def __unicode__ ( self ):
		analysis = self.analysis
		tech     = self.technology

		return u'({}) {}: {}'.format( analysis, tech, self.value )



class Param_GrowthRateSeed ( DM.Model ):
	growth_max = DM.ForeignKey( Param_GrowthRateMax, unique=True )
	value      = DM.FloatField()

	def __unicode__ ( self ):
		analysis = self.growth_max.process.analysis
		tech     = self.growth_max.technology

		return u'({}) {}: {}'.format( analysis, tech, vintage, self.value )


