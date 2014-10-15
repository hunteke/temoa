# vim:sw=3:ts=3:fileencoding=utf-8:list:listchars=tab\:»·,trail\:·:noexpandtab:
# :encoding=utf-8:indentSize=3:tabSize=3:noTabs=false:

from os import urandom
from random import randint, random
import re

import factory

from django.contrib.auth.models import User as DjangoUser
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
from django.db.utils import IntegrityError
from django.test import TestCase

from process_interface.models import (
  Analysis,
  AnalysisCommodity,
  Commodity,
  CommodityType,
  Param_MaxMinCapacity,
  Param_SegFrac,
  Param_TechInputSplit,
  Param_TechOutputSplit,
  Process,
  Technology,
  Vintage,
)



class UserFactory ( factory.django.DjangoModelFactory ):
	class Meta:
		model = DjangoUser

	is_active = True
	is_staff = False
	is_superuser = False
	first_name = 'Jiminy'
	last_name = 'Cricket'
	username = 'jimbob'
	email = 'mrjim@example.net'



class AnalysisFactory ( factory.django.DjangoModelFactory ):
	class Meta:
		model = Analysis

	user = factory.SubFactory( UserFactory )
	name = 'Unit Test Analysis'
	description = 'Analysis automatically created during unit testing.'
	period_0 = 0
	global_discount_rate = 0.05



class VintageFactory ( factory.django.DjangoModelFactory ):
	class Meta:
		model = Vintage

	analysis = factory.SubFactory( AnalysisFactory )
	vintage  = 0



class TechnologyFactory ( factory.django.DjangoModelFactory ):
	class Meta:
		model = Technology

	analysis = factory.SubFactory( AnalysisFactory )
	baseload = False
	capacitytoactivity = None
	description = 'Technology automatically created during unit testing.'
	lifetime = None
	loanlife = None
	name = 'Unit Test Technology'
	ratelimit = None
	rateseed = None
	storage = False



class CommodityFactory ( factory.django.DjangoModelFactory ):
	class Meta:
		model = Commodity

	name = 'Unit Test Commodity'
	description = 'Commodity automatically created during unit testing.'



class Param_SegFracFactory ( factory.django.DjangoModelFactory ):
	class Meta:
		model = Param_SegFrac

	analysis = factory.SubFactory( AnalysisFactory )
	season = 'Unit_Test_Season'
	time_of_day = 'Unit_Test_Day'
	value = 1
	demanddefaultdistribution = 0.8



class ExistingProcessFactory ( factory.django.DjangoModelFactory ):
	class Meta:
		model = Process

	technology       = factory.SubFactory( TechnologyFactory )
	vintage          = factory.SubFactory( VintageFactory )
	lifetime         = 10
	loanlife         = None
	costinvest       = None
	discountrate     = None
	existingcapacity = 31



class Param_MaxMinCapacityFactory ( factory.django.DjangoModelFactory ):
	class Meta:
		model = Param_MaxMinCapacity

	period = factory.SubFactory( VintageFactory )
	technology = factory.SubFactory( TechnologyFactory )
	maximum = 10
	minimum = 1



class ModelAnalysisTest ( TestCase ):

	def test_analysis_build ( self ):
		a = AnalysisFactory.build()
		attr = AnalysisFactory.attributes()

		self.assertEqual( a.name, attr['name'] )
		self.assertEqual( a.description, attr['description'] )
		self.assertEqual( a.period_0, attr['period_0'] )
		self.assertEqual( a.global_discount_rate, attr['global_discount_rate'] )


	def test_analysis_create ( self ):
		a = AnalysisFactory.create()
		b = Analysis.objects.get( pk=a.pk )

		self.assertEqual( a.pk, b.pk )
		self.assertEqual( a.user, b.user )
		self.assertEqual( a.name, b.name )
		self.assertEqual( a.description, b.description )
		self.assertEqual( a.period_0, b.period_0 )
		self.assertEqual( a.global_discount_rate, b.global_discount_rate )


	def test_analysis_update ( self ):
		a = AnalysisFactory.create()

		a.name        = new_name         = u'Something New'
		a.description = new_description  = u'New Description ...'
		a.period_0    = new_period_0     = 15
		a.global_discount_rate = new_gdr = 0.47
		a.save()

		b = Analysis.objects.get( pk=a.pk )
		self.assertEqual( b.pk, a.pk )
		self.assertEqual( b.user, a.user )
		self.assertEqual( b.name, new_name )
		self.assertEqual( b.description, new_description )
		self.assertEqual( b.period_0, new_period_0 )
		self.assertEqual( b.global_discount_rate, new_gdr )


	def test_analysis_period_0_is_integer ( self ):
		u = UserFactory.create()
		a = AnalysisFactory.build( user=u, period_0=5.85 )
		a.clean_fields()

		self.assertEqual( a.period_0, 5 )


	def test_save_cleans_fields ( self ):
		u = UserFactory.create()
		a = AnalysisFactory.build( user=u, period_0='asdf' )
		with self.assertRaises( ValidationError ) as ve:
			a.save()

		self.assertIn( 'period_0', ve.exception.message_dict )
		self.assertIn( ' must be an integer',
		  str(ve.exception.message_dict['period_0']) )


	def test_analysis_uniqueness ( self ):
		a = AnalysisFactory.create()
		with self.assertRaises( IntegrityError ) as ie:
			AnalysisFactory.create(user=a.user)


	def test_analysis_str_empty ( self ):
		a = Analysis()
		self.assertEqual( str(a), 'NoUser - NoName')


	def test_analysis_str_only_user ( self ):
		a = Analysis( user=UserFactory.create() )
		expected = u'{} - NoName'.format( a.user.username )
		self.assertEqual( str(a), expected )


	def test_analysis_str_only_name ( self ):
		a = Analysis( name='Unit Test Analysis' )
		expected = u'NoUser - {}'.format( a.name )
		self.assertEqual( str(a), expected )



