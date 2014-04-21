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
  Commodity,
  Param_SegFrac,
  Param_LifetimeTech,
  Process,
  Technology,
  Vintage,
  Set_tech_baseload,
)



class UserFactory ( factory.django.DjangoModelFactory ):
	FACTORY_FOR = DjangoUser

	is_active = True
	is_staff = False
	is_superuser = False
	first_name = 'Jiminy'
	last_name = 'Cricket'
	username = 'jimbob'
	email = 'mrjim@example.net'



class AnalysisFactory ( factory.django.DjangoModelFactory ):
	FACTORY_FOR = Analysis

	user = factory.SubFactory( UserFactory )
	name = 'Unit Test Analysis'
	description = 'Analysis automatically created during unit testing.'
	period_0 = 0
	global_discount_rate = 0.05



class VintageFactory ( factory.django.DjangoModelFactory ):
	FACTORY_FOR = Vintage

	analysis = factory.SubFactory( AnalysisFactory )
	vintage  = 0



class TechnologyFactory ( factory.django.DjangoModelFactory ):
	FACTORY_FOR = Technology

	user = factory.SubFactory( UserFactory )
	name = 'Unit Test Technology'
	description = 'Technology automatically created during unit testing.'
	capacity_to_activity = None



class CommodityFactory ( factory.django.DjangoModelFactory ):
	FACTORY_FOR = Commodity

	name = 'Unit Test Commodity'
	description = 'Commodity automatically created during unit testing.'



class Param_SegFracFactory ( factory.django.DjangoModelFactory ):
	FACTORY_FOR = Param_SegFrac

	analysis = factory.SubFactory( AnalysisFactory )
	season = 'Unit_Test_Season'
	time_of_day = 'Unit_Test_Day'
	value = 1



class Set_tech_baseloadFactory ( factory.django.DjangoModelFactory ):
	FACTORY_FOR = Set_tech_baseload

	analysis = factory.SubFactory( AnalysisFactory )
	technology = factory.SubFactory( TechnologyFactory )



class ExistingProcessFactory ( factory.django.DjangoModelFactory ):
	FACTORY_FOR = Process

	analysis         = factory.SubFactory( AnalysisFactory )
	technology       = factory.SubFactory( TechnologyFactory )
	vintage          = factory.SubFactory( VintageFactory )
	lifetime         = 10
	loanlife         = None
	costinvest       = None
	discountrate     = None
	existingcapacity = 31



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
		a = AnalysisFactory.build( period_0=5.85 )
		a.clean()

		self.assertEqual( a.period_0, 5 )


	def test_analysis_uniqueness ( self ):
		with self.assertRaises( IntegrityError ) as ie:
			a = AnalysisFactory.create()
			b = AnalysisFactory.create(user=a.user)

		self.assertIn( u'user_id, name are not unique', unicode(ie.exception) )



	def test_analysis_unicode_empty ( self ):
		a = Analysis()
		self.assertEqual( unicode(a), 'NoUser - NoName')


	def test_analysis_unicode_only_user ( self ):
		a = Analysis( user=UserFactory.create() )
		expected = u'{} - NoName'.format( a.user.username )
		self.assertEqual( unicode(a), expected )


	def test_analysis_unicode_only_name ( self ):
		a = Analysis( name='Unit Test Analysis' )
		expected = u'NoUser - {}'.format( a.name )
		self.assertEqual( unicode(a), expected )



class ModelTechnologyTest ( TestCase ):

	def test_name_with_bad_characters ( self ):
		t = TechnologyFactory.build()
		t.name = u'Name with \r\n\0\t\v bad characters'
		t.clean()
		self.assertNotIn( '\r', t.name )
		self.assertNotIn( '\n', t.name )
		self.assertNotIn( '\0', t.name )
		self.assertNotIn( '\t', t.name )
		self.assertNotIn( '\v', t.name )


	def test_no_name_raises_validation_error ( self ):
		t = TechnologyFactory.build()
		t.name = ''
		with self.assertRaises( ValidationError ) as ve:
			t.clean()

		self.assertIn( u'must have a name', unicode(ve.exception) )


	def test_no_description_raises_validation_error ( self ):
		t = TechnologyFactory.build()
		t.description = None
		with self.assertRaises( ValidationError ) as ve:
			t.clean()

		self.assertIn( u'must have a description', unicode(ve.exception) )


	def test_unicode_empty ( self ):
		t = Technology()
		expected = u'NoName'
		self.assertEqual( unicode(t), expected )


	def test_unicode_name ( self ):
		t = TechnologyFactory.build()
		expected = u'{}'.format( t.name )
		self.assertEqual( unicode(t), expected )



