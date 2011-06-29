from cStringIO import StringIO
from sys import argv, stderr as SE, stdout as SO

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
	if int is type(l_vflow_out):
		flow_in_expr = StringIO()
		l_vflow_in.pprint( ostream=flow_in_expr )
		msg = "Unable to meet an interprocess '%s' transfer in (%s, %s, %s).\n" \
		  "No flow out.  Constraint flow in:\n   %s\n"                          \
		  "Possible reasons:\n"                                                 \
		  " - Is there a missing period in set 'time_horizon'?\n"               \
		  " - Is there a missing tech in set 'tech_resource'?\n"                \
		  " - Is there a missing tech in set 'tech_production'?\n"              \
		  " - Is there a missing commodity in set 'commodity_physical'?\n"      \
		  " - Are there missing entries in the Efficiency parameter?\n"         \
		  " - Does a tech need a longer LifetimeTech parameter setting?"
		raise ValueError, msg % (A_carrier, A_season, A_time_of_day, A_period,
		                         flow_in_expr.getvalue() )


def DemandConstraintErrorCheck (
  l_supply, A_comm, A_period, A_season, A_time_of_day
):
	if int is type( l_supply ):
		msg = "Error: Demand '%s' for (%s, %s, %s) unable to be met by any "    \
		  "technology.\n\tPossible reasons:\n"                                  \
		  " - Is the Efficiency parameter missing an entry for this demand?\n"  \
		  " - Does a tech that satisfies this demand need a longer LifetimeTech?"\
		  "\n"
		raise ValueError, msg % (A_comm, A_period, A_season, A_time_of_day)

# End Temoa rule "partials"
###############################################################################

##############################################################################
# Begin validation and initialization routines

def validate_time ( M ):
	from sys import maxint

	if not len( M.time_horizon ):
		msg = 'Set "time_horizon" is empty!  Please specify at least one '      \
		      'period in set time_horizon.'
		raise ValueError, msg

	if not len( M.time_future ):
		msg = 'Set "time_future" is empty!  Please specify at least one year ' \
		      'in set time_future, so that the model may ascertain a final '   \
		      'period length for optimization and economic accounting.'
		raise ValueError, msg

	""" Ensure that the time_exist < time_horizon < time_future """
	exist    = len( M.time_exist ) and max( M.time_exist ) or -maxint
	horizonl = min( M.time_horizon )  # horizon "low"
	horizonh = max( M.time_horizon )  # horizon "high"
	future   = min( M.time_future )

	if not ( exist < horizonl ):
		msg = "All items in time_horizon must be larger that in time_exist.\n"  \
		      "time_exist max:   %s\ntime_horizon min: %s"
		raise ValueError, msg % (exist, horizonl)
	elif not ( horizonh < future ):
		msg = "All items in time_future must be larger that in time_horizon.\n" \
		      "time_horizon max:   %s\ntime_future min:    %s"
		raise ValueError, msg % (horizonh, future)

	return tuple()


def validate_SegFrac ( M ):

	total = sum( M.SegFrac.data().values() )

	if abs(float(total) - 1.0) > 1e-15:
		# We can't explicitly test for "!= 1.0" because of incremental roundoff
		# errors inherent in float manipulations and representations, so instead
		# compare against an epsilon value of "close enough".
		items = '\n   '.join( "%s: %s" % ii for ii in M.SegFrac.data().items() )

		msg = 'The values of the SegFrac parameter do not sum to 1.  Each item '\
		   'in SegFrac represents a fraction of a year, so they must total to ' \
		   '1.  Current values:\n   %s\n\tsum = %s'
		raise ValueError, msg % (items, total)

	return tuple()


def init_set_time_optimize ( M ):
	items = list( M.time_horizon )
	items.extend( list( M.time_future ) )

	return items[:-1]


def init_set_vintage_exist ( M ):
	return list( M.time_exist )


def init_set_vintage_future ( M ):
	return list( M.time_future )


def init_set_vintage_optimize ( M ):
	return list( M.time_optimize )


def init_set_vintage_all ( M ):
	return list( M.time_all )

# end validation and initialization routines
##############################################################################

##############################################################################
# Begin helper functions

# Global Variables (dictionaries to cache parsing of Efficiency parameter)
g_processInputs  = dict()
g_processOutputs = dict()
g_processVintages = dict()
g_processLoans = dict()

