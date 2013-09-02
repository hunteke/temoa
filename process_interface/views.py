from collections import defaultdict
from operator import itemgetter as i_get
import re

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import transaction
from django.db.models import Max
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
  Param_CostVariable,
  Param_Efficiency,
  Param_EmissionActivity,
  Param_GrowthRateMax,
  Param_GrowthRateSeed,
  Param_LifetimeTech,
  Param_LifetimeTechLoan,
  Param_TechInputSplit,
  Param_TechOutputSplit,
  Process,
  Set_commodity_emission,
  Set_commodity_physical,
  Set_commodity_output,
  Set_tech_baseload,
  Set_tech_storage,
  Technology,
  Vintage,
)

from forms import ProcessForm, getFormCostRows, getFormEfficiencyRows

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


def test_view ( req ):
	from django.shortcuts import redirect
	print req.POST
	return redirect('http://localhost:8000/analysis/1/process_info/3,4?json')

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


def get_process_info ( processes ):
	techs = set(p.technology for p in processes)

	analysis = processes[0].analysis

	def null ( ):
		return None

	BaseloadTechs = set( bt.technology
	  for bt in Set_tech_baseload.objects.filter( analysis=analysis )
	)
	StorageTechs = set( st.technology
	  for st in Set_tech_storage.objects.filter( analysis=analysis )
	)

	Efficiencies = defaultdict( dict )
	for e in Param_Efficiency.objects.filter( process__in=processes ):
		Efficiencies[ e.process ][ e.pk ] = (
		  unicode(e.inp_commodity.commodity),
		  unicode(e.out_commodity.commodity),
		  e.value
		)
	Efficiencies = defaultdict( null, Efficiencies )

	EmissionActivities = defaultdict( dict )
	for ea in Param_EmissionActivity.objects.filter(
	  efficiency__process__in=processes ):
		EmissionActivities[ ea.efficiency.process ][ ea.pk ] = (
		  unicode(ea.emission.commodity),
		  unicode(ea.efficiency.inp_commodity.commodity),
		  unicode(ea.efficiency.out_commodity.commodity),
		  ea.value
		)
	EmissionActivities = defaultdict( null, EmissionActivities )

	LifetimeTech = defaultdict( null )
	LifetimeTech.update({ lt.technology: lt.value
	  for lt in Param_LifetimeTech.objects.filter(
	    analysis=analysis,
	    technology__in=techs )
	})

	LifetimeTechLoan = defaultdict( null )
	LifetimeTechLoan.update({ ltl.technology: ltl.value
	  for ltl in Param_LifetimeTechLoan.objects.filter(
	    analysis=analysis,
	    technology__in=techs )
	})

	process_characteristics = [
	  {
	    'ProcessId'           : p.pk,
	    'Baseload'            : p.technology in BaseloadTechs,
	    'CostInvest'          : p.costinvest,
	    'DiscountRate'        : p.discountrate,
	    'Efficiencies'        : Efficiencies[ p ],
	    'EmissionActivity'    : EmissionActivities[ p ],
	    'ExistingCapacity'    : p.existingcapacity,
	    'GlobalDiscountRate'  : analysis.global_discount_rate,
	    'LifetimeProcess'     : p.lifetime,
	    'LifetimeProcessLoan' : p.loanlife,
	    'LifetimeTech'        : LifetimeTech[ p.technology ],
	    'LifetimeTechLoan'    : LifetimeTechLoan[ p.technology ],
	    'Storage'             : p.technology in StorageTechs,
	    'Technology'          : unicode( p.technology ),
	    'Vintage'             : p.vintage.vintage,
	  }

	  for p in processes
	]

	return process_characteristics



