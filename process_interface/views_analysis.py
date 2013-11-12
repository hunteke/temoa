from itertools import imap

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import simplejson as json
from django.views.decorators.cache import never_cache

from decorators.http import require_POST, require_DELETE
from decorators.auth import require_login

from view_helpers import set_cookie
from models import (
  Analysis,
  AnalysisCommodity,
  CommodityType,
  Vintage,
)
from forms import AnalysisForm, AnalysisCommodityForm, VintagesForm


@never_cache
def analysis_list ( req ):
	analyses = [
	  { 'id'                   : a.pk,
	    'username'             : a.user.username,
	    'name'                 : a.name,
	    'description'          : a.description,
	    'period_0'             : a.period_0,
	    'global_discount_rate' : a.global_discount_rate,
	  }

	  for a in Analysis.objects.all().order_by( 'user__username', 'name' )
	]

	for a in analyses:
		a['vintages'] = ', '.join(imap(str, sorted( v.vintage for v in
		  Vintage.objects.filter( analysis__pk=a['id'] ) )))

	data = json.dumps( analyses )
	res = HttpResponse( data, content_type='application/json' )
	res['Content-Length'] = len( data )
	set_cookie( req, res )

	return res


@never_cache
def analysis_info ( req, analysis_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id )

	data = {
	  'id'                   : analysis.pk,
	  'username'             : analysis.user.username,
	  'name'                 : analysis.name,
	  'description'          : analysis.description,
	  'period_0'             : analysis.period_0,
	  'global_discount_rate' : analysis.global_discount_rate,
	}

	data['vintages'] = ', '.join(imap(str, sorted( v.vintage for v in
		  Vintage.objects.filter( analysis=analysis ) )))

	data = json.dumps( data )
	res = HttpResponse( data, content_type='application/json' )
	res['Content-Length'] = len( data )

	set_cookie( req, res )
	return res


@never_cache
def analysis_commodity_list ( req, analysis_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id )

	types = CommodityType.objects.all()
	data = {}
	for ct in types:
		data[ ct.name ] = [{
		    'aId' : analysis.pk, 'id' : ac.pk, 'name' : ac.commodity.name
		  }
		  for ac in AnalysisCommodity.objects.filter(
		    analysis=analysis, commodity_type=ct )
		]

	data = { 'data' : [data] } # CanJS demands this data structure.  Sigh.
	data = json.dumps( data )
	res = HttpResponse( data, content_type='application/json' )
	res['Content-Length'] = len( data )

	set_cookie( req, res )
	return res


# All methods below this line should @require_login and another require (e.g.,
# @require_POST, @require_DELETE)


@require_login
@require_POST
@never_cache
def analysis_create ( req ):
	status = 201   # 201 = Created
	msgs = {}

	analysis = Analysis( user=req.user )
	aform = AnalysisForm( req.POST, instance=analysis )
	vform = VintagesForm( req.POST, analysis=analysis )
	if not aform.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( aform.errors )

	if not vform.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( vform.errors )

	if 201 == status:
		with transaction.commit_on_success():
			try:
				aform.save()
			except IntegrityError as ie:
				status = 422
				msgs['name'] = ['An analysis by this name already exists.']

			if 201 == status:
				vform.save()
				res = analysis_info( req, analysis.pk )
				res['Reason-Phrase'] = 'Created'
				res.status_code = status
				return res

	data = json.dumps( msgs )
	res = HttpResponse( data, content_type='application/json', status=status )
	res['Content-Length'] = len( data )

	set_cookie( req, res )
	return res


@require_login
@require_POST
@never_cache
def analysis_update ( req, analysis_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )

	status = 200   # 200 = General OK
	msgs = {}

	aform = AnalysisForm( req.POST, instance=analysis )
	vform = VintagesForm( req.POST, analysis=analysis )
	if not aform.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( aform.errors )

	if not vform.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( vform.errors )

	if 200 == status:
		with transaction.commit_on_success():
			vform.save()
			aform.save()
		return analysis_info( req, analysis.pk );

	data = json.dumps( msgs )
	res = HttpResponse( data, content_type='application/json', status=status )
	res['Content-Length'] = len( data )

	set_cookie( req, res )
	return res



@require_login
@require_POST
@never_cache
def analysis_create_commodity ( req, analysis_id, ctype ):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	commodity_type = get_object_or_404( CommodityType, name=ctype )

	status = 201  # 201 = Created
	msgs = {}

	acom = AnalysisCommodity( analysis=analysis, commodity_type=commodity_type )
	form = AnalysisCommodityForm( req.POST, instance=acom )

	if not form.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( form.errors )

	else:
		try:
			with transaction.commit_on_success():
				form.save()
			msgs.update(
			  aId  = analysis.pk,
			  id   = acom.pk,
			  name = acom.commodity.name
			)

		except IntegrityError as ie:
			status = 422  # to let Javascript know there was an error
			msg = 'Unable to create commodity ({}):  It already exists!'
			msg = msg.format( form.cleaned_data[ 'name' ] )
			msgs.update({ 'General Error' : msg })

	data = json.dumps( msgs )
	res = HttpResponse( data, content_type='application/json', status=status )
	res['Content-Length'] = len( data )

	set_cookie( req, res )
	return res



@require_login
@require_POST
@never_cache
def analysis_update_commodity ( req, analysis_id, commodity_id ):
	analysis  = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	acom = get_object_or_404( AnalysisCommodity,
	  pk=commodity_id, analysis=analysis )

	status = 200
	msgs = {}

	form = AnalysisCommodityForm( req.POST, instance=acom )

	if not form.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( form.errors )

	else:
		try:
			with transaction.commit_on_success():
				form.save()
			msgs.update(
			  aId  = analysis.pk,
			  id   = acom.pk,
			  name = acom.commodity.name
			)

		except IntegrityError as ie:
			status = 422  # to let Javascript know there was an error
			msg = ('Unable to update commodity ({}):  Another commodity by that '
			  'name already exists!')
			msg = msg.format( form.cleaned_data[ 'name' ] )
			msgs.update({ 'General Error' : msg })

	data = json.dumps( msgs )
	res = HttpResponse( data, content_type='application/json', status=status )
	res['Content-Length'] = len( data )

	set_cookie( req, res )
	return res


@require_login
@require_DELETE
@never_cache
def analysis_delete_commodity ( req, analysis_id, commodity_id ):
	analysis  = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	acom = get_object_or_404( AnalysisCommodity,
	  pk=commodity_id, analysis=analysis )

	acom.delete()

	status = 204  # "No Content"
	res = HttpResponse( '', status=status )
	set_cookie( req, res );

	return res


#############################################################################
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

