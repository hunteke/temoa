import factory

from django.contrib.auth.models import User as DjangoUser
from django.test import TestCase

from process_interface.forms import (
  AnalysisForm,
  LoginForm,
  VintagesForm,
  ProcessForm,
)

from process_interface.models import (
  Analysis,
  Process,
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


class NewProcessFactory ( factory.django.DjangoModelFactory ):
	FACTORY_FOR = Process

	analysis         = factory.SubFactory( AnalysisFactory )
	technology       = factory.SubFactory( TechnologyFactory )
	vintage          = factory.SubFactory( VintageFactory )
	lifetime         = 10
	loanlife         = 10
	costinvest       = 1000
	discountrate     = 0.15
	existingcapacity = None



class TestLoginForm ( TestCase ):

	def test_username_required ( self ):
		f = LoginForm({ b'password': b'asdf' })

		self.assertFalse( f.is_valid() )
		self.assertIn( 'username', f.errors )
		self.assertIn( 'is required', str(f.errors['username']) )


	def test_password_required ( self ):
		f = LoginForm({ b'username': b'asdf' })

		self.assertFalse( f.is_valid() )
		self.assertIn( 'password', f.errors )
		self.assertIn( 'is required', str(f.errors['password']) )


	def test_password_is_not_empty ( self ):
		f = LoginForm({ b'username': b'asdf', b'password': b'' })

		self.assertFalse( f.is_valid() )
		self.assertIn( 'password', f.errors )
		self.assertIn( 'is required', str(f.errors['password']) )


	def test_max_length_is_254 ( self ):
		f = LoginForm({ b'username': b'a' * 255, b'password': b'asdf' })

		self.assertFalse( f.is_valid() )
		self.assertIn( 'username', f.errors )
		self.assertIn( 'has at most 254 cha', str(f.errors['username']) )


	def test_valid_userpass ( self ):
		f = LoginForm({ b'username': b'UserName', b'password': b'UserPass' })

		self.assertTrue( f.is_valid() )


	def test_common_control_characters_invalid_in_username ( self ):
		data = { b'password': b'a' }

		for badChar in b'\0\n\r\t\v':
			data[ b'username' ] = b'a' + badChar
			f = LoginForm( data )

			self.assertFalse( f.is_valid() )
			self.assertIn( 'username', f.errors )
			self.assertIn( 'characters on the keyboard',
			  str(f.errors['username']) )


	def test_nullbyte_is_invalid_in_password ( self ):
		f = LoginForm({ b'username': b'a', b'password': b'a\0a' })

		self.assertFalse( f.is_valid() )
		self.assertIn( 'password', f.errors )
		self.assertIn( 'characters on the keyboard',
		  str(f.errors['password']) )



class TestAnalysisForm ( TestCase ):

	def test_name_is_required ( self ):
		data = {
		  b'name': b'',
		  b'description': b'Some description',
		  b'period_0': b'0',
		  b'global_discount_rate': b'0.05',
		}

		f = AnalysisForm( data )
		self.assertFalse( f.is_valid() )
		self.assertIn( 'name', f.errors )
		self.assertIn( 'required', str(f.errors['name']) )


	def test_description_is_required ( self ):
		data = {
		  b'name': b'Some Name',
		  b'description': b'',
		  b'period_0': b'0',
		  b'global_discount_rate': b'0.05',
		}

		f = AnalysisForm( data )
		self.assertFalse( f.is_valid() )
		self.assertIn( 'description', f.errors )
		self.assertIn( 'required', str(f.errors['description']) )


	def test_period_0_is_required ( self ):
		data = {
		  b'name': b'Some Name',
		  b'description': b'Some description',
		  b'period_0': b'',
		  b'global_discount_rate': b'0.05',
		}

		f = AnalysisForm( data )
		self.assertFalse( f.is_valid() )
		self.assertIn( 'period_0', f.errors )
		self.assertIn( 'required', str(f.errors['period_0']) )


	def test_gdr_is_required ( self ):
		data = {
		  b'name': b'Some Name',
		  b'description': b'Some description',
		  b'period_0': b'0',
		  b'global_discount_rate': b'',
		}

		f = AnalysisForm( data )
		self.assertFalse( f.is_valid() )
		self.assertIn( 'global_discount_rate', f.errors )
		self.assertIn( 'required', str(f.errors['global_discount_rate']) )


	def test_period_0_requires_integer ( self ):
		data = {
		  b'name': b'Some Name',
		  b'description': b'Some description',
		  b'period_0': b'0.5',
		  b'global_discount_rate': b'0.05',
		}

		f = AnalysisForm( data )
		self.assertFalse( f.is_valid() )
		self.assertIn( 'period_0', f.errors )
		self.assertIn( 'whole number', str(f.errors['period_0']) )


	def test_gdr_requires_number ( self ):
		data = {
		  b'name': b'Some Name',
		  b'description': b'Some description',
		  b'period_0': b'0',
		  b'global_discount_rate': b'df',
		}

		f = AnalysisForm( data )
		self.assertFalse( f.is_valid() )
		self.assertIn( 'global_discount_rate', f.errors )
		self.assertIn( 'Enter a number', str(f.errors['global_discount_rate']) )


	def test_name_removes_control_characters ( self ):
		data = {
		  b'name': b'Some \r\n\0\t\vName',
		  b'description': b'Some description',
		  b'period_0': b'0',
		  b'global_discount_rate': b'0.05',
		}

		f = AnalysisForm( data )
		self.assertTrue( f.is_valid() )
		self.assertEqual( f.cleaned_data['name'], b'Some Name' )


	def test_description_removes_control_characters ( self ):
		data = {
		  b'name': b'Some Name',
		  b'description': b'Some \r\n\0\t\vdescription',
		  b'period_0': b'0',
		  b'global_discount_rate': b'0.05',
		}

		f = AnalysisForm( data )
		self.assertTrue( f.is_valid() )
		self.assertEqual( f.cleaned_data['description'], b'Some \n\t\vdescription' )



class TestVintagesForm ( TestCase ):

	def setUp ( self ):
		self.analysis = AnalysisFactory.create()


	def tearDown ( self ):
		del self.analysis


	def test_vintages_required ( self ):
		f = VintagesForm( {}, analysis=self.analysis )

		self.assertFalse( f.is_valid() )
		self.assertIn( 'vintages', f.errors )
		self.assertIn( 'required', str(f.errors['vintages']) )


	def test_no_vintages_raises_error ( self ):
		f = VintagesForm( {'vintages': ','}, analysis=self.analysis )

		self.assertFalse( f.is_valid() )
		self.assertIn( 'vintages', f.errors )
		self.assertIn( 'no vintages', str(f.errors['vintages']) )


	def test_invalid_integer_vintage ( self ):
		f = VintagesForm( {'vintages': 'adf'}, analysis=self.analysis )

		self.assertFalse( f.is_valid() )
		self.assertIn( 'vintages', f.errors )
		self.assertIn( 'Unable to convert ', str(f.errors['vintages']) )


	def test_no_period0_raises ( self ):
		f = VintagesForm( {'vintages': '1,2,3'}, analysis=self.analysis )

		self.assertFalse( f.is_valid() )
		self.assertIn( 'vintages', f.errors )
		self.assertIn( 'not contain Period 0', str(f.errors['vintages']) )



class TestNewProcessForm ( TestCase ):

	def test_no_fields_are_there ( self ):
		p = NewProcessFactory.build()
		f = ProcessForm( instance=p )

		self.assertFalse( f.is_valid() )
		self.assertEqual( len(f.fields), 0 )


	def test_only_change_passed_field ( self ):
		"""
		Motivated by GitHub Issue #34 "submitting a single field change to a
		process clears other fields"
		"""
		a = AnalysisFactory.create()
		t = TechnologyFactory.create( user=a.user )
		v = VintageFactory.create( analysis=a, vintage=10 )
		v = VintageFactory.create( analysis=a, vintage=0 )
		p = NewProcessFactory.create(analysis=a, technology=t, vintage=v)

		for attr, val in (
		  ('costinvest', '2000'), ('discountrate', '0.05'), ('lifetime', '20'),
		  ('loanlife', '20')
		):
			data = { attr : val }
			f = ProcessForm( data, instance=p )
			self.assertTrue( f.is_valid() )
			self.assertEqual( len(f.fields), 1 )
			self.assertIn( attr, f.fields )

