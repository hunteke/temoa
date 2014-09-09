# vim:sw=3:ts=3:fileencoding=utf-8:list:listchars=tab\:»·,trail\:·:noexpandtab:
# :encoding=utf-8:indentSize=3:tabSize=3:noTabs=false:

from collections import defaultdict
import json

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.decorators.cache import never_cache

from decorators.http import require_POST, require_DELETE
from decorators.auth import require_login

from models import (
  Analysis,
  Param_CapacityFactorTech,
  Param_MaxMinCapacity,
  Param_SegFrac,
  Param_TechInputSplit,
  Param_TechOutputSplit,
  Process,
  Technology,
  Vintage,
)
from forms import (
  AnalysisTechnologyForm,
  CapacityFactorTechForm,
  TechInputSplitForm,
  TechOutputSplitForm,
)

from view_helpers import set_cookie


def get_technology_info ( analysis, technologies ):
	def null ( ):
		return None

	a_pk = analysis.pk
	p0 = analysis.period_0

	horizon = sorted( v.vintage for v in Vintage.objects.filter(
	  analysis=analysis, vintage__gte=p0 ) )[:-1]  # last year is not a vintage

	slices = []
	slices.extend( Param_SegFrac.objects.filter( analysis=analysis ).order_by(
	  'season', 'time_of_day' ).select_related( 'analysis'
	))

	CapacityFactors = defaultdict( dict )
	for cf in Param_CapacityFactorTech.objects.filter(
	  technology__in=technologies ).order_by(
	  'technology', 'timeslice__season', 'timeslice__time_of_day'
	):
		CapacityFactors[ cf.technology ][ cf.timeslice ] = {
		  'aId'   : a_pk,
		  'tId'   : cf.technology.pk,
		  'sfId'  : cf.timeslice.pk,
		  'id'    : cf.pk,
		  'value' : cf.value
		}

	for t in technologies:
		cf = CapacityFactors[ t ]
		CapacityFactors[ t ] = [ sl in cf and cf[ sl ] or None for sl in slices ]

	MaxMinCapacities = defaultdict( dict )
	for maxmin in Param_MaxMinCapacity.objects.filter(
	  technology__in=technologies ).order_by( 'period' ):
		MaxMinCapacities[ maxmin.technology ][ maxmin.period.vintage ] = {
		  'aId'     : a_pk,
		  'tId'     : maxmin.technology.pk,
		  'maximum' : maxmin.maximum,
		  'minimum' : maxmin.minimum
		}

	TechInputSplit = defaultdict( list )
	for isplit in Param_TechInputSplit.objects.filter(
	  technology__in=technologies ).order_by( 'inp_commodity__commodity__name' ):
		TechInputSplit[ isplit.technology ].append({
		  'aId'   : a_pk,
		  'tId'   : isplit.technology.pk,
		  'id'    : isplit.pk,
		  'inp'   : isplit.inp_commodity.commodity.name,
		  'value' : isplit.fraction
		})

	TechOutputSplit = defaultdict( list )
	for osplit in Param_TechOutputSplit.objects.filter(
	  technology__in=technologies ):
		TechOutputSplit[ osplit.technology ].append({
		  'aId'   : a_pk,
		  'tId'   : osplit.technology.pk,
		  'id'    : osplit.pk,
		  'out'   : osplit.out_commodity.commodity.name,
		  'value' : osplit.fraction
		})

	# The frontend expects process information in the form of a matrix for each
	# Technology.  If a process does not have a value, it expects a null value.
	# So, if a process does not have a value for a parameter, the following two
	# loops put in the required None/null.  (i.e., need a dense matrix, not a
	# sparse representation)

	Vintages = defaultdict( list )
	MaxC = {}
	MinC = {}
	CapFacs = defaultdict( list )
	CI = defaultdict( dict )
	DR = defaultdict( dict )
	EC = defaultdict( dict )
	Lifetimes = defaultdict( dict )
	Loanlives = defaultdict( dict )
	for p in Process.objects.filter( technology__in=technologies ).order_by(
	  'vintage__vintage' ):
		t, v = p.technology, p.vintage.vintage
		Vintages[ t ].append( v )
		CI[ t ][ v ] = p.costinvest
		DR[ t ][ v ] = p.discountrate
		EC[ t ][ v ] = p.existingcapacity
		Lifetimes[ t ][ v ] = p.lifetime
		Loanlives[ t ][ v ] = p.loanlife

		MaxMinCapacities[ t ]   # create the entry if it doesn't exist

	for t in Vintages:
		ci, dr, ec, life, loan = CI[t], DR[t], EC[t], Lifetimes[t], Loanlives[t]
		vs, mmc, cf = Vintages[t], MaxMinCapacities[t], CapacityFactors[t]
		CI[ t ] = [ v in ci and ci[v] or None for v in vs ]
		DR[ t ] = [ v in dr and dr[v] or None for v in vs ]
		EC[ t ] = [ v in ec and ec[v] or None for v in vs ]
		Lifetimes[ t ] = [ v in life and life[v] or None for v in vs ]
		Loanlives[ t ] = [ v in loan and loan[v] or None for v in vs ]

		MaxC[ t ] = [ v in mmc and mmc[v]['maximum'] or None for v in horizon
		  if v >= p0 ]
		MinC[ t ] = [ v in mmc and mmc[v]['minimum'] or None for v in horizon
		  if v >= p0 ]

	data = [
	  {
	    'id'                 : t.pk,
	    'aId'                : analysis.pk,
	    'baseload'           : t.baseload,
	    'capacitytoactivity' : t.capacitytoactivity,
	    'description'        : str( t.description ),
	    'growthratelimit'    : t.ratelimit,
	    'growthrateseed'     : t.rateseed,
	    'lifetime'           : t.lifetime,
	    'loanlife'           : t.loanlife,
	    'name'               : t.name,
	    'storage'            : t.storage,
	    'capacityfactors'    : CapacityFactors[ t ],
	    'inputsplits'        : TechInputSplit[ t ],
	    'maxcapacities'      : MaxC[ t ],
	    'mincapacities'      : MinC[ t ],
	    'outputsplits'       : TechOutputSplit[ t ],
	    'vintages'           : Vintages[ t ],
	    'processes'          : {
	      'costinvest'         : CI[ t ],
	      'discountrate'       : DR[ t ],
	      'existingcapacity'   : EC[ t ],
	      'lifetime'           : Lifetimes[ t ],
	      'loanlife'           : Loanlives[ t ],
	    },
	  }

	  for t in technologies
	]

	return data


