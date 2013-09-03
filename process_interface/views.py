from collections import defaultdict
from operator import itemgetter as i_get
import re

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import transaction
from django.db.models import Max
from django.db.utils import IntegrityError
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson as json
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.http import require_POST
from django.views.generic.edit import CreateView, UpdateView

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

from forms import (
  ProcessForm,
  EfficiencyForm,
  getEfficiencyForm,
  getEfficiencyForms,
  getFormCostRows,
  getFormEfficiencyRows,
  getFormEmissionActivityRows,
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

	c = {}
	c.update( analysis=analysis )
	c.update( process_characteristics=process_characteristics )

	if not req.user.is_authenticated():
		template = 'process_interface/process_info.html'
		c.update( username='' )

	else:
		template = 'process_interface/form_all_process_parameters.html'
		procs = {p.pk : p for p in processes}
		a = analysis

		for pc in process_characteristics:
			p = procs[ pc['ProcessId'] ]

			effs = pc['Efficiencies']

			kwargs = { 'prefix' : pc['ProcessId'] }

			pc['form_process'] = ProcessForm( p, **kwargs )  # process form
			pc['forms_efficiency'] = getEfficiencyForms( a, effs, **kwargs )

		c.update( csrf(req) )
		c.update( username=req.user.username )

	return render_to_response( template, c )


@login_required
@require_POST
def update_process ( req, analysis_id, process_id ):
	# first, ensure user owns the specified analysis
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	process = get_object_or_404( Process, pk=process_id, analysis=analysis )

	template = 'process_interface/form_process.html'

	process_characteristics = get_process_info( [process] )
	pc = process_characteristics[0]

	c = {}
	c.update(
	  username=req.user.username,
	  analysis=analysis,
	  process=process,
	  technology=process.technology.name,
	  vintage=process.vintage.vintage,
	  Baseload=pc['Baseload'],
	  Storage=pc['Storage']
	)
	c.update( csrf(req) )

	kwargs = { 'prefix' : process_id }
	pform = ProcessForm( process, req.POST, **kwargs )

	if pform.is_valid():
		clean = pform.cleaned_data
		with transaction.commit_on_success():
			process.update_with_data( clean )
			pform = ProcessForm( process, **kwargs )

	c.update( pform=pform )

	return render_to_response( template, c )



def get_messages ( req ):
	msg_storage = messages.get_messages( req )
	msgs = [ (m.tags, m.message) for m in msg_storage ]

	msg_storage.used = True  # remove the messages

	data = json.dumps( msgs )
	response = HttpResponse(
	  data,
	  content_type='application/json'
	)
	response['Content-Length'] = len( data )
	return response



@login_required
def new_efficiency ( req, analysis_id, process_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	process  = get_object_or_404( Process, pk=process_id, analysis=analysis )

	template = 'process_interface/form_efficiency_new.html'
	kwargs = { 'prefix' : process.pk }

	if req.POST:
		eform = EfficiencyForm( req.POST, analysis=analysis, prefix=process.pk )
		if eform.is_valid():
			clean = eform.cleaned_data
			inp = clean['inp']
			out = clean['out']
			value = clean['eff']
			if value:
				data = {
				  'analysis'      : analysis,
				  'inp_commodity' : inp,
				  'process'       : process,
				  'out_commodity' : out,
				  'value'         : value,
				}
				with transaction.commit_on_success():
					try:
						obj = Param_Efficiency.new_with_data( **data )
					except IntegrityError as ie:
						msg = ('Unable to save new Efficiency row.  A pairing of '
						  '({}, {}) already exists.  Edit or remove that one '
						  'instead.')
						messages.error( req, msg.format( inp, out ))

					template = 'process_interface/form_efficiency.html'
					eform = getEfficiencyForm( analysis, obj, **kwargs )

	else:
		if req.GET and req.GET['header']:
			template = 'process_interface/form_efficiency_new_header.html'

		eform = EfficiencyForm( analysis=analysis, **kwargs )

	c = {}
	c.update( analysis=analysis, process=process, eform=eform )
	c.update( csrf(req) )
	return render_to_response( template, c )


@login_required
@require_POST
def update_efficiency ( req, analysis_id, process_id, efficiency_id ):
	# first, ensure user owns the specified analysis and efficiency
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	process  = get_object_or_404( Process, pk=process_id, analysis=analysis )
	efficiency = get_object_or_404( Param_Efficiency,
	  pk=efficiency_id, process=process )

	template = 'process_interface/form_efficiency.html'

	c = {}
	c.update( analysis=analysis, process=process )
	c.update( csrf(req) )
	c.update( username=req.user.username )

	kwargs = { 'prefix' : process.pk }

	eform = getEfficiencyForm( analysis, efficiency, req.POST, **kwargs )
	if eform.is_valid():
		# the only way to change inp/out is by making a new row: since e_id
		# was passed via get, and it's now know good, we don't use the forms
		# inp/out.
		clean = eform.cleaned_data
		value = clean['eff']
		with transaction.commit_on_success():
			if not value:
				efficiency.delete()
				template = 'process_interface/form_efficiency_deleted.html'
			else:
				efficiency.value = value
				efficiency.clean()
				efficiency.save()
				eform = getEfficiencyForm( analysis, efficiency, **kwargs )

	c.update( eform=eform )
	return render_to_response( template, c )



