from collections import defaultdict

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import simplejson as json

from decorators.http import require_POST, require_DELETE
from decorators.auth import require_login

from models import (
  Analysis,
  Param_CostFixed,
  Param_CostVariable,
  Param_Efficiency,
  Param_EmissionActivity,
  Param_LifetimeTech,
  Param_LifetimeTechLoan,
  Process,
  Set_tech_baseload,
  Set_tech_storage,
)

from forms import (
	ProcessForm,
	CostForm, # handles both CostFixed and CostVariable
	EfficiencyForm,
	EmissionActivityForm,
)
from view_helpers import set_cookie
from views_technology import get_technology_info


def get_process_info ( processes ):
	techs = set(p.technology for p in processes)

	if not techs:
		return { 'data' : [] }

	analysis = processes[0].analysis

	def null ( ):
		return None

	Efficiencies = defaultdict( list )
	for e in Param_Efficiency.objects.filter( process__in=processes ):
		Efficiencies[ e.process ].append({
		  'aId'   : analysis.pk,
		  'pId'   : e.process.pk,
		  'id'    : e.pk,
		  'inp'   : e.inp_commodity.commodity.name,
		  'out'   : e.out_commodity.commodity.name,
		  'value' : e.value
		})

	EmissionActivities = defaultdict( list )
	for ea in Param_EmissionActivity.objects.filter(
	  efficiency__process__in=processes ):
		EmissionActivities[ ea.efficiency.process ].append({
		  'aId'       : analysis.pk,
		  'pId'       : ea.efficiency.process.pk,
		  'eId'       : ea.efficiency.pk,
		  'id'        : ea.pk,
		  'pollutant' : ea.emission.commodity.name,
		  'value'     : ea.value
		})

	CostFixed = defaultdict( list )
	for cf in Param_CostFixed.objects.filter( process__in=processes ):
		CostFixed[ cf.process ].append({
		  'aId'    : analysis.pk,
		  'pId'    : cf.process.pk,
		  'id'     : cf.pk,
		  'period' : cf.period.vintage,
		  'value'  : cf.value
		})

	CostVariable = defaultdict( list )
	for cv in Param_CostVariable.objects.filter( process__in=processes ):
		CostVariable[ cv.process ].append({
		  'aId'    : analysis.pk,
		  'pId'    : cv.process.pk,
		  'id'     : cv.pk,
		  'period' : cv.period.vintage,
		  'value'  : cv.value
		})

	process_characteristics = [{
	    'aId'                : analysis.pk, # needed for URL construction
	    'id'                 : p.pk,
	    'costinvest'         : p.costinvest,
	    'costsfixed'         : CostFixed[ p ],
	    'costsvariable'      : CostVariable[ p ],
	    'discountrate'       : p.discountrate,
	    'efficiencies'       : Efficiencies[ p ],
	    'emissionactivities' : EmissionActivities[ p ],
	    'existingcapacity'   : p.existingcapacity,
	    'lifetime'           : p.lifetime,
	    'loanlife'           : p.loanlife,
	    'vintage'            : p.vintage.vintage,
	    'tId'                : p.technology.pk,
	  }

	  for p in processes
	]

	return process_characteristics


def process_list ( req, analysis_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id )
	processes = Process.objects.filter( analysis=analysis )

	data = None
	if len( processes ):
		data = get_process_info( processes )

	data = json.dumps({ 'data' : data })
	res = HttpResponse( data, content_type='application/json' )
	res['Content-Length'] = len( data )

	set_cookie( req, res, analysis_id=analysis_id )
	return res

# Below here, every function should have two decorators: require_login and
# require_POST or require_DELETE.


## Process ####################################################################

@require_login
@require_POST
def process_new ( req, analysis_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )

	status = 201  # 201 = Created
	msgs = {}

	process = Process( analysis=analysis )
	form = ProcessForm( req.POST, instance=process )
	if not form.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( form.errors )

	else:
		try:
			form.save()
			msgs = get_process_info( [process] )[0]
			tech = process.technology
			msgs['technology'] = get_technology_info( analysis, [tech] )[0]

		except IntegrityError as ie:
			t = form.cleaned_data[ 'technology' ]
			v = form.cleaned_data[ 'vintage' ].vintage
			status = 422  # to let Javascript know there was an error
			msg = ('Unable to create new Process ({}, {}).  It already exists!')
			msgs.update({ 'General Error' : msg.format( t, v )})

	data = json.dumps( msgs )
	res = HttpResponse( data, content_type='application/json', status=status )
	res['Content-Length'] = len( data )

	set_cookie( req, res )
	return res


