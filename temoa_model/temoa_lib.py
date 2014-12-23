"""
Temoa - Tools for Energy Model Optimization and Analysis
  linear optimization; least cost; dynamic system visualization

Copyright (C) 2011-2014  Kevin Hunter, Joseph DeCarolis

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU Affero General Public License for more details.

Developers of this script will check out a complete copy of the GNU Affero
General Public License in the file COPYING.txt.  Users uncompressing this from
an archive may not have received this license file.  If not, see
<http://www.gnu.org/licenses/>.
"""


from cStringIO import StringIO
from itertools import product as cross_product, islice, izip
from operator import itemgetter as iget
from os import path, close as os_close, nice as os_nice
from sys import argv, stderr as SE, stdout as SO
from signal import signal, SIGINT, default_int_handler

import errno

# The assumption is that folks will run this either on their personal/business
# machine, or on a cluster.  If on their PC, then it'll be the only thing
# really running, and the rest of the machine can stay responsive.  Meanwhile,
# the same argument applies for a cluster, in which case this lets use of Temoa
# not impinge as rudely on other's work.  (And on most [all?] implementations,
# 1000 = 19.  But 1000 is nice and round.)
os_nice( 1000 )

import pyomo.environ
  # workaround for Coopr's brain dead signal handler
signal(SIGINT, default_int_handler)

TEMOA_GIT_VERSION  = 'HEAD'
TEMOA_RELEASE_DATE = 'Today'

from temoa_graphviz import CreateModelDiagrams