def InitializeProcessParameters ( M ):
	global g_processInputs
	global g_processOutputs
	global g_processVintages
	global g_processLoans

	l_first_period = min( M.time_horizon )

	for l_vintage in M.vintage_all:
		for l_tech in M.tech_all:
			l_process = (l_tech, l_vintage)
			l_lifetime = value( M.LifetimeTech[ l_process ] )

			if l_vintage in M.time_exist:
				# if existing tech & capacity is 0, don't include it
				if 0 == M.ExistingCapacity[ l_process ]: continue

				if l_vintage + l_lifetime <= l_first_period:
					msg = '\nNotice: %s specified as ExistingCapacity, but its '   \
					   'LifetimeTech parameter does not extend past the beginning '\
					   'of time_horizon.  (i.e. useless parameter)'                \
					   '\n\tLifetime:     %s'                                      \
					   '\n\tFirst period: %s\n'
					SE.write( msg % (l_process, l_lifetime, l_first_period) )

			for l_inp in M.commodity_physical:
				for l_out in M.commodity_carrier:

					eindex = (l_inp, l_tech, l_vintage, l_out)
					if M.Efficiency[ eindex ] > 0:
						for l_period in M.time_optimize:
							# can't build a vintage before it's been invented
							if l_period < l_vintage: continue

							if l_vintage in M.time_optimize:
								l_loan_life = value(M.LifetimeLoan[ l_process ])
								if l_vintage + l_loan_life > l_period:
									g_processLoans[l_period, l_tech, l_vintage] = True

							# if tech is no longer "alive", don't include it
							if l_vintage + l_lifetime <= l_period: continue

							pindex = (l_period, l_tech, l_vintage)
							if pindex not in g_processInputs:
								g_processInputs[  pindex ] = set()
								g_processOutputs[ pindex ] = set()
							if (l_period, l_tech) not in g_processVintages:
								g_processVintages[l_period, l_tech] = set()

							g_processVintages[l_period, l_tech].add( l_vintage )
							g_processInputs[ pindex ].add( l_inp )
							g_processOutputs[pindex ].add( l_out )

	return set()


def ProcessOutputs ( A_period, A_tech, A_vintage ):
	"""\
index = (period, tech, vintage)
	"""
	index = (A_period, A_tech, A_vintage)
	if index in g_processOutputs:
		return g_processOutputs[ index ]
	return set()


def ProcessInputs ( A_period, A_tech, A_vintage ):
	index = (A_period, A_tech, A_vintage)
	if index in g_processInputs:
		return g_processInputs[ index ]
	return set()


def ProcessInputsByOutput ( A_period, A_tech, A_vintage, A_output ):
	"""\
Return the set of input energy carriers used by a technology (A_tech) to
produce a given output carrier (A_output).
"""
	index = (A_period, A_tech, A_vintage)
	if index in g_processOutputs:
		if A_output in g_processOutputs[ index ]:
			return g_processInputs[ index ]

	return set()


def ProcessOutputsByInput ( A_period, A_tech, A_vintage, A_input ):
	"""\
Return the set of output energy carriers used by a technology (A_tech) to
produce a given input carrier (A_output).
"""
	index = (A_period, A_tech, A_vintage)
	if index in g_processInputs:
		if A_input in g_processInputs[ index ]:
			return g_processOutputs[ index ]

	return set()


def ProcessesByPeriodAndInput ( M, A_period, A_inp ):
	"""\
This function relies on the Model (argument M).  I'd like to update at some point to not rely on th emodel
"""
	processes = set()
	for l_tech in M.tech_all:
		for l_vin in M.vintage_all:
			index = (A_period, l_tech, l_vin)
			if index in g_processInputs and A_inp in g_processInputs[ index ]:
					processes.add( (l_tech, l_vin) )

	return processes


def ProcessesByPeriodAndOutput ( M, A_period, A_out ):
	"""\
This function relies on the Model (argument M).  I'd like to update at some point to not rely on th emodel
"""
	processes = set()
	for l_tech in M.tech_all:
		for l_vin in M.vintage_all:
			index = (A_period, l_tech, l_vin)
			if index in g_processOutputs and A_out in g_processOutputs[ index ]:
					processes.add( (l_tech, l_vin) )

	return processes


def ProcessVintages ( A_per, A_tech ):
	index = (A_per, A_tech)
	if index in g_processVintages:
		return g_processVintages[ index ]

	return set()


def isValidProcess ( A_period, A_inp, A_tech, A_vintage, A_out ):
	"""\
Returns a boolean (True or False) indicating whether, in any given period, a
technology can take a specified input carrier and convert it to and specified
output carrier.
"""
	index = (A_period, A_tech, A_vintage)
	if index in g_processInputs and index in g_processOutputs:
		if A_inp in g_processInputs[ index ]:
			if A_out in g_processOutputs[ index ]:
				return True

	return False


