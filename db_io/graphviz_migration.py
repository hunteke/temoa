from subprocess import call
from pyomo.core import value
from sys import argv, stderr as SE, stdout as SO
from shutil import rmtree
import argparse
import sqlite3
import os
import sys
import getopt
import re

try:
	from pyomo.core import (
	  AbstractModel, BuildAction, Constraint, NonNegativeReals, Reals, Objective, Param,
	  Set, Var, minimize, value
	)

except:
	msg = """
Unable to find 'pyomo.core' on the Python system path.  Are you running Pyomo's
version of Python?  Here is one way to check:

      # look for items that have to do with the Pyomo project
    python -c "import sys, pprint; pprint.pprint(sys.path)"

If you aren't running with Pyomo's environment for Python, you'll need to either
update your PATH environment variable to use Pyomo's Python setup, or always
explicitly use the Pyomo path.
"""

	raise ImportError( msg )

# Global Variables (dictionaries to cache parsing of Efficiency parameter)
g_processInputs  = dict()
g_processOutputs = dict()
g_processVintages = dict()
g_processLoans = dict()
g_activeFlow_psditvo = None
g_activeActivity_ptv = None
g_activeCapacity_tv = None
g_activeCapacityAvailable_pt = None
V_EnergyConsumptionByPeriodInputAndTech = {}
V_ActivityByPeriodTechAndOutput = dict()
V_EmissionActivityByPeriodAndTech = dict()
epsilon = 1e-9

M = AbstractModel( "TEMOA Entire Energy System Economic Optimization Model" )

M.time_exist    = Set( ordered=True )  # check for integerness performed
M.time_future   = Set( ordered=True )  # (with reasoning) in temoa_lib
M.time_optimize   = Set( ordered=True )
M.tech_all	= Set()
M.vintage_exist    = Set( ordered=True )
M.vintage_optimize = Set(ordered=True)
M.commodity_demand    = Set()
M.commodity_emissions = Set()
M.commodity_physical  = Set()
M.time_season     = Set()
M.time_of_day     = Set()
M.LifetimeProcess_tv = Set( dimen=2 )
M.LifetimeLoanProcess_tv = Set( dimen=2 )
M.EmissionActivity_eitvo = Set( dimen=5 )
M.CapacityVar_tv = Set( dimen=2 )
M.CapacityAvailableVar_pt = Set( dimen=2 )
M.ActivityByPeriodAndProcessVar_ptv = Set( dimen=3 )
M.FlowVar_psditvo = Set( dimen=7 )

def InitializeProcessParameters ( M ):
	global g_processInputs
	global g_processOutputs
	global g_processVintages
	global g_processLoans
	global g_activeFlow_psditvo
	global g_activeActivity_ptv
	global g_activeCapacity_tv
	global g_activeCapacityAvailable_pt

	l_first_period = min( M.time_future )
	l_exist_indices = M.ExistingCapacity.sparse_keys()
	l_used_techs = set()

	for i, t, v, o in M.Efficiency.sparse_iterkeys():
		l_process = (t, v)
		l_lifetime = value(M.LifetimeProcess[ l_process ])

		if v in M.vintage_exist:
			if l_process not in l_exist_indices:
				msg = ('Warning: %s has a specified Efficiency, but does not '
				  'have any existing install base (ExistingCapacity).\n')
				SE.write( msg % str(l_process) )
				continue
			if 0 == M.ExistingCapacity[ l_process ]:
				msg = ('Notice: Unnecessary specification of ExistingCapacity '
				  '%s.  If specifying a capacity of zero, you may simply '
				  'omit the declaration.\n')
				SE.write( msg % str(l_process) )
				continue
			if v + l_lifetime <= l_first_period:
				msg = ('\nWarning: %s specified as ExistingCapacity, but its '
				  'LifetimeProcess parameter does not extend past the beginning '
				  'of time_future.  (i.e. useless parameter)'
				  '\n\tLifetime:     %s'
				  '\n\tFirst period: %s\n')
				SE.write( msg % (l_process, l_lifetime, l_first_period) )
				continue

		eindex = (i, t, v, o)
		if 0 == M.Efficiency[ eindex ]:
			msg = ('\nNotice: Unnecessary specification of Efficiency %s.  If '
			  'specifying an efficiency of zero, you may simply omit the '
			  'declaration.\n')
			SE.write( msg % str(eindex) )
			continue

		l_used_techs.add( t )

		for p in M.time_optimize:
			# can't build a vintage before it's been invented
			if p < v: continue

			pindex = (p, t, v)

			if v in M.time_optimize:
				l_loan_life = value(M.LifetimeLoanProcess[ l_process ])
				if v + l_loan_life >= p:
					g_processLoans[ pindex ] = True

			# if tech is no longer "alive", don't include it
			if v + l_lifetime <= p: continue

			if pindex not in g_processInputs:
				g_processInputs[  pindex ] = set()
				g_processOutputs[ pindex ] = set()
			if (p, t) not in g_processVintages:
				g_processVintages[p, t] = set()

			g_processVintages[p, t].add( v )
			g_processInputs[ pindex ].add( i )
			g_processOutputs[pindex ].add( o )
	l_unused_techs = M.tech_all - l_used_techs
	if l_unused_techs:
		msg = ("Notice: '{}' specified as technology, but it is not utilized in "
		       'the Efficiency parameter.\n')
		for i in sorted( l_unused_techs ):
			SE.write( msg.format( i ))
	
	g_activeFlow_psditvo = set(
	  (p, s, d, i, t, v, o)

	  for p in M.time_optimize
	  for t in M.tech_all
	  for v in ProcessVintages( p, t )
	  for i in ProcessInputs( p, t, v )
	  for o in ProcessOutputs( p, t, v )
	  for s in M.time_season
	  for d in M.time_of_day
	)
	g_activeActivity_ptv = set(
	  (p, t, v)

	  for p in M.time_optimize
	  for t in M.tech_all
	  for v in ProcessVintages( p, t )
	)
	g_activeCapacity_tv = set(
	  (t, v)

	  for p in M.time_optimize
	  for t in M.tech_all
	  for v in ProcessVintages( p, t )
	)
	g_activeCapacityAvailable_pt = set(
	  (p, t)

	  for p in M.time_optimize
	  for t in M.tech_all
	  if ProcessVintages( p, t )
	)

def init_set_time_optimize ( M ):
	return sorted( M.time_future )[:-1]

def init_set_vintage_exist ( M ):
	return sorted( M.time_exist )

def init_set_vintage_optimize ( M ):
	return sorted( M.time_optimize )
	
def LifetimeProcessIndices ( M ):
	indices = set(
	  (t, v)

	  for i, t, v, o in M.Efficiency.sparse_iterkeys()
	)
	return indices

def LifetimeLoanProcessIndices ( M ):
	min_period = min( M.vintage_optimize )
	indices = set(
	  (t, v)

	  for i, t, v, o in M.Efficiency.sparse_iterkeys()
	  if v >= min_period
	)
	return indices

def ProcessInputs ( p, t, v ):
	index = (p, t, v)
	if index in g_processInputs:
		return g_processInputs[ index ]
	return set()


def ProcessOutputs ( p, t, v ):
	index = (p, t, v)
	if index in g_processOutputs:
		return g_processOutputs[ index ]
	return set()

def ProcessInputsByOutput ( p, t, v, o ):
	index = (p, t, v)
	if index in g_processOutputs:
		if o in g_processOutputs[ index ]:
			return g_processInputs[ index ]
	return set()

def ProcessOutputsByInput ( p, t, v, i ):
	index = (p, t, v)
	if index in g_processInputs:
		if i in g_processInputs[ index ]:
			return g_processOutputs[ index ]
	return set()

def ProcessesByInput ( i ):
	"""\
Returns the set of processes that take 'input'.  Note that a process is
conceptually a vintage of a technology.
"""
	processes = set(
	  (t, v)

	  for p, t, v in g_processInputs
	  if i in g_processInputs[p, t, v]
	)
	return processes

def ProcessesByOutput ( o ):
	"""\
Returns the set of processes that take 'output'.  Note that a process is
conceptually a vintage of a technology.
"""
	processes = set(
	  (t, v)

	  for p, t, v in g_processOutputs
	  if o in g_processOutputs[p, t, v]
	)
	return processes
	
def ProcessesByPeriodAndOutput ( p, o ):
	"""\
Returns the set of processes that operate in 'period' and take 'output'.  Note
that a process is a conceptually a vintage of a technology.
"""
	processes = set(
	  (t, v)

	  for Tp, t, v in g_processOutputs
	  if Tp == p
	  if o in g_processOutputs[p, t, v]
	)
	return processes

def ProcessVintages ( p, t ):
	index = (p, t)
	if index in g_processVintages:
		return g_processVintages[ index ]
	return set()
	
def ValidActivity ( p, t, v ):
	return (p, t, v) in g_activeActivity_ptv
	
def CapacityVariableIndices ( M ):
	return g_activeCapacity_tv
	
