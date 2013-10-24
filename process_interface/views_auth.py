from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse

from http import HttpResponseSeeOther

from forms import LoginForm
from view_helpers import set_cookie

def login_view ( req ):
	res = HttpResponseSeeOther(reverse('process_interface:view') )

	if req.POST:
		form = LoginForm( req.POST )
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate( username=username, password=password )
			if user is not None:
				if user.is_active:
					login( req, user )

	set_cookie( req, res )
	return res


def logout_view ( req ):
	logout( req )
	res = HttpResponseSeeOther(reverse('process_interface:view') )
	set_cookie( req, res )
	return res