class ModelTechnologyTest ( TestCase ):

	def test_name_with_bad_characters ( self ):
		t = TechnologyFactory.build()
		t.name = u'Name with \r\n\0\t\v bad characters'
		t.clean()
		self.assertNotIn( '\0', t.name )
		self.assertNotIn( '\n', t.name )
		self.assertNotIn( '\r', t.name )
		self.assertNotIn( '\t', t.name )
		self.assertNotIn( '\v', t.name )
		self.assertNotIn( ' ', t.name )


	def test_no_name_raises_validation_error ( self ):
		t = TechnologyFactory.build()
		t.name = ''
		with self.assertRaises( ValidationError ) as ve:
			t.clean()

		self.assertIn( u'must have a name', str(ve.exception) )


	def test_no_description_raises_validation_error ( self ):
		t = TechnologyFactory.build()
		t.description = None
		with self.assertRaises( ValidationError ) as ve:
			t.clean()

		self.assertIn( u'must have a description', str(ve.exception) )


	def test_str_empty ( self ):
		t = Technology()
		expected = u'(NoAnalysis) \r\nNoNameGiven\0\n'
		self.assertEqual( str(t), expected )


	def test_str_name ( self ):
		t = TechnologyFactory.build()
		expected = u'(NoAnalysis) {}'.format( t.name )
		self.assertEqual( str(t), expected )


	def test_capacitytoactivity_can_be_null ( self ):
		t = TechnologyFactory.build()

		t.capacitytoactivity = None
		try:
			t.clean_capacitytoactivity()
		except:
			msg = ('Technology parameter capacitytoactivity does not have to be '
			  'specified.')
			self.fail( msg )


	def test_capacitytoactivity_empty_is_converted_to_null ( self ):
		t = TechnologyFactory.build()

		for val in (0, [], {}, (), '', False):
			t.capacitytoactivity = val
			t.clean_capacitytoactivity()
			self.assertEqual( t.capacitytoactivity, None )


	def test_capacitytoactivity_requires_valid_number ( self ):
		t = TechnologyFactory.build()

		t.capacitytoactivity = 'asdf'
		with self.assertRaises( ValidationError ):
			t.clean_capacitytoactivity()


	def test_capacitytoactivity_cannot_be_negative ( self ):
		t = TechnologyFactory.build()

		t.capacitytoactivity = random() * randint(-1e9, -1)
		with self.assertRaises( ValidationError ):
			t.clean_capacitytoactivity()


	def test_capacitytoactivity_must_not_be_almost_zero ( self ):
		""" This will probably never occur, but the threshold is 1e-9.  Numbers
		smaller than that snuck past the 'not 0' test, but are close enough to be
		practically 0.  Thus, inform user of the error. """
		t = TechnologyFactory.build()

		t.capacitytoactivity = 1e-10
		with self.assertRaises( ValidationError ):
			t.clean_capacitytoactivity()


	def test_capacitytoactivity_can_be_positive ( self ):
		t = TechnologyFactory.build()

		t.capacitytoactivity = random() * randint(1, 1e9)
		try:
			t.clean_capacitytoactivity()
		except:
			self.fail('A positive capacitytoactivity should be valid.')
			raise


	def test_baseload_is_true_or_false ( self ):
		t = TechnologyFactory.build()

		t.baseload = None
		t.clean_baseload()
		self.assertEqual( t.baseload, False )

		t.baseload = 'asdf'
		t.clean_baseload()
		self.assertEqual( t.baseload, True )

		t.baseload = urandom( 2 )  # two bytes worth of random data
		truth_value = t.baseload and True or False
		t.clean_baseload()
		self.assertEqual( t.baseload, truth_value )


	def test_storage_is_true_or_false ( self ):
		t = TechnologyFactory.build()

		t.storage = None
		t.clean_storage()
		self.assertEqual( t.storage, False )

		t.storage = 'asdf'
		t.clean_storage()
		self.assertEqual( t.storage, True )

		t.storage = urandom( 2 )  # two bytes worth of random data
		truth_value = t.storage and True or False
		t.clean_storage()
		self.assertEqual( t.storage, truth_value )


	def test_lifetime_can_be_null ( self ):
		t = TechnologyFactory.build()

		t.lifetime = None
		try:
			t.clean_life()
		except:
			self.fail('Technology lifetime does not have to be specified.')


	def test_lifetime_empty_is_converted_to_null ( self ):
		t = TechnologyFactory.build()

		for val in (0, [], {}, (), '', False):
			t.lifetime = val
			t.clean_life()
			self.assertEqual( t.lifetime, None )


	def test_lifetime_requires_valid_number ( self ):
		t = TechnologyFactory.build()

		t.lifetime = 'asdf'
		with self.assertRaises( ValidationError ):
			t.clean_life()


	def test_lifetime_cannot_be_negative ( self ):
		t = TechnologyFactory.build()

		t.lifetime = random() * randint(-1e9, -1)
		with self.assertRaises( ValidationError ):
			t.clean_life()


	def test_lifetime_must_not_be_almost_zero ( self ):
		""" This will probably never occur, but the threshold is 1e-9.  Numbers
		smaller than that snuck past the 'not 0' test, but are close enough to be
		practically 0.  Thus, inform user of the error. """
		t = TechnologyFactory.build()

		t.lifetime = 1e-10
		with self.assertRaises( ValidationError ):
			t.clean_life()


	def test_lifetime_can_be_positive ( self ):
		t = TechnologyFactory.build()

		t.lifetime = random() * randint(1, 1e9)
		try:
			t.clean_life()
		except:
			self.fail('Positive lifetimes should be valid.')
			raise


	def test_loanlife_can_be_null ( self ):
		t = TechnologyFactory.build()

		t.loanlife = None
		try:
			t.clean_loanlife()
		except:
			self.fail('Technology loanlife does not have to be specified.')


	def test_loanlife_empty_is_converted_to_null ( self ):
		t = TechnologyFactory.build()

		for val in (0, [], {}, (), '', False):
			t.loanlife = val
			t.clean_loanlife()
			self.assertEqual( t.loanlife, None )


	def test_loanlife_requires_valid_number ( self ):
		t = TechnologyFactory.build()

		t.loanlife = 'asdf'
		with self.assertRaises( ValidationError ):
			t.clean_loanlife()


	def test_loanlife_cannot_be_negative ( self ):
		t = TechnologyFactory.build()

		t.loanlife = random() * randint(-1e9, -1)
		with self.assertRaises( ValidationError ):
			t.clean_loanlife()


	def test_loanlife_must_not_be_almost_zero ( self ):
		""" This will probably never occur, but the threshold is 1e-9.  Numbers
		smaller than that snuck past the 'not 0' test, but are close enough to be
		practically 0.  Thus, inform user of the error. """
		t = TechnologyFactory.build()

		t.loanlife = 1e-10
		with self.assertRaises( ValidationError ):
			t.clean_loanlife()


	def test_loanlife_can_be_positive ( self ):
		t = TechnologyFactory.build()

		t.loanlife = random() * randint(1, 1e9)
		try:
			t.clean_loanlife()
		except:
			self.fail('Positive loanlife values should be valid.')
			raise


	def test_growth_rate_fields_both_null_is_okay ( self ):
		t = TechnologyFactory.build()

		t.ratelimit = t.rateseed = None
		try:
			t.clean_growth_rate()
		except:
			msg = ('It should be allowed for both ratelimit and rateseed to be '
			  'null.')
			self.fail( msg )


	def test_growth_rate_only_1_field_set_is_error ( self ):
		t = TechnologyFactory.build()

		t.ratelimit = 0.5
		t.rateseed = None
		with self.assertRaises( ValidationError ):
			t.clean_growth_rate()

		t.ratelimit = None
		t.rateseed = 0.5
		with self.assertRaises( ValidationError ):
			t.clean_growth_rate()


	def test_growth_rate_requires_valid_numbers ( self ):
		t = TechnologyFactory.build()

		t.ratelimit = 'asdf'
		t.rateseed = 1
		with self.assertRaises( ValidationError ):
			t.clean_growth_rate()

		t.ratelimit = 1
		t.rateseed = 'asdf'
		with self.assertRaises( ValidationError ):
			t.clean_growth_rate()


	def test_growth_rate_accepts_valid_numbers ( self ):
		t = TechnologyFactory.build()

		t.ratelimit = -1
		t.rateseed = 1
		try:
			t.clean_growth_rate()
		except:
			self.fail('Growth Rate fields should accept any number.')