def CapacityAvailableVariableIndices ( M ):
	return g_activeCapacityAvailable_pt
	
def ActivityByPeriodAndProcessVarIndices ( M ):
	return g_activeActivity_ptv
	
def FlowVariableIndices ( M ):
	return g_activeFlow_psditvo
	
def EmissionActivityIndices ( M ):
	indices = set(
	  (e, i, t, v, o)
	  for i, t, v, o in M.Efficiency.sparse_iterkeys()
	  for e in M.commodity_emissions
	)
	return indices

def CreateLifetimes ( M ):
	# Steps
	#  1. Collect all possible processes
	#  2. Find the ones _not_ specified in LifetimeProcess and
	#     LifetimeLoanProcess
	#  3. Set them, based on Lifetime*Tech.

	# Shorter names, for us lazy programmer types
	LLN = M.LifetimeLoanProcess
	LPR = M.LifetimeProcess

	# Step 1
	lprocesses = set( M.LifetimeLoanProcess_tv )
	processes  = set( M.LifetimeProcess_tv )


	# Step 2
	unspecified_loan_lives = lprocesses.difference( LLN.sparse_iterkeys() )
	unspecified_tech_lives = processes.difference( LPR.sparse_iterkeys() )

	# Step 3

	# Some hackery: We futz with _constructed because Pyomo thinks that this
	# Param is already constructed.  However, in our view, it is not yet,
	# because we're specifically targeting values that have not yet been
	# constructed, that we know are valid, and that we will need.

	if unspecified_loan_lives:
		LLN._constructed = False
		for t, v in unspecified_loan_lives:
			LLN[t, v] = M.LifetimeLoanTech[ t ]
		LLN._constructed = True

	if unspecified_tech_lives:
		LPR._constructed = False
		for t, v in unspecified_tech_lives:
			LPR[t, v] = M.LifetimeTech[ t ]
		LPR._constructed = True

	
def calc_intermediates ( M ):
	global V_EnergyConsumptionByPeriodInputAndTech
	global V_ActivityByPeriodTechAndOutput
	global V_EmissionActivityByPeriodAndTech
	emission_keys = { (i, t, v, o) : e for e, i, t, v, o in M.EmissionActivity }
	
	con = sqlite3.connect(ifile)
	cur = con.cursor()   # a database cursor is a control structure that enables traversal over the records in a database
	con.text_factory = str #this ensures data is explored with the correct UTF-8 encoding
	
	for x in CapacityVariableIndices(M):
		M.CapacityVar_tv.add(x)
	M.V_Capacity = Param( M.CapacityVar_tv )
	for x,y in M.CapacityVar_tv:
		for row in cur.execute("SELECT capacity FROM V_Capacity WHERE tech is '"+x+"' and vintage is '"+str(y)+"'"):
			M.V_Capacity[x,y] = row[0]
	
	for x in CapacityAvailableVariableIndices(M):
		M.CapacityAvailableVar_pt.add(x)
	M.V_CapacityAvailableByPeriodAndTech = Param(	M.CapacityAvailableVar_pt	)
	for x,y in M.CapacityAvailableVar_pt:
		M.V_CapacityAvailableByPeriodAndTech[x,y] = 0
		for row in cur.execute("SELECT capacity FROM Output_Capacity WHERE t_periods is '"+str(x)+"' and tech is '"+y+"'"):
			M.V_CapacityAvailableByPeriodAndTech[x,y] = row[0]
	
	for x in ActivityByPeriodAndProcessVarIndices(M):
		M.ActivityByPeriodAndProcessVar_ptv.add(x)
	M.V_ActivityByPeriodAndProcess = Param(  M.ActivityByPeriodAndProcessVar_ptv	)
	for x,y,z in M.ActivityByPeriodAndProcessVar_ptv:
		M.V_ActivityByPeriodAndProcess[x,y,z] = 0
		for row in cur.execute("SELECT activity FROM V_ActivityByPeriodAndProcess WHERE t_periods is '"+str(x)+"' and tech is '"+y+"' and vintage is '"+str(z)+"'"):
			M.V_ActivityByPeriodAndProcess[x,y,z] = row[0]
	
	for x in FlowVariableIndices(M):
		M.FlowVar_psditvo.add(x)
	M.V_FlowIn  = Param( M.FlowVar_psditvo )
	M.V_FlowOut = Param( M.FlowVar_psditvo )
	for a,b,c,d,e,f,g in M.FlowVar_psditvo:
		M.V_FlowIn[a,b,c,d,e,f,g] = 0
		M.V_FlowOut[a,b,c,d,e,f,g] = 0
		for row in cur.execute("SELECT vflow_in FROM Output_VFlow_In WHERE t_periods is '"+str(a)+"' and t_season is '"+b+"' and t_day is '"+c+"' and input_comm is '"+d+"' and tech is '"+e+"' and vintage is '"+str(f)+"' and output_comm is '"+g+"'"):
			M.V_FlowIn[a,b,c,d,e,f,g] = row[0]
		for row in cur.execute("SELECT vflow_out FROM Output_VFlow_Out WHERE t_periods is '"+str(a)+"' and t_season is '"+b+"' and t_day is '"+c+"' and input_comm is '"+d+"' and tech is '"+e+"' and vintage is '"+str(f)+"' and output_comm is '"+g+"'"):
			M.V_FlowOut[a,b,c,d,e,f,g] = row[0]

	
	for p, s, d, i, t, v, o in M.V_FlowIn:
		val = value( M.V_FlowIn[p, s, d, i, t, v, o] )
		V_EnergyConsumptionByPeriodInputAndTech[p, i, t] = 0		
		if abs(val) < epsilon: continue
		if [p,i,t] not in V_EnergyConsumptionByPeriodInputAndTech.keys() :
			V_EnergyConsumptionByPeriodInputAndTech[p, i, t] = val
		else :
			V_EnergyConsumptionByPeriodInputAndTech[p, i, t] += val
		
	for p, s, d, i, t, v, o in M.V_FlowOut:
		val = value( M.V_FlowOut[p, s, d, i, t, v, o] )
		V_ActivityByPeriodTechAndOutput[p, t, o]    = 0
		V_EmissionActivityByPeriodAndTech[p, t] = 0
					
		if abs(val) < epsilon: continue
		if [p,t,o] not in V_ActivityByPeriodTechAndOutput.keys() :
			V_ActivityByPeriodTechAndOutput[p, t, o]    = val
		else :
			V_ActivityByPeriodTechAndOutput[p, t, o]    += val

		if (i, t, v, o) not in emission_keys: continue

		e = emission_keys[i, t, v, o]
		evalue = val * M.EmissionActivity[e, i, t, v, o]
		if [p,t] not in V_EmissionActivityByPeriodAndTech.keys() :
			V_EmissionActivityByPeriodAndTech[p, t] = evalue
		else:
			V_EmissionActivityByPeriodAndTech[p, t] += evalue
		
	cur.close()
	con.close()


