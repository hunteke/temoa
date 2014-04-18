from base64 import decodestring as b64decodestring
from os import urandom
from random import randint

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from process_interface.models import Analysis, Vintage

class ViewLoginLogout ( TestCase ):

	@classmethod
	def setUpClass ( cls ):
		from django.contrib.auth.models import User

		User.objects.create_user(
		  username='test_user',
		  password='SomethingSecure',
		  email='some@email'
		)
		cls.user = User.objects.get(email='some@email')


	@classmethod
	def tearDownClass ( cls ):
		cls.user.delete()


	def test_bad_logins_fail ( self ):
		c = Client()

		# some fuzz testing
		# 257 is one byte longer than 256.  Just testing a potential off-by-one
		# error, or length-issues.
		for i in range(10):
			len_username = randint( 1, 257 ) # 1 and 257 are possible results
			len_password = randint( 1, 257 ) # 1 and 257 are possible results
			u = urandom( len_username )
			p = urandom( len_password )
			if (u, p) == ('test_user', 'SomethingSecure'):
				# this is tested below, and should /not/ fail.
				continue

			login_url    = reverse('process_interface:login')
			interact_url = reverse('process_interface:view')
			res = c.post(login_url, {'username': u, 'password': p})

			cookie = b64decodestring( res.cookies['ServerState'].coded_value )

			# Ensure test-runner does not think we're logged in
			self.assertEqual( len(c.session.items()), 0 )

			# Do we get the expected SEE OTHER interaction?
			self.assertEqual( res.status_code, 303 )
			self.assertEqual( res.reason_phrase, u'SEE OTHER' )
			self.assertEqual( res.content, '' )
			self.assertTrue( res.has_header('Location'), True )
			self.assertTrue( res.get('Location').endswith( interact_url ))

			# Did server appropriately leave us as unauthenticated?
			self.assertEqual( cookie, '{"username": null}' )

			# Ensure that the response we get is for unauthenticated users
			res = c.get( res.get('Location') )

			cookie = b64decodestring( res.cookies['ServerState'].coded_value )

			self.assertEqual( len(c.session.items()), 0 )
			self.assertEqual( res.status_code, 200 )
			self.assertEqual( res.reason_phrase, u'OK' )
			self.assertEqual( cookie, '{"username": null}' )
			self.assertNotIn( " id='LogoutLink' ", res.content )
			self.assertIn( " id='LoginForm' ", res.content )


	def test_successful_login_returns_username_in_cookie ( self ):
		c = Client()
		u, p = 'test_user', 'SomethingSecure'

		login_url = reverse('process_interface:login')
		res = c.post(login_url, {'username': u, 'password': p})

		cookie = b64decodestring( res.cookies['ServerState'].coded_value )

		# Ensure test-runner thinks we're authenticated
		self.assertNotEqual( len(c.session.items()), 0 )

		# First, do we get the expected SEE OTHER interaction?
		self.assertEqual( res.status_code, 303 )
		self.assertEqual( res.reason_phrase, u'SEE OTHER' )
		self.assertEqual( res.content, '' )
		self.assertTrue( res.has_header('Location'), True )
		self.assertTrue( res.get('Location').endswith('/interact/') )

		# Did server tell us that we successfully authenticated?
		self.assertEqual( cookie, '{"username": "test_user"}' )

		# Ensure that the response we get is for unauthenticated users
		res = c.get( res.get('Location') )

		cookie = b64decodestring( res.cookies['ServerState'].coded_value )

		self.assertEqual( res.status_code, 200 )
		self.assertEqual( res.reason_phrase, u'OK' )
		self.assertEqual( cookie, '{"username": "test_user"}' )
		self.assertIn( " id='LogoutLink' ", res.content )
		self.assertNotIn( " id='LoginForm' ", res.content )


	def test_logout ( self ):
		"""
		Ensure that the test client knows of logout status, and that server
		returns a null value for the username.
		"""
		c = Client()
		u, p = 'test_user', 'SomethingSecure'

		login_url = reverse('process_interface:login')
		res = c.post(login_url, {'username': u, 'password': p})

		cookie = b64decodestring( res.cookies['ServerState'].coded_value )

		# First, ensure we've logged in properly
		self.assertNotEqual( len(c.session.items()), 0 )
		self.assertEqual( cookie, '{"username": "test_user"}' )

		logout_url = reverse('process_interface:logout')
		res = c.get( logout_url )

		cookie = b64decodestring( res.cookies['ServerState'].coded_value )

		self.assertEqual( len(c.session.items()), 0 )
		self.assertEqual( cookie, '{"username": null}' )