class ModelVintageTest ( TestCase ):

	def test_uniqueness_creation ( self ):
		with self.assertRaises( IntegrityError ) as ie:
			a = VintageFactory.create()
			b = VintageFactory.create(analysis=a.analysis)

		self.assertIn( u'analysis_id, vintage are not unique',
		  unicode(ie.exception) )


	def test_uniqueness_update ( self ):
		a = VintageFactory.create()
		b = VintageFactory.create( vintage=a.vintage+10, analysis=a.analysis )

		with self.assertRaises( IntegrityError ) as ie:
			b.vintage = a.vintage
			b.save()

		self.assertIn( u'analysis_id, vintage are not unique',
		  unicode(ie.exception) )


	def test_vintage_is_integer ( self ):
		a = VintageFactory.build( vintage=5.85 )
		a.clean()

		self.assertEqual( a.vintage, 5 )


	def test_unicode_empty ( self ):
		self.assertEqual( unicode(Vintage()), u'(NoAnalysis) NoVintage' )


	def test_unicode_only_vintage ( self ):
		self.assertEqual( unicode(Vintage(vintage=10)), u'(NoAnalysis) 10')


	def test_unicode_only_analysis ( self ):
		a = AnalysisFactory.create()
		expected = u'({}) NoVintage'.format(a)
		self.assertEqual( unicode(Vintage(analysis=a)), expected)



class ModelCommodityTest ( TestCase ):

	def test_uniqueness_creation ( self ):
		with self.assertRaises( IntegrityError ) as ie:
			CommodityFactory.create()
			CommodityFactory.create()

		self.assertIn( u'name is not unique', unicode(ie.exception) )


	def test_uniqueness_update ( self ):
		a = CommodityFactory.create()
		b = CommodityFactory.create( name=u'OtherCommodity' )

		with self.assertRaises( IntegrityError ) as ie:
			b.name = a.name
			b.save()

		self.assertIn( u'name is not unique', unicode(ie.exception) )


	def test_unicode_empty ( self ):
		t = Commodity()
		expected = u'NoName'
		self.assertEqual( unicode(t), expected )


	def test_unicode_name ( self ):
		t = CommodityFactory.build()
		expected = u'{}'.format( t.name )
		self.assertEqual( unicode(t), expected )



