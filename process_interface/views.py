from collections import defaultdict
from operator import itemgetter as i_get

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson as json
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.http import require_POST

from settings import JQUERYCD

from models import (
	Analysis,
	Commodity,
	Param_CapacityToActivity,
	Param_CostFixed,
	Param_CostInvest,
	Param_CostVariable,
	Param_DiscountRate,
	Param_Efficiency,
	Param_EmissionActivity,
	Param_ExistingCapacity,
	Param_GrowthRateMax,
	Param_GrowthRateSeed,
	Param_TechInputSplit,
	Param_TechOutputSplit,
	Process,
	Set_commodity_emission,
	Set_commodity_physical,
	Set_tech_baseload,
	Set_tech_storage,
	Vintage,
)

# Create your views here.
from IPython import embed as II


def home ( req ):
	return render_to_response('process_interface/home.html')


def view ( req ):
	c = {'JQUERYCD': JQUERYCD}
	c.update(csrf(req))
	c.update( username='' )
	if req.user.is_authenticated():
		c.update( username=req.user.username )

	return render_to_response( 'process_interface/view.html', c )


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


def analyses ( req, username ):
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

	analysis_information = {
	  'id'                   : analysis.pk,
	  'username'             : analysis.user.username,
	  'name'                 : analysis.name,
	  'description'          : analysis.description,
	  'period_0'             : analysis.period_0,
	  'global_discount_rate' : analysis.global_discount_rate,
	}

	data = json.dumps( analysis_information )
	response = HttpResponse(
	  data,
	  content_type='application/json'
	)
	response['Content-Length'] = len( data )
	return response


def process_list ( req, analysis_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id )
	processes = [
	  (p.id, p.technology.name, p.vintage.vintage)

	  for p in Process.objects.filter( analysis=analysis )
	]

	data = json.dumps( processes )
	response = HttpResponse(
	  data,
	  content_type='application/json'
	)
	response['Content-Length'] = len( data )
	return response



def process_info ( req, analysis_id, process_ids ):
	# TODO: wrap DB access in a transaction, for robustness

	analysis = get_object_or_404( Analysis, pk=analysis_id )
	process_ids = process_ids.split(',')
	processes = set(Process.objects.filter(
	  analysis=analysis,
	  pk__in=process_ids
	))

	# Collect the actual processes that the DB holds.  This /should/ be the
	# same as what was sent, but for security or ACID, don't assume so.
	process_ids = [ p.pk for p in processes ]
	techs = set(p.technology for p in processes)

	def null ( ):
		return None

	BaseloadTechs = set( bt.technology
	  for bt in Set_tech_baseload.objects.filter( analysis=analysis )
	)
	StorageTechs = set(st.technology
	  for st in Set_tech_storage.objects.filter( analysis=analysis )
	)
	ExistingCapacities = defaultdict( null )
	ExistingCapacities.update({ ec.process: ec.value
	  for ec in Param_ExistingCapacity.objects.filter( process__in=processes )
	})

	Efficiencies = defaultdict( dict )
	for e in Param_Efficiency.objects.filter( process__in=processes ):
		Efficiencies[ e.process ][ e.pk ] = (
		  unicode(e.inp_commodity.commodity),
		  unicode(e.out_commodity),
		  e.value
		)
	Efficiencies = defaultdict( null, Efficiencies )

	EmissionActivities = defaultdict( dict )
	for ea in Param_EmissionActivity.objects.filter(
	  efficiency__process__in=processes ):
		EmissionActivities[ ea.efficiency.process ][ ea.pk ] = (
		  unicode(ea.emission.commodity),
		  unicode(ea.efficiency.inp_commodity.commodity),
		  unicode(ea.efficiency.out_commodity),
		  ea.value
		)
	EmissionActivities = defaultdict( null, EmissionActivities )

	CostFixed = defaultdict( dict )
	for cf in Param_CostFixed.objects.filter( process__in=processes ):
		CostFixed[ cf.process ][ cf.pk ] = ( cf.period.vintage, cf.value )
	CostFixed = defaultdict( null, CostFixed )

	CostVariable = defaultdict( dict )
	for cv in Param_CostVariable.objects.filter( process__in=processes ):
		CostVariable[ cv.process ][ cv.pk ] = ( cv.period.vintage, cv.value )
	CostVariable = defaultdict( null, CostVariable )

	CostInvest = defaultdict( null )
	CostInvest.update({ ci.process : ci.value
	  for ci in Param_CostInvest.objects.filter( process__in=processes )
	})

	DiscountRate = defaultdict( null )
	DiscountRate.update({ dr.process : dr.value
	  for dr in Param_DiscountRate.objects.filter( process__in=processes )
	})

	process_characteristics = [
	  {
	    'ProcessId'         : p.pk,
	    'Technology'        : unicode( p.technology ),
	    'Vintage'           : p.vintage.vintage,
	    'ExistingCapacity'  : ExistingCapacities[ p ],
	    'Baseload'          : p.technology in BaseloadTechs,
	    'Storage'           : p.technology in StorageTechs,
	    'Efficiencies'      : Efficiencies[ p ],
	    'EmissionActivity'  : EmissionActivities[ p ],
	    'CostFixed'         : CostFixed[ p ],
	    'CostInvest'        : CostInvest[ p ],
	    'CostVariable'      : CostVariable[ p ],
	    'DiscountRate'      : DiscountRate[ p ],
	  }

	  for p in processes
	]

	data = json.dumps( process_characteristics )
	response = HttpResponse(
	  data,
	  content_type='application/json'
	)
	response['Content-Length'] = len( data )
	return response


