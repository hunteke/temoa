from cStringIO import StringIO

try:
	from coopr.pyomo import *
except:

	import os, sys
	ppath = '/path/to/coopr/bin'
	path = """Option 1:
$ PATH=%(ppath)s:$PATH
$ which python

Option 2:
$ %(ppath)s/python  %(base)s  ...
"""
	if 'win' in sys.platform:
		ppath = 'C:\\path\\to\\coopr\\bin'
		path = """Option 1:
C:\\> set PATH=%(ppath)s:%%PATH%%
C:\\> python  %(base)s  ...

Option 2:
C:\\> %(ppath)s\\python  %(base)s  ...
"""

	base = os.path.basename( sys.argv[0] )
	path %= { 'ppath' : ppath, 'base' : base }
	msg = """\
Unable to find coopr.pyomo on the Python system path.  Are you running Coopr's
version of Python?  Here is one way to check:

  # look for items that have to do with the Coopr project
python -c "import sys, pprint; pprint.pprint(sys.path)"

If you aren't running with Coopr's environment for Python, you'll need to either
update your PATH environment variable to use Coopr's Python setup, or always
explicitly use the Coopr path:

%s
"""

	raise ImportError, msg % path


###############################################################################
# Temoa rule "partial" functions (excised from indidivual constraints for
#   readability)

def CommodityBalanceConstraintErrorCheck (
  l_vflow_out, l_vflow_in, A_carrier, A_season, A_time_of_day, A_period
):
	if type(l_vflow_out) == type(l_vflow_in):
		if int is type(l_vflow_out):
			# Tell Pyomo not to create this constraint; it's useless because both
			# of the flows are 0.  i.e. carrier not needed and nothing makes it.
			return None
	elif int is type(l_vflow_out):
		flow_in_expr = StringIO()
		l_vflow_in.pprint( ostream=flow_in_expr )
		msg = "Unable to meet an interprocess '%s' transfer in (%s, %s, %s).\n" \
		  "No flow out.  Constraint flow in:\n   %s\n"                          \
		  "Possible reasons:\n"                                                 \
		  " - Is there a missing period in set 'time_period'?\n"                \
		  " - Is there a missing tech in set 'resource_tech'?\n"                \
		  " - Is there a missing tech in set 'production_tech'?\n"              \
		  " - Is there a missing commodity in set 'commodity_physical'?\n"      \
		  " - Are there missing entries in the Efficiency parameter?\n"         \
		  " - Does a tech need a longer Lifetime parameter setting?"
		raise ValueError, msg % (A_carrier, A_season, A_time_of_day, A_period,
		                         flow_in_expr.getvalue() )


def DemandConstraintErrorCheck (
  l_supply, A_comm, A_period, A_season, A_time_of_day
):
	if int is type( l_supply ):
		msg = "Error: Demand '%s' for (%s, %s, %s) unable to be met by any "   \
		  "technology.\n\tPossible reasons:\n"                                 \
		  " - Is the Efficiency parameter missing an entry for this demand?\n" \
		  " - Does a tech that satisfies this demand need a longer Lifetime?\n"
		raise ValueError, msg % (A_comm, A_period, A_season, A_time_of_day)

# End Temoa rule "partials"
###############################################################################

##############################################################################
# Begin validation and initialization routines

def validate_periods ( M ):
	""" Ensure that the time_exist < time_horizon < time_future """
	exist    = max( M.time_exist )
	horizonl = min( M.time_horizon )  # horizon "low"
	horizonh = max( M.time_horizon )  # horizon "high"
	future   = min( M.time_future )

	if not ( exist < horizonl ):
		msg = "All items in time_horizon must be larger that in time_exist.\n"  \
		      "time_exist max:   %s\ntime_horizon min: %s"
		raise ValueError, msg % (exist, horizonl)
	elif not ( horizonh < future ):
		msg = "All items in time_future must be larger that in time_horizon.\n" \
		      "time_horizon max:   %s\ntime_future min: %s"
		raise ValueError, msg % (horizonh, future)

	return tuple()

