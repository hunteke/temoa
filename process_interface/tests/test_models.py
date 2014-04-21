import factory

from django.contrib.auth.models import User as DjangoUser
from django.core.exceptions import ObjectDoesNotExist
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
		a = AnalysisFactory.create()
		a.period_0 = 5.85
		a.save()
		b = Analysis.objects.get( pk=a.pk )

		self.assertEqual( a.period_0, 5 )
		self.assertEqual( b.period_0, 5 )


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



class ModelVintageTest ( TestCase ):

	@classmethod
	def setUpClass ( cls ):
		from django.contrib.auth.models import User

		u = User( username='test_user', password='SomethingSecure',
		          email='some@email')
		u.save()
		cls.user = u


	@classmethod
	def tearDownClass ( cls ):
		cls.user.delete()


	def setUp ( self ):
		self.analysis = Analysis.objects.create(
		  user        = self.user,
		  name        = 'Some Analysis Name',
		  description = 'Some analysis description',
		  period_0    = 1,
		  global_discount_rate = 0.01,
		)


	def tearDown ( self ):
		self.analysis.delete()


	def test_create_vintages ( self ):
		a = self.analysis

		for i in xrange( 1, 11 ):
			v = Vintage.objects.create( analysis=a, vintage=i )
			self.assertEqual( unicode(v), '(test_user - Some Analysis Name) {}'.format(i) )

		self.assertEqual( Vintage.objects.filter( analysis=a ).count(), 10 )

		with self.assertRaises( IntegrityError ):
			with transaction.atomic():
				Vintage.objects.create( analysis=a, vintage=2 )

		with self.assertRaises( IntegrityError ):
			with transaction.atomic():
				v = Vintage( analysis=a, vintage=3 )
				v.save()