def db_file(ifile) : # Call this function if the input file is a database.
	#connect to the database
	con = sqlite3.connect(ifile)
	cur = con.cursor()   # a database cursor is a control structure that enables traversal over the records in a database
	con.text_factory = str #this ensures data is explored with the correct UTF-8 encoding

	'''cur.execute("SELECT input_comm, tech, output_comm FROM Efficiency WHERE input_comm is "+inp_comm+" or output_comm is "+out_comm)
	for row in cur:
		if row[0] != 'ethos':
			nodes.add(row[0])
		else :
			ltech.add(row[1])
		nodes.add(row[2])
		tech.add(row[1])
		# Now populate the dot file with the concerned commodities
		if row[0] != 'ethos':
			to_tech.add('"%s"' % row[0] + '\t->\t"%s"' % row[1]) 
		from_tech.add('"%s"' % row[1] + '\t->\t"%s"' % row[2])'''
		
	cur.execute("SELECT t_periods FROM time_periods WHERE flag is 'e'")
	for row in cur:
		M.time_exist.add(int(row[0]))
	cur.execute("SELECT t_periods FROM time_periods WHERE flag is 'f'")
	for row in cur:
		M.time_future.add(int(row[0]))
	for x in init_set_time_optimize(M):
		M.time_optimize.add(x)
	
	cur.execute("SELECT tech FROM technologies WHERE flag='r' OR flag='p' OR flag='pb' OR flag='ps'")
	for row in cur:
		M.tech_all.add(row[0])
	for x in init_set_vintage_exist(M):
		M.vintage_exist.add(x)
	M.ExistingCapacity = Param( M.tech_all, M.vintage_exist )
	for x,y in [(a,b) for a in M.tech_all for b in M.vintage_exist]:
		cur.execute("SELECT exist_cap FROM ExistingCapacity WHERE tech is '"+x+"' and vintage is '"+str(y)+"'")
		for row in cur:
			M.ExistingCapacity[x,y] = row[0]
	for x in init_set_vintage_optimize(M) :
		M.vintage_optimize.add(x)
	M.vintage_all      = M.time_exist | M.time_optimize

	cur.execute("SELECT comm_name FROM commodities WHERE flag is 'd'")
	for row in cur:
		M.commodity_demand.add(row[0])
	cur.execute("SELECT comm_name FROM commodities WHERE flag is 'p'")
	for row in cur:
		M.commodity_physical.add(row[0])
	cur.execute("SELECT comm_name FROM commodities WHERE flag is 'e'")
	for row in cur:
		M.commodity_emissions.add(row[0])
	M.commodity_carrier = M.commodity_physical | M.commodity_demand
	M.Efficiency = Param( M.commodity_physical, M.tech_all, M.vintage_all, M.commodity_carrier )
	for w,x,y,z in [(a,b,c,d) for a in M.commodity_physical for b in M.tech_all for c in M.vintage_all for d in M.commodity_carrier]:
		for row in cur.execute("SELECT efficiency FROM Efficiency WHERE input_comm is '"+w+"' and tech is '"+x+"' and vintage is '"+str(y)+"' and output_comm is '"+z+"'"):
			M.Efficiency[w,x,y,z] = row[0]

	for x in LifetimeProcessIndices(M):
		M.LifetimeProcess_tv.add(x)
	M.LifetimeProcess        = Param( M.LifetimeProcess_tv )
	for x,y in M.LifetimeProcess_tv:
		for row in cur.execute("SELECT life FROM LifetimeTech WHERE tech is '"+x+"'"):
			M.LifetimeProcess[x,y] = row[0]
		for row in cur.execute("SELECT life_process FROM LifetimeProcess WHERE tech is '"+x+"' and vintage is '"+str(y)+"'"):
			M.LifetimeProcess[x,y] = row[0]
	for x in LifetimeLoanProcessIndices(M):
		M.LifetimeLoanProcess_tv.add(x)
	M.LifetimeLoanProcess    = Param( M.LifetimeLoanProcess_tv )
	for x,y in M.LifetimeLoanProcess_tv:
		for row in cur.execute("SELECT loan FROM LifetimeLoanTech WHERE tech is '"+x+"'"):
			M.LifetimeLoanProcess[x,y] = row[0]
	
	for x in EmissionActivityIndices(M):
		M.EmissionActivity_eitvo.add(x) 
	M.EmissionActivity = Param( M.EmissionActivity_eitvo )
	for v,w,x,y,z in M.EmissionActivity_eitvo:
		for row in cur.execute("SELECT emis_act FROM EmissionActivity WHERE emis_comm is '"+v+"' and input_comm is '"+w+"' and tech is '"+x+"' and vintage is '"+str(y)+"' and output_comm is '"+z+"'"):
			M.EmissionActivity[v,w,x,y,z] = row[0]
	
	cur.execute("SELECT t_season FROM time_season")
	for row in cur:
		M.time_season.add(row[0])
	cur.execute("SELECT t_day FROM time_of_day")
	for row in cur:
		M.time_of_day.add(row[0])

	M.LifetimeTech           = Param( M.tech_all, default=30 )    # in years
	for x in M.tech_all:
		M.LifetimeTech[x] = 30
		for row in cur.execute("SELECT life FROM LifetimeTech WHERE tech is '"+x+"'"):
			M.LifetimeTech[x] = row[0]
	M.LifetimeLoanTech       = Param( M.tech_all, default=10 )    # in years
	for x in M.tech_all:
		M.LifetimeLoanTech[x] = 10
		for row in cur.execute("SELECT loan FROM LifetimeLoanTech WHERE tech is '"+x+"'"):
			M.LifetimeLoanTech[x] = row[0]
	

	cur.close()
	con.close()



###################################

def _getLen ( key ):
	def wrapped ( obj ):
		return len(obj[ key ])
	return wrapped


def create_text_nodes ( nodes, indent=1 ):
	"""\
Return a set of text nodes in Graphviz DOT format, optimally padded for easier
reading and debugging.

nodes: iterable of (id, attribute) node tuples
       e.g. [(node1, attr1), (node2, attr2), ...]

indent: integer, number of tabs with which to indent all Dot node lines
"""
	if not nodes: return '// no nodes in this section'

	# guarantee basic structure of nodes arg
	assert( len(nodes) == sum( 1 for a, b in nodes ) )

	# Step 1: for alignment, get max item length in node list
	maxl = max(map(_getLen(0), nodes)) + 2 # account for two extra quotes

	# Step 2: prepare a text format based on max node size that pads all
	#         lines with attributes
	nfmt_attr = '{0:<%d} [ {1} ] ;' % maxl      # node text format
	nfmt_noa  = '{0} ;'

	# Step 3: create each node, and place string representation in a set to
	#         guarantee uniqueness
	q = '"%s"' # enforce quoting for all nodes
	gviz = set( nfmt_attr.format( q % n, a ) for n, a in nodes if a )
	gviz.update( nfmt_noa.format( q % n ) for n, a in nodes if not a )

	# Step 4: return a sorted version of nodes, as a single string
	indent = '\n' + '\t' *indent
	return indent.join(sorted( gviz ))


def create_text_edges ( edges, indent=1 ):
	"""\
Return a set of text edge definitions in Graphviz DOT format, optimally padded
for easier reading and debugging.

edges: iterable of (from, to, attribute) edge tuples
       e.g. [(inp1, tech1, attr1), (inp2, tech2, attr2), ...]

indent: integer, number of tabs with which to indent all Dot edge lines
"""
	if not edges: return '// no edges in this section'

	# guarantee basic structure of edges arg
	assert( len(edges) == sum( 1 for a, b, c in edges ) )

	# Step 1: for alignment, get max length of items on left and right side of
	# graph operator token ('->')
	maxl, maxr = max(map(_getLen(0), edges)), max(map(_getLen(1), edges))
	maxl += 2  # account for additional two quotes
	maxr += 2  # account for additional two quotes

	# Step 2: prepare format to be "\n\tinp+PADDING -> out+PADDING [..."
	efmt_attr = '{0:<%d} -> {1:<%d} [ {2} ] ;' % (maxl, maxr) # with attributes
	efmt_noa  = '{0:<%d} -> {1} ;' % maxl                     # no attributes

	# Step 3: add each edge to a set (to guarantee unique entries only)
	q = '"%s"' # enforce quoting for all tokens
	gviz = set( efmt_attr.format( q % i, q % t, a ) for i, t, a in edges if a )
	gviz.update( efmt_noa.format( q % i, q % t ) for i, t, a in edges if not a )

	# Step 4: return a sorted version of the edges, as a single string
	indent = '\n' + '\t' *indent
	return indent.join(sorted( gviz ))


def CreateCompleteEnergySystemDiagram ( **kwargs ): #all_vintages_model
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

	M               = kwargs.get( 'model' )
	ffmt            = kwargs.get( 'image_format' )
	commodity_color = kwargs.get( 'commodity_color' )
	input_color     = kwargs.get( 'arrowheadin_color' )
	output_color    = kwargs.get( 'arrowheadout_color' )
	tech_color      = kwargs.get( 'tech_color' )

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
	rankdir = "LR";       // The direction of the graph goes from Left to Right

	node [ style="filled" ] ;
	edge [ arrowhead="vee", label="   " ] ;


	subgraph technologies {
		node [ color="%(tech_color)s", shape="box" ] ;

		%(techs)s
	}

	subgraph energy_carriers {
		node [ color="%(carrier_color)s", shape="circle" ] ;

		%(carriers)s
	}

	subgraph inputs {
		edge [ color="%(input_color)s" ] ;

		%(inputs)s
	}

	subgraph outputs {
		edge [ color="%(output_color)s" ];

		%(outputs)s
	}
}
"""

	carriers, techs = set(), set()
	inputs, outputs = set(), set()

	p_fmt = '%s, %s, %s'   # "Process format"

	for l_per, l_tech, l_vin in g_activeActivity_ptv:
		techs.add( (p_fmt % (l_per, l_tech, l_vin), None) )
		for l_inp in ProcessInputs( l_per, l_tech, l_vin ):
			carriers.add( (l_inp, None) )
			inputs.add( (l_inp, p_fmt % (l_per, l_tech, l_vin), None) )
		for l_out in ProcessOutputs( l_per, l_tech, l_vin ):
			carriers.add( (l_out, None) )
			outputs.add( (p_fmt % (l_per, l_tech, l_vin), l_out, None) )

	techs    = create_text_nodes( techs,    indent=2 )
	carriers = create_text_nodes( carriers, indent=2 )
	inputs   = create_text_edges( inputs,   indent=2 )
	outputs  = create_text_edges( outputs,  indent=2 )

	fname = 'all_vintages_model.'
	with open( fname + 'dot', 'w' ) as f:
		f.write( data % dict(
		  input_color   = 'forestgreen',
		  output_color  = 'firebrick',
		  carrier_color =  'lightsteelblue',
		  tech_color    = 'darkseagreen',
		  techs    = techs,
		  carriers = carriers,
		  inputs   = inputs,
		  outputs  = outputs,
		))

	# Outsource to Graphviz via the old Unix standby: temporary files
	cmd = ('dot', '-T' + ffmt, '-o' + fname + ffmt, fname + 'dot')
	call( cmd )


def CreateCommodityPartialGraphs ( **kwargs ):#commodities
	
	M               = kwargs.get( 'model' )
	images_dir      = kwargs.get( 'images_dir' )
	ffmt            = kwargs.get( 'image_format' )
	commodity_color = kwargs.get( 'commodity_color' )
	input_color     = kwargs.get( 'arrowheadin_color' )
	output_color    = kwargs.get( 'arrowheadout_color' )
	home_color      = kwargs.get( 'home_color' )
	usedfont_color  = kwargs.get( 'usedfont_color' )
	tech_color      = kwargs.get( 'tech_color' )

	os.chdir( 'commodities' )

	commodity_file_format = """\
