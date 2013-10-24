from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import simplejson as json
from django.views.decorators.http import require_POST

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

from view_helpers import set_cookie


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

	CostFixed = defaultdict( dict )
	for cf in Param_CostFixed.objects.filter( process__in=processes ):
		CostFixed[ cf.process ][ cf.pk ] = ( cf.period.vintage, cf.value )
	CostFixed = defaultdict( null, CostFixed )

	CostVariable = defaultdict( dict )
	for cv in Param_CostVariable.objects.filter( process__in=processes ):
		CostVariable[ cv.process ][ cv.pk ] = ( cv.period.vintage, cv.value )
	CostVariable = defaultdict( null, CostVariable )

	process_characteristics = [
	  {
	    'ProcessId'           : p.pk,
	    'Baseload'            : p.technology in BaseloadTechs,
	    'CostFixed'           : CostFixed[ p ],
	    'CostInvest'          : p.costinvest,
	    'CostVariable'        : CostVariable[ p ],
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


def process_list ( req, analysis_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id )
	processes = [
	  (p.id, p.technology.name, p.vintage.vintage)

	  for p in Process.objects.filter( analysis=analysis )
	]

	template = 'process_interface/process_list.html'

	c = {}
	c.update( processes=processes, analysis_id=analysis.pk )
	if req.user.is_authenticated():
		c.update( authed=True )
		c.update( csrf(req) )

	res = render( req, template, c )
	set_cookie( req, res, analysis_id=analysis_id )
	return res


@login_required
def process_new ( req, analysis_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )

	template = 'process_interface/form_process_new.html'
	kwargs = {
	  'prefix'   : 'new_process' + str(analysis.pk),
	  'analysis' : analysis
	}
	status = 200

	if req.POST:
		process = Process( analysis=analysis )
		form = NewProcessForm( req.POST, instance=process, **kwargs )
		if not form.is_valid():
			status = 422  # to let Javascript know there was an error
			msg = '\n'.join( m.as_text() for k, m in form.errors.iteritems() )
			messages.error( req, msg )

			res = HttpResponse( status=status )
			set_cookie( req, res )
			return res

		else:
			try:
				form.save()
				return process_list( req, analysis.pk )

			except IntegrityError as ie:
				t = form.cleaned_data[ 'technology' ]
				v = form.cleaned_data[ 'vintage' ]
				msg = ('Unable to create new Process ({}, {}).  It already exists!')
				messages.error( req, msg.format( t, v, ie ))
				status = 422

	else:
		form = NewProcessForm( **kwargs )

	c = {}
	c.update( analysis=analysis, form=form )
	c.update( csrf(req) )

	res = render( req, template, c, status=status )
	set_cookie( req, res )
	return res


@login_required
def process_remove ( req, analysis_id, process_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	process = get_object_or_404( Process, pk=process_id, analysis=analysis )

	process.delete()

	return process_list( req, analysis.pk )


def process_info ( req, analysis_id, process_ids ):
	analysis = get_object_or_404( Analysis, pk=analysis_id )
	process_ids = process_ids.split(',')
	processes = Process.objects.filter(
	  analysis=analysis,
	  pk__in=process_ids
	).distinct().order_by(
	  'technology__name',
	  'vintage__vintage'
	).select_related()
	process_ids = sorted( p.pk for p in processes )

	process_characteristics = get_process_info( processes )

	c = {}
	c.update( analysis=analysis )
	c.update( process_characteristics=process_characteristics )

	if not req.user.is_authenticated():
		template = 'process_interface/info_all_process_parameters.html'

	else:
		template = 'process_interface/form_all_process_parameters.html'
		procs = {p.pk : p for p in processes}
		a = analysis

		for pc in process_characteristics:

			p = procs[ pc['ProcessId'] ]

			effs = pc['Efficiencies']
			emas = pc['EmissionActivity']
			cf   = pc['CostFixed']
			cv   = pc['CostVariable']

			pform_kwargs  = { 'prefix' : 'pr' + str(p.pk) }
			eform_kwargs  = { 'prefix' : 'ef' + str(p.pk) }
			eaform_kwargs = { 'prefix' : 'ea' + str(p.pk), 'process' : p }
			cfform_kwargs = { 'prefix' : 'cf' + str(p.pk), 'process' : p }
			cvform_kwargs = { 'prefix' : 'cv' + str(p.pk), 'process' : p }

			pc['form_process']           = ProcessForm( p, **pform_kwargs )  # process form
			pc['forms_efficiency']       = getEfficiencyForms( a, effs, **eform_kwargs )
			pc['forms_emissionactivity'] = getEmissionActivityForms( emas, **eaform_kwargs )
			pc['forms_costfixed']        = getCostFixedForms( cf, **cfform_kwargs )
			pc['forms_costvariable']     = getCostVariableForms( cv, **cvform_kwargs )

		c.update( csrf(req) )
		c.update( username=req.user.username )

	res = render( req, template, c )
	set_cookie( req, res, process_ids=process_ids )
	return res


@login_required
@require_POST
def update_process ( req, analysis_id, process_id ):
	# first, ensure user owns the specified analysis
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	process = get_object_or_404( Process, pk=process_id, analysis=analysis )

	template = 'process_interface/form_process.html'
	status = 200

	process_characteristics = get_process_info( [process] )
	pc = process_characteristics[0]

	kwargs = { 'prefix' : 'pr' + str(process_id) }
	form = ProcessForm( process, req.POST, **kwargs )

	if not form.is_valid():
		status = 422  # to let Javascript know there was an error
		msg = '\n'.join( m.as_text() for k, m in form.errors.iteritems() )
		messages.error( req, msg )

	else:
		clean = form.cleaned_data
		with transaction.commit_on_success():
			try:
				process.update_with_data( clean )
				form = ProcessForm( process, **kwargs )
			except IntegrityError as ie:
				msg = 'Unable to update process.  DB said: {}'
				messages.error( req, msg.format( ie ))
				status = 422

	c = {}
	c.update(
	  analysis=analysis,
	  process=process,
	  technology=process.technology.name,
	  vintage=process.vintage.vintage,
	  Baseload=pc['Baseload'],
	  Storage=pc['Storage'],
	  form=form
	)
	c.update( csrf(req) )

	res = render( req, template, c, status=status )
	set_cookie( req, res )
	return res


@login_required
def new_efficiency ( req, analysis_id, process_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	process  = get_object_or_404( Process, pk=process_id, analysis=analysis )

	template = 'process_interface/form_efficiency_new.html'
	kwargs = { 'prefix' : 'ef' + str(process.pk) }
	status = 200

	if req.POST:
		form = EfficiencyForm( req.POST, analysis=analysis, **kwargs )
		if not form.is_valid():
			status = 422  # to let Javascript know there was an error
			msg = '\n'.join( m.as_text() for k, m in form.errors.iteritems() )
			messages.error( req, msg )

		else:
			clean = form.cleaned_data
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
						template = 'process_interface/form_efficiency.html'
						form = getEfficiencyForm( analysis, obj, **kwargs )
					except IntegrityError as ie:
						msg = ('Unable to save new Efficiency row.  A pairing of '
						  '({}, {}) already exists.  Edit or remove that one '
						  'instead.')
						messages.error( req, msg.format( inp, out ))
						status = 422

	else:
		if req.GET and req.GET['header']:
			template = 'process_interface/form_efficiency_new_header.html'

		form = EfficiencyForm( analysis=analysis, **kwargs )

	c = {}
	c.update( analysis=analysis, process=process, form=form )
	c.update( csrf(req) )

	res = render( req, template, c, status=status )
	set_cookie( req, res )
	return res


@login_required
@require_POST
def update_efficiency ( req, analysis_id, process_id, efficiency_id ):
	# first, ensure user owns the specified analysis and efficiency
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	process  = get_object_or_404( Process, pk=process_id, analysis=analysis )
	efficiency = get_object_or_404( Param_Efficiency,
	  pk=efficiency_id, process=process )

	template = 'process_interface/form_efficiency.html'
	kwargs = { 'prefix' : 'ef' + str(process.pk) }
	status = 200

	form = getEfficiencyForm( analysis, efficiency, req.POST, **kwargs )
	if not form.is_valid():
		status = 422  # to let Javascript know there was an error
		msg = '\n'.join( m.as_text() for k, m in form.errors.iteritems() )
		messages.error( req, msg )

	else:
		# the only way to change inp/out is by making a new row: since e_id
		# was passed via get, and it's now known good, we don't use the forms
		# inp/out.
		clean = form.cleaned_data
		value = clean['eff']
		with transaction.commit_on_success():
			try:
				if not value:
					efficiency.delete()
					template = 'process_interface/form_efficiency_deleted.html'
				else:
					efficiency.value = value
					efficiency.clean()
					efficiency.save()
					form = getEfficiencyForm( analysis, efficiency, **kwargs )
			except IntegrityError as ie:
				msg = ('Unable to complete action.  Database said: {}')
				messages.error( req, msg.format( ie ))
				status = 422

	c = {}
	c.update( analysis=analysis, process=process, form=form )
	c.update( csrf(req) )

	res = render( req, template, c, status=status )
	set_cookie( req, res )
	return res


@login_required
def new_emissionactivity ( req, analysis_id, process_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	process  = get_object_or_404( Process, pk=process_id, analysis=analysis )

	template = 'process_interface/form_emissionactivity_new.html'
	kwargs = { 'prefix': 'ea' + str(process.pk), 'process': process }
	status = 200  # HTTP Status code: 200 = everything's good

	if req.POST:
		form = EmissionActivityForm( req.POST, **kwargs )
		if not form.is_valid():
			status = 422  # to let Javascript know there was an error
			msg = '\n'.join( m.as_text() for k, m in form.errors.iteritems() )
			messages.error( req, msg )
		else:
			clean = form.cleaned_data
			pol = clean['pol']
			eff = clean['eff']
			val = clean['val']
			if val:
				data = {
				  'analysis'   : analysis,
				  'process'    : process,
				  'pollutant'  : pol,
				  'efficiency' : eff,
				  'value'      : val,
				}
				with transaction.commit_on_success():
					try:
						obj = Param_EmissionActivity.new_with_data( **data )
						template = 'process_interface/form_emissionactivity.html'
						form = getEmissionActivityForm( obj, **kwargs )
					except IntegrityError as ie:
						msg = ('Unable to save new EmissionActivity row.  A '
						  'tuple of ({}, {}) already exists.  Edit or remove that '
						  'row instead.')
						messages.error( req, msg.format( pol, eff ))
						status = 422


	else:
		if req.GET and req.GET['header']:
			template = 'process_interface/form_emissionactivity_new_header.html'

		form = EmissionActivityForm( **kwargs )

	c = {}
	c.update( analysis=analysis, process=process, form=form )
	c.update( csrf(req) )

	res = render( req, template, c, status=status )
	set_cookie( req, res )
	return res


@login_required
@require_POST
def update_emissionactivity (
  req, analysis_id, process_id, emissionactivity_id
):
	# first, ensure user owns the specified analysis and efficiency
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	process  = get_object_or_404( Process, pk=process_id, analysis=analysis )
	emactivity = get_object_or_404( Param_EmissionActivity,
	  pk=emissionactivity_id, efficiency__process=process )

	template = 'process_interface/form_emissionactivity.html'
	kwargs = { 'prefix' : 'ea' + str(process.pk), 'process': process }
	status = 200

	form = getEmissionActivityForm( emactivity, req.POST, **kwargs )
	if not form.is_valid():
		status = 422  # to let Javascript know there was an error
		msg = '\n'.join( m.as_text() for k, m in form.errors.iteritems() )
		messages.error( req, msg )
	else:
		# the only way to change inp/out is by making a new row: since e_id
		# was passed via get, and it's now known good, we don't use the form's
		# eff.
		clean = form.cleaned_data
		value = clean['val']
		with transaction.commit_on_success():
			if not value:
				emactivity.delete()
				template = 'process_interface/form_emissionactivity_deleted.html'
			else:
				emactivity.value = value
				emactivity.clean()
				emactivity.save()
				form = getEmissionActivityForm( emactivity, **kwargs )

	c = {}
	c.update( analysis=analysis, process=process, form=form )
	c.update( csrf(req) )

	res = render( req, template, c, status=status )
	set_cookie( req, res )
	return res


@login_required
def new_costfixed ( req, analysis_id, process_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	process  = get_object_or_404( Process, pk=process_id, analysis=analysis )

	template = 'process_interface/form_costfixed_new.html'
	kwargs = { 'prefix': 'cf' + str(process.pk), 'process': process }
	status = 200  # HTTP Status code: 200 = everything's good

	if req.POST:
		form = CostFixedForm( req.POST, **kwargs )
		if not form.is_valid():
			status = 422  # to let Javascript know there was an error
			msg = '\n'.join( m.as_text() for k, m in form.errors.iteritems() )
			messages.error( req, msg )
		else:
			clean = form.cleaned_data
			per = clean['per']
			val = clean['val']
			if val:
				data = {
				  'analysis' : analysis,
				  'process'  : process,
				  'period'   : per,
				  'value'    : val,
				}
				with transaction.commit_on_success():
					try:
						obj = Param_CostFixed.new_with_data( **data )
						template = 'process_interface/form_costfixed.html'
						form = getCostFixedForm( obj, **kwargs )
					except IntegrityError as ie:
						msg = ('Unable to save new CostFixed row.  A cost for '
						  'period {} already exists.  Edit or remove that value '
						  'instead.')
						messages.error( req, msg.format( per ))
						status = 422


	else:
		if req.GET and req.GET['header']:
			template = 'process_interface/form_costfixed_new_header.html'

		form = CostFixedForm( **kwargs )

	c = {}
	c.update( analysis=analysis, process=process, form=form )
	c.update( csrf(req) )

	res = render( req, template, c, status=status )
	set_cookie( req, res )
	return res


@login_required
@require_POST
def update_costfixed ( req, analysis_id, process_id, costfixed_id ):
	# first, ensure user owns the specified analysis and efficiency
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	process  = get_object_or_404( Process, pk=process_id, analysis=analysis )
	costfixed = get_object_or_404( Param_CostFixed,
	  pk=costfixed_id, process=process )

	template = 'process_interface/form_costfixed.html'
	kwargs = { 'prefix' : 'cf' + str(process.pk), 'process' : process }
	status = 200  # HTTP Status code: 200 = everything's good

	form = getCostFixedForm( costfixed, req.POST, **kwargs )
	if not form.is_valid():
		status = 422 # unprocessable entity
		msg = '\n'.join( m.as_text() for k, m in form.errors.iteritems() )
		messages.error( req, msg )

	else:
		# the only way to change inp/out is by making a new row: since e_id
		# was passed via get, and it's now known good, we don't use the form's
		# eff.
		clean = form.cleaned_data
		value = clean['val']
		with transaction.commit_on_success():
			if not value:
				costfixed.delete()
				template = 'process_interface/form_costfixed_deleted.html'
			else:
				costfixed.value = value
				costfixed.clean()
				costfixed.save()
				form = getCostFixedForm( costfixed, **kwargs )

	c = {}
	c.update( analysis=analysis, process=process, form=form )
	c.update( csrf(req) )

	res = render( req, template, c, status=status )
	set_cookie( req, res )
	return res


@login_required
def new_costvariable ( req, analysis_id, process_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	process  = get_object_or_404( Process, pk=process_id, analysis=analysis )

	template = 'process_interface/form_costvariable_new.html'
	kwargs = { 'prefix': 'cf' + str(process.pk), 'process': process }
	status = 200  # HTTP Status code: 200 = everything's good

	if req.POST:
		form = CostVariableForm( req.POST, **kwargs )
		if not form.is_valid():
			status = 422  # to let Javascript know there was an error
			msg = '\n'.join( m.as_text() for k, m in form.errors.iteritems() )
			messages.error( req, msg )
		else:
			clean = form.cleaned_data
			per = clean['per']
			val = clean['val']
			if val:
				data = {
				  'analysis' : analysis,
				  'process'  : process,
				  'period'   : per,
				  'value'    : val,
				}
				with transaction.commit_on_success():
					try:
						obj = Param_CostVariable.new_with_data( **data )
						template = 'process_interface/form_costvariable.html'
						form = getCostVariableForm( obj, **kwargs )
					except IntegrityError as ie:
						msg = ('Unable to save new CostVariable row.  A cost for '
						  'period {} already exists.  Edit or remove that value '
						  'instead.')
						messages.error( req, msg.format( per ))
						status = 422


	else:
		if req.GET and req.GET['header']:
			template = 'process_interface/form_costvariable_new_header.html'

		form = CostVariableForm( **kwargs )

	c = {}
	c.update( analysis=analysis, process=process, form=form )
	c.update( csrf(req) )

	res = render( req, template, c, status=status )
	set_cookie( req, res )
	return res


@login_required
@require_POST
def update_costvariable ( req, analysis_id, process_id, costvariable_id ):
	# first, ensure user owns the specified analysis and efficiency
	analysis = get_object_or_404( Analysis, pk=analysis_id, user=req.user )
	process  = get_object_or_404( Process, pk=process_id, analysis=analysis )
	costvariable = get_object_or_404( Param_CostVariable,
	  pk=costvariable_id, process=process )

	template = 'process_interface/form_costvariable.html'
	kwargs = { 'prefix' : 'cf' + str(process.pk), 'process' : process }
	status = 200  # HTTP Status code: 200 = everything's good

	form = getCostVariableForm( costvariable, req.POST, **kwargs )
	if not form.is_valid():
		status = 422 # unprocessable entity
		msg = '\n'.join( m.as_text() for k, m in form.errors.iteritems() )
		messages.error( req, msg )

	else:
		# the only way to change inp/out is by making a new row: since e_id
		# was passed via get, and it's now known good, we don't use the form's
		# eff.
		clean = form.cleaned_data
		value = clean['val']
		with transaction.commit_on_success():
			if not value:
				costvariable.delete()
				template = 'process_interface/form_costvariable_deleted.html'
			else:
				costvariable.value = value
				costvariable.clean()
				costvariable.save()
				form = getCostVariableForm( costvariable, **kwargs )

	c = {}
	c.update( analysis=analysis, process=process, form=form )
	c.update( csrf(req) )

	res = render( req, template, c, status=status )
	set_cookie( req, res )
	return res

