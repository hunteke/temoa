import json

from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.http import HttpResponse, Http404
from django.shortcuts import render, render_to_response
from django.views.decorators.cache import cache_control

from decorators.http import require_GET
from settings import CD   # CD = content delivery
from forms import LoginForm

from views_analysis import *
from views_auth import *
from views_download import *
from views_process import *
from views_technology import *

from view_helpers import set_cookie

@require_GET
def home ( req ):
	return render_to_response('process_interface/home.html')


@require_GET
def view ( req ):
	template = 'process_interface/view.html'

	c = {'CD': CD, 'username': None}
	c.update(csrf(req))

	if req.user.is_authenticated():
		c.update( username=req.user.username )
	else:
		c.update( password_form=LoginForm() )

	res = render( req, template, c )
	set_cookie( req, res )

	return res


@require_GET
@cache_control(public=True, max_age=300)  # in seconds
def get_client_template ( req, template ):
	# Client templates are templates rendered by the client (e.g., ejs).
	# Due to caching, these are somewhat difficult to update.  So, for the case
	# of a rollout, ensure that these templates have a reasonably small cache
	# life.  Reasonably small is probably 5 minutes, allowing a rollout during
	# the workday.
	return render_to_response('process_interface/client/' + template )


def tutorial ( req ):
	raise Http404


def user ( req ):
	users = [ (u.username, u.get_full_name() ) for u in User.objects.all() ]

	for i, (uname, fname) in enumerate( users ):
		if not fname:
			users[ i ] = (uname, 'unknown name')
	users.sort()

	data = json.dumps( users )
	response = HttpResponse(
	  data,
	  content_type='application/json'
	)
	response['Content-Length'] = len( data )
	return response