// This file is generated by the --graph_format option of the Temoa model.  It
// is a Graphviz DOT language text description of a Temoa model instance.  For
// the curious, Graphviz will read this file to create an equivalent image in
// a number of formats, including SVG, PNG, GIF, and PDF.  For example, here
// is how one might invoke Graphviz to create an SVG image from the dot file.
//
// dot -Tsvg -o model.svg model.dot
//
// For more information, see the Graphviz homepage: http://graphviz.org/

// This particular file is the dot language description of the flow of energy
// via the carrier '%(graph_label)s'.

strict digraph Temoa_energy_carrier {
	label = "%(graph_label)s"

	color       = "black";
	compound    = "True";
	concentrate = "True";
	rankdir     = "LR";
	splines     = "True";

	// Default node attributes
	node [ style="filled" ] ;

	// Default edge attributes
	edge [
	  arrowhead      = "vee",
	  fontsize       = "8",
	  label          = "   ",
	  labelfloat     = "false",
	  len            = "2",
	  weight         = "0.5",
	] ;


	// Define individual nodes (and non-default characteristics)
	subgraph techs {
		node [ color="%(tech_color)s", shape="box" ] ;

		%(tnodes)s
	}

	subgraph energy_carriers {
		node [ color="%(commodity_color)s", shape="circle" ] ;

		%(enodes)s
	}

	// Define individual edges (and non-default characteristics)
	subgraph outputs {
		edge [ color="%(output_color)s" ] ;

		%(oedges)s
	}

	subgraph inputs {
		edge [ color="%(input_color)s" ] ;

		%(iedges)s
	}
}
"""

	# Step 0: define the Graphviz Dot file format (above)

	model_url = 'href="../simple_model.%s"' % ffmt
	node_attr_fmt = 'href="../processes/process_%%s.%s"' % ffmt

	# Step 1: Define what to do for each energy carrier
	def createImages ( carriers ):
		# Step 1a: Create dot file for each item
		#   The basic gist is to create a set of nodes and edges, and then format
		#   them nicely in case a human needs to investigate the Dot file.
		for l_carrier in sorted( carriers ):
			# energy/tech nodes, in/out edges
			enodes, tnodes, iedges, oedges = set(), set(), set(), set()

			# Step 1b: populate nodes and edges sets with data
			enodes.add( (l_carrier, model_url) )

			for l_tech, l_vin in ProcessesByInput( l_carrier ):
				tnodes.add( (l_tech, node_attr_fmt % l_tech) )
				iedges.add( (l_carrier, l_tech, None) )
			for l_tech, l_vin in ProcessesByOutput( l_carrier ):
				tnodes.add( (l_tech, node_attr_fmt % l_tech) )
				oedges.add( (l_tech, l_carrier, None) )

			# Step 1c: convert the populated nodes and edges to Graphviz format
			tnodes = create_text_nodes( tnodes, indent=2 )
			enodes = create_text_nodes( enodes, indent=2 )
			iedges = create_text_edges( iedges, indent=2 )
			oedges = create_text_edges( oedges, indent=2 )

			# Step 1d: write out the Dot file for later Graphviz work
			with open( 'commodity_%s.dot' % l_carrier, 'w') as f:
				f.write( commodity_file_format % dict(
				  graph_label     = l_carrier,
				  images_dir      = images_dir,
				  commodity_color = commodity_color,
				  home_color      = home_color,
				  input_color     = input_color,
				  output_color    = output_color,
				  tech_color      = tech_color,
				  usedfont_color  = usedfont_color,
				  tnodes          = tnodes,
				  enodes          = enodes,
				  iedges          = iedges,
				  oedges          = oedges
				))

			# Step 1e: finally, have Graphviz actually create an image
			cmd = (
			  'dot',
			  '-T' + ffmt,
			  '-ocommodity_%s.%s' % (l_carrier, ffmt),
			  'commodity_%s.dot' % l_carrier
			)
			call( cmd )

	# Step 2: find the parts of the energy system this set of graphs address
	l_carriers = set()
	for index in g_processInputs:
		l_carriers.update( l_carrier for l_carrier in g_processInputs[ index ] )
		l_carriers.update( l_carrier for l_carrier in g_processOutputs[index ] )

	# sorting is not strictly necessary, but if there is some error, it lets
	# the user know on exactly which carrier it failed in terms of what has
	# (not) been written to disk.

	# Step 3: actually do the work
	createImages( sorted(l_carriers) )

	os.chdir('..')


def CreateProcessPartialGraphs ( **kwargs ): #processes
	"""\
