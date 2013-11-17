## Download ###################################################################

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache

from decorators.http import require_GET

from IPython import embed as II

from models import (
  Analysis,
  Param_Efficiency,
  Param_SegFrac,
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

{tech_production}

{segfrac}


param  GlobalDiscountRate  :=  {gdr} ;

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
	existing = [ v.vintage for v in vintages if v.vintage < analysis.period_0 ]
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

	efficiencies = Param_Efficiency.objects.filter( process__analysis=analysis )
	techs = sorted(set( e.process.technology.name
	  for e in efficiencies
	))

	tech_production = '# set tech_production := ... ;   # No flows (efficiencies) in DB'
	if techs:
		tech_production = '\n '.join( techs )
		tech_production = 'set  tech_production  :=\n {}\n\t;'.format( tech_production )

	data = dat_format.format(
		url         = req.build_absolute_uri(),
		user        = req.user.username,
		analysis_name = analysis.name,
		analysis_description = twrapper.fill( analysis.description ),
		set_periods = set_periods,
		time_season = time_season,
		time_of_day = time_of_day,
		tech_production = tech_production,
		segfrac     = segfrac,
		gdr         = analysis.global_discount_rate,
	)
	res = HttpResponse( data, content_type='text/plain' )
	res['Content-Length'] = len( data );

	return res