class ModelVintageTest ( TestCase ):

	def test_uniqueness_creation ( self ):
		a = VintageFactory.create()
		with self.assertRaises( IntegrityError ) as ie:
			VintageFactory.create(analysis=a.analysis)


	def test_uniqueness_update ( self ):
		a = VintageFactory.create()
		b = VintageFactory.create( vintage=a.vintage+10, analysis=a.analysis )

		b.vintage = a.vintage
		with self.assertRaises( IntegrityError ) as ie:
			b.save()


	def test_vintage_is_integer ( self ):
		a = AnalysisFactory.create()
		v = VintageFactory.build( analysis=a, vintage=5.85 )
		v.clean_fields()

		self.assertEqual( v.vintage, 5 )


	def test_save_cleans_fields ( self ):
		a = AnalysisFactory.create()
		v = VintageFactory.build( analysis=a, vintage='asdf' )
		with self.assertRaises( ValidationError ) as ve:
			v.save()

		self.assertIn( 'vintage', ve.exception.message_dict )
		self.assertIn( ' must be an integer',
		  str(ve.exception.message_dict['vintage']) )



	def test_str_empty ( self ):
		self.assertEqual( str(Vintage()), u'(NoAnalysis) NoVintage' )


	def test_str_only_vintage ( self ):
		self.assertEqual( str(Vintage(vintage=10)), u'(NoAnalysis) 10')


	def test_str_only_analysis ( self ):
		a = AnalysisFactory.create()
		expected = u'({}) NoVintage'.format(a)
		self.assertEqual( str(Vintage(analysis=a)), expected )