@never_cache
def technology_list ( req, analysis_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id )
	techs = Technology.objects.filter( analysis=analysis ).distinct()

	data = None
	if len( techs ):
		data = get_technology_info( analysis, techs )

	data = json.dumps( { 'data' : data } )
	res = HttpResponse( data, content_type='application/json' )
	res['Content-Length'] = len( data )

	set_cookie( req, res )
	return res


@never_cache
def technology_info ( req, analysis_id, technology_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id )
	tech = get_object_or_404( Technology, pk=technology_id )

	data = get_technology_info( analysis, [tech] )[0]

	data = json.dumps( data )
	res = HttpResponse( data, content_type='application/json' )
	res['Content-Length'] = len( data )

	set_cookie( req, res )
	return res


# All methods below this line should @require_login and @require_POST


## DB wide technologies #######################################################

@require_login
@require_POST
@never_cache
def technology_create ( req ):
	from forms import TechnologyForm

	status = 201  # 201 = Created
	msgs = {}

	tech = Technology( user=req.user )
	form = TechnologyForm( req.POST, instance=tech )
	if not form.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( form.errors )

	else:
		try:
			with transaction.atomic():
				form.save()

			msgs.update(
			  id                 = tech.pk,
			  username           = tech.user.username,
			  name               = tech.name,
			  capacitytoactivity = tech.capacitytoactivity,
			  description        = tech.description,
			)

		except IntegrityError as ie:
			status = 422  # to let Javascript know there was an error
			msg = 'Unable to create technology ({}).  It already exists!'
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
def technology_update ( req, technology_id ):
	from forms import TechnologyForm
	tech = get_object_or_404( Technology, pk=technology_id, user=req.user )

	status = 200
	msgs = {}

	data = req.POST
	if 'name' in data:
		# users may not rename technology.  They may, however, delete and
		# remake it
		data = req.POST.copy()
		del data['name']

	form = TechnologyForm( req.POST, instance=tech )
	if not form.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( form.errors )

	else:
		with transaction.atomic():
			form.save()

		msgs.update(
		  id                 = tech.pk,
		  username           = tech.user.username,
		  name               = tech.name,
		  capacitytoactivity = tech.capacitytoactivity,
		  description        = tech.description,
		)

	data = json.dumps( msgs )
	res = HttpResponse( data, content_type='application/json', status=status )
	res['Content-Length'] = len( data )

	set_cookie( req, res )
	return res


