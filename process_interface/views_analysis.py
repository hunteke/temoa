from collections import defaultdict
from itertools import imap
import json

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import never_cache

from decorators.http import require_POST, require_DELETE, require_GET
from decorators.auth import require_login

from view_helpers import set_cookie
from models import (
  Analysis,
  AnalysisCommodity,
  CommodityType,
  Param_Demand,
  Param_DemandDefaultDistribution,
  Param_DemandSpecificDistribution,
  Param_SegFrac,
  Vintage,
)
from forms import (
  AnalysisCommodityForm,
  AnalysisForm,
  DemandDefaultDistributionForm,
  DemandForm,
  DemandSpecificDistributionForm,
  SegFracForm,
  VintagesForm,
)


def get_analyses_data ( analyses ):
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

	DDDistribution = defaultdict(dict)
	for ddd in Param_DemandDefaultDistribution.objects.filter(
	  timeslice__analysis__in=analyses ).select_related('timeslice__analysis'
	):
		sf  = ddd.timeslice
		a   = sf.analysis
		tslice = '{}, {}'.format(sf.season, sf.time_of_day)
		DDDistribution[ a ][ tslice ] = {
		  u'aId'   : a.pk,
		  u'sfId'  : sf.pk,
		  u'id'    : ddd.pk,
		  u'value' : ddd.value
		}

	_DSDistribution = defaultdict( nested_defaultdict(dict) )
	for dsd in Param_DemandSpecificDistribution.objects.filter(
	  timeslice__analysis__in=analyses ).select_related(
	  'timeslice__analysis',
	  'demand__commodity'
	):
		sf  = dsd.timeslice
		a   = sf.analysis
		s   = sf.season
		tod = sf.time_of_day
		dem = dsd.demand.commodity.name
		_DSDistribution[ a ][ dem ][ '{}, {}'.format(s, tod) ] = {
		  u'aId'   : a.pk,
		  u'dId'   : dsd.demand.pk,
		  u'sfId'  : sf.pk,
		  u'id'    : dsd.pk,
		  u'value' : dsd.value
		}

	DSDistribution = defaultdict( list )
	for a in _DSDistribution:
		lst = []
		for dem in _DSDistribution[ a ]:
			_DSDistribution[ a ][ dem ][ 'name' ] = dem
			lst.append( _DSDistribution[ a ][ dem ] )
		DSDistribution[ a ] = lst

	Demands = defaultdict(dict)
	for dem in Param_Demand.objects.filter(
	  period__analysis__in=analyses ).select_related('period__analysis'
	):
		cname    = dem.demand.commodity.name
		period   = dem.period.vintage
		analysis = dem.period.analysis
		Demands[ analysis ][ '{}, {}'.format(cname, period) ] = {
		  u'aId'    : analysis.pk,
		  u'cId'    : dem.demand.pk,
		  u'id'     : dem.pk,
		  u'commodity_name' : cname,
		  u'period' : period,
		  u'value'  : dem.value
		}

	data = [{
	    u'id'                   : a.pk,
	    u'username'             : a.user.username,
	    u'name'                 : a.name,
	    u'description'          : a.description,
	    u'period_0'             : a.period_0,
	    u'global_discount_rate' : a.global_discount_rate,
	    u'vintages'             : Vintages[ a ],
	    u'future_demands'       : Demands[ a ],
	    u'segfracs'             : SegFracs[ a ],
	    u'demanddefaultdistribution' : DDDistribution[ a ],
	    u'demandspecificdistribution' : DSDistribution[ a ],
	  }

	  for a in analyses
	]

	return data


@require_GET
@never_cache
def analysis_list ( req ):
	analyses = Analysis.objects.all().order_by( 'user__username', 'name' )

	data = get_analyses_data( analyses )

	data = json.dumps({ 'data' : data })
	res = HttpResponse( data, content_type='application/json' )
	res['Content-Length'] = len( data )
	set_cookie( req, res )

	return res


def collect_analysis_info ( analysis ):
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

	return data


@require_GET
@never_cache
def analysis_info ( req, analysis_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id )

	data = collect_analysis_info( analysis )
	data = json.dumps( data )
	res = HttpResponse( data, content_type='application/json' )
	res['Content-Length'] = len( data )

	set_cookie( req, res )
	return res


