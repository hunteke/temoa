from django.test import TestCase

from process_interface.models import Analysis, Vintage

class ViewAnalysisTest ( TestCase ):

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