@require_login
@require_POST
def process_update ( req, analysis_id, process_id ):
	# first, ensure user owns the specified analysis
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	process = get_object_or_404( Process, pk=process_id, analysis=analysis )

	status = 200
	msgs = {}

	form = ProcessForm( req.POST, instance=process )

	if not form.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( form.errors )

	else:
		try:
			with transaction.commit_on_success():
				form.save()
			msgs = get_process_info( [process] )[0]

		except IntegrityError as ie:
			status = 422  # to let Javascript know there was an error
			msg = 'Unable to update process.  DB said: {}'
			msgs.update({ 'General Error' : msg.format( ie )})

	data = json.dumps( msgs )
	res = HttpResponse( data, content_type='application/json', status=status )
	res['Content-Length'] = len( data )

	set_cookie( req, res )
	return res


@require_login
@require_DELETE
def process_remove ( req, analysis_id, process_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	process = get_object_or_404( Process, pk=process_id, analysis=analysis )

	process.delete()

	status = 204  # "No Content"
	res = HttpResponse( '', status=status )
	set_cookie( req, res );

	return res


## CostFixed ##################################################################

@require_login
@require_POST
def process_costfixed_new ( req, analysis_id, process_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	process  = get_object_or_404( Process, pk=process_id, analysis=analysis )

	status = 201  # Created
	msgs = {}

	cf = Param_CostFixed( process=process )
	form = CostForm( req.POST, instance=cf )
	if not form.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( form.errors )
		for key in msgs.keys():
			msgs['CostFixedNew_' + key] = msgs.pop( key )

	else:
		try:
			with transaction.commit_on_success():
				form.save()

			msgs.update(
			  id     = cf.pk,
			  aId    = analysis.pk,
			  pId    = process.pk,
			  period = cf.period.vintage,
			  value  = cf.value,
			)

		except IntegrityError as e:
			status = 422  # to let Javascript know there was an error
			msg = ('Unable to create fixed cost.  It already exists!')
			msgs.update({ 'General Error' : msg })
		except ValidationError as e:
			status = 422  # to let Javascript know there was an error
			msg = ('Unable to create fixed cost.  Database said: {}')
			msgs.update({ 'General Error' : msg.format( e ) })

	data = json.dumps( msgs )
	res = HttpResponse( data, content_type='application/json', status=status )
	res['Content-Length'] = len( data )

	set_cookie( req, res )
	return res


@require_login
@require_POST
def process_costfixed_update ( req, analysis_id, process_id, costfixed_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	process  = get_object_or_404( Process, pk=process_id, analysis=analysis )
	cf = get_object_or_404( Param_CostFixed, process=process, pk=costfixed_id )

	status = 200
	msgs = {}

	form = CostForm( req.POST, instance=cf )
	if not form.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( form.errors )
		if 'value' in msgs.keys():
			msgs['CostFixed_{}'.format(cf.pk)] = msgs.pop( 'value' )

	else:
		try:
			with transaction.commit_on_success():
				form.save()

			msgs.update(
			  id     = cf.pk,
			  aId    = analysis.pk,
			  pId    = process.pk,
			  period = cf.period.vintage,
			  value  = cf.value,
			)
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
def process_costfixed_remove ( req, analysis_id, process_id, costfixed_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	process = get_object_or_404( Process, pk=process_id, analysis=analysis )
	cf = get_object_or_404( Param_CostFixed, process=process, pk=costfixed_id )

	cf.delete()

	status = 204  # "No Content"
	res = HttpResponse( '', status=status )

	set_cookie( req, res );
	return res


## CostVariable ###############################################################

@require_login
@require_POST
def process_costvariable_new ( req, analysis_id, process_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	process  = get_object_or_404( Process, pk=process_id, analysis=analysis )

	status = 201  # Created
	msgs = {}

	cv = Param_CostVariable( process=process )
	form = CostForm( req.POST, instance=cv )
	if not form.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( form.errors )
		for key in msgs.keys():
			msgs['CostVariableNew_' + key] = msgs.pop( key )

	else:
		try:
			with transaction.commit_on_success():
				form.save()

			msgs.update(
			  id     = cv.pk,
			  aId    = analysis.pk,
			  pId    = process.pk,
			  period = cv.period.vintage,
			  value  = cv.value,
			)

		except IntegrityError as e:
			status = 422  # to let Javascript know there was an error
			msg = ('Unable to create variable cost.  It already exists!')
			msgs.update({ 'General Error' : msg })
		except ValidationError as e:
			status = 422  # to let Javascript know there was an error
			msg = ('Unable to create variable cost.  Database said: {}')
			msgs.update({ 'General Error' : msg.format( e ) })

	data = json.dumps( msgs )
	res = HttpResponse( data, content_type='application/json', status=status )
	res['Content-Length'] = len( data )

	set_cookie( req, res )
	return res


@require_login
@require_POST
def process_costvariable_update (
  req, analysis_id, process_id, costvariable_id
):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	process  = get_object_or_404( Process, pk=process_id, analysis=analysis )
	cv = get_object_or_404( Param_CostVariable,
	  process=process, pk=costvariable_id )

	status = 200
	msgs = {}

	form = CostForm( req.POST, instance=cv )
	if not form.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( form.errors )
		if 'value' in msgs.keys():
			msgs['CostVariable_{}'.format(cv.pk)] = msgs.pop( 'value' )

	else:
		try:
			with transaction.commit_on_success():
				form.save()

			msgs.update(
			  id     = cv.pk,
			  aId    = analysis.pk,
			  pId    = process.pk,
			  period = cv.period.vintage,
			  value  = cv.value,
			)
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
def process_costvariable_remove (
  req, analysis_id, process_id, costvariable_id
):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	process  = get_object_or_404( Process, pk=process_id, analysis=analysis )
	cv = get_object_or_404( Param_CostVariable,
	  process=process, pk=costvariable_id )

	cv.delete()

	status = 204  # "No Content"
	res = HttpResponse( '', status=status )

	set_cookie( req, res );
	return res


## Efficiency #################################################################

@require_login
@require_POST
def process_efficiency_new ( req, analysis_id, process_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	process  = get_object_or_404( Process, pk=process_id, analysis=analysis )

	status = 201  # Created
	msgs = {}

	eff = Param_Efficiency( process=process )
	form = EfficiencyForm( req.POST, instance=eff )
	if not form.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( form.errors )
		for key in msgs.keys():
			msgs['EfficiencyNew_' + key] = msgs.pop( key )

	else:
		try:
			with transaction.commit_on_success():
				form.save()

			msgs.update(
			  id    = eff.pk,
			  aId   = analysis.pk,
			  pId   = process.pk,
			  inp   = eff.inp_commodity.commodity.name,
			  out   = eff.out_commodity.commodity.name,
			  value = eff.value,
			)

		except (IntegrityError, ValidationError) as e:
			status = 422  # to let Javascript know there was an error
			i = form.cleaned_data['inp'].commodity.name
			o = form.cleaned_data['out'].commodity.name
			msg = 'Unable to create efficiency {} &rarr; {}.  Database said: {}'
			msgs.update({ 'General Error' : msg.format( i, o, e ) })

	data = json.dumps( msgs )
	res = HttpResponse( data, content_type='application/json', status=status )
	res['Content-Length'] = len( data )

	set_cookie( req, res )
	return res


@require_login
@require_POST
def process_efficiency_update ( req, analysis_id, process_id, efficiency_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	process  = get_object_or_404( Process, pk=process_id, analysis=analysis )
	eff = get_object_or_404( Param_Efficiency,
	  pk=efficiency_id, process=process )

	status = 200
	msgs = {}

	form = EfficiencyForm( req.POST, instance=eff )
	if not form.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( form.errors )
		if 'value' in msgs.keys():
			msgs['Efficiency_{}'.format(eff.pk)] = msgs.pop( 'value' )

	else:
		try:
			with transaction.commit_on_success():
				form.save()

			msgs.update(
			  id    = eff.pk,
			  aId   = analysis.pk,
			  pId   = process.pk,
			  inp   = eff.inp_commodity.commodity.name,
			  out   = eff.out_commodity.commodity.name,
			  value = eff.value,
			)
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
def process_efficiency_remove ( req, analysis_id, process_id, efficiency_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	process  = get_object_or_404( Process, pk=process_id, analysis=analysis )
	eff      = get_object_or_404( Param_Efficiency,
	  pk=efficiency_id, process=process )

	eff.delete()

	status = 204  # "No Content"
	res = HttpResponse( '', status=status )

	set_cookie( req, res );
	return res


## EmissionActivity ###########################################################

@require_login
@require_POST
def process_emissionactivity_new ( req, analysis_id, process_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	process  = get_object_or_404( Process, pk=process_id, analysis=analysis )

	status = 201  # Created
	msgs = {}

	ema = Param_EmissionActivity()
	form = EmissionActivityForm( req.POST, instance=ema, process=process )
	if not form.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( form.errors )
		for key in msgs.keys():
			msgs['EmissionActivityNew_' + key] = msgs.pop( key )

	else:
		try:
			with transaction.commit_on_success():
				form.save()

			msgs.update(
			  id    = ema.pk,
			  aId   = analysis.pk,
			  pId   = process.pk,
			  eId   = ema.efficiency.pk,
			  pollutant = ema.emission.commodity.name,
			  value = ema.value,
			)

		except (IntegrityError, ValidationError) as e:
			status = 422  # to let Javascript know there was an error
			p = form.cleaned_data['pol'].commodity
			eff = form.cleaned_data['eff']
			i, o = eff.inp_commodity.commodity, eff.out_commodity.commodity
			msg = ('Unable to create emission activity {} (for {} &rarr; {}).  '
			  'Database said: {}')
			msgs.update({ 'General Error' : msg.format( p, i, o, e ) })

	data = json.dumps( msgs )
	res = HttpResponse( data, content_type='application/json', status=status )
	res['Content-Length'] = len( data )

	set_cookie( req, res )
	return res

@require_login
@require_POST
def process_emissionactivity_update (
  req, analysis_id, efficiency_id, emissionactivity_id
):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	eff = get_object_or_404( Param_Efficiency,
	  pk=efficiency_id, process__analysis=analysis )
	ema = get_object_or_404( Param_EmissionActivity,
	  pk=emissionactivity_id, efficiency=eff )

	status = 200
	msgs = {}

	form = EmissionActivityForm( req.POST, instance=ema, process=eff.process )
	if not form.is_valid():
		status = 422  # to let Javascript know there was an error
		msgs.update( form.errors )
		if 'value' in msgs.keys():
			msgs['EmissionActivity_{}'.format(ema.pk)] = msgs.pop( 'value' )

	else:
		try:
			with transaction.commit_on_success():
				form.save()

			msgs.update(
			  id    = ema.pk,
			  aId   = analysis.pk,
			  pId   = eff.process.pk,
			  eId   = ema.efficiency.pk,
			  pollutant = ema.emission.commodity.name,
			  value = ema.value,
			)
		except (IntegrityError, ValidationError) as e:
			status = 422  # to let Javascript know there was an error
			p = form.cleaned_data['pol'].commodity
			i, o = eff.inp_commodity.commodity, eff.out_commodity.commodity
			msg = ('Unable to update emission activity {} (for {} &rarr; {}).  '
			  'Database said: {}')
			msgs.update({ 'General Error' : msg.format( p, i, o, e ) })

	data = json.dumps( msgs )
	res = HttpResponse( data, content_type='application/json', status=status )
	res['Content-Length'] = len( data )

	set_cookie( req, res )
	return res


@require_login
@require_DELETE
def process_emissionactivity_remove (
  req, analysis_id, efficiency_id, emissionactivity_id
):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	eff = get_object_or_404( Param_Efficiency,
	  pk=efficiency_id, process__analysis=analysis )
	ema = get_object_or_404( Param_EmissionActivity,
	  pk=emissionactivity_id, efficiency=eff )

	ema.delete()

	status = 204  # "No Content"
	res = HttpResponse( '', status=status )

	set_cookie( req, res );
	return res