A new subgraph is created for every technology in the tech_all set.  Subgraphs
are named model_<tech>.<format>
"""
	
	M                  = kwargs.get( 'model' )
	ffmt               = kwargs.get( 'image_format' )
	arrowheadin_color  = kwargs.get( 'arrowheadin_color' )
	arrowheadout_color = kwargs.get( 'arrowheadout_color' )
	commodity_color    = kwargs.get( 'commodity_color' )
	sb_vp_color        = kwargs.get( 'sb_vp_color' )
	sb_vpbackg_color   = kwargs.get( 'sb_vpbackg_color' )
	color_list         = kwargs.get( 'color_list' )
	sb_incom_color     = kwargs.get( 'sb_incom_color' )
	sb_outcom_color    = kwargs.get( 'sb_outcom_color' )
	images_dir         = kwargs.get( 'images_dir' )
	usedfont_color     = kwargs.get( 'usedfont_color' )
	home_color         = kwargs.get( 'home_color' )
	tech_color         = kwargs.get( 'tech_color' )
	options            = kwargs.get( 'options' )

	os.chdir( 'processes' )

	show_capacity = options.show_capacity
	splinevar     = options.splinevar

	VintageCap = M.V_Capacity
	PeriodCap  = M.V_CapacityAvailableByPeriodAndTech

	url_fmt  = '../commodities/commodity_%%s.%s' % ffmt
	dummystr = '   '
	fname = 'process_%s.%s'

	def _create_separate ( l_tech ):
		# begin/end/period/vintage nodes
		bnodes, enodes, pnodes, vnodes = set(), set(), set(), set()
		eedges, vedges = set(), set()

		periods  = set()  # used to obtain the first vintage/period, so that
		vintages = set()  #   all connections can point to a common point
		for l_per, tmp, l_vin in g_processInputs:
			if tmp != l_tech: continue
			periods.add(l_per)
			vintages.add(l_vin)

		if not (periods and vintages):
			# apparently specified a technology in tech_resource, but never used
			# it in efficiency.
			return None

		mid_period  = sorted(periods)[ len(periods)  //2 ] # // is 'floordiv'
		mid_vintage = sorted(vintages)[len(vintages) //2 ]
		del periods, vintages

		p_fmt = 'p_%s'
		v_fmt = 'v_%s'
		niattr = 'color="%s", href="%s"' % (sb_incom_color, url_fmt)  # inp node
		noattr = 'color="%s", href="%s"' % (sb_outcom_color, url_fmt) # out node
		eattr = 'color="%s"'    # edge attribute
		pattr = None            # period node attribute
		vattr = None            # vintage node attribute
		  # "cluster-in attribute", "cluster-out attribute"
		ciattr = 'color="%s", lhead="cluster_vintage"' % arrowheadin_color
		coattr = 'color="%s", ltail="cluster_period"'  % arrowheadout_color

		if show_capacity:
			pattr_fmt = 'label="p%s\\nTotal Capacity: %.2f"'
			vattr_fmt = 'label="v%s\\nCapacity: %.2f"'

		j = 0
		for l_per, tmp, l_vin in g_processInputs:
			if tmp != l_tech: continue

			if show_capacity:
				pattr = pattr_fmt % (l_per, value( PeriodCap[l_per, l_tech] ))
				vattr = vattr_fmt % (l_vin, value( VintageCap[l_tech, l_vin] ))
			pnodes.add( (p_fmt % l_per, pattr) )
			vnodes.add( (v_fmt % l_vin, vattr) )

			for l_inp in ProcessInputs( l_per, l_tech, l_vin ):
				for l_out in ProcessOutputsByInput( l_per, l_tech, l_vin, l_inp ):
					# use color_list for the option 1 subgraph arrows 1, so as to
					# more easily delineate the connections in the graph.
					rainbow = color_list[j]
					j = (j +1) % len(color_list)

					enodes.add( (l_inp, niattr % l_inp) )
					bnodes.add( (l_out, noattr % l_out) )
					eedges.add( (l_inp, v_fmt % mid_vintage, ciattr) )
					vedges.add( (v_fmt % l_vin, p_fmt % l_per, eattr % rainbow) )
					eedges.add( (p_fmt % mid_period, '%s' % l_out, coattr) )

		bnodes = create_text_nodes( bnodes, indent=2 ) # beginning nodes
		enodes = create_text_nodes( enodes, indent=2 ) # ending nodes
		pnodes = create_text_nodes( pnodes, indent=2 ) # period nodes
		vnodes = create_text_nodes( vnodes, indent=2 ) # vintage nodes
		eedges = create_text_edges( eedges, indent=2 ) # external edges
		vedges = create_text_edges( vedges, indent=2 ) # vintage edges

		dot_fname = fname % (l_tech, 'dot')
		with open( dot_fname, 'w' ) as f:
			f.write( model_dot_fmt % dict(
			  cluster_url = '../simple_model.%s' % ffmt,
			  graph_label = l_tech,
			  dummy       = dummystr,
			  images_dir  = images_dir,
			  splinevar   = splinevar,
			  clusternode_color = sb_vp_color,
			  period_color      = sb_vpbackg_color,
			  vintage_color     = sb_vpbackg_color,
			  usedfont_color    = usedfont_color,
			  home_color        = home_color,
			  bnodes = bnodes,
			  enodes = enodes,
			  pnodes = pnodes,
			  vnodes = vnodes,
			  eedges = eedges,
			  vedges = vedges,
			))
		return dot_fname


	def _create_explicit ( l_tech ):
		v_fmt = 'p%s_v%s'

		nattr = 'color="%s", href="%s"' % (commodity_color, url_fmt)
		vattr = 'color="%s", href="model.%s"' % (tech_color, ffmt)
		etattr = 'color="%s", sametail="%%s"' % arrowheadin_color
		efattr = 'color="%s", samehead="%%s"' % arrowheadout_color

		if show_capacity:
			vattr = 'color="%s", label="p%%(p)s_v%%(v)s\\n' \
		           'Capacity = %%(val).2f", href="model.%s"' % (tech_color, ffmt)

		# begin/end/vintage nodes
		bnodes, enodes, vnodes, edges = set(), set(), set(), set()

		for l_per, tmp, l_vin in g_processInputs:
			if tmp != l_tech: continue

			for l_inp in ProcessInputs( l_per, l_tech, l_vin ):
				for l_out in ProcessOutputsByInput( l_per, l_tech, l_vin, l_inp ):
					bnodes.add( (l_inp, nattr % l_inp) )
					enodes.add( (l_out, nattr % l_out) )

					attr_args = dict()
					if show_capacity:
						val = value( VintageCap[l_tech, l_vin] )
						attr_args.update(p=l_per, v=l_vin, val=val)
					vnodes.add( (v_fmt % (l_per, l_vin),
					  vattr % attr_args ) )

					edges.add( (l_inp, v_fmt % (l_per, l_vin),
					  etattr % l_inp) )
					edges.add( (v_fmt % (l_per, l_vin), l_out, efattr % l_out) )

		if not (bnodes and enodes and vnodes and edges):
			# apparently specified a technology in tech_resource, but never used
			# it in efficiency.
			return None

		bnodes = create_text_nodes( bnodes, indent=2 )
		enodes = create_text_nodes( enodes, indent=2 )
		vnodes = create_text_nodes( vnodes )
		edges  = create_text_edges( edges )

		dot_fname = fname % (l_tech, 'dot')
		with open( fname, 'w' ) as f:
			f.write( model_dot_fmt % dict(
			  tech           = l_tech,
			  images_dir     = images_dir,
			  home_color     = home_color,
			  usedfont_color = usedfont_color,
			  dummy          = dummystr,
			  bnodes         = bnodes,
			  enodes         = enodes,
			  vnodes         = vnodes,
			  edges          = edges,
			))
		return dot_fname


	if options.graph_type == 'separate_vintages':
		create_dot_file = _create_separate
		model_dot_fmt = """\
strict digraph model {
	label = "%(graph_label)s" ;

	bgcolor     = "transparent" ;
	color       = "black" ;
	compound    = "True" ;
	concentrate = "True" ;
	rankdir     = "LR" ;
	splines     = "%(splinevar)s" ;

	node [ shape="box", style="filled" ];

	edge [
	  arrowhead  = "vee",
	  decorate   = "True",
	  dir        = "both",
	  fontsize   = "8",
	  label      = "%(dummy)s",
	  labelfloat = "false",
	  labelfontcolor = "lightgreen",
	  len        = "2",
	  weight     = "0.5"
	];

	subgraph cluster_vintage {
		label = "Vintages" ;

		color = "%(vintage_color)s" ;
		style = "filled";
		href  = "%(cluster_url)s" ;

		node [ color="%(clusternode_color)s" ]

		%(vnodes)s
	}

	subgraph cluster_period {
		label = "Period" ;
		color = "%(period_color)s" ;
		style = "filled" ;
		href  = "%(cluster_url)s" ;

		node [ color="%(clusternode_color)s" ]

		%(pnodes)s
	}

	subgraph energy_carriers {
		node [ shape="circle" ] ;

	  // Beginning nodes
		%(bnodes)s

	  // Ending nodes
		%(enodes)s
	}

	subgraph external_edges {
		edge [ arrowhead="normal", dir="forward" ] ;

		%(eedges)s
	}

	subgraph internal_edges {
		// edges between vintages and periods
		%(vedges)s
	}
}
"""
	elif options.graph_type == 'explicit_vintages':
		create_dot_file = _create_explicit
		model_dot_fmt = """\
strict digraph model {
	label = "%(tech)s" ;

	color       = "black" ;
	concentrate = "True" ;
	rankdir     = "LR" ;

	node [ shape="box", style="filled" ];

	edge [
	  arrowhead = "vee",
	  decorate  = "True",
	  label     = "%(dummy)s",
	  labelfontcolor = "lightgreen"
	];

	subgraph energy_carriers {
		node [ shape="circle" ] ;

	  // Input nodes
		%(bnodes)s

	  // Output nodes
		%(enodes)s
	}

		// Vintage nodes
	%(vnodes)s

	// Define edges and any specific edge attributes
	%(edges)s
}
"""

	# Now actually do the work
	#  Sorting is not necessary, but gives a clue to user about where to look
	#  if some sort of processing error occurs.

	for t in sorted( M.tech_all ):
		dot_fname = create_dot_file( t )
		if dot_fname:
			cmd = (
			  'dot',
			  '-T' + ffmt,
			  '-o' + fname % (t, ffmt),
			  fname % (t, 'dot')
			)
			call( cmd )

	os.chdir('..')


def CreateMainModelDiagram ( **kwargs ): #simple_model

	M                  = kwargs.get( 'model' )
	ffmt               = kwargs.get( 'image_format' )
	images_dir         = kwargs.get( 'images_dir' )
	arrowheadin_color  = kwargs.get( 'arrowheadin_color' )
	arrowheadout_color = kwargs.get( 'arrowheadout_color' )
	commodity_color    = kwargs.get( 'commodity_color' )
	home_color         = kwargs.get( 'home_color' )
	tech_color         = kwargs.get( 'tech_color' )
	usedfont_color     = kwargs.get( 'usedfont_color' )

	fname = 'simple_model.'

	model_dot_fmt = """\