class ModelCommodityTest ( TestCase ):

	def test_uniqueness_creation ( self ):
		CommodityFactory.create()
		with self.assertRaises( IntegrityError ) as ie:
			CommodityFactory.create()


	def test_uniqueness_update ( self ):
		a = CommodityFactory.create()
		b = CommodityFactory.create( name=u'OtherCommodity' )

		b.name = a.name
		with self.assertRaises( IntegrityError ) as ie:
			b.save()


	def test_str_empty ( self ):
		t = Commodity()
		expected = u'\r\nNoNameGiven\0\n'
		self.assertEqual( str(t), expected )


	def test_str_name ( self ):
		t = CommodityFactory.build()
		expected = u'{}'.format( t.name )
		self.assertEqual( str(t), expected )



class ModelParam_SegFracTest ( TestCase ):

	def test_uniqueness ( self ):
		a = Param_SegFracFactory.create()
		with self.assertRaises( IntegrityError ) as ie:
			Param_SegFracFactory.create( analysis=a.analysis )


	def test_clean_bad_season ( self ):
		sf = Param_SegFracFactory.build()
		name_re = re.compile( r'^[A-z_]\w*$' )
		sf.clean_season() # ensure it is valid to begin with

		# Fuzz test
		for i in range(10):
			length = randint(1, 1025)
			while name_re.match( sf.season ):
				sf.season = urandom( length )
			with self.assertRaises( ValidationError ):
				sf.clean_season()


	def test_clean_bad_timeofday ( self ):
		sf = Param_SegFracFactory.build()
		name_re = re.compile( r'^[A-z_]\w*$' )
		sf.clean_time_of_day() # ensure it is valid to begin with

		length = randint(1, 1025)
		while name_re.match( sf.time_of_day ):
			sf.time_of_day = urandom( length )

		with self.assertRaises( ValidationError ):
			sf.clean_time_of_day()


	def test_clean_value_requires_value ( self ):
		sf = Param_SegFracFactory.build()
		sf.value = None
		with self.assertRaises( ValidationError ):
			sf.clean_value()


	def test_clean_value_requires_valid_number ( self ):
		sf = Param_SegFracFactory.build()
		while True:
			length = randint(1, 20)
			sf.value = urandom( length )
			try:
				# ensure value is invalid
				float( sf.value )
			except:
				break

		with self.assertRaises( ValidationError ):
			sf.clean_value()


	def test_clean_value_requires_between_0_and_1 ( self ):
		sf = Param_SegFracFactory.build()

		sf.value = 0.5
		while 0 < sf.value <= 1:
			sf.value = random() * randint(-1e9, 1e9)

		with self.assertRaises( ValidationError ):
			sf.clean_value()


	def test_clean_demandefaultdistribution_can_be_null ( self ):
		sf = Param_SegFracFactory.build()
		sf.demanddefaultdistribution = None
		try:
			sf.clean_demanddefaultdistribution()
		except:
			self.fail( 'DemandDefaultDistribution should be allowed to be null.' )


	def test_clean_demandefaultdistribution_does_not_accept_invalid_number ( self ):
		sf = Param_SegFracFactory.build()
		while True:
			length = randint(1, 20)
			sf.demanddefaultdistribution = urandom( length )
			try:
				# ensure value is invalid
				float( sf.demanddefaultdistribution )
			except:
				break

		with self.assertRaises( ValidationError ):
			sf.clean_demanddefaultdistribution()


	def test_clean_demandefaultdistribution_requires_between_0_and_1 ( self ):
		sf = Param_SegFracFactory.build()

		sf.demanddefaultdistribution = 0.5
		while 0 < sf.demanddefaultdistribution <= 1:
			sf.demanddefaultdistribution = random() * randint(-1e9, 1e9)

		with self.assertRaises( ValidationError ):
			sf.clean_demanddefaultdistribution()


	def test_str_empty ( self ):
		sf = Param_SegFrac()
		expected = u'(NoAnalysis) NoSeason, NoTimeOfDay: NoValue'
		self.assertEqual( str(sf), expected )


	def test_str_only_analysis ( self ):
		sf = Param_SegFracFactory.create()
		sf.season = sf.time_of_day = sf.value = None
		expected = u'({}) NoSeason, NoTimeOfDay: NoValue'.format( sf.analysis )
		self.assertEqual( str(sf), expected )


	def test_str_only_season ( self ):
		sf = Param_SegFracFactory.build()
		sf.time_of_day = sf.value = None
		expected = u'(NoAnalysis) {}, NoTimeOfDay: NoValue'.format( sf.season )
		self.assertEqual( str(sf), expected )


	def test_str_only_time_of_day ( self ):
		sf = Param_SegFracFactory.build()
		sf.season = sf.value = None
		expected = u'(NoAnalysis) NoSeason, {}: NoValue'.format( sf.time_of_day )
		self.assertEqual( str(sf), expected )


	def test_str_only_value ( self ):
		sf = Param_SegFracFactory.build()
		sf.season = sf.time_of_day = None
		expected = u'(NoAnalysis) NoSeason, NoTimeOfDay: {}'.format( sf.value )
		self.assertEqual( str(sf), expected )


	def test_str ( self ):
		sf = Param_SegFracFactory.create()
		expected = u'({}) {}, {}: {}'.format(
		  sf.analysis, sf.season, sf.time_of_day, sf.value )
		self.assertEqual( str(sf), expected )



