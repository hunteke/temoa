import factory

from django.contrib.auth.models import User as DjangoUser
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
from django.db.utils import IntegrityError
from django.test import TestCase

from process_interface.models import (
  Analysis,
  Technology,
  Vintage,
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


	def test_analysis_delete ( self ):
		a = AnalysisFactory.create()
		pk = a.pk
		a.delete()
		self.assertIsNone( a.pk )

		with self.assertRaises( ObjectDoesNotExist ):
			Analysis.objects.get( pk=pk )


	def test_analysis_period_0_is_integer ( self ):
		a = AnalysisFactory.build( period_0=5.85 )
		a.clean()

		self.assertEqual( a.period_0, 5 )


	def test_analysis_uniqueness ( self ):
		with self.assertRaises( IntegrityError ):
			AnalysisFactory.create()
			AnalysisFactory.create()


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
		with self.assertRaisesRegexp( ValidationError, r'\bname\b' ):
			t.clean()


	def test_no_description_raises_validation_error ( self ):
		t = TechnologyFactory.build()
		t.description = None
		with self.assertRaisesRegexp( ValidationError, r'\bdescription\b' ):
			t.clean()


	def test_unicode_empty ( self ):
		t = Technology()
		expected = u'NoName'
		self.assertEqual( unicode(t), expected )


	def test_unicode_name ( self ):
		t = Technology(name='Unit Test of Technology')
		expected = u'{}'.format( t.name )
		self.assertEqual( unicode(t), expected )



class ModelVintageTest ( TestCase ):

	def test_uniqueness_creation ( self ):
		with self.assertRaises( IntegrityError ):
			VintageFactory.create()
			VintageFactory.create()


	def test_uniqueness_update ( self ):
		a = VintageFactory.create()
		b = VintageFactory.create( vintage=a.vintage+10, analysis=a.analysis )

		with self.assertRaises( IntegrityError ):
			b.vintage = a.vintage
			b.save()


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


