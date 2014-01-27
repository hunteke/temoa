from collections import defaultdict
import json

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache

from decorators.http import require_POST, require_DELETE
from decorators.auth import require_login

from models import (
  Analysis,
  Param_CapacityToActivity,
  Param_GrowthRate,
  Param_LifetimeTech,
  Param_LifetimeTechLoan,
  Param_TechInputSplit,
  Param_TechOutputSplit,
  Set_tech_baseload,
  Set_tech_storage,
  Technology,
)
from forms import (
  AnalysisTechnologyForm,
  TechInputSplitForm,
  TechOutputSplitForm,
)

from view_helpers import set_cookie

from IPython import embed as II

def technology_list ( req ):
	techs = Technology.objects.all().order_by('user__username', 'name')

	techs = [{
	    'id'                   : t.pk,
	    'username'             : t.user.username,
	    'name'                 : t.name,
	    'capacity_to_activity' : t.capacity_to_activity,
	    'description'          : t.description,
	  }

	  for t in techs
	]

	data = json.dumps( { 'data' : techs } )
	res = HttpResponse( data, content_type='application/json' )
	res['Content-Length'] = len( data )
	set_cookie( req, res )

	return res


def get_technology_info ( analysis, technologies ):
	def null ( ):
		return None

	BaseloadTechs = set( bt.technology
	  for bt in Set_tech_baseload.objects.filter(
	    analysis=analysis, technology__in=technologies )
	)

	StorageTechs = set( st.technology
	  for st in Set_tech_storage.objects.filter(
	    analysis=analysis, technology__in=technologies )
	)

	CapacityToActivity = defaultdict( null )
	CapacityToActivity.update({ c2a.technology : c2a.value
	  for c2a in Param_CapacityToActivity.objects.filter(
	    analysis=analysis, technology__in=technologies )
	})

	GrowthRate = defaultdict( null )
	for gr in Param_GrowthRate.objects.filter(
	  analysis=analysis, technology__in=technologies ):
		GrowthRate[ gr.technology, 'ratelimit' ] = gr.ratelimit
		GrowthRate[ gr.technology, 'seed' ] = gr.seed

	LifetimeTech = defaultdict( null )
	LifetimeTech.update({ lt.technology: lt.value
	  for lt in Param_LifetimeTech.objects.filter(
	    analysis=analysis, technology__in=technologies )
	})

	LifetimeTechLoan = defaultdict( null )
	LifetimeTechLoan.update({ ltl.technology: ltl.value
	  for ltl in Param_LifetimeTechLoan.objects.filter(
	    analysis=analysis, technology__in=technologies )
	})

	TechInputSplit = defaultdict( list )
	for isplit in Param_TechInputSplit.objects.filter(
	  inp_commodity__analysis=analysis, technology__in=technologies ):
		TechInputSplit[ isplit.technology ].append({
			'aId'   : analysis.pk,
			'tId'   : isplit.technology.pk,
			'id'    : isplit.pk,
			'inp'   : isplit.inp_commodity.commodity.name,
			'value' : isplit.fraction
		})

	TechOutputSplit = defaultdict( list )
	for osplit in Param_TechOutputSplit.objects.filter(
	  out_commodity__analysis=analysis, technology__in=technologies ):
		TechOutputSplit[ osplit.technology ].append({
			'aId'   : analysis.pk,
			'tId'   : osplit.technology.pk,
			'id'    : osplit.pk,
			'out'   : osplit.out_commodity.commodity.name,
			'value' : osplit.fraction
		})

	data = [
	  {
	    'id'                 : t.pk,
	    'aId'                : analysis.pk,
	    'baseload'           : t in BaseloadTechs,
	    'capacitytoactivity' : CapacityToActivity[ t ],
	    'description'        : unicode( t.description ),
	    'growthratelimit'    : GrowthRate[ t, 'ratelimit' ],
	    'growthrateseed'     : GrowthRate[ t, 'seed' ],
	    'storage'            : t in StorageTechs,
	    'inputsplits'        : TechInputSplit[ t ],
	    'outputsplits'       : TechOutputSplit[ t ],
	    'lifetime'           : LifetimeTech[ t ],
	    'loanlife'           : LifetimeTechLoan[ t ],
	    'name'               : t.name,
	  }

	  for t in technologies
	]

	return data


@never_cache
def analysis_technology_list ( req, analysis_id ):
	analysis = get_object_or_404( Analysis, pk=analysis_id )
	techs = Technology.objects.filter( process__analysis=analysis ).distinct()

	data = None
	if len( techs ):
		data = get_technology_info( analysis, techs )

	data = json.dumps( { 'data' : data } )
	res = HttpResponse( data, content_type='application/json' )
	res['Content-Length'] = len( data )

	set_cookie( req, res )
	return res


@never_cache
def analysis_technology_info ( req, analysis_id, technology_id ):
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
			  id                   = tech.pk,
			  username             = tech.user.username,
			  name                 = tech.name,
			  capacity_to_activity = tech.capacity_to_activity,
			  description          = tech.description,
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
		  id                   = tech.pk,
		  username             = tech.user.username,
		  name                 = tech.name,
		  capacity_to_activity = tech.capacity_to_activity,
		  description          = tech.description,
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