def process_info ( req, analysis_id, process_ids ):
	# TODO: wrap DB access in a transaction, for robustness

	analysis = get_object_or_404( Analysis, pk=analysis_id )
	process_ids = process_ids.split(',')
	processes = Process.objects.filter(
	  analysis=analysis,
	  pk__in=process_ids
	).distinct().order_by('technology__name', 'vintage__vintage').select_related()

	process_characteristics = get_process_info( processes )
	procs = {p.pk : p for p in processes}

	if 'json' in req.GET:
		data = json.dumps( process_characteristics )
		response = HttpResponse(
		  data,
		  content_type='application/json'
		)
		response['Content-Length'] = len( data )
		return response
	else:
		c = {}

		for pc in process_characteristics:
			p = procs[ pc['ProcessId'] ]
			kwargs = {
			  'prefix'               : pc['ProcessId'],
			  'CostFixedRows'        : getFormCostRows( 'fixed', p ),
			  'CostVariableRows'     : getFormCostRows( 'variable', p ),
			  'EfficiencyRows'       : getFormEfficiencyRows( pc['Efficiencies'] ),
			  'EmissionActivityRows' : (),
			}

			pc['form'] = ProcessForm( p, **kwargs )  # process form

		c.update(analysis=analysis)
		c.update({'process_characteristics': process_characteristics})
		c.update( csrf(req) )
		c.update( username='' )
		if req.user.is_authenticated():
			c.update( username=req.user.username )

		return render_to_response( 'process_interface/process_form.html', c )



@login_required
@require_POST
def update_analysis_process ( req, analysis_id, process_id ):
	# first, ensure user owns the specified analysis
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	process = get_object_or_404( Process, pk=process_id, analysis=analysis )

	c = {}
	c.update(analysis=analysis)
	c.update( csrf(req) )
	c.update( username=req.user.username )

	process_characteristics = get_process_info( [process] )
	pc = process_characteristics[0]

	kwargs = {
	  'prefix'               : process_id,
	  'CostFixedRows'        : getFormCostRows( 'fixed', process ),
	  'CostVariableRows'     : getFormCostRows( 'variable', process ),
	  'EfficiencyRows'       : getFormEfficiencyRows( pc['Efficiencies'] ),
	  'EmissionActivityRows' : (),
	}
	pform = ProcessForm( process, req.POST, **kwargs )

	if pform.is_valid():
		cleaned = pform.cleaned_data
		params = {
		  'variable'   : Param_CostVariable,
		  'fixed'      : Param_CostFixed,
		  'efficiency' : Param_Efficiency,
		}

		with transaction.commit_on_success():
			# 1. Update the directly attached process parameters
			process.update_with_data( cleaned )

			# 2. Update the row based parameters (i.e., could have more than 1)
			cv_re = r'^cost(fixed|variable)_(\d+|None)_(period|value)$'
			cv_re = re.compile( cv_re )
			eff_re = r'^(efficiency)_(\d+|None)_(input|output|value)$'
			eff_re = re.compile( eff_re )

			costkeys = set()
			effkeys = set()
			for key in cleaned:
				m = cv_re.match( key )
				if m:
					var, per, action = m.groups()
					per = eval( per )  # safe because of regex
					costkeys.add( (var, per) )
					continue

				m = eff_re.match( key )
				if m:
					var, epk, action = m.groups()
					epk = eval( epk )  # safe because of regex
					effkeys.add( (var, epk) )
					continue

			# Add/Update the CostVariable and CostFixed parameters
			for var, per in costkeys:
				period_key = 'cost{}_{}_period'.format( var, per )
				value_key  = 'cost{}_{}_value'.format( var, per )

				if not per:
					per = cleaned.get( period_key, None )

				if per:
					data = {
					  'analysis' : analysis,
					  'period'   : per,
					  'process'  : process,
					  'value'    : cleaned.get( value_key, None ),
					}
					params[ var ].update_with_data( **data )

			# Add/Update the Efficiency parameter
			for var, epk in effkeys:
				inp_key = 'efficiency_{}_input'.format( epk )
				out_key = 'efficiency_{}_output'.format( epk )
				val_key = 'efficiency_{}_value'.format( epk )

				inp = out = None
				if not epk:
					# request for a new efficiency
					inp = cleaned.get( inp_key, None )
					out = cleaned.get( out_key, None )
					if not (inp and out):
						continue

				if (inp is not None) or (epk is not None):
					# request to update or add a new efficiency
					data = {
					  'analysis'      : analysis,
					  'efficiency_pk' : epk,
					  'inp_commodity' : inp,
					  'process'       : process,
					  'out_commodity' : out,
					  'value'         : cleaned.get( val_key, None )
					}
					params[ var ].update_with_data( **data )

		return process_info( req, analysis.pk, str(process.pk) )
	else:
		pc['form'] = pform

		c.update({'process_characteristics': process_characteristics})

		return render_to_response( 'process_interface/process_form.html', c )