@require_GET
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
		with transaction.atomic():
			try:
				aform.save()
			except IntegrityError as ie:
				status = 422
				msgs['name'] = ['An analysis by this name already exists.']

			if 201 == status:
				vform.save()
				data = collect_analysis_info( analysis )
				data = json.dumps( data )
				res = HttpResponse(
				  data,
				  content_type='application/json',
				  status=status
				)
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
		with transaction.atomic():
			vform.save()
			aform.save()

		msgs = {
		  'id'                   : analysis.pk,
		  'username'             : analysis.user.username,
		  'name'                 : analysis.name,
		  'description'          : analysis.description,
		  'period_0'             : analysis.period_0,
		  'global_discount_rate' : analysis.global_discount_rate,
		}

		msgs['vintages'] = ', '.join(imap(str, sorted( v.vintage for v in
		  Vintage.objects.filter( analysis=analysis ) )))

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
			with transaction.atomic():
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
			with transaction.atomic():
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


## Demand #####################################################################

@require_login
@require_POST
@never_cache
def analysis_create_demand ( req, analysis_id, demand_commodity_id, period ):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	period = get_object_or_404( Vintage, vintage=period, analysis=analysis )
	endusedemand = get_object_or_404( AnalysisCommodity,
	  pk=demand_commodity_id,
	  commodity_type__name='demand',
	  analysis=analysis
	)

	status = 201  # 201 = Created
	msgs = {}

	dem = Param_Demand( period=period, demand=endusedemand )
	form = DemandForm( req.POST, instance=dem )

	if not form.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( form.errors )

		if 'value' in msgs:
			cname = endusedemand.commodity.name
			msgs[u'{}, {}'.format(cname, period.vintage)] = msgs.pop( 'value' )

	else:
		try:
			with transaction.atomic():
				form.save()
			msgs.update(
			  aId    = analysis.pk,
			  cId    = dem.demand.pk,
			  id     = dem.pk,
			  commodity_name = endusedemand.commodity.name,
			  period = period.vintage,
			  value  = dem.value
			)

		except IntegrityError as ie:
			status = 422  # to let Javascript know there was an error
			msg = 'Unable to create future demand ({}):  It already exists!'
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
def analysis_update_demand ( req, analysis_id, demand_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	dem = get_object_or_404( Param_Demand,
	  pk=demand_id, period__analysis=analysis )

	status = 200
	msgs = {}

	form = DemandForm( req.POST, instance=dem )

	if not form.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( form.errors )
		keys = set( msgs.keys() )

		if 'value' in keys:
			cname = dem.demand.commodity.name
			period = dem.period.vintage
			msgs[u'{}, {}'.format(cname, period)] = msgs.pop( 'value' )

	else:
		try:
			with transaction.atomic():
				form.save()
			msgs.update( value=dem.value )

		except IntegrityError as ie:
			status = 422  # to let Javascript know there was an error
			msg = 'Unable to update end use demand ({}).  Database said: {}'
			msg = msg.format( form.cleaned_data[ 'name' ], ie.messages[0] )
			msgs.update({ 'General Error' : msg })

	data = json.dumps( msgs )
	res = HttpResponse( data, content_type='application/json', status=status )
	res['Content-Length'] = len( data )

	set_cookie( req, res )
	return res


@require_login
@require_DELETE
@never_cache
def analysis_delete_demand ( req, analysis_id, demand_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	dem = get_object_or_404( Param_Demand,
		pk=demand_id, period__analysis=analysis )

	dem.delete()

	status = 204  # "No Content"
	res = HttpResponse( '', status=status )
	set_cookie( req, res );

	return res


## DemandDefaultDistribution ##################################################

@require_login
@require_POST
@never_cache
def analysis_create_demanddefaultdistribution ( req, analysis_id, segfrac_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	sf = get_object_or_404( Param_SegFrac, pk=segfrac_id, analysis=analysis )

	status = 201  # 201 = Created
	msgs = {}

	ddd = Param_DemandDefaultDistribution( timeslice=sf )
	form = DemandDefaultDistributionForm( req.POST, instance=ddd )

	if not form.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( form.errors )

		if 'value' in msgs:
			msgs['DDD_' + segfrac_id ] = msgs.pop( 'value' )

	else:
		try:
			with transaction.atomic():
				form.save()
			tslice = '{}, {}'.format(sf.season, sf.time_of_day)
			msgs.update(
			  aId   = analysis.pk,
			  sfId  = sf.pk,
			  id    = ddd.pk,
			  value = ddd.value
			)

		except IntegrityError as ie:
			status = 422  # to let Javascript know there was an error
			msg = 'Unable to create default distribution ({}):  It already exists!'
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
def analysis_update_demanddefaultdistribution ( req, analysis_id, ddd_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	ddd = get_object_or_404( Param_DemandDefaultDistribution,
		pk=ddd_id, timeslice__analysis=analysis )

	status = 200
	msgs = {}

	form = DemandDefaultDistributionForm( req.POST, instance=ddd )

	if not form.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( form.errors )
		keys = set( msgs.keys() )

		if 'value' in keys:
			msgs['DDD_{}'.format(ddd.timeslice.pk)] = msgs.pop( 'value' )

	else:
		try:
			with transaction.atomic():
				form.save()
			sf = ddd.timeslice
			tslice = '{}, {}'.format(sf.season, sf.time_of_day)
			msgs.update(
			  aId   = analysis.pk,
			  sfId  = sf.pk,
			  id    = ddd.pk,
			  value = ddd.value
			)

		except IntegrityError as ie:
			status = 422  # to let Javascript know there was an error
			msg = ('Unable to update default distribution ({}):  Another '
				'distribution by that name already exists!')
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
def analysis_delete_demanddefaultdistribution ( req, analysis_id, ddd_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	ddd = get_object_or_404( Param_DemandDefaultDistribution,
		pk=ddd_id, timeslice__analysis=analysis )

	ddd.delete()

	status = 204  # "No Content"
	res = HttpResponse( '', status=status )
	set_cookie( req, res );

	return res


## DemandSpecificDistribution #################################################

@require_login
@require_POST
@never_cache
def analysis_create_demandspecificdistribution (
  req, analysis_id, segfrac_id, demand_commodity_id
):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	sf = get_object_or_404( Param_SegFrac, pk=segfrac_id, analysis=analysis )
	endusedemand = get_object_or_404( AnalysisCommodity,
	  pk=demand_commodity_id,
	  commodity_type__name='demand',
	  analysis=analysis
	)
	status = 201  # 201 = Created
	msgs = {}

	dsd = Param_DemandSpecificDistribution( timeslice=sf, demand=endusedemand )
	form = DemandSpecificDistributionForm( req.POST, instance=dsd )

	if not form.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( form.errors )

		if 'value' in msgs:
			new_key = 'DSD_value_{},{}'.format(endusedemand.pk, sf.pk)
			msgs[ new_key ] = msgs.pop( 'value' )

	else:
		try:
			with transaction.atomic():
				form.save()
			tslice = '{}, {}'.format(sf.season, sf.time_of_day)
			msgs.update(
			  aId   = analysis.pk,
			  dId   = dsd.demand.pk,
			  sfId  = sf.pk,
			  id    = dsd.pk,
			  value = dsd.value
			)

		except IntegrityError as ie:
			status = 422  # to let Javascript know there was an error
			msg = 'Unable to create demand distribution ({}):  It already exists!'
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
def analysis_update_demandspecificdistribution ( req, analysis_id, dsd_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	dsd = get_object_or_404( Param_DemandSpecificDistribution,
		pk=dsd_id, timeslice__analysis=analysis )

	status = 200
	msgs = {}

	form = DemandSpecificDistributionForm( req.POST, instance=dsd )

	if not form.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( form.errors )
		keys = set( msgs.keys() )

		if 'value' in keys:
			new_key = 'DSD_values_{},{}'.format(dsd.demand.pk, dsd.timeslice.pk)
			msgs[ new_key ] = msgs.pop( 'value' )

	else:
		try:
			with transaction.atomic():
				form.save()
			msgs.update( value=dsd.value )

		except IntegrityError as ie:
			status = 422  # to let Javascript know there was an error
			msg = ('Unable to update demand distribution ({}):  Another '
				'distribution by that name already exists!')
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
def analysis_delete_demandspecificdistribution ( req, analysis_id, dsd_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	dsd = get_object_or_404( Param_DemandSpecificDistribution,
		pk=dsd_id, timeslice__analysis=analysis )

	dsd.delete()

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
			with transaction.atomic():
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
			with transaction.atomic():
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

