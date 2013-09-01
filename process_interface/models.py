from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models as DM   # Django Models


# One glaring deficiency with Django: lack of database level check constraints.
# Django has the basics like, > 0, not null, and unique/unique_together, but it
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
		return u'({}) {}, {}'.format(
		  self.analysis, self.technology, self.vintage.vintage )


	@property
	def name ( self ):
		return u'{}, {}'.format( self.technology.name, self.vintage.vintage )


	def clean ( self ):
		v = self.vintage.vintage
		e = self.existingcapacity
		l = self.lifetime
		p0 = self.analysis.period_0

		if e:
			if v >= p0:
				msg = ('Vintage is in optimization horizon: cannot specify '
				  'existing capacity.')
				raise ValidationError( msg )

			if e <= 0:
				msg = ('Must specify no existing (empty), or existing capacity '
				  'greater than 0.')
				raise ValidationError( msg )

		if l:
			if l <= 0:
				msg = ('Invalid lifetime: processes must have either no lifetime, '
				  'or a lifetime greater than 0.')
				raise ValidationError( msg )

			if v + l <= p0:
				msg = ('Invalid lifetime: vintage would not be used in analysis: '
				  '{} + {} <= {}')
				raise ValidationError( msg.format( v, l, p0 ))



class Param_LifetimeTech ( DM.Model ):
	analysis   = DM.ForeignKey( Analysis )
	technology = DM.ForeignKey( Technology )
	value      = DM.FloatField()

	class Meta:
		unique_together = ('analysis', 'technology')


	def __unicode__ ( self ):
		return u'({}) {}: {}'.format(
		  self.analysis, self.technology.name, self.value )




class Param_LifetimeTechLoan ( DM.Model ):
	analysis   = DM.ForeignKey( Analysis )
	technology = DM.ForeignKey( Technology )
	value      = DM.FloatField()

	class Meta:
		unique_together = ('analysis', 'technology')


	def __unicode__ ( self ):
		return u'({}) {}: {}'.format(
		  self.analysis, self.technology, self.value )



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


	def save ( self, *args, **kwargs ):
		# Currently, the assumption is that folks will call this in a transaction

		super(Set_commodity_demand, self).save(*args, **kwargs)
		obj, created = Set_commodity_output.objects.get_or_create(
		  analysis  = self.analysis,
		  commodity = self.commodity,
		  demand    = self
		)



class Set_commodity_physical ( DM.Model ):
	analysis  = DM.ForeignKey( Analysis )
	commodity = DM.ForeignKey( Commodity )

	class Meta:
		unique_together = ('analysis', 'commodity',)

	def __unicode__ ( self ):
		return u'({}) {}'.format( self.analysis, self.commodity )


	def save ( self, *args, **kwargs ):
		# Currently, the assumption is that folks will call this in a transaction

		super(Set_commodity_physical, self).save(*args, **kwargs)
		obj, created = Set_commodity_output.objects.get_or_create(
		  analysis  = self.analysis,
		  commodity = self.commodity,
		  physical  = self
		)



class Set_commodity_output ( DM.Model ):
	analysis  = DM.ForeignKey( Analysis )
	commodity = DM.ForeignKey( Commodity )
	demand    = DM.ForeignKey( Set_commodity_demand, null=True )
	physical  = DM.ForeignKey( Set_commodity_physical, null=True )

	class Meta:
		unique_together = ('analysis', 'commodity',)


	def __unicode__ ( self ):
		return '({}) {}'.format( self.analysis, self.commodity )



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
		ordering = ('process', 'period')


	def __unicode__ ( self ):
		try:
			period   = self.period.vintage
			analysis = self.process.analysis
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
			msg = ('Process fixed cost must not be 0, or it is a useless entry.  '
			  'Consider removing the row instead of marking it 0.')
			raise ValidationError( msg )

		if per.vintage < p.analysis.period_0:
			msg = ('Process cannot have a cost before the optimization starts!  '
			  '(period) {} < (start year) {}')
			raise ValidationError( msg.format( per.vintage, p.analysis.period_0 ))

		if per.vintage < p.vintage.vintage:
			msg = ('Process cannot have a cost before it is built!  '
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




class Param_CostVariable ( DM.Model ):
	# The check that period is >= Period_0 and is a valid analysis vintage
	# happens in valid()
	period  = DM.ForeignKey( Vintage )
	process = DM.ForeignKey( Process )
	value   = DM.FloatField()


	class Meta:
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
			msg = ('Process fixed cost must not be 0, or it is a useless entry.  '
			  'Consider removing the row instead of marking it 0.')
			raise ValidationError( msg )

		if per.vintage < p.analysis.period_0:
			msg = ('Process cannot have a cost before the optimization starts!  '
			  '(period) {} < (start year) {}')
			raise ValidationError( msg.format( per.vintage, p.analysis.period_0 ))

		if per.vintage < p.vintage.vintage:
			msg = ('Process cannot have a cost before it is built!  '
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


	update_with_data = classmethod( update_with_process_period_data )


class Param_TechInputSplit ( DM.Model ):
	# The check that technology is valid for this analysis is in valid()
	inp_commodity = DM.ForeignKey( Set_commodity_physical )
	technology    = DM.ForeignKey( Technology )
	fraction      = DM.FloatField()


	class Meta:
		unique_together = ('inp_commodity', 'technology')


	def __unicode__ ( self ):
		analysis = self.inp_commodity.analysis
		inp      = self.inp_commodity.commodity
		tech     = self.technology

		return u'({}) {}, {}: {}'.format( analysis, inp, tech, self.fraction )


	def clean ( self ):
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



class Param_TechOutputSplit ( DM.Model ):
	# The check that technology is valid for this analysis is in valid()
	technology    = DM.ForeignKey( Technology )
	out_commodity = DM.ForeignKey( Set_commodity_output )
	fraction      = DM.FloatField()


	class Meta:
		unique_together = ('technology', 'out_commodity',)


	def __unicode__ ( self ):
		analysis = self.out_commodity.analysis
		out      = self.out_commodity.commodity
		tech     = self.technology

		return u'({}) {}, {}: {}'.format( analysis, tech, out, self.fraction )


	def clean ( self ):
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
	# check that Analysis ids match is in clean()
	inp_commodity = DM.ForeignKey( Set_commodity_physical )
	process       = DM.ForeignKey( Process )
	out_commodity = DM.ForeignKey( Set_commodity_output )
	value         = DM.FloatField()

	class Meta:
		unique_together = ('inp_commodity', 'process', 'out_commodity')


	def __unicode__ ( self ):
		analysis = self.process.analysis
		inp      = self.inp_commodity.commodity
		tech     = self.process.technology
		vintage  = self.process.vintage
		out      = self.out_commodity.commodity

		return u'({}) {} {} {} {}: {}'.format(
		  analysis, inp, tech, vintage, out, self.value )


	def clean ( self ):
		if self.value == 0:
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



class Param_EmissionActivity ( DM.Model ):
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