def loanIsActive ( A_period, A_tech, A_vintage ):
	"""\
Return a boolean (True or False) whether a loan is still active in a period.
This is the implementation of imat in the rest of the documentation.
"""
	return (A_period, A_tech, A_vintage) in g_processLoans

# End helper functions
##############################################################################

##############################################################################
# Begin Graphviz routines

def _getLen ( key ):
	def wrapped ( obj ):
		return len(obj[ key ])
	return wrapped

def create_text_nodes ( nodes ):
	"""\
This routine returns a set of text nodes in Graphviz DOT format, optimally
padded for easier reading and debugging.
	"""
	maxl = max(map(_getLen(0), nodes))
	nfmt = '\n\t{0:<%d} [ {1} ];' % maxl      # node text format

	return ''.join(sorted(set( nfmt.format( n, a ) for n, a in nodes )))

def create_text_edges ( edges ):
	"""\
This routine returns a set of text edge definitions in Graphviz DOT format,
optimally padded for easier reading and debugging.
	"""
	icolor, ocolor = 'firebrick', 'forestgreen'

	# edges is a list valid process tuples.
	# e.g. [(inp1, tech1, out1), (inp2, tech2, out2), ...]

	# Step 1: for alignment, get max length of items on left and right side of
	# graph operator token ('->')
	maxl = max( max(map(_getLen(0), edges)), max(map(_getLen(1), edges)) )
	maxr = max( max(map(_getLen(1), edges)), max(map(_getLen(2), edges)) )

	# Step 2: prepare format to be "\n\tinp_PADDING -> out_PADDING [..."
	efmt  = '\n\t{0:<%d} -> {1:<%d} [ color={2} ];'
	efmt %= (maxl, maxr)
	edge_inp = [ efmt.format( i, t, icolor ) for i, t, o in edges ]
	edge_out = [ efmt.format( t, o, ocolor ) for i, t, o in edges ]

	# Step 3: return a sorted list, removing duplicates with set()
	return ''.join(sorted(set(edge_inp + edge_out)))


def CreateModelDiagram ( pyomo_instance, fileformat ):
	"""\
These first couple versions of CreateModelDiagram do not fully work, and should
be thought of merely as "proof of concept" code.  They create Graphviz DOT files
and equivalent PDFs, but the graphics are not "correct" representations of the
model.  Specifically, there are currently a few artifacts and missing pieces:

Artifacts:
 * Though the graph is "roughly" a left-right DAG, certain pieces currently a
   swapped around, especially on the left-hand side of the image.  This makes
   the graph a bit harder to visually follow.
 * Especially with the birth of energy, there are a few cycles.  For example,
   with the way the model currently creates energy, the graph makes it seem as
   if 'imp_coal' also receives coal, when it should only export coal.

Initially known missing pieces:
 * How should the graph represent the notion of periods?
 * How should the graph represent the vintages?
 * Should the graph include time slices? (e.g. day, season)

Notes:
* For _any_ decently sized system, displaying this type of graph of the entire
  model will be infeasible, or effectively unusable.  We need a way to
  dynamically look at only subsections of the graph, while still giving a 10k'
  foot view of the overall system.

* We need to create a system that puts results into a database, or common result
  format, such that we can archive them for later.  In this manner, directly
  creating graphs at the point of model instantiation and running is not the
  right place.  Creating graphs needs to be a post processing action, and less
  tightly coupled (not coupled at all!) to the internal Pyomo data structure.
"""
	import os

	data = """\
// This file is generated by the --graph_format option of the Temoa model.  It
// is a Graphviz DOT language text description of a Temoa model instance.  For
// the curious, Graphviz will read this file to create an equivalent image in
// a number of formats, including SVG, PNG, GIF, and PDF.  For example, here
// is how one might invoke Graphviz to create an SVG image from the dot file.
//
// dot -Tsvg -o model.svg model.dot
//
// For more information, see the Graphviz homepage: http://graphviz.org/

strict digraph TemoaModel {
	rankdir = LR;       // The direction of the graph goes from Left to Right
	color   = black;    // currently unused; cluster outline color

	// Default node attributes, unless otherwise defined
	node [ shape=box, style=filled, color=lightblue, name=anode ];

	// Default edge attributes, unless otherwise defined
	edge [ labelfontcolor=lightgreen, arrowhead=vee, label="   " ];

	// Define individual node characteristics
%s

	// Define individual edges (and characteristics)
%s
}
"""
	M = pyomo_instance     # short for 'the generic model'

	tattr = 'color=darkseagreen'
	cattr = 'color=lightsteelblue, shape=circle'
	aattr = 'color=lightsteelblue, shape=circle'
	nodes  = list(set(
	(
	  '"(%s, %s, %s)"' % (l_per, l_tech, l_vin),
	  tattr
	)
	  for l_tech in M.tech_all
	  for l_inp  in M.commodity_all
	  for l_out  in M.commodity_all
	  for l_per  in M.time_horizon
	  for l_vin  in M.vintage_all
	  if isValidProcess( l_per, l_inp, l_tech, l_vin, l_out )
	))
	nodes.extend( (l_inp,  cattr) for l_inp in M.commodity_physical )
	nodes.extend( (l_out,  aattr) for l_out in M.commodity_all )
	nodes = create_text_nodes( nodes )

	edges = [
	(
	  '"%s"' % l_inp,
	  '"(%s, %s, %s)"' % (l_per, l_tech, l_vin),
	  '"%s"' % l_out
	)
	  for l_tech in M.tech_all
	  for l_inp  in M.commodity_all
	  for l_out  in M.commodity_all
	  for l_per  in M.time_horizon
	  for l_vin  in M.vintage_all
	  if isValidProcess( l_per, l_inp, l_tech, l_vin, l_out )
	]
	edges = create_text_edges( edges )

	dotfile = open( 'model.dot', 'w' )
	dotfile.write( data % (nodes, edges) )
	dotfile.close()

	# Outsource to Graphviz via the old Unix standby: temporary files
	ffmt = fileformat.lower()
	os.system('dot -T%(ffmt)s -o model.%(ffmt)s model.dot' % dict(ffmt=ffmt))