class ModelExistingProcessTest ( TestCase ):

	def test_str_empty ( self ):
		p = Process()
		expected = u'(NoAnalysis) NoTechnology, NoVintage'
		self.assertEqual( str(p), expected )


	def test_str_only_technology ( self ):
		t = TechnologyFactory.create()
		p = ExistingProcessFactory.build( technology=t )
		expected = u'{}, NoVintage'.format( p.technology )
		self.assertEqual( str(p), expected )


	def test_str_only_vintage ( self ):
		v = VintageFactory.create()
		p = ExistingProcessFactory.build( vintage=v )
		expected = u'(NoAnalysis) NoTechnology, {}'.format( p.vintage.vintage )
		self.assertEqual( str(p), expected )


	def test_ensure_vintage ( self ):
		t = TechnologyFactory.create()
		p = Process( technology=t )

		with self.assertRaises( ValidationError ) as ve:
			p.clean_valid_vintage()

		self.assertIn( u'Process must have a vintage.', str(ve.exception) )

	def test_ensure_vintage_in_analysis ( self ):
		a1 = AnalysisFactory.create(name='A Different Unit Test Analysis' )
		a2 = AnalysisFactory.create(user=a1.user)
		t1 = TechnologyFactory.create(analysis=a1)

		# intentional misuse of a2 and a1
		v = VintageFactory( analysis=a2, vintage=a1.period_0 -10 )
		p = Process( technology=t1, vintage=v )
		with self.assertRaises( ValidationError ) as ve:
			p.clean_valid_vintage()

		self.assertIn( u'Vintage does not exist in this analysis.',
		  str(ve.exception) )


	def test_ensure_vintage_is_not_final_year ( self ):
		t = TechnologyFactory.create()
		a = t.analysis

		# the first and only vintage in analysis
		v = VintageFactory.create( analysis=a )

		p = Process(technology=t, vintage=v)
		with self.assertRaises( ValidationError ) as ve:
			p.clean_valid_vintage()

		self.assertIn( u'The final year in ', str(ve.exception) )


	def test_ensure_none_or_positive_lifetime ( self ):
		p = Process()
		try:
			p.clean_valid_lifetime()
		except:
			self.fail('Unspecified process lifetime should be valid.')
			raise  # so as not to hide the actual exception

		p.lifetime = 0
		with self.assertRaises( ValidationError ) as ve:
			p.clean_valid_lifetime()
		self.assertIn( u' positive integer or ', str(ve.exception) )

		p.lifetime = -10
		with self.assertRaises( ValidationError ) as ve:
			p.clean_valid_lifetime()
		self.assertIn( u' positive integer or ', str(ve.exception) )


	def test_ensure_valid_existingcapacity ( self ):
		p = Process()
		try:
			p.clean_valid_existingcapacity()
		except:
			self.fail('Unspecified process existingcapacity should be valid.')
			raise  # so as not to hide the actual exception

		p.existingcapacity = 0
		with self.assertRaises( ValidationError ) as ve:
			p.clean_valid_existingcapacity()
		self.assertIn( u' positive integer or ', str(ve.exception) )

		p.existingcapacity = -10
		with self.assertRaises( ValidationError ) as ve:
			p.clean_valid_existingcapacity()
		self.assertIn( u' positive integer or ', str(ve.exception) )