try:
	from pyomo.core import (
	  AbstractModel, BuildAction, Constraint, NonNegativeReals, Objective, Param,
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


class TemoaError ( Exception ): pass
class TemoaCommandLineArgumentError ( TemoaError ): pass
class TemoaKeyError ( TemoaError ): pass
class TemoaObjectNotFoundError ( TemoaError ): pass
class TemoaFlowError ( TemoaError ): pass
class TemoaValidationError ( TemoaError ): pass
class TemoaNoExecutableError ( TemoaError ): pass
class TemoaInfeasibleError ( TemoaError ): pass

def get_str_padding ( obj ):
	return len(str( obj ))

def iter_in_chunks ( iterable, chunk_size ):
	"""
Group iterable items into chunks.

Given an iterable, e.g. ('a', 1, 'b', 2, 'c', 3), this function converts this
length / chunk_size tuples.  The 'length' in the previous sentence is a
misnomer, however, as this function works with any iterable.

Caveat emptor: with the last example (below), note that incomplete tuples are
   silently discarded.  This function assumes an there are only "complete"
   chunks within the iterable; there are no 'partial chunks'.

For example:

    >>> some_tuple = ('a', 1, 'b', 2, 'c', 3)
    >>> for i in iter_in_chunks( some_tuple, 2 )
    >>>    print i
    ('a', 1)
    ('b', 2)
    ('c', 3)

    >>> for i in iter_in_chunks( some_tuple, 3 )
    >>>    print i
    ('a', 1, 'b')
    (2, 'c', 3)

    >>> for i in iter_in_chunks( some_tuple, 4 )
    >>>    print i
    ('a', 1, 'b', 2)

"""

	return izip( *[islice(iterable, i, None, chunk_size)
	             for i in xrange(chunk_size)] )

###############################################################################
# Temoa rule "partial" functions (excised from indidivual constraints for
#   readability)

def CommodityBalanceConstraintErrorCheck ( vflow_out, vflow_in, p, s, d, c ):
	if int is type(vflow_out):
		flow_in_expr = StringIO()
		vflow_in.pprint( ostream=flow_in_expr )
		msg = ("Unable to meet an interprocess '{}' transfer in ({}, {}, {}).\n"
		  'No flow out.  Constraint flow in:\n   {}\n'
		  'Possible reasons:\n'
		  " - Is there a missing period in set 'time_future'?\n"
		  " - Is there a missing tech in set 'tech_resource'?\n"
		  " - Is there a missing tech in set 'tech_production'?\n"
		  " - Is there a missing commodity in set 'commodity_physical'?\n"
		  ' - Are there missing entries in the Efficiency parameter?\n'
		  ' - Does a process need a longer LifetimeProcess parameter setting?')
		raise TemoaFlowError( msg.format(
		  c, s, d, p, flow_in_expr.getvalue()
		))


def DemandConstraintErrorCheck ( supply, p, s, d, dem ):
	if int is type( supply ):
		msg = ("Error: Demand '{}' for ({}, {}, {}) unable to be met by any "
		  'technology.\n\tPossible reasons:\n'
		  ' - Is the Efficiency parameter missing an entry for this demand?\n'
		  ' - Does a tech that satisfies this demand need a longer '
		  'LifetimeProcess?\n')
		raise TemoaFlowError( msg.format(dem, p, s, d) )

# End Temoa rule "partials"
###############################################################################

##############################################################################
# Begin validation and initialization routines

def validate_time ( M ):
	from sys import maxint

	# We check for integer status here, rather then asking Coopr to do this via
	# a 'within=Integers' clause in the definition so that we can have a very
	# specific error message.  If we instead use Coopr's mechanism, the
	# coopr_python invocation of Temoa throws an error (including a traceback)
	# that has proven to be scary and/or impenetrable for the typical modeler.
	for year in M.time_exist:
		if isinstance(year, int): continue

		msg = ('Set "time_exist" requires integer-only elements.\n\n  Invalid '
		  'element: "{}"')
		raise TemoaValidationError( msg.format( year ))

	for year in M.time_future:
		if isinstance(year, int): continue

		msg = ('Set "time_future" requires integer-only elements.\n\n  Invalid '
		  'element: "{}"')
		raise TemoaValidationError( msg.format( year ))

	if len( M.time_future ) < 2:
		msg = ('Set "time_future" needs at least 2 specified years.  Temoa '
		  'treats the integer numbers specified in this set as boundary years '
		  'between periods, and uses them to automatically ascertain the length '
		  '(in years) of each period.  Note that this means that there will be '
		  'one less optimization period than the number of elements in this set.'
		)
		raise TemoaValidationError( msg )

	# Ensure that the time_exist < time_future
	exist    = len( M.time_exist ) and max( M.time_exist ) or -maxint
	horizonl = min( M.time_future )  # horizon "low"

	if not ( exist < horizonl ):
		msg = ('All items in time_future must be larger than in time_exist.\n'
		  'time_exist max:   {}\ntime_future min: {}')
		raise TemoaValidationError( msg.format(exist, horizonl) )


def validate_SegFrac ( M ):

	total = sum( i for i in M.SegFrac.itervalues() )

	if abs(float(total) - 1.0) > 1e-15:
		# We can't explicitly test for "!= 1.0" because of incremental roundoff
		# errors inherent in float manipulations and representations, so instead
		# compare against an epsilon value of "close enough".

		key_padding = max(map( get_str_padding, M.SegFrac.sparse_iterkeys() ))

		format = "%%-%ds = %%s" % key_padding
			# Works out to something like "%-25s = %s"

		items = sorted( M.SegFrac.items() )
		items = '\n   '.join( format % (str(k), v) for k, v in items )

		msg = ('The values of the SegFrac parameter do not sum to 1.  Each item '
		  'in SegFrac represents a fraction of a year, so they must total to '
		  '1.  Current values:\n   {}\n\tsum = {}')

		raise TemoaValidationError( msg.format(items, total ))


def CheckEfficiencyIndices ( M ):
	"Ensure that there are no unused items in any of the Efficiency index sets."

	c_physical = set( i for i, t, v, o in M.Efficiency.sparse_iterkeys() )
	techs      = set( t for i, t, v, o in M.Efficiency.sparse_iterkeys() )
	c_outputs  = set( o for i, t, v, o in M.Efficiency.sparse_iterkeys() )

	symdiff = c_physical.symmetric_difference( M.commodity_physical )
	if symdiff:
		msg = ('Unused or unspecified physical carriers.  Either add or remove '
		  'the following elements to the Set commodity_physical.'
		  '\n\n    Element(s): {}')
		symdiff = (str(i) for i in symdiff)
		raise TemoaValidationError( msg.format( ', '.join(symdiff) ))

	symdiff = techs.symmetric_difference( M.tech_all )
	if symdiff:
		msg = ('Unused or unspecified technologies.  Either add or remove '
		  'the following technology(ies) to the tech_resource or '
		  'tech_production Sets.\n\n    Technology(ies): {}')
		symdiff = (str(i) for i in symdiff)
		raise TemoaValidationError( msg.format( ', '.join(symdiff) ))

	diff = M.commodity_demand - c_outputs
	if diff:
		msg = ('Unused or unspecified outputs.  Either add or remove the '
		  'following elements to the commodity_demand Set.'
		  '\n\n    Element(s): {}')
		diff = (str(i) for i in diff)
		raise TemoaValidationError( msg.format( ', '.join(diff) ))


def CreateCapacityFactors ( M ):
	# Steps
	#  1. Collect all possible processes
	#  2. Find the ones _not_ specified in CapacityFactorProcess
	#  3. Set them, based on CapacityFactorTech.

	# Shorter names, for us lazy programmer types
	CFP = M.CapacityFactorProcess

	# Step 1
	processes  = set( (t, v) for i, t, v, o in M.Efficiency.sparse_iterkeys() )

	all_cfs = set(
	  (s, d, t, v)

	  for s, d, (t, v) in cross_product(
	    M.time_season,
	    M.time_of_day,
	    processes
	  )
	)

	# Step 2
	unspecified_cfs = all_cfs.difference( CFP.sparse_iterkeys() )

	# Step 3

	# Some hackery: We futz with _constructed because Pyomo thinks that this
	# Param is already constructed.  However, in our view, it is not yet,
	# because we're specifically targeting values that have not yet been
	# constructed, that we know are valid, and that we will need.

	if unspecified_cfs:
		CFP._constructed = False
		for s, d, t, v in unspecified_cfs:
			CFP[s, d, t, v] = M.CapacityFactorTech[s, d, t]
		CFP._constructed = True


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


def CreateDemands ( M ):
	# Steps to create the demand distributions
	# 1. Use Demand keys to ensure that all demands in commodity_demand are used
	#
	# 2. Find any slices not set in DemandDefaultDistribution, and set them
	#    based on the associated SegFrac slice.
	#
	# 3. Validate that the DemandDefaultDistribution sums to 1.
	#
	# 4. Find any per-demand DemandSpecificDistribution values not set, and set
	#    set them from DemandDefaultDistribution.  Note that this only sets a
	#    distribution for an end-use demand if the user has *not* specified _any_
	#    anything for that end-use demand.  Thus, it is up to the user to fully
	#    specify the distribution, or not.  No in-between.
	#
	# 5. Validate that the per-demand distributions sum to 1.

	# Step 0: some setup for a couple of reusable items

	# iget(2): 2 = magic number to specify the third column.  Currently the
	# demand in the tuple (s, d, dem)
	DSD_dem_getter = iget(2)

	# Step 1
	used_dems = set(dem for p, dem in M.Demand.sparse_iterkeys())
	unused_dems = sorted(M.commodity_demand.difference( used_dems ))
	if unused_dems:
		for dem in unused_dems:
			msg = ("Warning: Demand '{}' is unused\n")
			SE.write( msg.format( dem ) )

	# Step 2
	DDD = M.DemandDefaultDistribution   # Shorter, for us lazy programmer types
	unset_defaults = set(M.SegFrac.sparse_iterkeys())
	unset_defaults.difference_update(
	   DDD.sparse_iterkeys() )
	if unset_defaults:
		# Some hackery because Pyomo thinks that this Param is constructed.
		# However, in our view, it is not yet, because we're specifically
		# targeting values that have not yet been constructed, that we know are
		# valid, and that we will need.
		DDD._constructed = False
		for tslice in unset_defaults:
			DDD[ tslice ] = M.SegFrac[ tslice ]
		DDD._constructed = True

	# Step 3
	total = sum( i for i in DDD.itervalues() )
	if abs(float(total) - 1.0) > 1e-15:
		# We can't explicitly test for "!= 1.0" because of incremental roundoff
		# errors inherent in float manipulations and representations, so instead
		# compare against an epsilon value of "close enough".

		key_padding = max(map( get_str_padding, DDD.sparse_iterkeys() ))

		format = "%%-%ds = %%s" % key_padding
			# Works out to something like "%-25s = %s"

		items = sorted( DDD.items() )
		items = '\n   '.join( format % (str(k), v) for k, v in items )

		msg = ('The values of the DemandDefaultDistribution parameter do not '
		  'sum to 1.  The DemandDefaultDistribution specifies how end-use '
		  'demands are distributed among the time slices (i.e., time_season, '
		  'time_of_day), so together, the data must total to 1.  Current '
		  'values:\n   {}\n\tsum = {}')

		raise TemoaValidationError( msg.format(items, total) )

	# Step 4
	DSD = M.DemandSpecificDistribution

	demands_specified = set(map( DSD_dem_getter,
	   (i for i in DSD.sparse_iterkeys()) ))
	unset_demand_distributions = used_dems.difference( demands_specified )
	unset_distributions = set(
	   cross_product(M.time_season, M.time_of_day, unset_demand_distributions))

	if unset_distributions:
		# Some hackery because Pyomo thinks that this Param is constructed.
		# However, in our view, it is not yet, because we're specifically
		# targeting values that have not yet been constructed, that we know are
		# valid, and that we will need.
		DSD._constructed = False
		for s, d, dem in unset_distributions:
			DSD[s, d, dem] = DDD[s, d]
		DSD._constructed = True

	# Step 5
	for dem in used_dems:
		keys = (k for k in DSD.sparse_iterkeys() if DSD_dem_getter(k) == dem )
		total = sum( DSD[ i ] for i in keys )

		if abs(float(total) - 1.0) > 1e-15:
			# We can't explicitly test for "!= 1.0" because of incremental roundoff
			# errors inherent in float manipulations and representations, so
			# instead compare against an epsilon value of "close enough".

			keys = [k for k in DSD.sparse_iterkeys() if DSD_dem_getter(k) == dem ]
			key_padding = max(map( get_str_padding, keys ))

			format = "%%-%ds = %%s" % key_padding
				# Works out to something like "%-25s = %s"

			items = sorted( (k, DSD[k]) for k in keys )
			items = '\n   '.join( format % (str(k), v) for k, v in items )

			msg = ('The values of the DemandSpecificDistribution parameter do not '
			  'sum to 1.  The DemandSpecificDistribution specifies how end-use '
			  'demands are distributed per time-slice (i.e., time_season, '
			  'time_of_day).  Within each end-use Demand, then, the distribution '
			  'must total to 1.\n\n   Demand-specific distribution in error: '
			  ' {}\n\n   {}\n\tsum = {}')

			raise TemoaValidationError( msg.format(dem, items, total) )


def CreateCosts ( M ):
	# Steps
	#  1. Collect all possible cost indices (CostFixed, CostVariable)
	#  2. Find the ones _not_ specified in CostFixed and CostVariable
	#  3. Set them, based on Cost*VintageDefault

	# Shorter names, for us lazy programmer types
	CF = M.CostFixed
	CV = M.CostVariable

	# Step 1
	fixed_indices = set( M.CostFixed_ptv )
	var_indices   = set( M.CostVariable_ptv )

	# Step 2
	unspecified_fixed_prices = fixed_indices.difference( CF.sparse_iterkeys() )
	unspecified_var_prices   = var_indices.difference( CV.sparse_iterkeys() )

	# Step 3

	# Some hackery: We futz with _constructed because Pyomo thinks that this
	# Param is already constructed.  However, in our view, it is not yet,
	# because we're specifically targeting values that have not yet been
	# constructed, that we know are valid, and that we will need.

	if unspecified_fixed_prices:
		CF._constructed = False
		for p, t, v in unspecified_fixed_prices:
			if (t, v) in M.CostFixedVintageDefault:
				CF[p, t, v] = M.CostFixedVintageDefault[t, v]
		CF._constructed = True

	if unspecified_var_prices:
		CV._constructed = False
		for p, t, v in unspecified_var_prices:
			if (t, v) in M.CostVariableVintageDefault:
				CV[p, t, v] = M.CostVariableVintageDefault[t, v]
		CV._constructed = True


def validate_TechFlowSplits ( M ):
	from collections import defaultdict

	ispl = M.TechInputSplit
	ospl = M.TechOutputSplit

	isummed = defaultdict( float )
	osummed = defaultdict( float )
	for i, t in ispl:
		isummed[t] += value(ispl[i, t])
	for t, o in ospl:
		osummed[t] += value(ospl[t, o])

	epsilon = 1e-15
	for t, val in isummed.iteritems():
		# small enough; likely a rounding error
		if abs(val - 1) < epsilon: continue

		msg = ('TechInputSplit not fully specified for technology "{}".  The '
		  'sum over all inputs for each technology must sum to 1.\n\n    '
		  'Current sum: {}')

		raise TemoaValidationError( msg.format(t, val) )

	for t, val in osummed.iteritems():
		# small enough; likely a rounding error
		if abs(val - 1) < epsilon: continue

		msg = ('TechOutputSplit not fully specified for technology "{}".  The '
		  'sum over all outputs for each technology must sum to 1.\n\n    '
		  'Current sum: {}')

		raise TemoaValidationError( msg.format(t, val) )


def init_set_time_optimize ( M ):
	return sorted( M.time_future )[:-1]


def init_set_vintage_exist ( M ):
	return sorted( M.time_exist )


def init_set_vintage_optimize ( M ):
	return sorted( M.time_optimize )


# end validation and initialization routines
##############################################################################

##############################################################################
# Begin helper functions

# Global Variables (dictionaries to cache parsing of Efficiency parameter)
g_processInputs  = dict()
g_processOutputs = dict()
g_processVintages = dict()
g_processLoans = dict()
g_activeFlow_psditvo = None
g_activeActivity_ptv = None
g_activeCapacity_tv = None
g_activeCapacityAvailable_pt = None

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


##############################################################################
# Sparse index creation functions

# These functions serve to create sparse index sets, so that Coopr need only
# create the parameter, variable, and constraint indices with which it will
# actually operate.  This *tremendously* cuts down on memory usage, which
# decreases time and increases the maximum specifiable problem size.

##############################################################################
# Parameters

def CapacityFactorProcessIndices ( M ):
	indices = set(
	  (s, d, t, v)

	  for i, t, v, o in M.Efficiency.sparse_iterkeys()
	  for s in M.time_season
	  for d in M.time_of_day
	)

	return indices


def CapacityFactorTechIndices ( M ):
	indices = set(
	  (s, d, t)

	  for s, d, t, v in M.CapacityFactor_sdtv
	)

	return indices


def CostFixedIndices ( M ):
	return g_activeActivity_ptv


def CostVariableIndices ( M ):
	return g_activeActivity_ptv


def CostInvestIndices ( M ):
	indices = set(
	  (t, v)

	  for p, t, v in g_processLoans
	)

	return indices


def EmissionActivityIndices ( M ):
	indices = set(
	  (e, i, t, v, o)

	  for i, t, v, o in M.Efficiency.sparse_iterkeys()
	  for e in M.commodity_emissions
	)

	return indices


def LoanLifeFracIndices ( M ):
	"""\
Returns the set of (period, tech, vintage) tuples of process loans that die
between period boundaries.  The tuple indicates the last period in which a
process is active.
"""
	l_periods = set( M.time_optimize )
	l_max_year = max( M.time_future )

	indices = set()
	for t, v in M.LifetimeLoanProcess.sparse_iterkeys():
		l_death_year = v + value(M.LifetimeLoanProcess[t, v])
		if l_death_year < l_max_year and l_death_year not in l_periods:
			p = max( yy for yy in M.time_optimize if yy < l_death_year )
			indices.add( (p, t, v) )

	return indices


def ModelProcessLifeIndices ( M ):
	"""\
Returns the set of sensical (period, tech, vintage) tuples.  The tuple indicates
the periods in which a process is active, distinct from TechLifeFracIndices that
returns indices only for processes that EOL mid-period.
"""
	return g_activeActivity_ptv


def LifetimeProcessIndices ( M ):
	"""\
Based on the Efficiency parameter's indices, this function returns the set of
process indices that may be specified in the LifetimeProcess parameter.
"""
	indices = set(
	  (t, v)

	  for i, t, v, o in M.Efficiency.sparse_iterkeys()
	)

	return indices


def LifetimeLoanProcessIndices ( M ):
	"""\
Based on the Efficiency parameter's indices and time_future parameter, this
function returns the set of process indices that may be specified in the
CostInvest parameter.
"""
	min_period = min( M.vintage_optimize )

	indices = set(
	  (t, v)

	  for i, t, v, o in M.Efficiency.sparse_iterkeys()
	  if v >= min_period
	)

	return indices


# End parameters
##############################################################################

##############################################################################
# Variables

def CapacityVariableIndices ( M ):
	return g_activeCapacity_tv

def CapacityAvailableVariableIndices ( M ):
	return g_activeCapacityAvailable_pt

def FlowVariableIndices ( M ):
	return g_activeFlow_psditvo


def ActivityVariableIndices ( M ):
	activity_indices = set(
	  (p, s, d, t, v)

	  for p, t, v in g_activeActivity_ptv
	  for s in M.time_season
	  for d in M.time_of_day
	)

	return activity_indices


def ActivityByPeriodAndProcessVarIndices ( M ):
	return g_activeActivity_ptv


# End variables
##############################################################################

##############################################################################
# Constraints


def DemandActivityConstraintIndices ( M ):
	indices = set()

	dem_slices = dict()
	for p, s, d, dem in M.DemandConstraint_psdc:
		if (p, dem) not in dem_slices:
			dem_slices[p, dem] = set()
		dem_slices[p, dem].add( (s, d) )

	for (p, dem), slices in dem_slices.iteritems():
		# No need for this constraint if demand is only in one slice.
		if not len( slices ) > 1: continue
		slices = sorted( slices )
		first = slices[0]
		tmp = set(
		  (p, s, d, t, v, dem, first[0], first[1])

		  for Fp, Fs, Fd, i, t, v, Fo in M.V_FlowOut.iterkeys()
		  if Fp == p and Fo == dem
		  for s, d in slices[1:]
		  if Fs == s and Fd == d
		)
		indices.update( tmp )

	return indices


def DemandConstraintIndices ( M ):
	used_dems = set(dem for p, dem in M.Demand.sparse_iterkeys())
	DSD_keys = M.DemandSpecificDistribution.sparse_keys()
	dem_slices = { dem : set(
	    (s, d)
	    for s in M.time_season
	    for d in M.time_of_day
	    if (s, d, dem) in DSD_keys )
	  for dem in used_dems
	}

	indices = set(
	  (p, s, d, dem)

	  for p, dem in M.Demand.sparse_iterkeys()
	  for s, d in dem_slices[ dem ]
	)

	return indices


def BaseloadDiurnalConstraintIndices ( M ):
	indices = set(
	  (p, s, d, t, v)

	  for p in M.time_optimize
	  for t in M.tech_baseload
	  for v in ProcessVintages( p, t )
	  for s in M.time_season
	  for d in M.time_of_day
	)

	return indices


def CommodityBalanceConstraintIndices ( M ):
	indices = set(
	  (p, s, d, o)

	  for p in M.time_optimize
	  for t in M.tech_all
	  for v in ProcessVintages( p, t )
	  for i in ProcessInputs( p, t, v )
	  for o in ProcessOutputsByInput( p, t, v, i )
	  for s in M.time_season
	  for d in M.time_of_day
	)

	return indices


def ProcessBalanceConstraintIndices ( M ):
	indices = set(
	  (p, s, d, i, t, v, o)

	  for p in M.time_optimize
	  for t in M.tech_all
	  if t not in M.tech_storage
	  for v in ProcessVintages( p, t )
	  for i in ProcessInputs( p, t, v )
	  for o in ProcessOutputsByInput( p, t, v, i )
	  for s in M.time_season
	  for d in M.time_of_day
	)

	return indices


def StorageConstraintIndices ( M ):
	indices = set(
	  (p, s, i, t, v, o)

	  for p in M.time_optimize
	  for t in M.tech_storage
	  for v in ProcessVintages( p, t )
	  for i in ProcessInputs( p, t, v )
	  for o in ProcessOutputsByInput( p, t, v, i )
	  for s in M.time_season
	)

	return indices


def TechInputSplitConstraintIndices ( M ):
	indices = set(
	  (p, s, d, i, t, v)

	  for i, t in M.TechInputSplit.sparse_iterkeys()
	  for p in M.time_optimize
	  for v in ProcessVintages( p, t )
	  for s in M.time_season
	  for d in M.time_of_day
	)

	return indices


def TechOutputSplitConstraintIndices ( M ):
	indices = set(
	  (p, s, d, t, v, o)

	  for t, o in M.TechOutputSplit.sparse_iterkeys()
	  for p in M.time_optimize
	  for v in ProcessVintages( p, t )
	  for s in M.time_season
	  for d in M.time_of_day
	)

	return indices

# End constraints
##############################################################################

# End sparse index creation functions
##############################################################################

##############################################################################
# Helper functions

# These functions utilize global variables that are created in
# InitializeProcessParameters, to aid in creation of sparse index sets, and
# to increase readability of Coopr's often programmer-centric syntax.

def ProcessInputs ( p, t, v ):
	index = (p, t, v)
	if index in g_processInputs:
		return g_processInputs[ index ]
	return set()


def ProcessOutputs ( p, t, v ):
	"""\
index = (period, tech, vintage)
	"""
	index = (p, t, v)
	if index in g_processOutputs:
		return g_processOutputs[ index ]
	return set()


def ProcessInputsByOutput ( p, t, v, o ):
	"""\
Return the set of input energy carriers used by a process (t, v) in period (p)
to produce a given output carrier (o).
"""
	index = (p, t, v)
	if index in g_processOutputs:
		if o in g_processOutputs[ index ]:
			return g_processInputs[ index ]

	return set()


def ProcessOutputsByInput ( p, t, v, i ):
	"""\
Return the set of output energy carriers used by a process (t, v) in period (p)
to produce a given input carrier (o).
"""
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


def ValidCapacity ( t, v ):
	return (t, v) in g_activeCapacity_tv


def isValidProcess ( p, i, t, v, o ):
	"""\
Returns a boolean (True or False) indicating whether, in any given period, a
technology can take a specified input carrier and convert it to and specified
output carrier.
"""
	index = (p, t, v)
	if index in g_processInputs and index in g_processOutputs:
		if i in g_processInputs[ index ]:
			if o in g_processOutputs[ index ]:
				return True

	return False



# End helper functions
##############################################################################

###############################################################################
# Miscellaneous routines


def version ( ):
	from sys import stdout as SO
	from os.path import basename, dirname

	bname = basename( dirname( __file__ ))

	if 'HEAD' == TEMOA_GIT_VERSION:
		msg = """
{}: Temoa Model, v"Bleeding Edge"

You are using a development version of Temoa.  Use Git to determine the current
branch name and number.  Command line hints:

      # from within the code directory
    $ git branch
    $ git status    # to remind you of any changes you have made
    $ git log -1    # -1 is optional, showing only the most recent commit
"""

		args = (bname,)

	else:
		msg = """
{}: Temoa Model, Release Date: {}
Git Hash: {}

Temoa does not currently have version numbers, but uses the date of release as a
proxy.  The hexadecimal Git Hash number uniquely identifies the exact
branch/commit that created '{}'.
"""

		args = (bname, TEMOA_RELEASE_DATE, TEMOA_GIT_VERSION, bname)

	msg += """
Copyright (C) 2011-2014 Kevin Hunter, Joseph F. DeCarolis

We provide Temoa -- the model and associated scripts -- "as-is" with no express
or implied warranty for accuracy or accessibility.  Temoa is a research tool,
given in good faith to the community (anyone who uses Temoa for any purpose) as
free software under the terms of the GNU Affero Public License, version 3 or, at
your option, any later version (AGPLv3+).
"""

	SO.write( msg.format( *args ))
	raise SystemExit


def bibliographicalInformation ( ):
	from sys import stdout as SO

	msg = """
Please cite the following paper if your use of Temoa leads to a publishable
result:

  Title:     Modeling for Insight Using Tools for Energy Model Optimization and Analysis (Temoa)
  Authors:   Kevin Hunter, Sarat Sreepathi, Joseph F. DeCarolis
  Date:      November, 2013
  Publisher: Elsevier
  Journal:   Energy Economics
  Volume:    40
  Pages:     339 - 349
  ISSN:      0140-9883
  DOI:       http://dx.doi.org/10.1016/j.eneco.2013.07.014
  URL:       http://www.sciencedirect.com/science/article/pii/S014098831300159X

For copy and paste or BibTex use:

  Kevin Hunter, Sarat Sreepathi, Joseph F. DeCarolis, Modeling for Insight Using Tools for Energy Model Optimization and Analysis (Temoa), Energy Economics, Volume 40, November 2013, Pages 339-349, ISSN 0140-9883, http://dx.doi.org/10.1016/j.eneco.2013.07.014.

  (BibTeX)
@article{Hunter_etal_2013,
  title   = "Modeling for {I}nsight {U}sing {T}ools for {E}nergy {M}odel {O}ptimization and {A}nalysis ({T}emoa)",
  journal = "Energy Economics",
  volume  = "40",
  pages   = "339 - 349",
  month   = "November",
  year    = "2013",
  issn    = "0140-9883",
  doi     = "http://dx.doi.org/10.1016/j.eneco.2013.07.014",
  url     = "http://www.sciencedirect.com/science/article/pii/S014098831300159X",
  author  = "Kevin Hunter and Sarat Sreepathi and Joseph F. DeCarolis"
}

"""

	SO.write( msg )
	raise SystemExit


def parse_args ( ):
	import argparse, platform, sys

	from pyomo.opt import SolverFactory as SF
	from logging import getLogger

	# used for some error messages below.
	red_bold = cyan_bold = reset = ''
	if platform.system() != 'Windows' and SE.isatty():
		red_bold  = '\x1b[1;31m'
		cyan_bold = '\x1b[1;36m'
		reset     = '\x1b[0m'

	logger = getLogger('pyomo.solvers')
	logger_status = logger.disabled
	logger.disabled = True  # no need for warnings: it's what we're testing!

	available_solvers = set()
	for sname in SF.services():   # list of solver interface names
		# initial underscore ('_'): Coopr's method to mark non-public plugins
		if '_' == sname[0]: continue

		solver = SF( sname )
		if not solver: continue

		if 'os' == sname: continue     # Workaround current bug in Coopr
		if not solver.available( exception_flag=False ): continue
		available_solvers.add( sname )

	logger.disabled = logger_status  # put back the way it was.

	if available_solvers:
		if 'cplex' in available_solvers:
			default_solver = 'cplex'
		elif 'gurobi' in available_solvers:
			default_solver = 'gurobi'
		elif 'cbc' in available_solvers:
			default_solver = 'cbc'
		elif 'glpk' in available_solvers:
			default_solver = 'glpk'
		else:
			default_solver = iter(available_solvers).next()
	else:
		default_solver = 'NONE'
		SE.write('\nNOTICE: Coopr did not find any suitable solvers.  Temoa will '
		   'not be able to solve any models.  If you need help, ask on the '
		   'Temoa Project forum: http://temoaproject.org/\n\n' )

	parser = argparse.ArgumentParser()
	parser.prog = path.basename( argv[0].strip('/') )

	graphviz    = parser.add_argument_group('Graphviz Options')
	solver      = parser.add_argument_group('Solver Options')
	stochastic  = parser.add_argument_group('Stochastic Options')
	postprocess = parser.add_argument_group('Postprocessing Options')

	parser.add_argument('dot_dat',
	  type=str,
	  nargs='*',
	  help='AMPL-format data file(s) with which to create a model instance. '
	       'e.g. "data.dat"'
	)


	parser.add_argument( '--fix_variables',
	  help='Path to file containing variables to fix.  The file format is the '
	    'same as the default Temoa output.',
	  action='store',
	  dest='fix_variables',
	  default=None)

	parser.add_argument( '--how_to_cite',
	  help='Bibliographical information for citation, in the case that Temoa '
	    'contributes to a project that leads to a scientific publication.',
	  action='store_true',
	  dest='how_to_cite',
	  default=False)

	parser.add_argument( '-V', '--version',
	  help='Display the Temoa version information, then exit.',
	  action='store_true',
	  dest='version',
	  default=False
	)


	graphviz.add_argument( '--graph_format',
	  help='Create a system-wide visual depiction of the model.  The '
	       'available options are the formats available to Graphviz.  To get '
	       'a list of available formats, use the "dot" command: dot -Txxx. '
	       '[Default: None]',
	  action='store',
	  dest='graph_format',
	  default=None)

	graphviz.add_argument('--show_capacity',
	  help='Choose whether or not the capacity shows up in the subgraphs.  '
	       '[Default: not shown]',
	  action='store_true',
	  dest='show_capacity',
	  default=False)

	graphviz.add_argument( '--graph_type',
	  help='Choose the type of subgraph depiction desired.  [Default: '
	       'separate_vintages]',
	  action='store',
	  dest='graph_type',
	  choices=('explicit_vintages', 'separate_vintages'),
	  default='separate_vintages')

	graphviz.add_argument('--use_splines',
	  help='Choose whether the subgraph edges needs to be straight or curved.'
	       '  [Default: use straight lines, not splines]',
	  action='store_true',
	  dest='splinevar',
	  default=False)


	solver.add_argument('--solver',
	  help="Which backend solver to use.  See 'pyomo --help-solvers' for a list "
	       'of solvers with which Coopr can interface.  The list shown here is '
	       'what Coopr can currently find on this system.  [Default: {}]'
	       .format(default_solver),
	  action='store',
	  choices=sorted(available_solvers),
	  dest='solver',
	  default=default_solver)

	solver.add_argument('--generate_solver_lp_file',
	  help='Request that solver create an LP representation of the optimization '
	       'problem.  Mainly used for model debugging purposes.  The file name '
	       'will have the same base name as the first dot_dat file specified.  '
	       '[Note: this option currently only works with the GLPK solver.] '
	       '[Default: do not create solver LP file]',
	  action='store_true',
	  dest='generateSolverLP',
	  default=False)

	solver.add_argument('--keep_pyomo_lp_file',
	  help='Save the LP file as written by Pyomo.  This is distinct from the '
	       "solver's generated LP file, but /should/ represent the same model.  "
	       'Mainly used for debugging purposes.  '
	       '[Default: remove Pyomo LP file]',
	  action='store_true',
	  dest='keepPyomoLP',
	  default=False)


	stochastic.add_argument('--eciu',
	  help='"Expected Cost of Ignoring Uncertainty" -- Calculate the costs of '
	       'ignoring the uncertainty of a stochastic tree.  Specify the path '
	       'to the stochastic scenario directory.  (i.e., where to find '
	       'ScenarioStructure.dat)',
	  metavar='STOCHASTIC_DIRECTORY',
	  dest='eciu',
	  default=None)


	options = parser.parse_args()

	# First, the options that exit or do not perform any "real" computation
	if options.version:
		version()
		# this function exits

	if options.how_to_cite:
		bibliographicalInformation()
		# this function exits.

	# It would be nice if this implemented with add_mutually_exclusive_group
	# but I /also/ want them in separate groups for display.  Bummer.
	if not (options.dot_dat or options.eciu):
		usage = parser.format_usage()
		msg = ('Missing a data file to optimize (e.g., test.dat)')
		msg = '{}\n{}{}{}'.format( usage, red_bold, msg, reset )
		raise TemoaCommandLineArgumentError( msg )

	elif options.dot_dat and options.eciu:
		usage = parser.format_usage()
		msg = ('Conflicting option and arguments: --eciu and data files\n\n'
		       '--eciu is for performing an analysis on a directory of data '
		       'files, as are used in a stochastic analysis with PySP.  Please '
		       'remove either of --eciu or the data files from the command '
		       'line.')
		msg = '{}\n{}{}{}'.format( usage, red_bold, msg, reset )
		raise TemoaCommandLineArgumentError( msg )
	elif options.eciu:
		# can this be subsumed directly into the argparse module functionality?
		from os.path import isdir, isfile, join
		edir = options.eciu

		if not isdir( options.eciu ):
			msg = "{}--eciu requires a directory.{}".format( red_bold, reset )
			msg = "{}\n\nSupplied path: '{}'".format( msg, edir )
			raise TemoaCommandLineArgumentError( msg )

		structure_file = join( edir, 'ScenarioStructure.dat' )
		if not isfile( structure_file ):
			msg = "'{}{}{}' does not appear to contain a PySP stochastic program."
			msg = '{}{}{}'.format( red_bold, msg, reset )
			raise TemoaCommandLineArgumentError(
			   msg.format( reset, edir, red_bold ))

	if options.graph_format:
		try:
			from subprocess import call
			from os import devnull

			with open(devnull, 'wb') as fnull:
				call(('dot', '-Txxx'), stdout=fnull, stderr=fnull)

		except OSError:
			msg = ('Missing Graphviz.\n\nYou have requested to generate Graphviz '
			  'images of your model.  Unfortunately, Python is not able to find '
			  'the "dot" executable from the Graphviz suite.  Do you need to '
			  'install the Graphviz suite?  If you need help with this step, '
			  'please Google, or consult the Temoa forum.\n\n')

			raise TemoaNoExecutableError( msg )

	s_choice = str( options.solver ).upper()
	SE.write('Notice: Using the {} solver interface.\n'.format( s_choice ))
	SE.flush()

	return options

# End miscellaneous routines
###############################################################################

###############################################################################
# Direct invocation methods (when modeler runs via "python model.py ..."

def solve_perfect_foresight ( model, optimizer, options ):
	from time import clock
	import sys, os, gc

	from pyomo.core import DataPortal

	from pformat_results import pformat_results

	opt = optimizer              # for us lazy programmer types
	dot_dats = options.dot_dat

	if options.generateSolverLP:
		opt.options.wlp = path.basename( dot_dats[0] )[:-4] + '.lp'
		SE.write('\nSolver will write file: {}\n\n'.format( opt.options.wlp ))

	SE.write( '[        ] Reading data files.'); SE.flush()
	# Recreate the pyomo command's ability to specify multiple "dot dat" files
	# on the command line
	begin = clock()
	duration = lambda: clock() - begin

	modeldata = DataPortal( model=model )
	for fname in dot_dats:
		if fname[-4:] != '.dat':
			msg = "\n\nExpecting a dot dat (e.g., data.dat) file, found '{}'\n"
			raise TemoaValidationError( msg.format( fname ))
		modeldata.load( filename=fname )
	SE.write( '\r[%8.2f\n' % duration() )

	SE.write( '[        ] Creating Temoa model instance.'); SE.flush()
	instance = model.create( modeldata )
	SE.write( '\r[%8.2f\n' % duration() )

	if options.fix_variables:
		SE.write( '[        ] Fixing supplied variables.'); SE.flush()
		import re

		# Assumption: All variables are indexed
		# We accept \S+ instead of the more precise (\d+(?:\.\d+)?) because we
		# want to be helpful in case of a user typo.
		var_data_re = re.compile( r'^ *(\S+) +(V_\w+)\[(\S+)\]$' )
		int_re = re.compile( r'^\d+$' )

		with open( options.fix_variables, 'rb' ) as f:
			for lineno, line in enumerate( f, 1 ):    # humans think 1-based
				match = var_data_re.match( line )

				# We ignore (and thereby allow) lines that don't match the Temoa
				# value variable[index] per line output.  This enables folks to
				# comment and uncomment lines if they'd like.
				if not match: continue

				try:
					value, vgroup, vindex = match.groups()
					vindex = vindex.split(',')
					value = float( value )
				except ValueError as ve:
					msg = '\nLine {:d}: Unable to parse value for "{}{}" ({})\n'
					raise TemoaValidationError( msg.format(
					  lineno, vgroup, vindex, value ))

				for i, index in enumerate( vindex ):
					# if index is an integer, convert it so it matches indices
					# Problem: if modeler has used integer values for indices
					# other than period or vintage.
					if int_re.match( index ):
						vindex[ i ] = int( index )

				try:
					m_var = getattr( instance, vgroup )[ tuple(vindex) ]
					m_var.fixed = True
					m_var.set_value( value )

				except AttributeError as ae:
					if "'AbstractModel' object has no attribute " in str(ae):
						# This could be so much cleaner if Coopr had Coopr-specific
						# error classes.  Sigh.

						msg = 'Line {:d}: Model does not have a variable named "{}".'
						msg = msg.format( lineno, vgroup )
						raise TemoaObjectNotFoundError( msg )

					raise

				except KeyError as ke:
					if 'Error accessing indexed component' in str(ke):
						# This could be so much cleaner if Coopr had Coopr-specific
						# error classes.  Sigh.

						msg = 'Line {:d}: Variable "{}" has no index "{}".'
						vindex = str( tuple(vindex) )
						msg = msg.format( lineno, vgroup, vindex )
						raise TemoaKeyError( msg )

					raise

		SE.write( '\r[%8.2f\n' % duration() )
		SE.write( '[        ] Preprocessing fixed variables.'); SE.flush()
		instance.preprocess()
		SE.write( '\r[%8.2f\n' % duration() )

	# Now do the solve and ...
	SE.write( '[        ] Solving.'); SE.flush()
	if opt:
		result = opt.solve( instance )
		SE.write( '\r[%8.2f\n' % duration() )

		# return signal handlers to defaults, again
		signal(SIGINT, default_int_handler)

	else:
		SE.write( '\r---------- Not solving: no available solver\n' )
		return

	# ... print the easier-to-read/parse format
	msg = '[        ] Calculating reporting variables and formatting results.'
	SE.write( msg ); SE.flush()
	updated_results = instance.update_results( result )
	instance.load( result )
	formatted_results = pformat_results( instance, updated_results )
	SE.write( '\r[%8.2f\n' % duration() )

	SO.write( formatted_results.getvalue() )

	if options.graph_format:
		# we can't simply call SO.close() here, because we use multiprocess.Process
		# in _graphviz, which also calls close() -- an operation that may only be
		# called once on a file object.  We also can't simply close stdout, because
		# Python treats it specially with a guarantee that std* objects are /never/
		# closed.  XXX: And still, for now, this doesn't appear to work at all
		SO.flush()
		os.close( SO.fileno() )
		import sys
		sys.stdout = open( '/dev/null', 'w' )

		SE.write( '[        ] Creating Temoa model diagrams.' ); SE.flush()
		instance.load( result )
		CreateModelDiagrams( instance, options )
		SE.write( '\r[%8.2f\n' % duration() )


def solve_true_cost_of_guessing ( optimizer, options, epsilon=1e-6 ):
	import multiprocessing as MP, os, cPickle as pickle

	from collections import deque, defaultdict
	from os import getcwd, chdir
	from os.path import isfile, abspath, exists

	from pyomo.core import DataPortal, Var
	from pyomo.pysp.util.scenariomodels import scenario_tree_model
	from pyomo.pysp.phutils import extractVariableNameAndIndex

	from temoa_model import temoa_create_model
	from temoa_rules import PeriodCost_rule

	pwd = abspath( getcwd() )
	chdir( options.eciu )
	sStructure = scenario_tree_model.create( filename='ScenarioStructure.dat' )

	# Step 1: find the root node.  PySP doesn't make this very easy ...

	# a child -> parent mapping, because every child has only one parent, but
	# not vice-versa
	ctpTree = dict()

	to_process = deque()
	to_process.extend( sStructure.Children.keys() )
	while to_process:
		node = to_process.pop()
		if node in sStructure.Children:
			# it's a parent!
			new_nodes = set( sStructure.Children[ node ] )
			to_process.extend( new_nodes )
			ctpTree.update({n : node for n in new_nodes })

	                 # parents           -     children
	root_node = (set( ctpTree.values() ) - set( ctpTree.keys() )).pop()

	ptcTree = defaultdict( list )
	for c, p in ctpTree.iteritems():
		ptcTree[ p ].append( c )
	ptcTree = dict( ptcTree )   # be slightly defensive; catch any additions

	leaf_nodes = set(ctpTree.keys()) - set(ctpTree.values())

	scenario_nodes = dict()
	for node in leaf_nodes:
		s = list()
		scenario_nodes[ node ] = s
		while node in ctpTree:
			s.append( node )
			node = ctpTree[ node ]
		s.append( node )
		s.reverse()

	leaf_nodes_by_node = defaultdict(set)
	for fnode in leaf_nodes:
		node = fnode
		while node in ctpTree:
			leaf_nodes_by_node[ node ].add( fnode )
			node = ctpTree[ node ]
		leaf_nodes_by_node[ node ].add( fnode ) # get the root node
	leaf_nodes_by_node = dict( leaf_nodes_by_node )   # be slightly defensive


	def build_full_solve_dict ( tree, node, ptc ):
		if node not in ptc: return

		for child in ptc[ node ]:
			if child not in tree:
				tree[ child ] = tree[ node ]  # i.e., CondProb = 100%
			build_full_solve_dict( tree, child, ptc )


	def build_minimal_solve_dict ( tree, leaves_by_node, node, last, ptc ):
		""" Remove redundant solves """
		assume = tuple( leaves_by_node[ node ] )
		new_assume = assume
		if last:
			assume = tuple( sorted( ','.join(i)
			  for i in cross_product( last, assume ))
			)
			new_assume = list()

			for i, a in enumerate(assume):
				items = a.split(',')
				if items[ -1 ] != items[ -2 ]:
					# This is the crux of the check: if the final two assumptions
					# are the same, then the second is redundant.
					new_assume.append( assume[i] )

		tree[ node ] = tuple( new_assume )

		while node in ptc and len( ptc[ node ] ) == 1:
			node = ptc[ node ][0]

		if node in ptc:
			for child in ptc[ node ]:
				build_minimal_solve_dict( tree, leaves_by_node, child, assume, ptc )

	##### Begin multiprocessing function #####

	def do_solve (
	  sem,                # BoundedSemaphore
	  exc_q,              # This is an MP project: give exceptions to head
	  solver_options,
	  solve_counts,
	  scen_nodes,         # nodes to scenario: { scen : [R, Rs0, ... scen] }
	  this_node,          # a string, representing which node in the tree
	  this_assumptions,   # Assumptions so far, comma separated, last one is
	                      # the assumptions to make from this_node
	  file_locks,         # MP.Lock dict: to prevent read/write collisions
	  s_structure,        # PySP Scenario structure object
	):
		solve_num, num_solves = solve_counts

		try:
			from setproctitle import setproctitle as setProcessTitle
			msg = '({}/{}) Solving assumption: {}'
			msg = msg.format( solve_num, num_solves, this_assumptions )
			setProcessTitle( msg )
			del msg
		except ImportError, e:
			pass

		CP = s_structure.ConditionalProbability

		assumptions = this_assumptions.split(',')
		assumed_fs = assumptions[-1]
		assumptions = assumptions[:-1]

		node_path = scen_nodes[ assumed_fs ]
		node_index = node_path.index( this_node )

		# path_so_far = nodes to here, _not_ including here
		path_so_far = node_path[0:node_index]

		# nodes from here to assumed_fs, _including_ here
		this_subpath = node_path[node_index:]

		msg = ("({}) Solving from node '{}', having assumed '{}' and assuming "
		  "'{}'.\n")
		SE.write( msg.format( solve_num, this_node, ','.join(assumptions),
		   assumed_fs ))

		from pyomo.opt import SolverFactory
		opt = SolverFactory( solver_options )

		model = temoa_create_model()

		mdata = DataPortal( model=model )
		for node_name in scen_nodes[ assumed_fs ]:
			mdata.load( filename=node_name + '.dat' )
		m = model.create( mdata )

		# path_so_far includes nodes with CP of 1.
		past_assumed = ''
		last_assumed = ''               # TODO: this is currently a hack, because
		i_assume = iter( assumptions )  # TODO: of an inconsistent data structure
		for node in path_so_far:
			if CP[ node ] < 1 or node == 'R':
				assumed = next( i_assume )
				if past_assumed:
					past_assumed += ',' + assumed
				else:
					past_assumed += assumed
			last_assumed = assumed        # TODO: hack: deal with CP = 1

			fname = node + '.pickle'

			with file_locks[ n ]:
				# Gzip might be nice, but it takes long enough that it's a
				# bottleneck.  I have not tried any compression less than the
				# default (9), so it may yet be a win.  However, for now, it kills
				# parallelism because it happens within the file locks (which are,
				# unfortunately, a necessity)..
				with open( fname, 'rb' ) as f:
					try:
						saved_data = pickle.load( f )[ past_assumed ]
					except:
						msg = ( 'An exception, while loading {}[{}], from node {}, '
						  ' with path_so_far {};  my_assumptions: {}\n')
						msg = msg.format( fname, past_assumed, this_node,
						                  path_so_far, assumptions )
						exception_q.put( TemoaError( msg ))
						sem.release()
						return

			# the pickle loaded a dict, saved_data is now a tuple of
			#  (node_cost, {'var' : (index, val, index, val ...)})

			node_cost, var_values = saved_data
			# Fix variables per what was pickled previously
			for vname, values in var_values.iteritems():
				m_var = getattr(m, vname)
				for index, val in iter_in_chunks( values, 2 ):
					v = m_var[ index ]
					v.fixed = True
					v.set_value( val )

		# do the preprocess and solve.
		m.preprocess()
		results = opt.solve( m )
		m.load( results )

		if 'infeasible' in str( results['Solver'] ):
			msg = ('Infeasible solve.  Node: {}, path_so_far {}; my_assumptions: '
			  '{}\n\n  Writing fixed variable values to {}')
			msg = msg.format( this_node, path_so_far, assumptions, fname )
			exc_q.put( TemoaInfeasibleError( msg ) )
			sem.release()
			return

		# now, save the variables for any subsequent runs
		node_assumptions = this_assumptions
		for node in this_subpath:
			stage = s_structure.NodeStage[ node ]
			stage_vars = s_structure.StageVariables[ stage ]

			# Cheat, and assume some knowledge of the underlying data
			#   This removes the leading s; e.g., s1990 -> 1990
			period = int( stage[1:] )
			node_cost = value( PeriodCost_rule( m, period ))

			vars_to_save = defaultdict( set )
			node_vars    = defaultdict( list )
			for var_string in stage_vars:
				vname, index = extractVariableNameAndIndex( var_string )
				vars_to_save[ vname ].add( index )

			for vname, indices in vars_to_save.iteritems():
				m_var = getattr(m, vname)
				for index in indices:
					try:
						val = value( m_var[ index ] )
					except:
						if 'infeasible' in str( sol ):

							msg = ( '    ---> Solver found problem infeasible <---' )
							SE.write( '\n' + msg + '\n\n')
						raise
					if val < epsilon:
						# variables can't be negative, and they may be when within an
						# epsilon of 0 (because the solver said "good enough")
						val = 0
					node_vars[ vname ].extend( (index, val) )

			data_to_save = (node_cost, node_vars)

			fname = node + '.pickle'

			with file_locks[ node ]:
				with open( fname, 'rb' ) as f:
					saved_node_data = pickle.load( f )

				saved_node_data[ node_assumptions ] = data_to_save
				with open( fname, 'wb' ) as f:
					pickle.dump( saved_node_data, f, pickle.HIGHEST_PROTOCOL )
					f.flush()
					os.fdatasync( f.fileno() )

				if node in s_structure.Children:
					if len( s_structure.Children[ node ] ) > 1:
						node_assumptions += ',' + assumed_fs

		# sem = the process BoundedSemaphor.  Still shared memory ...
		sem.release()


	###### End multiprocessing function #####


	# Step 1: Find out what we need to solve
	to_solve = dict()
	build_minimal_solve_dict( to_solve, leaf_nodes_by_node, 'R', (), ptcTree )

	# For printing the solution, need to include all nodes.
	solved = dict( to_solve )
	build_full_solve_dict( solved, 'R', ptcTree )

	file_locks     = dict()

	# Step 2: Find out what -- if anything -- has already been processed
	for n, assumptions in to_solve.iteritems():
		fname = n + '.pickle'
		fd = os.open( fname, os.O_CREAT, 0600 )
		with os.fdopen( fd, 'rb' ) as f:
			try:
				saved_data = pickle.load( f )
			except EOFError as e:
				# an empty or corrupt file.  No matter.
				saved_data = {}

		with open( fname, 'wb' ) as f:
			pickle.dump( saved_data, f, pickle.HIGHEST_PROTOCOL )
			f.flush()
			os.fdatasync( f.fileno() )

		file_locks[ n ] = MP.Lock()

	for n in sStructure.Nodes:
		if n in to_solve: continue
		file_locks[ n ] = MP.Lock()

		fname = n + '.pickle'
		f = os.open( fname, os.O_CREAT, 0600 )
		with os.fdopen( f, 'rb' ) as pickle_file:
			try:
				saved_data = pickle.load( pickle_file )
			except EOFError as e:
				saved_data = {}

		with open( fname, 'wb' ) as f:
			pickle.dump( saved_data, f, pickle.HIGHEST_PROTOCOL )
			f.flush()
			os.fdatasync( f.fileno() )


	jobs_capacity = int( 1.5 * MP.cpu_count() )
	process_sem = MP.BoundedSemaphore( jobs_capacity )
	exception_q = MP.Queue()

	# sort is not strictly necessary, but doing so allows us to only start a
	# small number of processes, rather than potentially overwhelming the OS
	# process table.
	last = ''

	import inspect

	def lineno():
		"""Returns the current line number in our program."""
		return inspect.currentframe().f_back.f_lineno

	# In fact, sort is half of what we want.  Through observation, it appears
	# that at larger ECIU stages (i.e. 4+ stage), one partial bottleneck is file
	# access.  Since the amount of data that needs to be shared for 4-stage is
	# ~110 MiB, and the amount of data to share for 5 stage is ~400 MiB, there
	# are two steps that we could take to speed computation:
	# 1. First, sorting is good, letting us do a stage wise progression.
	#    However, we're getting hung on disk access, so we should instead solve
	#    either from random nodes, or divide the list into slices and
	#    round-robin through them.
	# 2. For "reasonable" expected sizes of data, could use a tmpfs backing,
	#    or some sort of shared memory approach
	class Serial ( object ):
		def __init__ ( self, beg=0 ):
			self.beg = beg

		def __call__ ( self ):
			self.beg += 1
			return self.beg

	from itertools import cycle

	def roundrobin( *iterables ):
		"roundrobin('ABC', 'D', 'EF') --> A D E B F C"
		# Recipe credited to George Sakkis
		pending = len(iterables)
		nexts = cycle(iter(it).next for it in iterables)
		while pending:
			try:
				for next in nexts:
					yield next()
			except StopIteration:
				pending -= 1
				nexts = cycle(islice(nexts, pending))

	to_solve_stages = defaultdict( set )     # { 1 : set('R'), 2 : set('Rs0s0s0', 'Rs0s0s1'), }
	stage_tracker = defaultdict( Serial() )  # { 'R' : 1, 'Rs0s0' : 2, ...}
	for i in sorted( to_solve ):
		stage_num = stage_tracker[ len(i) ]  # referencing it increments the Serial object
		to_solve_stages[ stage_num ].add( i )

	for stage, nodes in sorted( to_solve_stages.iteritems() ):

		# first, attempt to relieve a file access bottleneck by accessing
		# files in a chunked round-robin fashion.

		# this is still a poor substitute for a depth-first traversal, but
		# I have not yet figured that logic out.
		indices = list(xrange( stage ))
		indices.reverse()
		indexgetter = iget( *indices )

		assumptions_to_nodes = defaultdict(set)
		for n in nodes:
			for a in to_solve[ n ]:
				assumptions_to_nodes[ a ].add( n )
		to_solve_assumptions = assumptions_to_nodes.keys()
		to_solve_assumptions = [i.split(',') for i in to_solve_assumptions]
		to_solve_assumptions.sort( key=indexgetter )
		to_solve_assumptions = [','.join(i) for i in to_solve_assumptions]

		to_solve_pairs = [
		  (n, a)

		  for a in to_solve_assumptions
		  for n in assumptions_to_nodes[ a ]
		]
		del assumptions_to_nodes, to_solve_assumptions

		step = int(len( to_solve_pairs ) / jobs_capacity)
		step = max( 1, step )
		iters = [islice( to_solve_pairs, i, i + step )
		         for i in xrange( 0, len(to_solve_pairs), step )]

		# Preparing to solve the next stage.  Let this stage finish, first.
		active_children = MP.active_children()
		for p in active_children:
			p.join()

		num_solves = len( to_solve_pairs )
		solve_counter = 0
		SE.write('\nThere are {} solves in this stage\n'.format( num_solves ))
		for node, a in roundrobin( *iters ):
			process_sem.acquire()
			if not exception_q.empty():
				for i in xrange( jobs_capacity -1 ):
					process_sem.acquire()
				e = exception_q.get()

				raise e
			solve_counter += 1  # For informing of progress through process names

			args = (
			  process_sem,
			  exception_q,
			  options.solver,
			  (solve_counter, num_solves),
			  scenario_nodes,
			  node,
			  a,
			  file_locks,
			  sStructure
			)

			MP.Process( target=do_solve, args=args ).start()
			# do_solve( *args )   # in case of need to debug: uncomment

		# don't care who's active; just clean up any zombies at end stage
		MP.active_children()

	# _Now_ we care, because active children mean we can't read results yet.
	processes = MP.active_children()
	for p in processes:
		p.join()

	# Finally: let's marshal the results and give 'em to the modeler!
	data = list()
	data.append(('','','','"Previously Assumed" is a chronologically ordered list of assumptions made, up to "this" node',))
	data.append(('At Node', 'Previously Assumed', 'Node Cost'))

	to_process.append( root_node )  # invariant from above: was empty deque
	last = root_node                # for blank lines between stages
	while to_process:
		node = to_process.popleft()
		if len( node ) != len( last ):
			data.append( tuple() ) # blank line

		fname = node + '.pickle'
		with open( fname, 'rb' ) as f:
			node_data = pickle.load( f )
		for assumption in sorted( node_data ):
			row = [ node, assumption, node_data[ assumption ][ 0 ] ]
			data.append( row )
		del node_data

		if node in ptcTree:
			to_process.extend( ptcTree[ node ] )
		last = node

	import csv, cStringIO
	csvdata = cStringIO.StringIO()
	writer = csv.writer( csvdata ); writer.writerows( data )
	print csvdata.getvalue()
	chdir( pwd )


def temoa_solve ( model ):
	from sys import argv, version_info

	if version_info < (2, 7):
		msg = ("Temoa requires Python v2.7 to run.\n\nIf you've "
		  "installed Coopr with Python 2.6 or less, you'll need to reinstall "
		  'Coopr, taking care to install with a Python 2.7 (or greater) '
		  'executable.')
		raise SystemExit( msg )

	options = parse_args()

	from pyomo.opt import SolverFactory

	opt = SolverFactory( options.solver )
	if opt:
		if options.keepPyomoLP:
			opt.keepfiles = True
			opt.symbolic_solver_labels = True

	elif options.solver != 'NONE':
		SE.write( "\nWarning: Unable to initialize solver interface for '{}'\n\n"
			.format( options.solver ))
		if SE.isatty():
			SE.write( "Please press enter to continue or Ctrl+C to quit." )
			raw_input()
		else:
			SE.write(
			  '\n\n  Not stopping for user input because stderr is not a tty.'
			  '\n  (This suggests that Temoa is currently running as part of a'
			  '\n  a larger script and the user is not able to see this'
			  '\n  message currently.  The user script is responsible for'
			  '\n  handling this situation appropriately.\n\n')

	try:
		if options.dot_dat:
			solve_perfect_foresight( model, opt, options )
		elif options.eciu:
			solve_true_cost_of_guessing( opt, options )
	except IOError as e:
		if e.errno == errno.EPIPE:
			# stdout has been closed, e.g., a user has quit the 'less' pager
			# There is no error on our part, so just quit gracefully
			return
		raise
	except KeyboardInterrupt as e:
		SE.write( '\n\nUser requested quit.  Exiting Temoa ...\n' )
		SE.flush()
	except SystemExit as e:
		SE.write( '\n\nTemoa exit requested.  Exiting ...\n' )
		SE.flush()


# End direct invocation methods
###############################################################################