class ModelParam_SegFracTest ( TestCase ):

	def test_uniqueness ( self ):
		with self.assertRaises( IntegrityError ) as ie:
			a = Param_SegFracFactory.create()
			b = Param_SegFracFactory.create( analysis=a.analysis )

		self.assertIn( u'season, time_of_day are not unique',
		  unicode(ie.exception) )


	def test_clean_bad_season ( self ):
		sf = Param_SegFracFactory.build()
		name_re = re.compile( r'^[A-z_]\w*$' )
		sf.clean() # ensure it is valid to begin with

		# Fuzz test
		for i in range(10):
			length = randint(1, 1025)
			while name_re.match( sf.season ):
				sf.season = urandom( length )
			with self.assertRaises( ValidationError ):
				sf.clean()


	def test_clean_bad_timeofday ( self ):
		sf = Param_SegFracFactory.build()
		name_re = re.compile( r'^[A-z_]\w*$' )
		sf.clean() # ensure it is valid to begin with

		# Fuzz test
		for i in range(10):
			length = randint(1, 1025)
			while name_re.match( sf.time_of_day ):
				sf.time_of_day = urandom( length )
			with self.assertRaises( ValidationError ):
				sf.clean()


	def test_clean_value ( self ):
		sf = Param_SegFracFactory.build()
		sf.clean() # ensure it is valid to begin with

		# Fuzz test
		for i in range(10):
			multiplier = randint(-1e9, 1e9)
			value = 0.5
			while 0 < value <= 1:
				value = random() * multiplier
			sf.value = value
			with self.assertRaises( ValidationError ):
				sf.clean()


	def test_unicode_empty ( self ):
		sf = Param_SegFrac()
		expected = u'(NoAnalysis) NoSeason, NoTimeOfDay: NoValue'
		self.assertEqual( unicode(sf), expected )


	def test_unicode_only_analysis ( self ):
		sf = Param_SegFracFactory.create()
		sf.season = sf.time_of_day = sf.value = None
		expected = u'({}) NoSeason, NoTimeOfDay: NoValue'.format( sf.analysis )
		self.assertEqual( unicode(sf), expected )


	def test_unicode_only_season ( self ):
		sf = Param_SegFracFactory.build()
		sf.time_of_day = sf.value = None
		expected = u'(NoAnalysis) {}, NoTimeOfDay: NoValue'.format( sf.season )
		self.assertEqual( unicode(sf), expected )


	def test_unicode_only_time_of_day ( self ):
		sf = Param_SegFracFactory.build()
		sf.season = sf.value = None
		expected = u'(NoAnalysis) NoSeason, {}: NoValue'.format( sf.time_of_day )
		self.assertEqual( unicode(sf), expected )


	def test_unicode_only_value ( self ):
		sf = Param_SegFracFactory.build()
		sf.season = sf.time_of_day = None
		expected = u'(NoAnalysis) NoSeason, NoTimeOfDay: {}'.format( sf.value )
		self.assertEqual( unicode(sf), expected )


	def test_unicode ( self ):
		sf = Param_SegFracFactory.create()
		expected = u'({}) {}, {}: {}'.format(
		  sf.analysis, sf.season, sf.time_of_day, sf.value )
		self.assertEqual( unicode(sf), expected )



class ModelsTechnologySetMemberTest ( TestCase ):

	def test_tech_baseload_uniqueness_creation ( self ):
		a = AnalysisFactory.create()
		t = TechnologyFactory.create(user=a.user)
		with self.assertRaises( IntegrityError ) as ie:
			Set_tech_baseloadFactory.create( analysis=a, technology=t )
			Set_tech_baseloadFactory.create( analysis=a, technology=t )

		self.assertIn( u' analysis_id, technology_id are not unique',
		  unicode(ie.exception) )


	def test_tech_baseload_unicode_empty ( self ):
		bl = Set_tech_baseload()
		expected = u'(NoAnalysis) NoTechnology'
		self.assertEqual( unicode(bl), expected )


	def test_tech_baseload_only_analysis ( self ):
		a = AnalysisFactory.create()
		bl = Set_tech_baseloadFactory.build( analysis=a )
		expected = u'({}) NoTechnology'.format( bl.analysis )
		self.assertEqual( unicode(bl), expected )


	def test_tech_baseload_only_technology ( self ):
		t = TechnologyFactory.create()
		bl = Set_tech_baseloadFactory.build( technology=t )
		expected = u'(NoAnalysis) {}'.format( bl.technology )
		self.assertEqual( unicode(bl), expected )



