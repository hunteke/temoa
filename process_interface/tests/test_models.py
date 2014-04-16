from django.db import transaction
from django.db.utils import IntegrityError
from django.test import TestCase

from process_interface.models import Analysis, Vintage

class ModelAnalysisTest ( TestCase ):

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


	def test_create_update_delete_analysis ( self ):
		"""
		Tests that analyses can be created.
		"""

		a = Analysis.objects.create(
		  user        = self.user,
		  name        = 'Some Analysis Name',
		  description = 'Some analysis description',
		  period_0    = 1,
		  global_discount_rate = 0.01,
		)

		self.assertIsNotNone( a )
		self.assertEqual( a.name, u'Some Analysis Name' )
		self.assertIs( a.user, self.user )
		self.assertEqual( a.description, u'Some analysis description' )
		self.assertEqual( a.period_0, 1 )
		self.assertEqual( a.global_discount_rate, 0.01 )
		self.assertEqual( unicode(a), u'test_user - Some Analysis Name')

		b = Analysis.objects.get( user=self.user )
		self.assertEqual( a, b )

		b.name = 'New Analysis Name'
		b.save()

		# Poor man's way to refresh object, due to Django ticket 901:
		#    http://code.djangoproject.com/ticket/901
		#
		# See also: http://stackoverflow.com/questions/4377861/reload-django-object-from-database
		a = Analysis.objects.get( pk=a.pk )
		self.assertEqual( str(a.name), 'New Analysis Name' )

		self.assertEqual( b, a )

		a.delete()
		self.assertIsNone( a.pk )

		b.delete()  # redundant to a.
		self.assertIsNone( b.pk )
		self.assertEqual( a, b )


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