@require_login
@require_DELETE
@never_cache
def technology_remove ( req, technology_id ):
	get_object_or_404( Technology, pk=technology_id, user=req.user ).delete()

	status = 204  # "No Content"
	res = HttpResponse( '', status=status )
	set_cookie( req, res );

	return res


## AnalysisTechnology #########################################################

@require_login
@require_POST
@never_cache
def analysis_technology_update ( req, analysis_id, technology_id ):
	# first, ensure user owns the specified analysis
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	tech = get_object_or_404( Technology, pk=technology_id )

	status = 200
	msgs = {}

	form_kwargs = {'analysis' : analysis, 'technology' : tech}
	form = AnalysisTechnologyForm( req.POST, **form_kwargs )

	if not form.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( form.errors )

	else:
		try:
			with transaction.atomic():
				form.save()
			info = get_technology_info( analysis, [tech] )[0]
			for k in form.data:
				msgs[ k ] = info[ k ]

		except (IntegrityError, ValidationError) as e:
			status = 422  # to let Javascript know there was an error
			msg = 'Unable to update technology.  DB said: {}'
			msgs.update({ 'General Error' : msg.format( ie )})

	data = json.dumps( msgs )
	res = HttpResponse( data, content_type='application/json', status=status )
	res['Content-Length'] = len( data )

	set_cookie( req, res )
	return res


## CapacityFactor #############################################################