def technology_info ( req, analysis_id, process_id ):
	# TODO: wrap DB access in a transaction, for robustness

	analysis = get_object_or_404( Analysis, pk=analysis_id )
	process = get_object_or_404( Process, pk=process_id, analysis=analysis )

	def null ( ):
		return None

	# Collect the actual processes that the DB holds.  This /should/ be the
	# same as what was sent, but for security or ACID, don't assume so.
	tech = process.technology

	is_baseload = Set_tech_baseload.objects.filter(
	  analysis=analysis, technology=tech ).exists()

	is_storage = Set_tech_storage.objects.filter(
	  analysis=analysis, technology=tech ).exists()

	CapacityToActivity = defaultdict( null )
	CapacityToActivity.update({
	  c2a.technology : c2a.value

	  for c2a in Param_CapacityToActivity.objects.filter(
	    analysis=analysis,
	    technology=tech
	)})

	GrowthRateMax = defaultdict( null )
	GrowthRateMax.update({ grm.process : grm.value
	  for grm in Param_GrowthRateMax.objects.filter( technology=tech )
	})

	GrowthRateSeed = defaultdict( null )
	GrowthRateSeed.update({ grs.process : grs.value
	  for grs in Param_GrowthRateSeed.objects.filter(
	    growth_max__technology=tech
	)})

	TechInputSplit = defaultdict( list )
	for isplit in Param_TechInputSplit.objects.filter( technology=tech ):
		TechInputSplit[ isplit.technology ].append(
		  ( unicode(isplit.inp_commodity.commodity),
		    unicode(isplit.out_commodity),
		    isplit.fraction
		  )
		)
	TechInputSplit = defaultdict( null, TechInputSplit )

	TechOutputSplit = defaultdict( list )
	for osplit in Param_TechOutputSplit.objects.filter( technology=tech ):
		TechOutputSplit[ osplit.technology ].append(
		  ( unicode(osplit.inp_commodity),
		    unicode(osplit.out_commodity),
		    osplit.fraction
		  )
		)
	TechOutputSplit = defaultdict( null, TechOutputSplit )

	# not necessary, but I'm CDO (Like OCD, but alphabetized)
	for t in TechInputSplit:  TechInputSplit[ t ].sort()
	for t in TechOutputSplit: TechOutputSplit[ t ].sort()

	technology_characteristics = {
	  'TechnologyId'       : tech.pk,
	  'Name'               : tech.name,
	  'Description'        : unicode( tech.description ),
	  'Baseload'           : is_baseload,
	  'Storage'            : is_storage,
	  'CapacityToActivity' : CapacityToActivity[ tech ],
	  'GrowthRateMax'      : GrowthRateMax[ tech ],
	  'GrowthRateSeed'     : GrowthRateSeed[ tech ],
	  'TechInputSplit'     : TechInputSplit[ tech ],
	  'TechOutputSplit'    : TechOutputSplit[ tech ]
	}

	data = json.dumps( technology_characteristics )
	response = HttpResponse(
	  data,
	  content_type='application/json'
	)
	response['Content-Length'] = len( data )
	return response