strict digraph model {
	rankdir = "LR" ;

	// Default node and edge attributes
	node [ style="filled" ] ;
	edge [ arrowhead="vee", labelfontcolor="lightgreen" ] ;

	// Define individual nodes
	subgraph techs {
		node [ color="%(tech_color)s", shape="box" ] ;

		%(tnodes)s
	}

	subgraph energy_carriers {
		node [ color="%(commodity_color)s", shape="circle" ] ;

		%(enodes)s
	}

	// Define edges and any specific edge attributes
	subgraph inputs {
		edge [ color="%(arrowheadin_color)s" ] ;

		%(iedges)s
	}

	subgraph outputs {
		edge [ color="%(arrowheadout_color)s" ] ;

		%(oedges)s
	}
}
"""

	tech_attr_fmt    = 'href="processes/process_%%s.%s"' % ffmt
	carrier_attr_fmt = 'href="commodities/commodity_%%s.%s"' % ffmt

	# edge/tech nodes, in/out edges
	enodes, tnodes, iedges, oedges = set(), set(), set(), set()

	for l_per, l_tech, l_vin in g_processInputs:
		tnodes.add( (l_tech, tech_attr_fmt % l_tech) )
		for l_inp in ProcessInputs( l_per, l_tech, l_vin ):
			enodes.add( (l_inp, carrier_attr_fmt % l_inp) )
			for l_out in ProcessOutputsByInput( l_per, l_tech, l_vin, l_inp ):
				enodes.add( (l_out, carrier_attr_fmt % l_out) )
				iedges.add( (l_inp, l_tech, None) )
				oedges.add( (l_tech, l_out, None) )

	enodes = create_text_nodes( enodes, indent=2 )
	tnodes = create_text_nodes( tnodes, indent=2 )
	iedges = create_text_edges( iedges, indent=2 )
	oedges = create_text_edges( oedges, indent=2 )

	with open( fname + 'dot', 'w' ) as f:
		f.write( model_dot_fmt % dict(
		  images_dir         = images_dir,
		  arrowheadin_color  = arrowheadin_color,
		  arrowheadout_color = arrowheadout_color,
		  commodity_color    = commodity_color,
		  home_color         = home_color,
		  tech_color         = tech_color,
		  usedfont_color     = usedfont_color,
		  enodes             = enodes,
		  tnodes             = tnodes,
		  iedges             = iedges,
		  oedges             = oedges,
		))
	del enodes, tnodes, iedges, oedges

	cmd = ('dot', '-T' + ffmt, '-o' + fname + ffmt, fname + 'dot')
	call( cmd )

def CreateTechResultsDiagrams ( **kwargs ): #results

	M                  = kwargs.get( 'model' )
	ffmt               = kwargs.get( 'image_format' )
	images_dir         = kwargs.get( 'images_dir' )
	arrowheadin_color  = kwargs.get( 'arrowheadin_color' )
	arrowheadout_color = kwargs.get( 'arrowheadout_color' )
	sb_vpbackg_color   = kwargs.get( 'sb_vpbackg_color' )
	sb_vp_color        = kwargs.get( 'sb_vp_color' )
	commodity_color    = kwargs.get( 'commodity_color' )
	home_color         = kwargs.get( 'home_color' )
	tech_color         = kwargs.get( 'tech_color' )
	usedfont_color     = kwargs.get( 'usedfont_color' )
	options            = kwargs.get( 'options' )

	splinevar = options.splinevar

	os.chdir( 'results' )

	model_dot_fmt = """\
strict digraph model {
	label = "Results for %(tech)s in %(period)s" ;

	compound    = "True" ;
	concentrate = "True";
	rankdir     = "LR" ;
	splines     = "%(splinevar)s" ;

	node [ style="filled" ] ;
	edge [ arrowhead="vee" ] ;

	subgraph cluster_vintages {
		label = "Vintages\\nCapacity: %(total_cap).2f" ;

		href  = "results%(period)s.%(ffmt)s" ;
		style = "filled"
		color = "%(vintage_cluster_color)s"

		node [ color="%(vintage_color)s", shape="box" ] ;

		%(vnodes)s
	}

	subgraph energy_carriers {
		node [
		  color     = "%(commodity_color)s",
		  fontcolor = "%(usedfont_color)s",
		  shape     = "circle"
		] ;

		%(enodes)s
	}

	subgraph inputs {
		edge [ color="%(input_color)s" ] ;

		%(iedges)s
	}

	subgraph outputs {
		edge [ color="%(output_color)s" ] ;

		%(oedges)s
	}
}
"""
	enode_attr_fmt = 'href="../commodities/rc_%%s_%%s.%s"' % ffmt
	vnode_attr_fmt = 'href="results_%%s_p%%sv%%s_segments.%s", ' % ffmt
	vnode_attr_fmt += 'label="%s\\nCap: %.2f"'

	for per, tech in g_activeCapacityAvailable_pt:
		total_cap = value( M.V_CapacityAvailableByPeriodAndTech[per, tech] )

		# energy/vintage nodes, in/out edges
		enodes, vnodes, iedges, oedges = set(), set(), set(), set()

		for l_vin in ProcessVintages( per, tech ):
			if not M.V_ActivityByPeriodAndProcess[per, tech, l_vin]:
				continue

			cap = M.V_Capacity[tech, l_vin]
			vnode = str(l_vin)
			for l_inp in ProcessInputs( per, tech, l_vin ):
				for l_out in ProcessOutputsByInput( per, tech, l_vin, l_inp ):
					flowin = sum(
					  value( M.V_FlowIn[per, ssn, tod, l_inp, tech, l_vin, l_out] )
					  for ssn in M.time_season
					  for tod in M.time_of_day
					)
					flowout = sum(
					  value( M.V_FlowOut[per, ssn, tod, l_inp, tech, l_vin, l_out] )
					  for ssn in M.time_season
					  for tod in M.time_of_day
					)
					index = (per, l_inp, tech, l_vin)

					vnodes.add( (vnode, vnode_attr_fmt %
					  (tech, per, l_vin, l_vin, cap)) )
					enodes.add( (l_inp, enode_attr_fmt % (l_inp, per)) )
					enodes.add( (l_out, enode_attr_fmt % (l_out, per)) )
					iedges.add( (l_inp, vnode, 'label="%.2f"' % flowin) )
					oedges.add( (vnode, l_out, 'label="%.2f"' % flowout) )

		if not vnodes: continue

		enodes = create_text_nodes( enodes, indent=2 )
		vnodes = create_text_nodes( vnodes, indent=2 )
		iedges = create_text_edges( iedges, indent=2 )
		oedges = create_text_edges( oedges, indent=2 )

		fname = 'results_%s_%s.' % (tech, per)
		with open( fname + 'dot', 'w' ) as f:
			f.write( model_dot_fmt % dict(
			  images_dir      = images_dir,
			  tech            = tech,
			  period          = per,
			  ffmt            = ffmt,
			  commodity_color = commodity_color,
			  usedfont_color  = usedfont_color,
			  home_color      = home_color,
			  input_color     = arrowheadin_color,
			  output_color    = arrowheadout_color,
			  vintage_cluster_color = sb_vpbackg_color,
			  vintage_color   = sb_vp_color,
			  splinevar       = splinevar,
			  total_cap       = total_cap,
			  vnodes          = vnodes,
			  enodes          = enodes,
			  iedges          = iedges,
			  oedges          = oedges,
			))
		cmd = ('dot', '-T' + ffmt, '-o' + fname + ffmt, fname + 'dot')
		call( cmd )

	os.chdir( '..' )


def CreatePartialSegmentsDiagram ( **kwargs ): #results_segment

	M                  = kwargs.get( 'model' )
	ffmt               = kwargs.get( 'image_format' )
	arrowheadin_color  = kwargs.get( 'arrowheadin_color' )
	arrowheadout_color = kwargs.get( 'arrowheadout_color' )
	sb_vpbackg_color   = kwargs.get( 'sb_vpbackg_color' )
	sb_vp_color        = kwargs.get( 'sb_vp_color' )
	commodity_color    = kwargs.get( 'commodity_color' )
	home_color         = kwargs.get( 'home_color' )
	tech_color         = kwargs.get( 'tech_color' )
	usedfont_color     = kwargs.get( 'usedfont_color' )
	options            = kwargs.get( 'options' )

	splinevar = options.splinevar

	os.chdir( 'results' )

	slice_dot_fmt = """\