def technology_info ( req, analysis_id, process_ids ):
	# TODO: wrap DB access in a transaction, for robustness

	analysis = get_object_or_404( Analysis, pk=analysis_id )
	process_ids = process_ids.split(',')
	techs = set(p.technology
	  for p in Process.objects.filter(
	    analysis=analysis,
	    pk__in=process_ids
	))

	def null ( ):
		return None

	BaseloadTechs = set( bt.technology
	  for bt in Set_tech_baseload.objects.filter(
	    analysis=analysis,
	    technology__in=techs
	))

	StorageTechs = set( st.technology
	  for st in Set_tech_storage.objects.filter(
	    analysis=analysis,
	    technology__in=techs
	))

	CapacityToActivity = defaultdict( null )
	CapacityToActivity.update({
	  c2a.technology : c2a.value

	  for c2a in Param_CapacityToActivity.objects.filter(
	    analysis=analysis,
	    technology__in=techs
	)})

	grm_objects = Param_GrowthRateMax.objects.filter(
	  analysis=analysis,
	  technology__in=techs
	)

	GrowthRateMax = defaultdict( null )
	GrowthRateMax.update({ grm.technology : grm.value for grm in grm_objects})

	GrowthRateSeed = defaultdict( null )
	GrowthRateSeed.update({ grs.growth_max.technology : grs.value
	  for grs in Param_GrowthRateSeed.objects.filter(
	    growth_max__in=grm_objects
	)})

	LifetimeTech = defaultdict( null )
	LifetimeTech.update({ lt.technology: lt.value
	  for lt in Param_LifetimeTech.objects.filter(
	    analysis=analysis,
	    technology__in=techs )
	})

	LifetimeTechLoan = defaultdict( null )
	LifetimeTechLoan.update({ ltl.technology: ltl.value
	  for ltl in Param_LifetimeTechLoan.objects.filter(
	    analysis=analysis,
	    technology__in=techs )
	})

	TechInputSplit = defaultdict( dict )
	for isplit in Param_TechInputSplit.objects.filter(
	  inp_commodity__analysis=analysis,
	  technology__in=techs
	):
		TechInputSplit[ isplit.technology ][ isplit.pk ] = (
		  unicode(isplit.inp_commodity.commodity),
		  isplit.fraction
		)
	TechInputSplit = defaultdict( null, TechInputSplit )

	TechOutputSplit = defaultdict( dict )
	for osplit in Param_TechOutputSplit.objects.filter(
	  out_commodity__analysis=analysis,
	  technology__in=techs
	):
		TechOutputSplit[ osplit.technology ][ osplit.pk ] = (
		  unicode(osplit.out_commodity.commodity),
		  osplit.fraction
		)
	TechOutputSplit = defaultdict( null, TechOutputSplit )

	technology_characteristics = [
	  {
	    'TechnologyId'       : t.pk,
	    'Baseload'           : t in BaseloadTechs,
	    'CapacityToActivity' : CapacityToActivity[ t ],
	    'Description'        : unicode( t.description ),
	    'GrowthRateMax'      : GrowthRateMax[ t ],
	    'GrowthRateSeed'     : GrowthRateSeed[ t ],
	    'LifetimeTech'       : LifetimeTech[ t ],
	    'LifetimeTechLoan'   : LifetimeTechLoan[ t ],
	    'Name'               : t.name,
	    'Storage'            : t in StorageTechs,
	    'TechInputSplit'     : TechInputSplit[ t ],
	    'TechOutputSplit'    : TechOutputSplit[ t ],
	  }

	  for t in sorted( techs )
	]

	data = json.dumps( technology_characteristics )
	response = HttpResponse(
	  data,
	  content_type='application/json'
	)
	response['Content-Length'] = len( data )
	return response