@login_required
@require_POST
def update_analysis_process ( req, analysis_id, process_id ):
	# first, ensure user owns the specified analysis
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	process = get_object_or_404( Process, pk=process_id, analysis=analysis )

	status_code = None

	status = u'fail'  # assume failure until success
	try:
		parameter = req.POST['parameter']

		if 'ExistingCapacity' == parameter:
			value = req.POST['value']
			with transaction.commit_on_success():
				obj, created = Param_ExistingCapacity.objects.get_or_create(
				  process=process, defaults={'value': value} )
				obj.full_clean()
				if not created:
					obj.value = value
					obj.full_clean()
					obj.save()

				status = obj.pk

		elif 'DiscountRate' == parameter:
			value = req.POST['value']
			with transaction.commit_on_success():
				obj, created = Param_DiscountRate.objects.get_or_create(
				  process=process, defaults={'value': value} )
				obj.full_clean()
				if not created:
					obj.value = value
					obj.full_clean()
					obj.save()

				status = obj.pk

		elif 'Efficiencies' == parameter:
			rowid    = req.POST['rowid']
			inp_name = req.POST['Input']
			out_name = req.POST['Output']
			value    = req.POST['Value']

			try:
				inp = Set_commodity_physical.objects.get(
				  analysis=analysis, commodity__name=inp_name )
			except ObjectDoesNotExist as e:
				msg = "Input '{}' does not exist in this analysis ({})."
				raise ValidationError( msg.format( inp_name, analysis.name ))

			try:
				out = Commodity.objects.get( name=out_name )
			except ObjectDoesNotExist as e:
				msg = "Output commodity '{}' does not exist in database."
				raise ValidationError( msg.format( out_name ))

			with transaction.commit_on_success():
				if 'NewRow' == rowid:
					obj = Param_Efficiency()
				else:
					obj = Param_Efficiency.objects.get( pk=rowid )

				obj.inp_commodity = inp
				obj.process       = process
				obj.out_commodity = out
				obj.value         = value
				obj.full_clean()
				obj.save()

				status = obj.pk

		elif 'EmissionActivity' == parameter:
			pol_name = req.POST['Pollutant']
			inp_name = req.POST['Input']
			out_name = req.POST['Output']
			value    = req.POST['Value']

			try:
				pol = Set_commodity_emission.objects.get(
				  analysis=analysis, commodity__name=pol_name )
			except ObjectDoesNotExist as e:
				msg = "Pollutant '{}' does not exist in this analysis ({})."
				raise ValidationError( msg.format( pol_name, analysis.name ))

			try:
				eff = Param_Efficiency.objects.get(
				  inp_commodity__commodity__name=inp_name,
				  process=process,
				  out_commodity__name=out_name
				)
			except ObjectDoesNotExist as e:
				raise ValidationError( 'No matching efficiency.' )

			with transaction.commit_on_success():
				obj, created = Param_EmissionActivity.objects.get_or_create(
				  emission=pol, efficiency=eff, defaults={'value': value} )
				obj.full_clean()
				if not created:
					obj.value = value
					obj.full_clean()
					obj.save()

				status = obj.pk

		elif 'CostFixed' == parameter:
			year  = req.POST['Period']
			value = req.POST['Value']
			try:
				period = Vintage.objects.get( analysis=analysis, vintage=year )
			except ObjectDoesNotExist as e:
				msg = "Period '{}' does not exist in this analysis ({})."
				raise ValidationError( msg.format( year, analysis.name ))

			with transaction.commit_on_success():
				obj, created = Param_CostFixed.objects.get_or_create(
				  period=period,
				  process=process,
				  defaults={'value': value}
				)
				obj.full_clean()
				if not created:
					obj.value = value
					obj.full_clean()
					obj.save()

				status = obj.pk

		elif 'CostVariable' == parameter:
			year  = req.POST['Period']
			value = req.POST['Value']
			try:
				period = Vintage.objects.get( analysis=analysis, vintage=year )
			except ObjectDoesNotExist as e:
				msg = "Period '{}' does not exist in this analysis ({})."
				raise ValidationError( msg.format( year, analysis.name ))

			with transaction.commit_on_success():
				obj, created = Param_CostVariable.objects.get_or_create(
				  period=period,
				  process=process,
				  defaults={'value': value}
				)
				obj.full_clean()
				if not created:
					obj.value = value
					obj.full_clean()
					obj.save()

				status = obj.pk


	except ValidationError as e:
		status_code = 422 # unprocessable entity
		status = unicode( e.messages.pop() )
	except ValueError as e:
		status_code = 422 # unprocessable entity
		status = unicode( e.message )
	except MultiValueDictKeyError as e:
		status_code = 400 # bad request
		status = 'Malformed request: You may need to reload the page.'
		from pprint import pformat
		print pformat( req.POST )

	response = HttpResponse(
		json.dumps( status ),
		content_type='application/json'
	)

	if status_code:
		response.status_code = status_code

	return response


@login_required
@require_POST
def remove_analysis_process_datum ( req, analysis_id, process_id, parameter ):
	# first, ensure user owns the specified analysis
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	process = get_object_or_404( Process, pk=process_id, analysis=analysis )

	status = 'Removed Successfully'
	status_code = None
	try:
		if 'rowid' not in req.POST:
			raise ValueError( 'No row specified to delete!' )
		pk = req.POST['rowid']  # process=process assures that user is owner

		if 'Efficiencies' == parameter:
			obj = Param_Efficiency.objects.get( pk=pk, process=process )
		elif 'EmissionActivity' == parameter:
			obj = Param_EmissionActivity.objects.get(
			  pk=pk, efficiency__process=process )
		elif 'CostFixed' == parameter:
			obj = Param_CostFixed.objects.get( pk=pk, process=process )
		elif 'CostVariable' == parameter:
			obj = Param_CostVariable.objects.get( pk=pk, process=process )

		obj.delete()

	except ObjectDoesNotExist as e:
		status_code = 422 # unprocessable entity
		status = 'Content not there'
	except ValueError as e:
		status_code = 422 # unprocessable entity
		status = e.message

	response = HttpResponse(
	  json.dumps( status ),
	  content_type='application/json'
	)

	if status_code:
		response.status_code = status_code

	return response