class ModelCommodityTypeTest ( TestCase ):

	def test_empty_name_not_valid ( self ):
		with self.assertRaises( ValidationError ) as ve:
			CommodityType().clean()
		self.assertIn( 'No name specified ', str(ve.exception) )


	def test_cleaned_name_removes_whitespace_chars ( self ):
		ct = CommodityType( name=u'\nAw\res\tom\ve\0 Name\0\n\t\v\r' )
		ct.clean()
		self.assertEqual( ct.name, u'Awesome Name' )


	def test_uniqueness ( self ):
		CommodityType(name='Unit Test CommodityType').save()
		with self.assertRaises( IntegrityError ) as ie:
			CommodityType(name='Unit Test CommodityType').save()



class ModelParam_TechInputSplitTest ( TestCase ):

	def test_str_empty ( self ):
		tis = Param_TechInputSplit()
		expected = u'(NoAnalysis) NoInput, NoTechnology: NoValue'
		self.assertEqual( str(tis), expected )


	def test_str_only_technology ( self ):
		t = TechnologyFactory.create()
		tis = Param_TechInputSplit( technology=t )
		expected = u'({}) NoInput, {}: NoValue'.format( t.analysis, t.name )
		self.assertEqual( str(tis), expected )


	def test_str_only_inpcommodity ( self ):
		a = AnalysisFactory.create()
		ct = CommodityType.objects.get_or_create(name='physical')[0]
		c = CommodityFactory.create()
		ac = AnalysisCommodity.objects.create(
		  analysis=a, commodity_type=ct, commodity=c )
		tis = Param_TechInputSplit( inp_commodity=ac )
		expected = u'(NoAnalysis) {}, NoTechnology: NoValue'.format( c )
		self.assertEqual( str(tis), expected )


	def test_str_only_fraction ( self ):
		fraction = random()
		tis = Param_TechInputSplit( fraction=fraction )
		expected = u'(NoAnalysis) NoInput, NoTechnology: {}'.format( fraction )
		self.assertEqual( str(tis), expected )


	def test_uniqueness ( self ):
		t = TechnologyFactory.create()
		a = t.analysis
		ct = CommodityType.objects.get_or_create(name='physical')[0]
		c = CommodityFactory.create()
		ac = AnalysisCommodity.objects.create(
		  analysis=a, commodity_type=ct, commodity=c )

		Param_TechInputSplit.objects.create(
		  inp_commodity=ac, technology=t, fraction=random() )

		with self.assertRaises( IntegrityError ) as ie:
			Param_TechInputSplit.objects.create(
			  inp_commodity=ac, technology=t, fraction=random() )


	def test_commodity_is_an_input ( self ):
		t = TechnologyFactory.create()
		a = t.analysis
		ct = CommodityType.objects.get_or_create(name='physical')[0]
		c = CommodityFactory.create()
		ac = AnalysisCommodity.objects.create(
		  analysis=a, commodity_type=ct, commodity=c )

		Param_TechInputSplit(
		  inp_commodity=ac, technology=t, fraction=random() ).clean()
		ac.delete()

		ct = CommodityType.objects.get_or_create(name='demand')[0]
		ac = AnalysisCommodity.objects.create(
		  analysis=a, commodity_type=ct, commodity=c )
		with self.assertRaises( ValidationError ):
			Param_TechInputSplit(
			  inp_commodity=ac, technology=t, fraction=random() ).clean()
		ac.delete()

		ct = CommodityType.objects.get_or_create(name='emission')[0]
		ac = AnalysisCommodity.objects.create(
		  analysis=a, commodity_type=ct, commodity=c )
		with self.assertRaises( ValidationError ):
			Param_TechInputSplit(
			  inp_commodity=ac, technology=t, fraction=random() ).clean()


	def test_fraction_is_between_0_and_1 ( self ):
		t = TechnologyFactory.create()
		a = t.analysis
		ct = CommodityType.objects.get_or_create(name='physical')[0]
		c = CommodityFactory.create()
		ac = AnalysisCommodity.objects.create(
		  analysis=a, commodity_type=ct, commodity=c )

		Param_TechInputSplit(
		  inp_commodity=ac, technology=t, fraction=random() ).clean()

		with self.assertRaises( ValidationError ):
			Param_TechInputSplit(
			  inp_commodity=ac, technology=t, fraction=random() -2 ).clean()

		with self.assertRaises( ValidationError ):
			Param_TechInputSplit(
			  inp_commodity=ac, technology=t, fraction=random() +2 ).clean()



