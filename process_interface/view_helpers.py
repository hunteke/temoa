from base64 import b64encode

from django.contrib import messages
from django.http import HttpResponse
from django.utils import simplejson as json

def get_messages ( req ):
	msg_storage = messages.get_messages( req )
	msgs = [ (m.tags, m.message) for m in msg_storage ]

	msg_storage.used = True  # remove the messages

	data = json.dumps( msgs )
	res = HttpResponse( data, content_type='application/json' )
	res['Content-Length'] = len( data )
	return res


def set_cookie ( req, res, **kwargs ):
	cookie = {}
	if req.user.is_authenticated():
		cookie[ 'username' ] = req.user.username
	else:
		cookie[ 'username' ] = None

	for key in ( 'analysis_id', 'process_ids',):
		if key in kwargs:
			cookie[ key ] = kwargs[ key ]

	cookie = b64encode(json.dumps( cookie ))
	res.set_cookie( 'ServerState', value=cookie, max_age=None ) # session only

