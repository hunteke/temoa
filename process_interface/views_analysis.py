from itertools import imap

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.db import transaction
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, get_object_or_404
from django.utils import simplejson as json
from django.views.decorators.http import require_POST

from view_helpers import set_cookie
from models import (
  Analysis,
  AnalysisCommodity,
  CommodityType,
  Vintage,
)
from forms import AnalysisForm


def get_analysis_list ( user ):
	analyses = [
	  { 'pk'   : a.pk,
	    'name' : '{} - {}'.format( a.user.username, a.name )
	  }

	  for a in Analysis.objects.all().order_by( 'user__username', 'name' ) ]

	if user.is_authenticated():
		analyses.insert( 0, { 'pk': 'New', 'name' : 'Create Analysis ...' } )

	return analyses


def list_analyses ( req ):
	analyses = get_analysis_list( req.user )

	c = {}
	c.update( analyses=analyses )
	return render_to_response('process_interface/analyses_list.html', c)


def user_analyses ( req, username ):
	if 'all' == username:
		analyses = [ (a.id, unicode(a) )  for a in Analysis.objects.all() ]
		analyses.sort( key=i_get(1) )
	elif username:
		user = get_object_or_404( User, username=username )
		analyses = [
		  (a.id, unicode(a) )  for a in Analysis.objects.filter( user=user )
		]
		analyses.sort( key=i_get(1) )

	else:
		raise Http404

	data = json.dumps( analyses )
	response = HttpResponse(
	  data,
	  content_type='application/json'
	)
	response['Content-Length'] = len( data )
	return response


def analysis_info ( req, analysis_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id )
	analyses = get_analysis_list( req.user )

	c = {}
	c.update( analysis_id=analysis.pk, analyses=analyses )
	c.update( csrf(req) )

	if req.user.pk is not analysis.user.pk:
		# test against .pk because req.user is lazy object.
		template = 'process_interface/info_analysis.html'
		c.update(
		  username             = analysis.user.username,
		  name                 = analysis.name,
		  description          = analysis.description,
		  period_0             = analysis.period_0,
		  global_discount_rate = analysis.global_discount_rate,
		)

	else:
		template = 'process_interface/form_analysis.html'
		form = AnalysisForm( instance=analysis )
		c.update( form=form )

	res = render( req, template, c )
	set_cookie( req, res, analysis_id=analysis_id )
	return res


@login_required
@require_POST
def analysis_update ( req, analysis_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	analyses = get_analysis_list( req.user )

	template = 'process_interface/form_analysis.html'
	status = 200

	if req.POST:
		form = AnalysisForm( req.POST, instance=analysis )
		if not form.is_valid():
			status = 422  # to let Javascript know there was an error
			msg = '\n'.join( m.as_text() for k, m in form.errors.iteritems() )
			messages.error( req, msg )

		else:
			try:
				form.save()
				form = AnalysisForm( instance=analysis )
			except IntegrityError as ie:
				msg = 'Unable to update analysis.  Database said: {}'
				messages.error( req, msg.format( ie ))
				status = 422

	else:
		form = AnalysisForm( instance=analysis )

	c = {}
	c.update( form=form, analysis_id=analysis.pk, analyses=analyses )
	c.update( csrf(req) )

	res = render( req, template, c, status=status )
	set_cookie( req, res )
	return res


@login_required
def analysis_new ( req ):
	analyses = get_analysis_list( req.user )
	template = 'process_interface/form_analysis_new.html'

	status = 200

	if req.POST:
		analysis = Analysis( user=req.user )
		form = AnalysisForm( req.POST, instance=analysis )

		if not form.is_valid():
			status = 422  # to let Javascript know there was an error
			msg = '\n'.join( m.as_text() for k, m in form.errors.iteritems() )
			messages.error( req, msg )

		else:
			try:
				form.save()
				return analysis_update( req, analysis.pk )

			except IntegrityError as ie:
				msg = 'Unable to create new analysis.  Database said: {}'
				messages.error( req, msg.format( ie ))
				status = 422

	else:
		form = AnalysisForm()

	c = {}
	c.update( form=form, analyses=analyses )
	c.update( csrf(req) )

	res = render( req, template, c, status=status )
	set_cookie( req, res, analysis_id='New' )
	return res