@login_required
@require_POST
def remove_analysis_process_datum ( req, analysis_id, process_id, parameter ):
	# first, ensure user owns the specified analysis and process
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	process = get_object_or_404( Process, pk=process_id, analysis=analysis )

	status = 'Removed Successfully'
	status_code = None
	parameterToModel = {
	  'CostInvest'          : Param_CostInvest,             # t,v
	  'DiscountRate'        : Param_DiscountRate,           # t,v
	  'ExistingCapacity'    : Param_ExistingCapacity,       # t,v
	  'LifetimeProcess'     : Param_LifetimeProcess,        # t,v
	  'LifetimeProcessLoan' : Param_LifetimeProcessLoan,    # t,v
	  'CostFixed'           : Param_CostFixed,              # p,t,v
	  'CostVariable'        : Param_CostVariable,           # p,t,v
	  'Efficiencies'        : Param_Efficiency,             # i,t,v,o
	  'EmissionActivity'    : Param_EmissionActivity,       # c,i,t,v,o
	}
	TV = ('CostInvest', 'DiscountRate', 'ExistingCapacity', 'LifetimeProcess',
	      'LifetimeProcessLoan')
	try:
		model = parameterToModel[ parameter ]

		# first the parameters where the process is the key
		if parameter in TV:
			obj = model.objects.get( process=process )

		# then those parameters for which we're using a rowid
		else:
			pk = req.POST['rowid']  # process=process assures that user is owner
			if 'EmissionActivity' == parameter:
				obj = model.objects.get( pk=pk, efficiency__process=process )
			else:
				obj = model.objects.get( pk=pk, process=process )

		obj.delete()

	except ObjectDoesNotExist as e:
		status_code = 204 # No Content
		status = 'Content not there'
	except ValueError as e:
		status_code = 422 # unprocessable entity
		status = e.message
	except (MultiValueDictKeyError, KeyError) as e:
		status_code = 400 # bad request
		status = 'Malformed request: You may need to reload the page.'

	response = HttpResponse(
	  json.dumps( status ),
	  content_type='application/json'
	)

	if status_code:
		response.status_code = status_code

	return response


