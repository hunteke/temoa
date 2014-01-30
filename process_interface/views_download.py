## Download ###################################################################

from operator import itemgetter

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache

from decorators.http import require_GET

from IPython import embed as II

from models import (
  Analysis,
  Param_CapacityFactorTech,
  Param_CapacityToActivity,
  Param_CostFixed,
  Param_CostVariable,
  Param_Demand,
  Param_DemandDefaultDistribution,
  Param_DemandSpecificDistribution,
  Param_Efficiency,
  Param_EmissionActivity,
  Param_GrowthRate,
  Param_LifetimeTech,
  Param_LifetimeTechLoan,
  Param_MaxCapacity,
  Param_MinCapacity,
  Param_SegFrac,
  Param_TechInputSplit,
  Param_TechOutputSplit,
  Process,
  Set_tech_baseload,
  Set_tech_storage,
  Vintage,
)

@require_GET
@never_cache
def analysis_download_as_dat ( req, analysis_id ):
	from django.contrib.sites.models import Site
	from textwrap import TextWrapper

	analysis = get_object_or_404( Analysis, pk=analysis_id )

	dat_format = """\
# This is an automatically generated data file for input into the Temoa energy
# economy optimization (EEO) model.  This file was downloaded via the url:
#
#     {url}
#
# Analysis title and description:
#
#     {analysis_name}
#         (owner: {user})
#
{analysis_description}
#
# The structure of this file loosely follows the data file format for AMPL, but
# is only guaranteed to be valid for Coopr.   Note, however, that validity for
# Coopr does _not_ imply an actually valid model.  That privilege (onus?) is on
# the modeler.
#
# To run Temoa with this data, invoke this file similar to:
#
#     $ ./temoa.py  <this_file_name>
#     $ coopr_python  temoa.py  <this_file_name>   [alternative]
#
# Or, if you're working with a development version of Temoa, run the Temoa
# directory directly:
#
#      $ coopr_python temoa_model/  <this_file_name>
#
# For more information, please see http://temoaproject.org/

data ;

{set_periods}

{time_season}
{time_of_day}

{segfrac}

{tech_production}
{tech_baseload}
{tech_storage}

{commodity_demand}
{commodity_emission}
{commodity_physical}

param  GlobalDiscountRate  :=  {gdr} ;

{demanddefaultdistribution}

{demandspecificdistribution}

{demand}

{efficiency}

{emissionactivity}

{existingcapacity}

{capacitytoactivity}

{capacityfactortech}

param  CapacityFactorProcess  := ... ;   NOT YET IMPLEMENTED IN DB FRONTEND

{costinvest}

{costfixed}

{costvariable}

{lifetimetech}

{processlife}

{lifetimeloantech}

{processloanlife}

{techinputsplit}

{techoutputsplit}

{maxcapacity}

{mincapacity}

{growthratemax}

{growthrateseed}
"""

	twrapper = TextWrapper(
	  width=79,
	  initial_indent='#       ',
	  subsequent_indent='#   ',
	  expand_tabs=False,
	  fix_sentence_endings=True,
	  break_long_words=False,
	  drop_whitespace=True
	)

	vintages = Vintage.objects.filter( analysis=analysis )
	existing = [ v.vintage for v in vintages if v.vintage <  analysis.period_0 ]
	future   = [ v.vintage for v in vintages if v.vintage >= analysis.period_0 ]
	existing = '  '.join( sorted( str(v) for v in existing ))
	future   = '  '.join( sorted( str(v) for v in future ))
	if existing:
		existing = 'set  time_exist   :=  {} ;\n'.format( existing )
	set_periods = '{}set  time_future  :=  {} ;'.format( existing, future )

	segfracs = Param_SegFrac.objects.filter( analysis=analysis )
	seasons = sorted( set(sf.season for sf in segfracs ))
	times_of_day = sorted( set(sf.time_of_day for sf in segfracs ))

	if not segfracs:
		time_season = '# set time_season := ... ;   # No SegFracs in DB'
		time_of_day = '# set time_of_day := ... ;   # No SegFracs in DB'
		segfrac     = '# param SegFrac := ... ;     # No SegFracs in DB'

	else:
		time_season = '  '.join( seasons )
		time_of_day = '  '.join( times_of_day )
		time_season = 'set  time_season  :=  {} ;'.format( time_season )
		time_of_day = 'set  time_of_day  :=  {} ;'.format( time_of_day )

		maxlen_s = max(map(len, seasons ))
		maxlen_d = max(map(len, times_of_day ))
		slices = sorted( (sf.season, sf.time_of_day, sf.value)
		  for sf in segfracs )
		fmt = r'{{:<{}}}  {{:<{}}}  {{}}'.format( maxlen_s, maxlen_d )
		for i, s in enumerate( slices ):
			slices[ i ] = fmt.format( *s )
		segfrac = '\n '.join( slices )
		segfrac = 'param  SegFrac  :=\n {}\n\t;'.format( segfrac )

	efficiencies = Param_Efficiency.objects.filter(
	  process__analysis=analysis )
	techs_prod = sorted(set( e.process.technology.name
	  for e in efficiencies
	))
	processes = set( eff.process for eff in efficiencies )
	process_ids = set( p.pk for p in processes )

	tech_production = '# set tech_production := ... ;   # No flows (efficiencies) in DB'
	tech_baseload   = '# set tech_baseload := ... ;   # No baseload technologies in DB'
	tech_storage    = '# set tech_storage := ... ;   # No storage technologies in DB'

	if techs_prod:
		tech_production = '\n '.join( techs_prod )
		tech_production = 'set  tech_production  :=\n {}\n\t;'.format( tech_production )

	techs_base = Set_tech_baseload.objects.filter(
	  analysis=analysis,
	  technology__name__in=techs_prod
	)
	if techs_base:
		techs_base = sorted(set( t.technology.name for t in techs_base ))
		tech_baseload = '\n '.join( techs_base )
		tech_baseload = '\nset  tech_baseload  :=\n {}\n\t;'.format( tech_baseload )

	techs_store = Set_tech_storage.objects.filter(
	  analysis=analysis,
	  technology__name__in=techs_prod
	)
	if techs_store:
		techs_store = sorted(set( t.technology.name for t in techs_store ))
		tech_storage = '\n '.join( techs_store )
		tech_storage = '\nset  tech_storage  :=\n {}\n\t;'.format( tech_storage )

	demands   = Param_Demand.objects.filter( demand__analysis=analysis )
	emissions = Param_EmissionActivity.objects.filter( emission__analysis=analysis )
	physicals = set( e.inp_commodity for e in efficiencies )
	physicals |= set( e.out_commodity for e in efficiencies )
	physicals -= set( d.demand for d in demands )

	c_demand   = '# set commodity_demand := ... ;   # No demand commodities in DB'
	c_emission = '# set commodity_emissions := ... ;   # No emission commodities in DB'
	c_physical = '# set commodity_physical := ... ;   # No emission commodities in DB'

	if demands:
		c_demand = sorted(set( d.demand.commodity.name for d in demands ))
		c_demand = '\n '.join( c_demand )
		c_demand = '\nset  commodity_demand  :=\n {}\n\t;'.format( c_demand )

	if emissions:
		c_emission = sorted(set( em.emission.commodity.name for em in emissions ))
		c_emission = '\n '.join( c_emission )
		c_emission = '\nset  commodity_emissions  :=\n {}\n\t;'.format( c_emission )

	if physicals:
		c_physical = sorted(set( p.commodity.name for p in physicals ))
		c_physical = '\n '.join( c_physical )
		c_physical = '\nset  commodity_physical  :=\n {}\n\t;'.format( c_physical )

	ddds = Param_DemandDefaultDistribution.objects.filter(
	  timeslice__analysis=analysis )
	dsds = Param_DemandSpecificDistribution.objects.filter(
	  timeslice__analysis=analysis )

	ddd = '# param DemandDefaultDistribution := ... ;   # None specified in DB: SegFrac is the default distribution.'
	dsd = '# param DemandSpecificDistribution := ... ;   # None specified in DB: Demands will be apportioned per DemandDefaultDistribution.'
	dem = '# param Demand := ... ;   # No demands specified.  This should be an easy solve!'

	if ddds:
		lines = sorted( [d.timeslice.season, d.timeslice.time_of_day, d.value]
		  for d in ddds )

		maxlen_s = max(map(len, (i[0] for i in lines) )) # season
		maxlen_d = max(map(len, (i[1] for i in lines) )) # time_of_day
		fmt = r'{{:<{}}}  {{:<{}}}  {{}}'.format( maxlen_s, maxlen_d )
		for i, s in enumerate( slices ):
			lines[ i ] = fmt.format( *s )
		ddd = '\n '.join( lines )
		ddd = 'param  DemandDefaultDistribution  :=\n {}\n\t;'.format( ddd )

	if dsds:
		lines = [ [
		    d.timeslice.season,
		    d.timeslice.time_of_day,
		    d.demand.commodity.name,
		    d.value
		  ]
		  for d in dsds
		]
		lines.sort( key=itemgetter(2, 0) )

		maxlen_s = max(map(len, (i[0] for i in lines) )) # season
		maxlen_d = max(map(len, (i[1] for i in lines) )) # time_of_day
		maxlen_o = max(map(len, (i[2] for i in lines) )) # demands/outputs
		fmt = r'{{:<{}}}  {{:<{}}}  {{:<{}}}  {{}}'
		fmt = fmt.format( maxlen_s, maxlen_d, maxlen_o )
		for i, s in enumerate( lines ):
			lines[ i ] = fmt.format( *s )

		dsd = '\n '.join( lines )
		dsd = 'param  DemandSpecificDistribution  :=\n {}\n\t;'.format( dsd )

	if demands:
		lines = [ [
		    str(d.period.vintage),
		    d.demand.commodity.name,
		    str(int(d.value)),
		    str(d.value - int(d.value))[1:]  # remove leading 0
		  ]
		  for d in demands ]
		lines.sort( key=itemgetter(1, 0) )

		# work out column alignment, just in case a human consumes this file ...
		maxlen_p   = max(map(len, (i[0] for i in lines) ))
		maxlen_dem = max(map(len, (i[1] for i in lines) ))
		maxlen_int = max(map(len, (i[2] for i in lines) ))
		fmt = r'{{:<{}}}  {{:<{}}}  {{:>{}}}{{}}'
		fmt = fmt.format( maxlen_p, maxlen_dem, maxlen_int )
		for i, s in enumerate( lines ):
			lines[ i ] = fmt.format( *s )

		dem = '\n '.join( lines )
		dem = 'param  Demand  :=\n {}\n\t;'.format( dem )

	eff = '# param Efficiency := ... ;   # None specified in DB'
	if efficiencies:
		lines = [ [
		    e.inp_commodity.commodity.name,
		    e.process.technology.name,
		    str(e.process.vintage.vintage),
		    e.out_commodity.commodity.name,
		    str(int(e.value)),
		    str(e.value - int(e.value))[1:]  # remove leading 0
		  ]
		  for e in efficiencies
		]
		lines.sort( key=itemgetter(1, 2, 0, 3) )

		maxlen_i   = max(map(len, (i[0] for i in lines) ))
		maxlen_t   = max(map(len, (i[1] for i in lines) ))
		maxlen_v   = max(map(len, (i[2] for i in lines) ))
		maxlen_o   = max(map(len, (i[3] for i in lines) ))
		maxlen_int = max(map(len, (i[4] for i in lines) ))
		fmt = r'{{:<{}}}  {{:<{}}}  {{:<{}}}  {{:<{}}}  {{:>{}}}{{}}'
		fmt = fmt.format( maxlen_i, maxlen_t, maxlen_v, maxlen_o, maxlen_int )
		for i, s in enumerate( lines ):
			lines[ i ] = fmt.format( *s )

		eff = '\n '.join( lines )
		eff = 'param  Efficiency  :=\n {}\n\t;'.format( eff )

	ems = '# param EmissionActivity := ... ;   # None specified in DB'
	if emissions:
		lines = [ [
		    em.emission.commodity.name,
		    em.efficiency.inp_commodity.commodity.name,
		    em.efficiency.process.technology.name,
		    str(em.efficiency.process.vintage.vintage),
		    em.efficiency.out_commodity.commodity.name,
		    str(int(em.value)),
		    str(em.value - int(em.value))[1:]  # remove leading 0
		  ]
		  for em in emissions
		]
		lines.sort( key=itemgetter(2, 3, 1, 4, 0) )

		maxlen_e   = max(map(len, (i[0] for i in lines) ))
		maxlen_i   = max(map(len, (i[1] for i in lines) ))
		maxlen_t   = max(map(len, (i[2] for i in lines) ))
		maxlen_v   = max(map(len, (i[3] for i in lines) ))
		maxlen_o   = max(map(len, (i[4] for i in lines) ))
		maxlen_int = max(map(len, (i[5] for i in lines) ))
		fmt = r'{{:<{}}}  {{:<{}}}  {{:<{}}}  {{:<{}}}  {{:<{}}}  {{:>{}}}{{}}'
		fmt = fmt.format( maxlen_e, maxlen_i, maxlen_t, maxlen_v, maxlen_o, maxlen_int )
		for i, s in enumerate( lines ):
			lines[ i ] = fmt.format( *s )

		ems = '\n '.join( lines )
		ems = 'param  EmissionActivity  :=\n {}\n\t;'.format( ems )

	existingcap = Process.objects.filter(
	  id__in=process_ids,
	  vintage__vintage__lt=analysis.period_0,
	  existingcapacity__gt=0
	)

	ecap = '# param ExistingCapacity := ... ;   # None specified in DB'
	if existingcap:
		lines = sorted( [
		    ec.technology.name,
		    str(ec.vintage.vintage),
		    str(int(ec.existingcapacity)),
		    str(ec.existingcapacity - int(ec.existingcapacity))[1:],
		  ]
		  for ec in existingcap
		)

		maxlen_t   = max(map(len, (i[0] for i in lines) ))
		maxlen_v   = max(map(len, (i[1] for i in lines) ))
		maxlen_int = max(map(len, (i[2] for i in lines) ))
		fmt = r'{{:<{}}}  {{:<{}}}  {{:>{}}}{{}}'
		fmt = fmt.format( maxlen_t, maxlen_v, maxlen_int )
		for i, s in enumerate( lines ):
			lines[ i ] = fmt.format( *s )

		ecap = '\n '.join( lines )
		ecap = 'param  ExistingCapacity  :=\n {}\n\t;'.format( ecap )

	cap2act = Param_CapacityToActivity.objects.filter(
	  analysis=analysis,
	  technology__name__in=techs_prod  # to make tech is actually used
	)

	c2a = '# param CapacityToActivity := ... ;   # None specified in DB'
	if cap2act:
		lines = sorted( [
		    cta.technology.name,
		    str(int( cta.value )),
		    str(cta.value - int(cta.value))[1:]
		  ]
		  for cta in cap2act
		)

		maxlen_t   = max(map(len, (i[0] for i in lines) ))
		maxlen_int = max(map(len, (i[1] for i in lines) ))
		fmt = r'{{:<{}}}  {{:>{}}}{{}}'
		fmt = fmt.format( maxlen_t, maxlen_int )
		for i, s in enumerate( lines ):
			lines[ i ] = fmt.format( *s )

		c2a = '\n '.join( lines )
		c2a = 'param  CapacityToActivity  :=\n {}\n\t;'.format( c2a )

	capfactech = Param_CapacityFactorTech.objects.filter(
	  timeslice__analysis=analysis,
	  technology__name__in=techs_prod  # make sure tech is actually used
	)

	cftech = '# param CapacityFactorTech := ... ;   # None specified in DB'
	if capfactech:
		lines = [ [
		    cft.timeslice.season,
		    cft.timeslice.time_of_day,
		    cft.technology.name,
		    str(int( cft.value )),
		    str(cft.value - int(cft.value))[1:]
		  ]
		  for cft in capfactech
		]
		lines.sort( key=itemgetter(2, 0, 1) )

		maxlen_s   = max(map(len, (i[0] for i in lines) ))
		maxlen_d   = max(map(len, (i[1] for i in lines) ))
		maxlen_t   = max(map(len, (i[2] for i in lines) ))
		maxlen_int = max(map(len, (i[3] for i in lines) ))
		fmt = r'{{:<{}}}  {{:<{}}}  {{:<{}}}  {{:>{}}}{{}}'
		fmt = fmt.format( maxlen_s, maxlen_d, maxlen_t, maxlen_int )
		for i, s in enumerate( lines ):
			lines[ i ] = fmt.format( *s )

		cftech = '\n '.join( lines )
		cftech = 'param  CapacityToActivity  :=\n {}\n\t;'.format( cftech )

	costinvest = Process.objects.filter(
	  id__in=process_ids,
	  vintage__vintage__gte=analysis.period_0,
	  costinvest__gt=0,
	)

	ci = '# param CostInvest := ... ;   # None specified in DB'
	if costinvest:
		lines = sorted( [
		    i.technology.name,
		    str(i.vintage.vintage),
		    str(int(i.costinvest)),
		    str(i.costinvest - int(i.costinvest))[1:],
		  ]
		  for i in costinvest
		)

		maxlen_t   = max(map(len, (i[0] for i in lines) ))
		maxlen_v   = max(map(len, (i[1] for i in lines) ))
		maxlen_int = max(map(len, (i[2] for i in lines) ))
		fmt = r'{{:<{}}}  {{:<{}}}  {{:>{}}}{{}}'
		fmt = fmt.format( maxlen_t, maxlen_v, maxlen_int )
		for i, s in enumerate( lines ):
			lines[ i ] = fmt.format( *s )

		ci = '\n '.join( lines )
		ci = 'param  CostInvest  :=\n {}\n\t;'.format( ci )

	costfixed = Param_CostFixed.objects.filter(
	  period__vintage__gt=analysis.period_0,
	  process_id__in=process_ids,
	  value__gt=0
	)

	cf = '# param CostFixed := ... ;   # None specified in DB'
	if costfixed:
		lines = sorted( [
		    str(i.period.vintage),
		    i.process.technology.name,
		    str(i.process.vintage.vintage),
		    str(int(i.value)),
		    str(i.value - int(i.value))[1:],
		  ]
		  for i in costfixed
		)

		maxlen_p   = max(map(len, (i[0] for i in lines) ))
		maxlen_t   = max(map(len, (i[1] for i in lines) ))
		maxlen_v   = max(map(len, (i[2] for i in lines) ))
		maxlen_int = max(map(len, (i[3] for i in lines) ))
		fmt = r'{{:<{}}}  {{:<{}}}  {{:<{}}}  {{:>{}}}{{}}'
		fmt = fmt.format( maxlen_p, maxlen_t, maxlen_v, maxlen_int )
		for i, s in enumerate( lines ):
			lines[ i ] = fmt.format( *s )

		cf = '\n '.join( lines )
		cf = 'param  CostFixed  :=\n {}\n\t;'.format( cf )

	costvariable = Param_CostVariable.objects.filter(
	  process_id__in=process_ids,
	  period__vintage__gt=analysis.period_0,
	  value__gt=0
	)

	cv = '# param CostVariable := ... ;   # None specified in DB'
	if costvariable:
		lines = sorted( [
		    str(i.period.vintage),
		    i.process.technology.name,
		    str(i.process.vintage.vintage),
		    str(int(i.value)),
		    str(i.value - int(i.value))[1:],
		  ]
		  for i in costvariable
		)

		maxlen_p   = max(map(len, (i[0] for i in lines) ))
		maxlen_t   = max(map(len, (i[1] for i in lines) ))
		maxlen_v   = max(map(len, (i[2] for i in lines) ))
		maxlen_int = max(map(len, (i[3] for i in lines) ))
		fmt = r'{{:<{}}}  {{:<{}}}  {{:<{}}}  {{:>{}}}{{}}'
		fmt = fmt.format( maxlen_p, maxlen_t, maxlen_v, maxlen_int )
		for i, s in enumerate( lines ):
			lines[ i ] = fmt.format( *s )

		cv = '\n '.join( lines )
		cv = 'param  CostVariable  :=\n {}\n\t;'.format( cv )

	tech_life = Param_LifetimeTech.objects.filter(
	  analysis=analysis,
	  technology__name__in=techs_prod
	)

	tlife = '# param LifetimeTech := ... ;   # None specified in DB'
	if tech_life:
		lines = sorted( [
		    tl.technology.name,
		    str(int(tl.value)),
		    str(tl.value - int(tl.value))[1:],
		  ]
		  for tl in tech_life
		)

		maxlen_t   = max(map(len, (i[0] for i in lines) ))
		maxlen_int = max(map(len, (i[1] for i in lines) ))
		fmt = r'{{:<{}}}  {{:>{}}}{{}}'
		fmt = fmt.format( maxlen_t, maxlen_int )
		for i, s in enumerate( lines ):
			lines[ i ] = fmt.format( *s )

		tlife = '\n '.join( lines )
		tlife = 'param  LifetimeTech  :=\n {}\n\t;'.format( tlife )

	process_life = Process.objects.filter(
	  id__in=process_ids,
	  lifetime__gt=0
	)

	plife = '# param LifetimeProcess := ... ;   # None specified in DB'
	if process_life:
		lines = sorted( [
		    pl.technology.name,
		    str(pl.vintage.vintage),
		    str(int(pl.lifetime)),
		    str(pl.lifetime - int(pl.lifetime))[1:],
		  ]
		  for pl in process_life
		)

		maxlen_t   = max(map(len, (i[0] for i in lines) ))
		maxlen_v   = max(map(len, (i[1] for i in lines) ))
		maxlen_int = max(map(len, (i[2] for i in lines) ))
		fmt = r'{{:<{}}}  {{:<{}}}  {{:>{}}}{{}}'
		fmt = fmt.format( maxlen_t, maxlen_v, maxlen_int )
		for i, s in enumerate( lines ):
			lines[ i ] = fmt.format( *s )

		plife = '\n '.join( lines )
		plife = 'param  LifetimeProcess  :=\n {}\n\t;'.format( plife )

	tech_loanlife = Param_LifetimeTechLoan.objects.filter(
	  analysis=analysis,
	  technology__name__in=techs_prod,
	  value__gt=0
	)

	tllife = '# param LifetimeLoanTech := ... ;   # None specified in DB'
	if tech_loanlife:
		lines = sorted( [
		    tll.technology.name,
		    str(int(tll.value)),
		    str(tll.value - int(tll.value))[1:],
		  ]
		  for tll in tech_life
		)

		maxlen_t   = max(map(len, (i[0] for i in lines) ))
		maxlen_int = max(map(len, (i[1] for i in lines) ))
		fmt = r'{{:<{}}}  {{:>{}}}{{}}'
		fmt = fmt.format( maxlen_t, maxlen_int )
		for i, s in enumerate( lines ):
			lines[ i ] = fmt.format( *s )

		tllife = '\n '.join( lines )
		tllife = 'param  LifetimeLoanTech  :=\n {}\n\t;'.format( tllife )

	process_loanlife = Process.objects.filter(
	  id__in=process_ids,
	  loanlife__gt=0
	)

	pllife = '# param LifetimeLoanProcess := ... ;   # None specified in DB'
	if process_loanlife:
		lines = sorted( [
		    pl.technology.name,
		    str(pl.vintage.vintage),
		    str(int(pl.loanlife)),
		    str(pl.loanlife - int(pl.loanlife))[1:],
		  ]
		  for pl in process_loanlife
		)

		maxlen_t   = max(map(len, (i[0] for i in lines) ))
		maxlen_v   = max(map(len, (i[1] for i in lines) ))
		maxlen_int = max(map(len, (i[2] for i in lines) ))
		fmt = r'{{:<{}}}  {{:<{}}}  {{:>{}}}{{}}'
		fmt = fmt.format( maxlen_t, maxlen_v, maxlen_int )
		for i, s in enumerate( lines ):
			lines[ i ] = fmt.format( *s )

		pllife = '\n '.join( lines )
		pllife = 'param  LifetimeLoanProcess  :=\n {}\n\t;'.format( pllife )

	tis = '# param TechInputSplit := ... ;   # None specified in DB'
	tos = '# param TechOutputSplit := ... ;   # None specified in DB'

	tech_is = Param_TechInputSplit.objects.filter(
	  inp_commodity__analysis=analysis,
	  technology__name__in=techs_prod,
	  fraction__gt=0
	)
	tech_os = Param_TechOutputSplit.objects.filter(
	  out_commodity__analysis=analysis,
	  technology__name__in=techs_prod,
	  fraction__gt=0
	)

	if tech_is:
		lines = sorted( [
		    inps.inp_commodity.commodity.name,
		    inps.technology.name,
		    str(int(inps.fraction)),
		    str(inps.fraction - int(inps.fraction))[1:]
		  ]
		  for inps in tech_is
		)

		maxlen_c   = max(map(len, (i[0] for i in lines) ))
		maxlen_t   = max(map(len, (i[1] for i in lines) ))
		maxlen_int = max(map(len, (i[2] for i in lines) ))
		fmt = r'{{:<{}}}  {{:<{}}}  {{:>{}}}{{}}'
		fmt = fmt.format( maxlen_c, maxlen_t, maxlen_int )
		for i, s in enumerate( lines ):
			lines[ i ] = fmt.format( *s )

		tis = '\n '.join( lines )
		tis = 'param  TechInputSplit  :=\n {}\n\t;'.format( tis )

	if tech_os:
		lines = sorted( [
		    outs.technology.name,
		    outs.out_commodity.commodity.name,
		    str(int(outs.fraction)),
		    str(outs.fraction - int(outs.fraction))[1:]
		  ]
		  for outs in tech_os
		)

		maxlen_t   = max(map(len, (i[0] for i in lines) ))
		maxlen_c   = max(map(len, (i[1] for i in lines) ))
		maxlen_int = max(map(len, (i[2] for i in lines) ))
		fmt = r'{{:<{}}}  {{:<{}}}  {{:>{}}}{{}}'
		fmt = fmt.format( maxlen_t, maxlen_c, maxlen_int )
		for i, s in enumerate( lines ):
			lines[ i ] = fmt.format( *s )

		tos = '\n '.join( lines )
		tos = 'param  TechOutputSplit  :=\n {}\n\t;'.format( tos )

	maxcap = '# param MaxCapacity := ... ;   # None specified in DB'
	mincap = '# param MinCapacity := ... ;   # None specified in DB'

	max_caps = Param_MaxCapacity.objects.filter(
	  period__analysis=analysis,
	  period__vintage__gte=analysis.period_0,
	  technology__name__in=techs_prod
	)
	min_caps = Param_MinCapacity.objects.filter(
	  period__analysis=analysis,
	  period__vintage__gte=analysis.period_0,
	  technology__name__in=techs_prod
	)

	if max_caps:
		lines = [ [
		    str(mc.period.vintage),
		    mc.technology.name,
		    str(int(mc.value)),
		    str(mc.value - int(mc.value))[1:]
		  ]
		  for mc in max_caps
		]
		lines.sort( key=itemgetter(1, 0) )

		maxlen_p   = max(map(len, (i[0] for i in lines) ))
		maxlen_t   = max(map(len, (i[1] for i in lines) ))
		maxlen_int = max(map(len, (i[2] for i in lines) ))
		fmt = r'{{:<{}}}  {{:<{}}}  {{:>{}}}{{}}'
		fmt = fmt.format( maxlen_p, maxlen_t, maxlen_int )
		for i, s in enumerate( lines ):
			lines[ i ] = fmt.format( *s )

		maxcap = '\n '.join( lines )
		maxcap = 'param  MaxCapacity  :=\n {}\n\t;'.format( maxcap )

	if min_caps:
		lines = [ [
		    str(mc.period.vintage),
		    mc.technology.name,
		    str(int(mc.value)),
		    str(mc.value - int(mc.value))[1:]
		  ]
		  for mc in min_caps
		]
		lines.sort( key=itemgetter(1, 0) )

		maxlen_p   = max(map(len, (i[0] for i in lines) ))
		maxlen_t   = max(map(len, (i[1] for i in lines) ))
		maxlen_int = max(map(len, (i[2] for i in lines) ))
		fmt = r'{{:<{}}}  {{:<{}}}  {{:>{}}}{{}}'
		fmt = fmt.format( maxlen_p, maxlen_t, maxlen_int )
		for i, s in enumerate( lines ):
			lines[ i ] = fmt.format( *s )

		mincap = '\n '.join( lines )
		mincap = 'param  MinCapacity  :=\n {}\n\t;'.format( mincap )

	growthrate = Param_GrowthRate.objects.filter(
	  analysis=analysis,
	  technology__name__in=techs_prod,
	  ratelimit__gt=0
	)

	grm = '# param GrowthRateMax := ... ;   # None specified in DB'
	grs = '# param GrowthRateSeed := ... ;   # None specified in DB'
	if growthrate:
		lines = sorted( [
		    gr.technology.name,
		    str(int(gr.ratelimit)),
		    str(gr.ratelimit - int(gr.ratelimit))[1:]
		  ]
		  for gr in growthrate
		)

		maxlen_t   = max(map(len, (i[0] for i in lines) ))
		maxlen_int = max(map(len, (i[1] for i in lines) ))
		fmt = r'{{:<{}}}  {{:>{}}}{{}}'
		fmt = fmt.format( maxlen_t, maxlen_int )
		for i, s in enumerate( lines ):
			lines[ i ] = fmt.format( *s )

		grm = '\n '.join( lines )
		grm = 'param  GrowthRateMax  :=\n {}\n\t;'.format( grm )

		lines = sorted( [
		    gr.technology.name,
		    str(int(gr.seed)),
		    str(gr.seed - int(gr.seed))[1:]
		  ]
		  for gr in growthrate
		)

		maxlen_t   = max(map(len, (i[0] for i in lines) ))
		maxlen_int = max(map(len, (i[1] for i in lines) ))
		fmt = r'{{:<{}}}  {{:>{}}}{{}}'
		fmt = fmt.format( maxlen_t, maxlen_int )
		for i, s in enumerate( lines ):
			lines[ i ] = fmt.format( *s )

		grs = '\n '.join( lines )
		grs = 'param  GrowthRateSeed  :=\n {}\n\t;'.format( grs )

	data = dat_format.format(
		url         = req.build_absolute_uri(),
		user        = req.user.username,
		analysis_name = analysis.name,
		analysis_description = twrapper.fill( analysis.description ),
		set_periods = set_periods,
		time_season = time_season,
		time_of_day = time_of_day,
		segfrac     = segfrac,
		tech_production = tech_production,
		tech_baseload   = tech_baseload,
		tech_storage    = tech_storage,
		commodity_demand   = c_demand,
		commodity_emission = c_emission,
		commodity_physical = c_physical,
		demanddefaultdistribution  = ddd,
		demandspecificdistribution = dsd,
		demand      = dem,
		efficiency  = eff,
		emissionactivity = ems,
		existingcapacity = ecap,
		capacitytoactivity = c2a,
		capacityfactortech = cftech,
		costinvest   = ci,
		costfixed    = cf,
		costvariable = cv,
		lifetimetech = tlife,
		processlife  = plife,
		lifetimeloantech = tllife,
		processloanlife  = pllife,
		techinputsplit  = tis,
		techoutputsplit = tos,
		maxcapacity = maxcap,
		mincapacity = mincap,
		growthratemax  = grm,
		growthrateseed = grs,
		gdr         = analysis.global_discount_rate,
	)
	res = HttpResponse( data, content_type='text/plain' )
	res['Content-Length'] = len( data );

	return res

