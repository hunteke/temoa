import factory

from django.test import TestCase

from process_interface.forms import (
  LoginForm,
)

class TestLoginForm ( TestCase ):

	def test_username_required ( self ):
		form = LoginForm({ b'password': b'asdf' })

		self.assertFalse( form.is_valid() )
		self.assertIn( 'username', form.errors )
		self.assertIn( 'is required', str(form.errors['username']) )


	def test_password_required ( self ):
		form = LoginForm({ b'username': b'asdf' })

		self.assertFalse( form.is_valid() )
		self.assertIn( 'password', form.errors )
		self.assertIn( 'is required', str(form.errors['password']) )


	def test_password_is_not_empty ( self ):
		form = LoginForm({ b'username': b'asdf', b'password': b'' })

		self.assertFalse( form.is_valid() )
		self.assertIn( 'password', form.errors )
		self.assertIn( 'is required', str(form.errors['password']) )


	def test_max_length_is_254 ( self ):
		form = LoginForm({ b'username': b'a' * 255, b'password': b'asdf' })

		self.assertFalse( form.is_valid() )
		self.assertIn( 'username', form.errors )
		self.assertIn( 'has at most 254 cha', str(form.errors['username']) )


	def test_valid_userpass ( self ):
		form = LoginForm({ b'username': b'UserName', b'password': b'UserPass' })

		self.assertTrue( form.is_valid() )

