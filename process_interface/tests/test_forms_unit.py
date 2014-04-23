import factory

from django.test import TestCase

from process_interface.forms import (
  LoginForm,
)

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