class ModelParam_TechOutputSplitTest ( TestCase ):

	def test_str_empty ( self ):
		tos = Param_TechOutputSplit()
		expected = u'(NoAnalysis) NoTechnology, NoOutput: NoValue'
		self.assertEqual( str(tos), expected )


	def test_str_only_technology ( self ):
		t = TechnologyFactory.create()
		tos = Param_TechOutputSplit( technology=t )
		expected = u'{}, NoOutput: NoValue'.format( t )
		self.assertEqual( str(tos), expected )


	def test_str_only_outcommodity ( self ):
		a = AnalysisFactory.create()
		ct = CommodityType.objects.get_or_create(name='demand')[0]
		c = CommodityFactory.create()
		dc = AnalysisCommodity.objects.create(
		  analysis=a, commodity_type=ct, commodity=c )
		tos = Param_TechOutputSplit( out_commodity=dc )
		expected = u'(NoAnalysis) NoTechnology, {}: NoValue'.format( c )
		self.assertEqual( str(tos), expected )


	def test_str_only_fraction ( self ):
		fraction = random()
		tos = Param_TechOutputSplit( fraction=fraction )
		expected = u'(NoAnalysis) NoTechnology, NoOutput: {}'.format( fraction )
		self.assertEqual( str(tos), expected )


	def test_uniqueness ( self ):
		t = TechnologyFactory.create()
		a = t.analysis
		ct = CommodityType.objects.get_or_create(name='demand')[0]
		c = CommodityFactory.create()
		dc = AnalysisCommodity.objects.create(
		  analysis=a, commodity_type=ct, commodity=c )

		Param_TechOutputSplit.objects.create(
		  technology=t, out_commodity=dc, fraction=random() )

		with self.assertRaises( IntegrityError ) as ie:
			Param_TechOutputSplit.objects.create(
			  technology=t, out_commodity=dc, fraction=random() )


	def test_commodity_is_an_output ( self ):
		t = TechnologyFactory.create()
		a = t.analysis
		ct = CommodityType.objects.get_or_create(name='demand')[0]
		c = CommodityFactory.create()
		ac = AnalysisCommodity.objects.create(
		  analysis=a, commodity_type=ct, commodity=c )

		Param_TechOutputSplit(
		  technology=t, out_commodity=ac, fraction=random() ).clean()
		ac.delete()

		ct = CommodityType.objects.get_or_create(name='physical')[0]
		ac = AnalysisCommodity.objects.create(
		  analysis=a, commodity_type=ct, commodity=c )
		Param_TechOutputSplit(
		  technology=t, out_commodity=ac, fraction=random() ).clean()
		ac.delete()

		ct = CommodityType.objects.get_or_create(name='emission')[0]
		ac = AnalysisCommodity.objects.create(
		  analysis=a, commodity_type=ct, commodity=c )
		with self.assertRaises( ValidationError ):
			Param_TechOutputSplit(
			  technology=t, out_commodity=ac, fraction=random() ).clean()


	def test_fraction_is_between_0_and_1 ( self ):
		t = TechnologyFactory.create()
		a = t.analysis
		ct = CommodityType.objects.get_or_create(name='demand')[0]
		c = CommodityFactory.create()
		ac = AnalysisCommodity.objects.create(
		  analysis=a, commodity_type=ct, commodity=c )

		Param_TechOutputSplit(
		  technology=t, out_commodity=ac, fraction=random() ).clean()

		with self.assertRaises( ValidationError ):
			Param_TechOutputSplit(
			  technology=t, out_commodity=ac, fraction=random() -2 ).clean()

		with self.assertRaises( ValidationError ):
			Param_TechOutputSplit(
			  technology=t, out_commodity=ac, fraction=random() +2 ).clean()