@login_required
@require_POST
def update_analysis_technology ( req, analysis_id, technology_id ):
	# first, ensure user owns the specified analysis
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	allowed_techs = Technology.objects.filter( process__analysis=analysis )
	technology = get_object_or_404( Technology,
	  pk=technology_id, pk__in=allowed_techs )

	status_code = None

	status = u'fail'  # assume failure until success
	validParameters = {
	  'Name'               : Technology,
	  'Description'        : Technology,
	  'Baseload'           : Set_tech_baseload,
	  'Storage'            : Set_tech_storage,
	  'GrowthRateSeed'     : Param_GrowthRateSeed,
	  'LifetimeTechLoan'   : Param_LifetimeTechLoan,
	  'LifetimeTech'       : Param_LifetimeTech,
	  'CapacityToActivity' : Param_CapacityToActivity,
	  'GrowthRateMax'      : Param_GrowthRateMax,
	  'TechInputSplit'     : Param_TechInputSplit,
	  'TechOutputSplit'    : Param_TechOutputSplit,
	}
	T = ('LifetimeTechLoan', 'LifetimeTech', 'CapacityToActivity',
	     'GrowthRateMax')
	Booleans = ('Baseload', 'Storage')

	try:
		params = defaultdict( dict )
		for p in req.POST.keys():
			if '-' in p:
				name, column = p.split('-')
				params[ name ][ column ] = req.POST[ p ]
			else:
				params[ p ] = req.POST[ p ]
		params = dict(params)

		with transaction.commit_on_success():
			for p in Booleans:
				model = validParameters[ p ]
				if p in params:
					obj, created = model.objects.get_or_create(
					  analysis=analysis, technology=technology)
					obj.save()

				else:
					obj = model.objects.filter(
					  analysis=analysis, technology=technology).distinct()
					if obj:
						obj.delete()


			for p in params:
				model = validParameters[ p ]

				if p in T:
					value = params[ p ]
					obj, created = model.objects.get_or_create(
					  analysis=analysis,
					  technology=technology,
					  defaults={'value': value}
					)
					obj.value = value
					obj.full_clean()
					obj.save()

				elif 'Name' == p:
					value = params[ p ]
					obj = technology
					obj.Name = value
					obj.full_clean()
					obj.save()

				elif 'Description' == p:
					value = params[ p ]
					obj = technology
					obj.Description = value
					obj.full_clean()
					obj.save()

				elif 'GrowthRateSeed' == p:
					value = params[ p ]
					try:
						grm = Param_GrowthRateMax.objects.get(
						  analysis=analysis, technology=technology )
					except ObjectDoesNotExist as e:
						msg = ('Cannot create GrowthRateSeed for technology class: '
						  ' first create a GrowthRateMax.')
						raise ValidationError( msg )

					obj, create = model.objects.get_or_create(
					  growth_max=grm, defaults={'value': value} )
					obj.value = value
					obj.full_clean()
					obj.save()

				elif 'TechInputSplit' == p:
					rowid    = params[ p ]['rowid']
					if 'Input' in params[ p ]:
						inp_name = params[ p ]['Input']
						fraction = params[ p ]['Fraction']
					else:
						continue

					try:
						inp = Set_commodity_physical.objects.get(
						  analysis=analysis, commodity__name=inp_name )
					except ObjectDoesNotExist as e:
						msg = 'No such input commodity in this analysis: {}.'
						raise ValidationError( msg.format( inp_name ))

					if 'NewRow' == rowid:
						obj = model()
					else:
						try:
							obj = model.objects.get( pk=rowid )
						except ObjectDoesNotExist as e:
							msg = 'Input split not found.  Try reloading the page.'
							raise ValidationError( msg )

					obj.inp_commodity = inp
					obj.technology    = technology
					obj.fraction      = fraction
					obj.full_clean()
					obj.save()

				elif 'TechOutputSplit' == p:
					rowid    = params[ p ]['rowid']
					if 'Output' in params[ p ]:
						out_name = params[ p ]['Output']
						fraction = params[ p ]['Fraction']
					else:
						continue

					try:
						out = Set_commodity_output.objects.get(
						  analysis=analysis, commodity__name=out_name )
					except ObjectDoesNotExist as e:
						msg = 'No such output commodity in this analysis: {}.'
						raise ValidationError( msg.format( out_name ))

					if 'NewRow' == rowid:
						obj = model()
					else:
						try:
							obj = model.objects.get( pk=rowid )
						except ObjectDoesNotExist as e:
							msg = 'Output split not found.  Try reloading the page.'
							raise ValidationError( msg )

					obj.out_commodity = out
					obj.technology    = technology
					obj.fraction      = fraction
					obj.full_clean()
					obj.save()

	except ValidationError as e:
		status_code = 422 # unprocessable entity
		status = unicode( e.messages.pop() )
	except ValueError as e:
		status_code = 422 # unprocessable entity
		status = unicode( e.message )
	except (MultiValueDictKeyError, KeyError) as e:
		status_code = 400 # bad request
		status = 'Malformed request: You may need to reload the page.'

	response = HttpResponse(
		json.dumps( status ),
		content_type='application/json'
	)

	if status_code:
		response.status_code = status_code

	return response



@login_required
@require_POST
def remove_analysis_technology_datum ( req, analysis_id, technology_id ):
	pass