strict digraph model {
	label = "Activity split of process %(tech)s, %(vintage)s in year %(period)s" ;

	compound    = "True" ;
	concentrate = "True";
	rankdir     = "LR" ;
	splines     = "%(splinevar)s" ;

	node [ style="filled" ] ;
	edge [ arrowhead="vee" ] ;

	subgraph cluster_slices {
		label = "%(vintage)s Capacity: %(total_cap).2f" ;

		color = "%(vintage_cluster_color)s" ;
		rank  = "same" ;
		style = "filled" ;

		node [ color="%(vintage_color)s", shape="box" ] ;

		%(snodes)s
	}

	subgraph energy_carriers {
		node [
		  color     = "%(commodity_color)s",
		  fontcolor = "%(usedfont_color)s",
		  shape     = "circle"
		] ;

		%(enodes)s
	}

	subgraph inputs {
		edge [ color="%(input_color)s" ] ;

		%(iedges)s
	}

	subgraph outputs {
		edge [ color="%(output_color)s" ] ;

		%(oedges)s
	}
}
"""
	enode_attr_fmt = 'href="../commodities/rc_%%s_%%s.%s"' % ffmt

	for p, t in g_activeCapacityAvailable_pt:
		total_cap = value( M.V_CapacityAvailableByPeriodAndTech[p, t] )

		for v in ProcessVintages( p, t ):
			if not M.V_ActivityByPeriodAndProcess[p, t, v]:
				continue

			cap = M.V_Capacity[t, v]
			vnode = str( v )
			for i in ProcessInputs( p, t, v ):
				for o in ProcessOutputsByInput( p, t, v, i ):
					# energy/vintage nodes, in/out edges
					snodes, enodes, iedges, oedges = set(), set(), set(), set()
					for s in M.time_season:
						for d in M.time_of_day:
							flowin = value( M.V_FlowIn[p, s, d, i, t, v, o] )
							if not flowin: continue
							flowout = value( M.V_FlowOut[p, s, d, i, t, v, o] )
							snode = "%s, %s" % (s, d)
							snodes.add( (snode, None) )
							enodes.add( (i, enode_attr_fmt % (i, p)) )
							enodes.add( (o, enode_attr_fmt % (o, p)) )
							iedges.add( (i, snode, 'label="%.2f"' % flowin) )
							oedges.add( (snode, o, 'label="%.2f"' % flowout) )

					if not snodes: continue

					snodes = create_text_nodes( snodes, indent=2 )
					enodes = create_text_nodes( enodes, indent=2 )
					iedges = create_text_edges( iedges, indent=2 )
					oedges = create_text_edges( oedges, indent=2 )

					fname = 'results_%s_p%sv%s_segments.' % (t, p, v)
					with open( fname + 'dot', 'w' ) as f:
						f.write( slice_dot_fmt % dict(
						  period          = p,
						  tech            = t,
						  vintage         = v,
						  ffmt            = ffmt,
						  commodity_color = commodity_color,
						  usedfont_color  = usedfont_color,
						  home_color      = home_color,
						  input_color     = arrowheadin_color,
						  output_color    = arrowheadout_color,
						  vintage_cluster_color = sb_vpbackg_color,
						  vintage_color   = sb_vp_color,
						  splinevar       = splinevar,
						  total_cap       = total_cap,
						  snodes          = snodes,
						  enodes          = enodes,
						  iedges          = iedges,
						  oedges          = oedges,
						))
					cmd = ('dot', '-T' + ffmt, '-o' + fname + ffmt, fname + 'dot')
					call( cmd )

	os.chdir( '..' )


def CreateCommodityPartialResults ( **kwargs ): #partial commodities

	M               = kwargs.get( 'model' )
	ffmt            = kwargs.get( 'image_format' )
	images_dir      = kwargs.get( 'images_dir' )
	sb_arrow_color  = kwargs.get( 'sb_arrow_color' )
	commodity_color = kwargs.get( 'commodity_color' )
	home_color      = kwargs.get( 'home_color' )
	tech_color      = kwargs.get( 'tech_color' )
	usedfont_color  = kwargs.get( 'usedfont_color' )
	unused_color    = kwargs.get( 'unused_color' )
	options         = kwargs.get( 'options' )

	splinevar = options.splinevar

	os.chdir( 'commodities' )

	commodity_dot_fmt = """\
strict digraph result_commodity_%(commodity)s {
	label       = "%(commodity)s - %(period)s" ;

	compound    = "True" ;
	concentrate = "True" ;
	rankdir     = "LR" ;
	splines     = "True" ;

	node [ shape="box", style="filled" ] ;
	edge [
	  arrowhead  = "vee",
	  fontsize   = "8",
	  label      = "   ",
	  labelfloat = "False",
	  labelfontcolor = "lightgreen"
	  len        = "2",
	  weight     = "0.5",
	] ;

	%(resource_node)s

	subgraph used_techs {
		node [ color="%(tech_color)s" ] ;

		%(used_nodes)s
	}

	subgraph used_techs {
		node [ color="%(unused_color)s" ] ;

		%(unused_nodes)s
	}

	subgraph in_use_flows {
		edge [ color="%(sb_arrow_color)s" ] ;

		%(used_edges)s
	}

	subgraph unused_flows {
		edge [ color="%(unused_color)s" ] ;

		%(unused_edges)s
	}
}
"""

	FI = M.V_FlowIn
	FO = M.V_FlowOut
	used_carriers, used_techs = set(), set()

	for p, t, v in g_processInputs:
		for i in ProcessInputs( p, t, v ):
			for o in ProcessOutputsByInput( p, t, v, i ):
				flowin = sum(
				  value( FI[p, s, d, i, t, v, o] )
				  for s in M.time_season
				  for d in M.time_of_day
				)
				if flowin:
					flowout = sum(
					  value( FO[p, s, d, i, t, v, o] )
					  for s in M.time_season
					  for d in M.time_of_day
					)
					used_carriers.update( g_processInputs[p, t, v] )
					used_carriers.update( g_processOutputs[p, t, v] )
					used_techs.add( t )

	period_results_url_fmt = '../results/results%%s.%s' % ffmt
	node_attr_fmt = 'href="../results/results_%%s_%%s.%s"' % ffmt
	rc_node_fmt = 'color="%s", href="%s", shape="circle"'

	for l_per in M.time_future:
		url = period_results_url_fmt % l_per
		for l_carrier in used_carriers:
			# enabled/disabled nodes/edges
			enodes, dnodes, eedges, dedges = set(), set(), set(), set()

			rcnode = ((l_carrier, rc_node_fmt % (commodity_color, url)),)

			for l_tech, l_vin in ProcessesByInput( l_carrier ):
				if l_tech in used_techs:
					enodes.add( (l_tech, node_attr_fmt % (l_tech, l_per)) )
					eedges.add( (l_carrier, l_tech, None) )
				else:
					dnodes.add( (l_tech, None) )
					dedges.add( (l_carrier, l_tech, None) )
			for l_tech, l_vin in ProcessesByOutput( l_carrier ):
				if l_tech in used_techs:
					enodes.add( (l_tech, node_attr_fmt % (l_tech, l_per)) )
					eedges.add( (l_tech, l_carrier, None) )
				else:
					dnodes.add( (l_tech, None) )
					dedges.add( (l_tech, l_carrier, None) )

			rcnode = create_text_nodes( rcnode )
			enodes = create_text_nodes( enodes, indent=2 )
			dnodes = create_text_nodes( dnodes, indent=2 )
			eedges = create_text_edges( eedges, indent=2 )
			dedges = create_text_edges( dedges, indent=2 )

			fname = 'rc_%s_%s.' % (l_carrier, l_per)
			with open( fname + 'dot' ,'w') as f:
				f.write( commodity_dot_fmt % dict(
				  images_dir     = images_dir,
				  home_color     = home_color,
				  usedfont_color = usedfont_color,
				  sb_arrow_color = sb_arrow_color,
				  tech_color     = tech_color,
				  commodity      = l_carrier,
				  period         = l_per,
				  unused_color   = unused_color,
				  resource_node  = rcnode,
				  used_nodes     = enodes,
				  unused_nodes   = dnodes,
				  used_edges     = eedges,
				  unused_edges   = dedges,
				))

			cmd = ('dot', '-T' + ffmt, '-o' + fname + ffmt, fname + 'dot')
			call( cmd )

	os.chdir( '..' )


def CreateMainResultsDiagram ( **kwargs ): #results_main

	M                  = kwargs.get( 'model' )
	images_dir         = kwargs.get( 'images_dir' )
	ffmt               = kwargs.get( 'image_format' )
	options            = kwargs.get( 'options' )
	arrowheadin_color  = kwargs.get( 'arrowheadin_color' )
	arrowheadout_color = kwargs.get( 'arrowheadout_color' )
	commodity_color    = kwargs.get( 'commodity_color' )
	tech_color         = kwargs.get( 'tech_color' )
	unused_color       = kwargs.get( 'unused_color' )
	unusedfont_color   = kwargs.get( 'unusedfont_color' )
	usedfont_color     = kwargs.get( 'usedfont_color' )

	splinevar = options.splinevar

	os.chdir( 'results' )

	results_dot_fmt = """\