class ModelParam_MaxMinCapacityTest ( TestCase ):

	def test_period_must_be_in_horizon ( self ):
		mmc = Param_MaxMinCapacityFactory.build()

		mmc.period.vintage = 10
		mmc.period.analysis.period_0 = 10000

		with self.assertRaises( ValidationError ):
			mmc.clean_period_and_technology()


	def test_period_technology_analysis_must_be_equal ( self ):
		mmc = Param_MaxMinCapacityFactory.build()
		mmc.technology.analysis = Analysis()

		with self.assertRaises( ValidationError ):
			mmc.clean_period_and_technology()


	def test_minimum_capacity_can_be_null ( self ):
		mmc = Param_MaxMinCapacityFactory.build()

		mmc.minimum = None
		try:
			mmc.clean_minimum()
		except:
			self.fail('Specification of minimum capacity should not be required.')


	def test_maximum_capacity_can_be_null ( self ):
		mmc = Param_MaxMinCapacityFactory.build()

		mmc.maximum = None
		try:
			mmc.clean_maximum()
		except:
			self.fail('Specification of maximum capacity should not be required.')


	def test_maximum_capacity_zero_is_allowed ( self ):
		mmc = Param_MaxMinCapacityFactory.build()

		for val in (0, False):
			mmc.maximum = val
			mmc.clean_maximum()
			self.assertEqual( mmc.maximum, 0 )


	def test_maximum_capacity_can_be_null ( self ):
		mmc = Param_MaxMinCapacityFactory.build()
		mmc.maximum = None
		mmc.clean_maximum()
		self.assertEqual( mmc.maximum, None )


	def test_minimum_capacity_requires_valid_number ( self ):
		mmc = Param_MaxMinCapacityFactory.build()

		mmc.minimum = 'asdf'
		with self.assertRaises( ValidationError ):
			mmc.clean_minimum()


	def test_maximum_capacity_requires_valid_number ( self ):
		mmc = Param_MaxMinCapacityFactory.build()

		mmc.maximum = 'asdf'
		with self.assertRaises( ValidationError ):
			mmc.clean_maximum()


	def test_minimum_capacity_cannot_be_negative ( self ):
		mmc = Param_MaxMinCapacityFactory.build()

		mmc.minimum = random() * randint(-1e9, -1)
		with self.assertRaises( ValidationError ):
			mmc.clean_minimum()


	def test_maximum_capacity_cannot_be_negative ( self ):
		mmc = Param_MaxMinCapacityFactory.build()

		mmc.maximum = random() * randint(-1e9, -1)
		with self.assertRaises( ValidationError ):
			mmc.clean_maximum()


	def test_minimum_must_not_be_almost_zero ( self ):
		""" This will probably never occur, but the threshold is 1e-9.  Numbers
		smaller than that snuck past the 'not 0' test, but are close enough to be
		practically 0.  Thus, inform user of the error. """
		mmc = Param_MaxMinCapacityFactory.build()

		mmc.minimum = 1e-10
		with self.assertRaises( ValidationError ):
			mmc.clean_minimum()


	def test_maximum_can_be_zero ( self ):
		mmc = Param_MaxMinCapacityFactory.build()

		mmc.maximum = 0
		try:
			mmc.clean_maximum()
		except:
			self.fail('Maximum capacity should be allowed to be 0.')
			raise


	def test_minimum_can_be_positive ( self ):
		mmc = Param_MaxMinCapacityFactory.build()

		mmc.minimum = random() * randint(1, 1e9)
		try:
			mmc.clean_minimum()
		except:
			self.fail('A positive minimum capacity should be valid.')
			raise


	def test_maximum_can_be_positive ( self ):
		mmc = Param_MaxMinCapacityFactory.build()

		mmc.maximum = random() * randint(1, 1e9)
		try:
			mmc.clean_maximum()
		except:
			self.fail('A positive maximum capacity should be valid.')
			raise


	def test_maximum_minimum_capacity_cannot_both_be_null ( self ):
		mmc = Param_MaxMinCapacityFactory.build()

		mmc.maximum = mmc.minimum = None
		with self.assertRaises( ValidationError ):
			mmc.clean_max_and_min()

