from collections import defaultdict
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
  Param_SegFrac,
  Vintage,
)
from forms import (
  AnalysisForm,
  AnalysisCommodityForm,
  SegFracForm,
  VintagesForm,
)


def get_analysis_info ( analyses ):
	if not analyses:
		return { 'data' : [] }

	def nested_defaultdict ( cls ):
		def wrapped ( ):
			return defaultdict( cls )
		return wrapped

	Vintages = defaultdict(list)
	for v in Vintage.objects.filter(
	  analysis__in=analyses ).select_related('analysis'):
		Vintages[ v.analysis ].append( v.vintage )
	for a in Vintages:
		Vintages[ a ] = ', '.join( imap( str, sorted( Vintages[ a ] )))

	SegFracs = defaultdict(list)
	for sf in Param_SegFrac.objects.filter(
	  analysis__in=analyses ).select_related(
	  'analysis'
	):
		s   = sf.season
		tod = sf.time_of_day
		SegFracs[ sf.analysis ].append({
		  u'aId'         : sf.analysis.pk,
		  u'id'          : sf.pk,
		  u'season'      : sf.season,
		  u'time_of_day' : sf.time_of_day,
		  u'value'       : sf.value
		})
	for a in SegFracs:
		SegFracs[ a ].sort( key=lambda x: (x['season'], x['time_of_day']) )

	data = [{
	    u'id'                   : a.pk,
	    u'username'             : a.user.username,
	    u'name'                 : a.name,
	    u'description'          : a.description,
	    u'period_0'             : a.period_0,
	    u'global_discount_rate' : a.global_discount_rate,
	    u'vintages'             : Vintages[ a ],
	    u'segfracs'             : SegFracs[ a ],
	  }

	  for a in analyses
	]

	return data


@never_cache
def analysis_list ( req ):
	analyses = Analysis.objects.all().order_by( 'user__username', 'name' )

	data = get_analysis_info( analyses )

	data = json.dumps({ 'data' : data })
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


## SegFrac ####################################################################

@require_login
@require_POST
@never_cache
def analysis_create_segfrac ( req, analysis_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )

	status = 201  # 201 = Created
	msgs = {}

	sf = Param_SegFrac( analysis=analysis )
	form = SegFracForm( req.POST, instance=sf )

	if not form.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( form.errors )
		keys = set( msgs.keys() )

		if '__all__' in keys:
			msgs['General Error'] = msgs.pop('__all__')

		if 'season' in keys:
			msgs['SliceName_New'] = msgs.pop( 'season' )
		elif 'time_of_day' in keys:
			msgs['SliceName_New'] = msgs.pop( 'time_of_day' )

		if 'value' in keys:
			msgs['SliceValue_New'] = msgs.pop( 'value' )


	else:
		try:
			with transaction.commit_on_success():
				form.save()
			tslice = '{}, {}'.format(sf.season, sf.time_of_day)
			msgs.update(
			  aId   = analysis.pk,
			  id    = sf.pk,
			  value = sf.value
			)

		except IntegrityError as ie:
			status = 422  # to let Javascript know there was an error
			msg = 'Unable to create time slice ({}):  It already exists!'
			msg = msg.format( form.cleaned_data[ 'name' ] )
			msgs.update({ 'General Error' : msg })
		except ValidationError as ve:
			status = 422  # to let Javascript know there was an error
			msg = 'Unable to create time slice ({}).  Database said: {}'
			msg = msg.format( form.cleaned_data[ 'name' ], ve.messages[0] )
			msgs.update({ 'General Error' : msg })

	data = json.dumps( msgs )
	res = HttpResponse( data, content_type='application/json', status=status )
	res['Content-Length'] = len( data )

	set_cookie( req, res )
	return res



@require_login
@require_POST
@never_cache
def analysis_update_segfrac ( req, analysis_id, segfrac_id ):
	analysis  = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	sf = get_object_or_404( Param_SegFrac, pk=segfrac_id, analysis=analysis )

	status = 200
	msgs = {}

	form = SegFracForm( req.POST, instance=sf )

	if not form.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( form.errors )
		keys = set( msgs.keys() )

		if '__all__' in keys:
			msgs['General Error'] = msgs.pop('__all__')

		if 'season' in keys:
			msgs['SliceName_{}'.format(sf.pk)] = msgs.pop( 'season' )
		elif 'time_of_day' in keys:
			msgs['SliceName_{}'.format(sf.pk)] = msgs.pop( 'time_of_day' )

		if 'value' in keys:
			msgs['SliceValue_{}'.format(sf.pk)] = msgs.pop( 'value' )

	else:
		try:
			with transaction.commit_on_success():
				form.save()
			tslice = '{}, {}'.format(sf.season, sf.time_of_day)
			msgs.update(
			  aId   = analysis.pk,
			  id    = sf.pk,
			  value = sf.value
			)

		except IntegrityError as ie:
			status = 422  # to let Javascript know there was an error
			msg = ('Unable to update time slice ({}):  Another time slice by that '
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
def analysis_delete_segfrac ( req, analysis_id, segfrac_id ):
	analysis  = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	sf = get_object_or_404( Param_SegFrac, pk=segfrac_id, analysis=analysis )

	sf.delete()

	status = 204  # "No Content"
	res = HttpResponse( '', status=status )
	set_cookie( req, res );

	return res


## Commodity ##################################################################

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
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
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