# End Graphviz routines
###############################################################################

###############################################################################
# Miscellaneous routines

def parse_args ( ):
	import argparse

	parser = argparse.ArgumentParser()

	parser.add_argument('dot_dat',
	  type=str,
	  nargs='+',
	  help='AMPL-format data file(s) with which to create a model instance. '  \
	       'e.g. "data.dat"'
	)

	parser.add_argument( '--graph_format',
	  help='Create a system-wide visual depiction of the model.  The '        \
	       'available options are the formats available to Graphviz.  To get '\
	       'a list of available formats, use the "dot" command: dot -Txxx. '  \
	       '[Default: None]',
	  action='store',
	  dest='graph_format',
	  default=None)
	options = parser.parse_args()
	return options

# End miscellaneous routines
###############################################################################

###############################################################################
# Direct invocation methods (when modeler runs via "python model.py ..."

def temoa_solve ( model ):
	from sys import argv, version_info

	if version_info < (2, 7):
		msg = "Temoa requires Python v2.7 or greater to run.\n\nIf you've "     \
		   "installed Coopr with Python 2.6 or less, you'll need to reinstall " \
		   "Coopr, taking care to install with a Python 2.7 (or greater) "      \
		   "executable."
		raise SystemExit, msg

	from time import clock

	from coopr.opt import SolverFactory
	from coopr.pyomo import ModelData

	from pformat_results import pformat_results

	options = parse_args()
	dot_dats = options.dot_dat

	opt = SolverFactory('glpk_experimental')
	opt.keepFiles = False
	opt.options.wlp = "temoa_model.lp"  # output GLPK LP understanding of model

	SE.write( '[        ] Reading data files.'); SE.flush()
	# Recreate the pyomo command's ability to specify multiple "dot dat" files
	# on the command line
	begin = clock()
	duration = lambda: clock() - begin

	mdata = ModelData()
	for f in dot_dats:
		if f[-4:] != '.dat':
			SE.write( "Expecting a dot dat (data.dat) file, found %s\n" % f )
			raise SystemExit
		mdata.add( f )
	mdata.read( model )
	SE.write( '\r[%8.2f\n' % duration() )

	SE.write( '[        ] Creating Temoa model instance.'); SE.flush()
	# Now do the solve and ...
	instance = model.create( mdata )
	SE.write( '\r[%8.2f\n' % duration() )

	SE.write( '[        ] Solving.'); SE.flush()
	result = opt.solve( instance )
	SE.write( '\r[%8.2f\n' % duration() )

	SE.write( '[        ] Formatting results.' ); SE.flush()
	# ... print the easier-to-read/parse format
	formatted_results = pformat_results( instance, result )
	SE.write( '\r[%8.2f\n' % duration() )
	SO.write( formatted_results )

	if options.graph_format:
		SE.write( '[        ] Creating Temoa model diagram ... ' ); SE.flush()
		CreateModelDiagram( instance, options.graph_format )
		SE.write( '\r[%8.2f\n' % duration() )

		#SE.write( '[        ] Creating Temoa model results diagram ... '); SE.flush()
		#instance.load( result )
		#CreateModelResultsDiagram( instance, options.graph_format )
		#SE.write( '\r[%8.2f\n' % duration() )


# End direct invocation methods
###############################################################################