@require_login
@require_POST
@never_cache
def analysis_technology_capacityfactor_new ( req, analysis_id, technology_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	tech = get_object_or_404( Technology, pk=technology_id )

	# ensure technology exists in this analysis
	process = get_list_or_404( Process, analysis=analysis, technology=tech )

	status = 201  # Created
	msgs = {}

	cf = Param_CapacityFactorTech( technology=tech )
	form = CapacityFactorTechForm( req.POST, instance=cf, analysis=analysis )
	if not form.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( form.errors )
		for key in msgs.keys():  # .keys() -> complete list prior to iteration
			msgs['CapacityFactorTechNew_' + key] = msgs.pop( key )

	else:
		try:
			with transaction.atomic():
				form.save()

			msgs.update(
			  aId   = analysis.pk,
			  tId   = tech.pk,
			  sfId  = cf.timeslice.pk,
			  id    = cf.pk,
			  value = cf.value,
			)

		except IntegrityError as e:
			status = 422  # to let Javascript know there was an error
			msg = ('Unable to create capacity factor.  It already exists!')
			msgs.update({ 'General Error' : msg })
		except ValidationError as e:
			status = 422  # to let Javascript know there was an error
			msg = ('Unable to create capacity factor.  Database said: {}')
			msgs.update({ 'General Error' : msg.format( e ) })

	data = json.dumps( msgs )
	res = HttpResponse( data, content_type='application/json', status=status )
	res['Content-Length'] = len( data )

	set_cookie( req, res )
	return res


@require_login
@require_POST
@never_cache
def analysis_technology_capacityfactor_update (
  req, analysis_id, technology_id, cf_id
):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	tech = get_object_or_404( Technology, pk=technology_id )
	process = get_list_or_404( process, analysis=analysis, technology=tech )
	cf = get_object_or_404( Param_CapacityFactorTech, technology=tech, pk=cf_id )

	status = 200
	msgs = {}

	form = CapacityFactorTechForm( req.POST, instance=cf, analysis=analysis )
	if not form.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( form.errors )
		if 'value' in msgs.keys():
			msgs['CapacityFactorTech_{}'.format(cf.pk)] = msgs.pop( 'value' )

	else:
		try:
			with transaction.atomic():
				form.save()

			msgs.update( value=cf.value )
		except (IntegrityError, ValidationError) as e:
			status = 422  # to let Javascript know there was an error
			msg = ('Unable to complete update.  Database said: {}')
			msgs.update({ 'General Error' : msg.format( e ) })

	data = json.dumps( msgs )
	res = HttpResponse( data, content_type='application/json', status=status )
	res['Content-Length'] = len( data )

	set_cookie( req, res, analysis_id=analysis_id )
	return res


@require_login
@require_DELETE
@never_cache
def analysis_technology_capacityfactor_remove (
  req, analysis_id, technology_id, cf_id
):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	tech = get_object_or_404( Technology, pk=technology_id )
	process = get_list_or_404( Process, analysis=analysis, technology=tech )
	cf = get_object_or_404( Param_CapacityFactorTech, technology=tech, pk=cf_id )

	cf.delete()

	status = 204  # "No Content"
	res = HttpResponse( '', status=status )

	set_cookie( req, res );
	return res


## InputSplit #################################################################

@require_login
@require_POST
@never_cache
def analysis_technology_inputsplit_new ( req, analysis_id, technology_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	tech = get_object_or_404( Technology, pk=technology_id )

	status = 201  # Created
	msgs = {}

	tis = Param_TechInputSplit( technology=tech )
	form = TechInputSplitForm( req.POST, instance=tis, analysis=analysis )
	if not form.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( form.errors )
		for key in msgs.keys():
			msgs['InputSplitNew_' + key] = msgs.pop( key )

	else:
		try:
			with transaction.atomic():
				form.save()

			msgs.update(
			  aId   = analysis.pk,
			  tId   = tech.pk,
			  id    = tis.pk,
			  inp   = tis.inp_commodity.commodity.name,
			  value = tis.fraction,
			)

		except IntegrityError as e:
			status = 422  # to let Javascript know there was an error
			msg = ('Unable to create tech input split.  It already exists!')
			msgs.update({ 'General Error' : msg })
		except ValidationError as e:
			status = 422  # to let Javascript know there was an error
			msg = ('Unable to create tech input split.  Database said: {}')
			msgs.update({ 'General Error' : msg.format( e ) })

	data = json.dumps( msgs )
	res = HttpResponse( data, content_type='application/json', status=status )
	res['Content-Length'] = len( data )

	set_cookie( req, res )
	return res


@require_login
@require_POST
@never_cache
def analysis_technology_inputsplit_update (
  req, analysis_id, technology_id, tis_id
):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	tech = get_object_or_404( Technology, pk=technology_id )
	tis = get_object_or_404( Param_TechInputSplit, technology=tech, pk=tis_id )

	status = 200
	msgs = {}

	form = TechInputSplitForm( req.POST, instance=tis, analysis=analysis )
	if not form.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( form.errors )
		if 'value' in msgs.keys():
			msgs['InputSplit_{}'.format(tis.pk)] = msgs.pop( 'value' )

	else:
		try:
			with transaction.atomic():
				form.save()

			msgs.update( value=tis.fraction )
		except (IntegrityError, ValidationError) as e:
			status = 422  # to let Javascript know there was an error
			msg = ('Unable to complete update.  Database said: {}')
			msgs.update({ 'General Error' : msg.format( e ) })

	data = json.dumps( msgs )
	res = HttpResponse( data, content_type='application/json', status=status )
	res['Content-Length'] = len( data )

	set_cookie( req, res, analysis_id=analysis_id )
	return res


@require_login
@require_DELETE
@never_cache
def analysis_technology_inputsplit_remove (
  req, analysis_id, technology_id, tis_id
):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	tech = get_object_or_404( Technology, pk=technology_id )
	tis = get_object_or_404( Param_TechInputSplit, technology=tech, pk=tis_id )

	tis.delete()

	status = 204  # "No Content"
	res = HttpResponse( '', status=status )

	set_cookie( req, res );
	return res


## OutputSplit ################################################################

@require_login
@require_POST
@never_cache
def analysis_technology_outputsplit_new ( req, analysis_id, technology_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	tech = get_object_or_404( Technology, pk=technology_id )

	status = 201  # Created
	msgs = {}

	tos = Param_TechOutputSplit( technology=tech )
	form = TechOutputSplitForm( req.POST, instance=tos, analysis=analysis )
	if not form.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( form.errors )
		for key in msgs.keys():
			msgs['OutputSplitNew_' + key] = msgs.pop( key )

	else:
		try:
			with transaction.atomic():
				form.save()

			msgs.update(
			  aId   = analysis.pk,
			  tId   = tech.pk,
			  id    = tos.pk,
			  out   = tos.out_commodity.commodity.name,
			  value = tos.fraction,
			)

		except IntegrityError as e:
			status = 422  # to let Javascript know there was an error
			msg = ('Unable to create tech output split.  It already exists!')
			msgs.update({ 'General Error' : msg })
		except ValidationError as e:
			status = 422  # to let Javascript know there was an error
			msg = ('Unable to create tech output split.  Database said: {}')
			msgs.update({ 'General Error' : msg.format( e ) })

	data = json.dumps( msgs )
	res = HttpResponse( data, content_type='application/json', status=status )
	res['Content-Length'] = len( data )

	set_cookie( req, res )
	return res


@require_login
@require_POST
@never_cache
def analysis_technology_outputsplit_update (
  req, analysis_id, technology_id, tos_id
):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	tech = get_object_or_404( Technology, pk=technology_id )
	tos = get_object_or_404( Param_TechOutputSplit, technology=tech, pk=tos_id )

	status = 200
	msgs = {}

	form = TechOutputSplitForm( req.POST, instance=tos, analysis=analysis )
	if not form.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( form.errors )
		if 'value' in msgs.keys():
			msgs['OutputSplit_{}'.format(tos.pk)] = msgs.pop( 'value' )

	else:
		try:
			with transaction.atomic():
				form.save()

			msgs.update( value=tos.fraction )
		except (IntegrityError, ValidationError) as e:
			status = 422  # to let Javascript know there was an error
			msg = ('Unable to complete update.  Database said: {}')
			msgs.update({ 'General Error' : msg.format( e ) })

	data = json.dumps( msgs )
	res = HttpResponse( data, content_type='application/json', status=status )
	res['Content-Length'] = len( data )

	set_cookie( req, res, analysis_id=analysis_id )
	return res


@require_login
@require_DELETE
@never_cache
def analysis_technology_outputsplit_remove (
  req, analysis_id, technology_id, tos_id
):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	tech = get_object_or_404( Technology, pk=technology_id )
	tos = get_object_or_404( Param_TechOutputSplit, technology=tech, pk=tos_id )

	tos.delete()

	status = 204  # "No Content"
	res = HttpResponse( '', status=status )

	set_cookie( req, res );
	return res