def init_set_time_optimize ( M ):
	items = sorted( year for year in M.time_horizon )
	items.extend( sorted( year for year in M.time_future ) )
	return items[:-1]

# end validation and initialization routines
##############################################################################

##############################################################################
# Begin helper functions

# Global Variables (dictionaries to cache parsing of Efficiency parameter)
g_processInputs  = dict()
g_processOutputs = dict()

def InitProcessParams ( M ):
	global g_processInputs
	global g_processOutputs

	for l_vintage in M.vintage_all:
		for l_tech in M.tech_all:
			for l_inp in M.commodity_physical:
				for l_out in M.commodity_all:

					eindex = (l_inp, l_tech, l_vintage, l_out)
					if M.Efficiency[ eindex ] > 0:
						for l_period in M.time_optimize:
							if l_period < l_vintage: continue
							l_lifetime = value( M.Lifetime[l_tech, l_vintage] )
							if l_period > l_vintage + l_lifetime: continue

							pindex = (l_period, l_tech, l_vintage)
							if pindex not in g_processInputs:
								g_processInputs[  pindex ] = set()
								g_processOutputs[ pindex ] = set()
							g_processInputs[ pindex ].add( l_inp )
							g_processOutputs[pindex ].add( l_out )


def ProcessOutputs ( *index ):
	"""\
index = (period, tech, vintage)
	"""
	if index in g_processOutputs:
		return g_processOutputs[ index ]
	return set()


def ProcessInputs ( *index ):
	if index in g_processInputs:
		return g_processInputs[ index ]
	return set()


def ProcessInputsByOutput ( index, A_output ):
	"""\
Return the set of input energy carriers used by a technology (A_tech) to
produce a given output carrier (A_output).
"""
	if index in g_processOutputs:
		if A_output in g_processOutputs[ index ]:
			return g_processInputs[ index ]

	return set()


def ProcessOutputsByInput ( index, A_input ):
	"""\
Return the set of output energy carriers used by a technology (A_tech) to
produce a given input carrier (A_output).
"""
	if index in g_processInputs:
		if A_input in g_processInputs[ index ]:
			return g_processOutputs[ index ]

	return set()


def isValidProcess( A_period, A_inp, A_tech, A_vintage, A_out ):
	"""\
Returns a boolean (True or False) indicating whether, in any given period, a technology can take a specified input carrier and convert it to and specified output carrier.
"""
	index = (A_period, A_tech, A_vintage)
	if index in g_processInputs and index in g_processOutputs:
		if A_inp in g_processInputs[ index ]:
			if A_out in g_processOutputs[ index ]:
				return True

	return False

# End helper functions
##############################################################################

###############################################################################
# Miscellaneous routines

def parse_args ( ):
	import argparse

	parser = argparse.ArgumentParser()

	parser.add_argument('dot_dat',
	  type=str,
	  nargs='+',
	  help='AMPL-format data file(s) with which to create a model instance. e.g. "data.dat"'
	)

	options = parser.parse_args()
	return options

# End miscellaneous routines
###############################################################################

###############################################################################
# Direct invocation methods (when modeler runs via "python model.py ..."

def temoa_solve ( model ):
	from sys import argv, stderr, stdout

	from coopr.opt import SolverFactory
	from coopr.pyomo import ModelData

	from pformat_results import pformat_results

	SE, SO = stderr.write, stdout.write

	options = parse_args()
	dot_dats = options.dot_dat

	opt = SolverFactory('glpk_experimental')
	opt.keepFiles = False
	# opt.options.wlp = "temoa_model.lp"  # output GLPK LP understanding of model

	# Recreate the pyomo command's ability to specify multiple "dot dat" files
	# on the command line
	mdata = ModelData()
	for f in dot_dats:
		if f[-4:] != '.dat':
			SE( "Expecting a dot dat (data.dat) file, found %s\n" % f )
			raise SystemExit
		mdata.add( f )
	mdata.read( model )

	# Now do the solve and ...
	instance = model.create( mdata )
	result = opt.solve( instance )

	# ... print the easier-to-read/parse format
	SO( pformat_results( instance, result ) )


# End direct invocation methods
###############################################################################