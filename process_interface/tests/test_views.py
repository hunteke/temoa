# vim:sw=3:ts=3:fileencoding=utf-8:list:listchars=tab\:»·,trail\:·:noexpandtab:
# :encoding=utf-8:indentSize=3:tabSize=3:noTabs=false:

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

		self.analysis_a_id = Analysis.objects.create(
		  user=self.user,
		  name='A',
		  description='desc',
		  period_0=1,
		  global_discount_rate=0.05
		).pk

		self.analysis_b_id = Analysis.objects.create(
		  user=self.user,
		  name='B',
		  description='desc',
		  period_0=1,
		  global_discount_rate=0.05
		).pk


	def tearDown ( self ):
		logout_url = reverse('process_interface:logout')
		self.client.get( logout_url )
		del self.client

		ids = (self.analysis_a_id, self.analysis_b_id)
		del self.analysis_a_id, self.analysis_b_id

		analyses = Analysis.objects.filter( id__in=ids )
		for a in analyses:
			a.delete()


	def test_anonymous_user_cannot_create_analyses ( self ):
		c = self.client   # already authenticated per setUp

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

		c = self.client   # already authenticated per setUp

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
		  'period_0'    : '2010',
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
		vintages = u', '.join( str(i) for i in vintages)
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
		vintages = u', '.join( str(i) for i in vintages)
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


	def test_analysis_update ( self ):
		"""
		Ensure that:
		 1. user can change own analysis information (name, description, etc.)
		 2. updated model characteristics returned as JSON in response
		 3. user cannot change analysis name to match another of user's analyses
		 4. period_0 only accepts integers, with appropriate error message
		 5. period_0 is always a member of vintages[:-1]
		 6. only POST protocol is accepted (e.g. GET, PUT, HEAD return NOT ALLOWED
		 7. user cannot change another users analysis
		 8. anonymous requests are forbidden
		"""
		import json

		c = self.client   # already authenticated per setUp

		analysis = Analysis.objects.get( pk=self.analysis_a_id )

		analysis_list_url   = reverse('process_interface:analysis_list')
		analysis_update_url = reverse('process_interface:analysis_update',
		  kwargs={'analysis_id': analysis.pk})

		analysis_1_new_data = {
		  'name'        : 'More accurate name',
		  'description' : 'An updated description',
		  'period_0'    : '-2',
		  'global_discount_rate' : '0.15',
		  'vintages'    : '-5, -4,-3,-2,5,3,2,1,0'
		}
		period_0_not_in_vintages_data = {
		  'name'        : 'AnalysisName',
		  'description' : 'AnalysisDescription',
		  'global_discount_rate' : '0.05'
		}

		# Part 1 and 2: Ensure user can successfully update and that server
		#     returns the updated data through JSON
		res = c.post( analysis_update_url, analysis_1_new_data )

		try:
			ret_data = json.loads( res.content )
		except ValueError as e:
			msg = ('HttpResponse (updated analysis) object content is not valid '
			  'JSON: {}')
			self.fail( msg.format( res.content ))
		self.assertEqual( res.status_code, 200 )
		self.assertEqual( res.reason_phrase, u'OK' )
		self.assertGreater( len(ret_data), 0 )

		analysis = Analysis.objects.get( pk=analysis.pk )
		vintages = Vintage.objects.filter( analysis=analysis )
		vintages = sorted( v.vintage for v in vintages )
		vintages = u', '.join( str(i) for i in vintages )

		self.assertEqual( analysis.name, ret_data['name'] )
		self.assertEqual( analysis.description, ret_data['description'] )
		self.assertEqual( analysis.period_0, ret_data['period_0'] )
		self.assertAlmostEqual( analysis.global_discount_rate, ret_data['global_discount_rate'] )
		self.assertEqual( vintages, ret_data['vintages'] )

		# Part 3: Ensure user cannot choose a name already chosen
		analysis_1_new_data['name'] = 'B'

		res = c.post( analysis_update_url, analysis_1_new_data )

		self.assertEqual( res.status_code, 422 )
		self.assertEqual( res.reason_phrase, u'UNPROCESSABLE ENTITY' )
		self.assertGreater( len(res.content), 0 )

		try:
			ret_data = json.loads( res.content )
		except ValueError as e:
			msg = ('HttpResponse (analysis update error) content is not valid '
			  'JSON: {}')
			self.fail( msg.format( res.content ))
		self.assertIn( 'Unable to change name ', res.content )
		self.assertTrue( isinstance( ret_data, dict ))
		self.assertIn( 'General Error', ret_data )

		# Part 4: Ensure period_0 only accepts integers, with appropriate error
		#   message
		analysis_1_new_data['name'] = 'SomethingUnique'
		_old_p0 = analysis_1_new_data['period_0']

		# Fuzz testing: should always return 422 if bad period_0 sent
		for i in range(10):
			length = randint(1, 257)

			# get random bytes, removing any whitespace
			p0 = urandom( length ).strip()
			length = len( p0 )  # size of p0 after removing whitespace
			count = 0   # count of characters that are ASCII digits
			for char in p0:
				if 48 <= char < 58: # i.e. is '0' through '9'
					count += 1
			if count == length:
				# this is trivially an integer as all bytes are digits; skip
				# this test
				continue
			analysis_1_new_data['period_0'] = p0
			res = c.post( analysis_update_url, analysis_1_new_data )

			self.assertEqual( res.status_code, 422 )
			self.assertEqual( res.reason_phrase, u'UNPROCESSABLE ENTITY' )
			self.assertGreater( len(res.content), 0 )

			try:
				ret_data = json.loads( res.content )
			except ValueError as e:
				msg = ('HttpResponse (analysis update error) content is not valid '
				  'JSON: {}')
				self.fail( msg.format( res.content ))
			self.assertIn( 'Enter a whole number', res.content )
			self.assertTrue( isinstance( ret_data, dict ))
			self.assertIn( 'period_0', ret_data )

		analysis_1_new_data['period_0'] = _old_p0
		del _old_p0

		# Part 5: Ensure period_0 is always a member of vintages[:-1]
		#   Fuzz testing: should always get a 422 response
		vintages = sorted( randint(-1e9, 1e9) for i in range(10) )
		vintages_str = u', '.join(map(str, vintages))
		period_0_not_in_vintages_data['vintages'] = vintages_str
		for i in range(10):
			period_0 = randint(-1e9, 1e9)
			if period_0 in vintages: continue
			period_0_not_in_vintages_data['period_0'] = period_0

			res = c.post( analysis_update_url, period_0_not_in_vintages_data )

			self.assertEqual( res.status_code, 422 )
			self.assertEqual( res.reason_phrase, u'UNPROCESSABLE ENTITY' )
			self.assertGreater( len(res.content), 0 )
			self.assertIn( 'Vintages does not contain Period 0', res.content )
			try:
				ret_data = json.loads( res.content )
			except ValueError as e:
				msg = ('HttpResponse (analysis update error) content is not valid '
				  'JSON: {}')
				self.fail( msg.format( res.content ))
			self.assertTrue( isinstance( ret_data, dict ))
			self.assertIn( 'vintages', ret_data )

		# Part 6: Other protocols are forbidden (e.g. GET, PATCH, PUT, HEAD)
		for func in (c.delete, c.get, c.patch, c.put, c.head):
			res = func( analysis_update_url, analysis_1_new_data )

			self.assertEqual( res.status_code, 405 )
			self.assertEqual( res.reason_phrase, u'METHOD NOT ALLOWED' )
			self.assertEqual( len(res.content), 0 )

		# Part 7: Ensure one user cannot change another's analysis data
		analysis = Analysis.objects.exclude( user=self.user )[0]
		analysis_update_url = reverse('process_interface:analysis_update',
		  kwargs={'analysis_id': analysis.pk})

		res = c.post( analysis_update_url, analysis_1_new_data )

		self.assertEqual( res.status_code, 403 )
		self.assertEqual( res.reason_phrase, u'FORBIDDEN' )
		self.assertGreater( len(res.content), 0 )

		try:
			ret_data = json.loads( res.content )
		except ValueError as e:
			msg = ('HttpResponse (analysis update error) content is not valid '
			  'JSON: {}')
			self.fail( msg.format( res.content ))
		self.assertIn( ' does not own analysis ', ret_data )

		# Part 8: Anonymous requests are forbidden
		logout_url = reverse('process_interface:logout')

		res = c.get( logout_url )

		self.assertEqual( res.status_code, 303 )
		self.assertEqual( res.reason_phrase, u'SEE OTHER' )

		analysis_before = Analysis.objects.get( pk=analysis.pk )
		res = c.post( analysis_update_url, analysis_1_new_data )
		analysis_after  = Analysis.objects.get( pk=analysis.pk )

		self.assertEqual( res.status_code, 401 )
		self.assertEqual( res.reason_phrase, u'UNAUTHORIZED' )

		for attr in ('name', 'description', 'period_0', 'global_discount_rate'):
			self.assertEqual(
			  getattr(analysis_before, attr),
			  getattr(analysis_after, attr)
			)