strict digraph model {
	label = "Results for %(period)s"

	rankdir = "LR" ;
	smoothtype = "power_dist" ;
	splines = "%(splinevar)s" ;

	node [ style="filled" ] ;
	edge [ arrowhead="vee" ] ;

	subgraph unused_techs {
		node [
		  color     = "%(unused_color)s",
		  fontcolor = "%(unusedfont_color)s",
		  shape     = "box"
		] ;

		%(dtechs)s
	}

	subgraph unused_energy_carriers {
		node [
		  color     = "%(unused_color)s",
		  fontcolor = "%(unusedfont_color)s",
		  shape     = "circle"
		] ;

		%(dcarriers)s
	}

	subgraph unused_emissions {
		node [
		  color     = "%(unused_color)s",
		  fontcolor = "%(unusedfont_color)s",
		  shape     = "circle"
		]

		%(demissions)s
	}

	subgraph in_use_techs {
		node [
		  color     = "%(tech_color)s",
		  fontcolor = "%(usedfont_color)s",
		  shape     = "box"
		] ;

		%(etechs)s
	}

	subgraph in_use_energy_carriers {
		node [
		  color     = "%(commodity_color)s",
		  fontcolor = "%(usedfont_color)s",
		  shape     = "circle"
		] ;

		%(ecarriers)s
	}

	subgraph in_use_emissions {
		node [
		  color     = "%(commodity_color)s",
		  fontcolor = "%(usedfont_color)s",
		  shape     = "circle"
		] ;

		%(eemissions)s
	}

	subgraph unused_flows {
		edge [ color="%(unused_color)s" ]

		%(dflows)s
	}

	subgraph in_use_flows {
		subgraph inputs {
			edge [ color="%(arrowheadin_color)s" ] ;

			%(eflowsi)s
		}

		subgraph outputs {
			edge [ color="%(arrowheadout_color)s" ] ;

			%(eflowso)s
		}
	}
}
"""

	tech_attr_fmt = 'label="%%s\\nCapacity: %%.2f", href="results_%%s_%%s.%s"'
	tech_attr_fmt %= ffmt
	commodity_fmt = 'href="../commodities/rc_%%s_%%s.%s"' % ffmt
	flow_fmt = 'label="%.2f"'

	V_Cap = M.V_CapacityAvailableByPeriodAndTech
	FI = M.V_FlowIn
	FO = M.V_FlowOut
	EI = V_EnergyConsumptionByPeriodInputAndTech    # Energy In
	EO = V_ActivityByPeriodTechAndOutput            # Energy Out
	EmiO = V_EmissionActivityByPeriodAndTech

	epsilon = 0.005  # we only care about last two decimals
	  # but perhaps this should be configurable?  Not until we can do this
	  # both after the fact (i.e. not synchronous with a solve), and via a
	  # configuration file.

	for pp in M.time_optimize:
		# enabled/disabled   techs/carriers/emissions/flows   in/out
		etechs, dtechs, ecarriers = set(), set(), set()
		eemissions = set()
		eflowsi, eflowso, dflows = set(), set(), set()   # edges
		usedc, usede = set(), set()    # used carriers, used emissions

		for tt in M.tech_all:
			if (pp, tt) not in V_Cap: continue

			cap = V_Cap[pp, tt]

			if cap:
				etechs.add( (tt, tech_attr_fmt % (tt, cap, tt, pp)) )
			else:
				dtechs.add( (tt, None) )

			for vv in ProcessVintages( pp, tt ):
				for ii in ProcessInputs( pp, tt, vv ):
					inp = value( EI[pp, ii, tt] )
					if inp >= epsilon:
						eflowsi.add( (ii, tt, flow_fmt % inp) )
						ecarriers.add( (ii, commodity_fmt % (ii, pp)) )
						usedc.add( ii )
					else:
						dflows.add( (ii, tt, None) )
				for oo in ProcessOutputs( pp, tt, vv ):
					out = value( EO[pp, tt, oo] )
					if out >= epsilon:
						eflowso.add( (tt, oo, flow_fmt % out) )
						ecarriers.add( (oo, commodity_fmt % (oo, pp)) )
						usedc.add( oo )
					else:
						dflows.add( (tt, oo, None) )

		for ee, ii, tt, vv, oo in M.EmissionActivity.sparse_keys():
			if ValidActivity( pp, tt, vv ):
				amt = value( EmiO[pp, tt] )
				if amt < epsilon: continue

				eflowso.add( (tt, ee, flow_fmt % amt) )
				eemissions.add( (ee, None) )
				usede.add( ee )

		dcarriers = set( (cc, None)
		  for cc in M.commodity_carrier if cc not in usedc )
		demissions = set( (ee, None)
		  for ee in M.commodity_emissions if ee not in usede )

		dtechs     = create_text_nodes( dtechs,     indent=2 )
		etechs     = create_text_nodes( etechs,     indent=2 )
		dcarriers  = create_text_nodes( dcarriers,  indent=2 )
		ecarriers  = create_text_nodes( ecarriers,  indent=2 )
		demissions = create_text_nodes( demissions, indent=2 )
		eemissions = create_text_nodes( eemissions, indent=2 )
		dflows     = create_text_edges( dflows,     indent=2 )
		eflowsi    = create_text_edges( eflowsi,    indent=3 )
		eflowso    = create_text_edges( eflowso,    indent=3 )

		# link to periods: Do we want to include this in the SVG, or just let the
		# modeler use the standard browser buttons?  I think the latter.
		# for randstr in l_perset:
			# url = 'results%s.%s' % (randstr, ffmt)
			# l_file.write (str(randstr) + '[URL="' + url + '",fontcolor=' + usedfont_color + ', rank="min", style=filled, shape=box, color=' + menu_color + '];\n')
		# l_file.write( images + '[URL="..",shape=house, style=filled, fontcolor=' + usedfont_color + ', color=' + home_color + '];\n')
		# l_file.write ("}\n");
		# l_file.close()

		fname = 'results%s.' % pp
		with open( fname + 'dot', 'w' ) as f:
			f.write( results_dot_fmt % dict(
			  period             = pp,
			  splinevar          = splinevar,
			  arrowheadin_color  = arrowheadin_color,
			  arrowheadout_color = arrowheadout_color,
			  commodity_color    = commodity_color,
			  tech_color         = tech_color,
			  unused_color       = unused_color,
			  unusedfont_color   = unusedfont_color,
			  usedfont_color     = usedfont_color,
			  dtechs     = dtechs,
			  etechs     = etechs,
			  dcarriers  = dcarriers,
			  ecarriers  = ecarriers,
			  demissions = demissions,
			  eemissions = eemissions,
			  dflows     = dflows,
			  eflowsi    = eflowsi,
			  eflowso    = eflowso,
			))

		cmd = ('dot', '-T' + ffmt, '-o' + fname + ffmt, fname + 'dot')
		call( cmd )

	os.chdir( '..' )


def CreateModelDiagrams ( M, options ):
	# This function is a "master", calling many other functions based on command
	# line input.  Other than code cleanliness, there is no reason that the
	# logic couldn't be in main()

	# if the user has listed more than one dot_dat, arbitrarily choose the first
	# as the name of this run.
	#datname = os.path.basename( options.dot_dat[0] )[:-4]
	datname = 'my_run'
	images_dir = "images_" + datname

	if os.path.exists( images_dir ):
		rmtree( images_dir )

	os.mkdir( images_dir )
	os.chdir( images_dir )

	os.makedirs( 'commodities' )
	os.makedirs( 'processes' )
	os.makedirs( 'results' )

	##############################################
	#MAIN MODEL AND RESULTS AND EVERYTHING ELSE
	kwargs = dict(
	  model              = M,
	  images_dir         = 'images_%s' % datname,
	  image_format       = options.graph_format.lower(),
	  options            = options,

	  tech_color         = 'darkseagreen',
	  commodity_color    = 'lightsteelblue',
	  unused_color       = 'powderblue',
	  arrowheadout_color = 'forestgreen',
	  arrowheadin_color  = 'firebrick',
	  usedfont_color     = 'black',
	  unusedfont_color   = 'chocolate',
	  menu_color         = 'hotpink',
	  home_color         = 'gray75',

	  #MODELDETAILED,
	  md_tech_color      = 'hotpink',

	  #SUBGRAPHS (option 1),
	  sb_incom_color     = 'lightsteelblue',
	  sb_outcom_color    = 'lawngreen',
	  sb_vpbackg_color   = 'lightgrey',
	  sb_vp_color        = 'white',
	  sb_arrow_color     = 'forestgreen',

	  #SUBGRAPH 1 ARROW COLORS
	    # feel free to add more colors here
	  color_list = ('red', 'orange', 'gold', 'green', 'blue', 'purple',
	                'hotpink', 'cyan', 'burlywood', 'coral', 'limegreen',
	                'black', 'brown'),
	)
	####################################

	# Do all necessary work in parallel, taking advantage of whatever cores
	# are available to the computer on which this code is run.  To add a
	# function to the pool, ensure that the function is in the 'gvizFunctions'
	# tuple below, and that the function has all it needs to work passed in
	# via the 'kwargs' dict above.

	gvizFunctions = (
	  CreateCompleteEnergySystemDiagram,
	  CreateCommodityPartialGraphs,
	  CreateProcessPartialGraphs,
	  CreateMainModelDiagram,
	  CreateTechResultsDiagrams,
	  CreateCommodityPartialResults,
	  CreateMainResultsDiagram,
	  CreatePartialSegmentsDiagram,
	)

	if 'win' in sys.platform:
		msg = ('\n\nRunning in Windows ... Temoa is currently unable to use '
		       'multiple processes.  Generating graphs will take a bit longer.'
		       '\n')
		SE.write( msg )
		for func in gvizFunctions:
			func( **kwargs )

	else:
		sem = MP.Semaphore( MP.cpu_count() )
		def do_work ( func ):
			sem.acquire()
			func( **kwargs )
			sem.release()

		processes = [
		  MP.Process( target=do_work, args=(func,) )
		  for func in gvizFunctions
		]
		for p in processes: p.start()
		for p in processes: p.join()

	os.chdir( '..' )

	

options = AbstractModel("DEMO")
options.graph_format = 'svg'
options.show_capacity = False
options.graph_type = 'separate_vintages'
options.splinevar = False

ifile = argv[1]
db_file(ifile)
CreateLifetimes(M)
InitializeProcessParameters ( M )
calc_intermediates(M)
CreateModelDiagrams ( M, options )