class ViewAnalysisTest ( TestCase ):

	@classmethod
	def setUpClass ( cls ):
		from django.contrib.auth.models import User

		User.objects.create_user(
		  username='test_user',
		  password='SomethingSecure',
		  email='some@email'
		)
		cls.user = User.objects.get(email='some@email')


	@classmethod
	def tearDownClass ( cls ):
		cls.user.delete()


	def setUp ( self ):
		self.client = Client()
		up = {'username': 'test_user', 'password': 'SomethingSecure'}
		res = self.client.post(reverse('process_interface:login'), up)

		cookie = b64decodestring( res.cookies['ServerState'].coded_value )

		self.assertEqual( res.status_code, 303 )
		self.assertEqual( res.reason_phrase, u'SEE OTHER' )
		self.assertEqual( cookie, '{"username": "test_user"}' )


	def tearDown ( self ):
		self.client.get('/logout/')
		del self.client


	def test_anonymous_user_cannot_create_analyses ( self ):
		c = self.client

		# First become an anonymous user
		res = c.get( reverse('process_interface:logout') )

		cookie = b64decodestring( res.cookies['ServerState'].coded_value )

		# First, ensure we're properly anonymous
		self.assertEqual( len(c.session.items()), 0 )
		self.assertEqual( cookie, '{"username": null}' )

		analysis_create_url = reverse('process_interface:analysis_create')
		post_data = {}

		# Fuzz testing: should *always* get 401 (UNAUTHORIZED) in return
		for i in range(10):
			post_data.update(
			  name        = urandom( randint(1, 32769) ), # bounds on field length
			  description = urandom( randint(1, 32769) ), # just some large number
			  period_0    = urandom( randint(1, 32769) ), #  just " " "
			  global_discount_rate = urandom( randint(1, 32769) ), #  just " " "
			  vintages    = urandom( randint(1, 32769) ), # just " " "
			)
			res = c.post( analysis_create_url, post_data )

			self.assertEqual( res.reason_phrase, 'UNAUTHORIZED')
			self.assertEqual( len(c.session.items()), 0 )


	def test_analysis_creation ( self ):
		"""
		Ensure that:
		 1. a user can create a analysis
		 2. new analysis details are returned in response
		 3. new analysis is listed by analysis_list
		 4. a second analysis by the same name fails
		 5. a second analysis by a different name succeeds
		 6. analysis creation fails if no vintages are passed
		 7. analysis name removes any newline characters
		 8. analysis description stripped, and contains only unix newlines (\n)
		"""
		import json

		c = self.client

		analysis_create_url = reverse('process_interface:analysis_create')
		analysis_list_url   = reverse('process_interface:analysis_list')
		analysis_1 = {
		  'name'        : 'Test Analysis 1',
		  'description' : 'Some really awesome description',
		  'period_0'    : '0',
		  'global_discount_rate' : '0',
		  'vintages'    : '-5, -4,-3,-2,5,3,2,1,0'
		}
		analysis_2 = {
		  'name'        : 'Test Analysis 2',
		  'description' : 'Some other description',
		  'period_0'    : '0',
		  'global_discount_rate' : '0',
		  'vintages'    : '2010, 2013, 2011'
		}
		no_vintages = {
		  'name'        : 'No Vintages ... Should fail',
		  'description' : 'Another description',
		  'period_0'    : '0',
		  'global_discount_rate' : '0.5'
		}
		newlines_in_name = {
		  'name'        : '\n\rAre\0\t\r\n control\n characters\r removed?\n ',
		  'description' : 'Some description',
		  'period_0'    : '15',
		  'global_discount_rate' : '0.5',
		  'vintages'    : '15, 17, 19'
		}
		nonunix_newlines_in_description = {
		  'name'        : 'Some Analysis name',
		  'description' : '\r\nSome \r\n descripti\ton \n \r\r \t ',
		  'period_0'    : '15',
		  'global_discount_rate' : '0.5',
		  'vintages'    : '15, 17, 19'
		}

		# Part 1: Can we successfully create a new analysis?
		res = c.post( analysis_create_url, analysis_1 )

		self.assertEqual( res.status_code, 201 )
		self.assertGreater( len(res.content), 0 )

		# Part 2: Is new analysis data returned as a JSON object in response?
		try:
			ret_data = json.loads( res.content )
		except ValueError as e:
			msg = 'Newly created analysis data not JSON encoded: {}'
			self.fail( msg.format( res.content ))

		self.assertIn( 'id', ret_data )
		self.assertTrue( isinstance( ret_data['id'], int ))
		self.assertGreater( ret_data['id'], 0 )

		analysis = Analysis.objects.get( id=ret_data['id'] )

		# this will need to be updated for Python3, due to unicode vs bytes
		# but from the department of "Deal with that later" ...
		self.assertEqual( ret_data['username'], self.user.username )
		self.assertEqual( ret_data['name'], analysis.name )
		self.assertEqual( ret_data['description'], analysis.description )
		self.assertEqual( ret_data['period_0'], analysis.period_0 )
		self.assertAlmostEqual( ret_data['global_discount_rate'], analysis.global_discount_rate )

		vintages = Vintage.objects.filter( analysis=analysis )
		vintages = sorted( v.vintage for v in vintages )
		vintages = u', '.join( unicode(i) for i in vintages)
		self.assertEqual( ret_data['vintages'], vintages )

		# Part 3: ensure TemoaDB has stored new analysis for others to view
		res = c.get( analysis_list_url )

		try:
			ret_data = json.loads( res.content )
		except ValueError as e:
			msg = 'Analysis listing is not valid JSON: {}'
			self.fail( msg.format( res.content ))

		self.assertIn( 'data', ret_data )
		ret_data = ret_data['data']
		ids = set( a_data['id'] for a_data in ret_data )
		names = set( a_data['name'] for a_data in ret_data )

		self.assertIn( analysis.pk, ids )
		self.assertIn( analysis.name, names )

		# Part 4: Ensure that attempting to create a second analysis by the
		#         same name fails, and returns HTTP Status code 422
		res = c.post( analysis_create_url, analysis_1 )

		self.assertEqual( res.status_code, 422 )
		self.assertEqual( res.reason_phrase, u'UNPROCESSABLE ENTITY' )
		self.assertIn( 'An analysis by this name already exists.', res.content )

		try:
			ret_data = json.loads( res.content )
		except ValueError as e:
			msg = 'HttpResponse (error) object content is not valid JSON: {}'
			self.fail( msg.format( res.content ))

		# Part 5: Ensure that attempting to create a second analysis by a
		#         different name succeeds.
		res = c.post( analysis_create_url, analysis_2 )

		self.assertEqual( res.status_code, 201 )
		self.assertEqual( res.reason_phrase, u'CREATED' )
		self.assertGreater( len(res.content), 0 )

		# And is the second analysis data returned as a JSON object in response?
		try:
			ret_data = json.loads( res.content )
		except ValueError as e:
			msg = 'Newly created analysis data not JSON encoded: {}'
			self.fail( msg.format( res.content ))

		self.assertIn( 'id', ret_data )
		self.assertTrue( isinstance( ret_data['id'], int ))
		self.assertGreater( ret_data['id'], 0 )

		analysis = Analysis.objects.get( id=ret_data['id'] )

		# this will need to be updated for Python3, due to unicode vs bytes
		# but from the department of "Deal with that later" ...
		self.assertEqual( ret_data['username'], self.user.username )
		self.assertEqual( ret_data['name'], analysis.name )
		self.assertEqual( ret_data['description'], analysis.description )
		self.assertEqual( ret_data['period_0'], analysis.period_0 )
		self.assertAlmostEqual( ret_data['global_discount_rate'], analysis.global_discount_rate )

		vintages = Vintage.objects.filter( analysis=analysis )
		vintages = sorted( v.vintage for v in vintages )
		vintages = u', '.join( unicode(i) for i in vintages)
		self.assertEqual( ret_data['vintages'], vintages )

		# Part 6: Ensure that having some vintages is enforced
		res = c.post( analysis_create_url, no_vintages )

		self.assertEqual( res.status_code, 422 )
		self.assertEqual( res.reason_phrase, u'UNPROCESSABLE ENTITY' )
		self.assertIn( 'vintages', res.content )
		self.assertIn( 'required', res.content )

		try:
			ret_data = json.loads( res.content )
		except ValueError as e:
			msg = 'HttpResponse (error) object content is not valid JSON: {}'
			self.fail( msg.format( res.content ))

		# Part 7: Ensure name with newline/tab characters gets cleaned
		res = c.post( analysis_create_url, newlines_in_name )

		self.assertEqual( res.status_code, 201 )
		self.assertEqual( res.reason_phrase, u'CREATED' )

		try:
			ret_data = json.loads( res.content )
		except ValueError as e:
			msg = 'HttpResponse (new analysis) object content is not valid JSON: {}'
			self.fail( msg.format( res.content ))

		self.assertNotIn( u'\n', ret_data['name'] )
		self.assertNotIn( u'\r', ret_data['name'] )
		self.assertNotIn( u'\t', ret_data['name'] )
		self.assertNotIn( u'\0', ret_data['name'] )
		self.assertFalse( ret_data['name'].startswith(' ') )
		self.assertFalse( ret_data['name'].endswith(' ') )

		# Part 8: Ensure description is strip()ed and has '\r' characters del'd.
		res = c.post( analysis_create_url, nonunix_newlines_in_description )

		self.assertEqual( res.status_code, 201 )
		self.assertEqual( res.reason_phrase, u'CREATED' )

		try:
			ret_data = json.loads( res.content )
		except ValueError as e:
			msg = 'HttpResponse (new analysis) object content is not valid JSON: {}'
			self.fail( msg.format( res.content ))

		self.assertNotIn( u'\r', ret_data['description'] )
		self.assertNotIn( u'\0', ret_data['description'] )
		self.assertFalse( ret_data['description'].startswith(' ') )
		self.assertFalse( ret_data['description'].endswith(' ') )