class ModelExistingProcessTest ( TestCase ):

	def test_unicode_empty ( self ):
		p = Process()
		expected = u'(NoAnalysis) NoTechnology, NoVintage'
		self.assertEqual( unicode(p), expected )


	def test_unicode_only_analysis ( self ):
		a = AnalysisFactory.create()
		p = ExistingProcessFactory.build( analysis=a )
		expected = u'({}) NoTechnology, NoVintage'.format( p.analysis )
		self.assertEqual( unicode(p), expected )


	def test_unicode_only_technology ( self ):
		t = TechnologyFactory.create()
		p = ExistingProcessFactory.build( technology=t )
		expected = u'(NoAnalysis) {}, NoVintage'.format( p.technology )
		self.assertEqual( unicode(p), expected )


	def test_unicode_only_vintage ( self ):
		v = VintageFactory.create()
		p = ExistingProcessFactory.build( vintage=v )
		expected = u'(NoAnalysis) NoTechnology, {}'.format( p.vintage.vintage )
		self.assertEqual( unicode(p), expected )


	def test_ensure_vintage ( self ):
		a = AnalysisFactory.create()
		p = Process(analysis=a)

		with self.assertRaises( ValidationError ) as ve:
			p.clean_valid_vintage()

		self.assertIn( u'Process must have a vintage.', unicode(ve.exception) )

	def test_ensure_vintage_in_analysis ( self ):
		a1 = AnalysisFactory.create(name='A Different Unit Test Analysis' )
		a2 = AnalysisFactory.create(user=a1.user)

		# intentional misuse of a2 and a1
		v = VintageFactory( analysis=a2, vintage=a1.period_0 -10 )
		p = Process( analysis=a1, vintage=v )
		with self.assertRaises( ValidationError ) as ve:
			p.clean_valid_vintage()

		self.assertIn( u'Vintage does not exist in this analysis.',
		  unicode(ve.exception) )


	def test_ensure_vintage_is_not_final_year ( self ):
		a = AnalysisFactory.create()

		# the first and only vintage in analysis
		v = VintageFactory.create( analysis=a )

		p = Process(analysis=a, vintage=v)
		with self.assertRaises( ValidationError ) as ve:
			p.clean_valid_vintage()

		self.assertIn( u'The final year in ', unicode(ve.exception) )


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
		self.assertIn( u' positive integer or ', unicode(ve.exception) )

		p.lifetime = -10
		with self.assertRaises( ValidationError ) as ve:
			p.clean_valid_lifetime()
		self.assertIn( u' positive integer or ', unicode(ve.exception) )


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
		self.assertIn( u' positive integer or ', unicode(ve.exception) )

		p.existingcapacity = -10
		with self.assertRaises( ValidationError ) as ve:
			p.clean_valid_existingcapacity()
		self.assertIn( u' positive integer or ', unicode(ve.exception) )



class ModelParam_LifetimeTechProcessTest ( TestCase ):

	def test_unicode_empty ( self ):
		tl = Param_LifetimeTech()
		expected = u'(NoAnalysis) NoTechnology: NoValue'
		self.assertEqual( unicode(tl), expected )


	def test_unicode_only_analysis ( self ):
		a = AnalysisFactory.create()
		tl = Param_LifetimeTech( analysis=a )
		expected = u'({}) NoTechnology: NoValue'.format( tl.analysis )
		self.assertEqual( unicode(tl), expected )


	def test_unicode_only_technology ( self ):
		t = TechnologyFactory.create()
		tl = Param_LifetimeTech( technology=t )
		expected = u'(NoAnalysis) {}: NoValue'.format( tl.technology )
		self.assertEqual( unicode(tl), expected )


	def test_unicode_only_value ( self ):
		tl = Param_LifetimeTech( value='15.2' )
		expected = u'(NoAnalysis) NoTechnology: {}'.format( tl.value )
		self.assertEqual( unicode(tl), expected )


	def test_value_is_valid_number ( self ):
		for i in range(10):
			length = randint(1, 256)
			value = urandom( length )
			try:
				value = float(value)
				continue
			except ValueError:
				pass

			with self.assertRaises( ValidationError ) as ve:
				Param_LifetimeTech( value=value ).clean()
			self.assertIn( u' be a valid float', unicode(ve.exception) )


	def test_value_is_positive_number ( self ):
		with self.assertRaises( ValidationError ) as ve:
			Param_LifetimeTech( value=0 ).clean()
		self.assertIn( u'greater than 0', unicode(ve.exception) )

		with self.assertRaises( ValidationError ) as ve:
			Param_LifetimeTech( value=-randint(1, 1e9)*random() ).clean()
		self.assertIn( u'greater than 0', unicode(ve.exception) )

		try:
			Param_LifetimeTech( value=randint(1, 1e9)*random() ).clean()
		except:
			self.fail( 'Positive lifetime values should be valid.' )

