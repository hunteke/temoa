"""
Temoa - Tools for Energy Model Optimization and Analysis
  linear optimization; least cost; dynamic system visualization

Copyright (C) 2011-2012  Kevin Hunter, Joseph DeCarolis

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
from itertools import product as cross_product
from operator import itemgetter as iget
from os import path
from sys import argv, stderr as SE, stdout as SO

from temoa_graphviz import CreateModelDiagrams

try:
	from coopr.pyomo import *
except:

	import sys
	cpath = path.join('path', 'to', 'coopr', 'executable', 'coopr_python')
	if 'win' not in sys.platform:
		msg = """\
Option 1:
$ PATH=%(cpath)s:$PATH
$ coopr_python %(base)s  [options]  data.dat

Option 2:
$ %(cpath)s  %(base)s  [options]  data.dat
"""

	else:
		msg = """\
Option 1:
C:\\> set PATH=%(cpath)s:%%PATH%%
C:\\> coopr_python  %(base)s  [options]  data.dat

Option 2:
C:\\> %(cpath)s  %(base)s  [options]  data.dat
"""

	base = path.basename( sys.argv[0] )
	msg %= { 'cpath' : cpath, 'base' : base }
	msg = """\
Unable to find coopr.pyomo on the Python system path.  Are you running Coopr's
version of Python?  Here is one way to check:

  # look for items that have to do with the Coopr project
python -c "import sys, pprint; pprint.pprint(sys.path)"

If you aren't running with Coopr's environment for Python, you'll need to either
update your PATH environment variable to use Coopr's Python setup, or always
explicitly use the Coopr path:

%s
""" % msg

	raise ImportError( msg )


class TemoaError ( Exception ): pass
class TemoaCommandLineArgumentError ( TemoaError ): pass
class TemoaFlowError ( TemoaError ): pass
class TemoaValidationError ( TemoaError ): pass

def get_str_padding ( obj ):
	return len(str( obj ))

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
		  " - Is there a missing period in set 'time_horizon'?\n"
		  " - Is there a missing tech in set 'tech_resource'?\n"
		  " - Is there a missing tech in set 'tech_production'?\n"
		  " - Is there a missing commodity in set 'commodity_physical'?\n"
		  ' - Are there missing entries in the Efficiency parameter?\n'
		  ' - Does a tech need a longer LifetimeTech parameter setting?')
		raise TemoaFlowError( msg.format(
		  c, s, d, p, flow_in_expr.getvalue()
		))


def DemandConstraintErrorCheck ( supply, p, s, d, dem ):
	if int is type( supply ):
		msg = ("Error: Demand '{}' for ({}, {}, {}) unable to be met by any "
		  'technology.\n\tPossible reasons:\n'
		  ' - Is the Efficiency parameter missing an entry for this demand?\n'
		  ' - Does a tech that satisfies this demand need a longer LifetimeTech?'
		  '\n')
		raise TemoaFlowError( msg.format(dem, p, s, d) )

# End Temoa rule "partials"
###############################################################################

##############################################################################
# Begin validation and initialization routines

def validate_time ( M ):
	from sys import maxint

	if not len( M.time_horizon ):
		msg = ('Set "time_horizon" is empty!  Please specify at least one '
		  'period in set time_horizon.')
		raise TemoaValidationError( msg )

	if not len( M.time_future ):
		msg = ('Set "time_future" is empty!  Please specify at least one year '
		  'in set time_future, so that the model may ascertain a final period '
		  'period length for optimization and economic accounting.')
		raise TemoaValidationError( msg )

	""" Ensure that the time_exist < time_horizon < time_future """
	exist    = len( M.time_exist ) and max( M.time_exist ) or -maxint
	horizonl = min( M.time_horizon )  # horizon "low"
	horizonh = max( M.time_horizon )  # horizon "high"
	future   = min( M.time_future )

	if not ( exist < horizonl ):
		msg = ('All items in time_horizon must be larger than in time_exist.\n'
		  'time_exist max:   {}\ntime_horizon min: {}')
		raise TemoaValidationError( msg.format(exist, horizonl) )
	elif not ( horizonh < future ):
		msg = ('All items in time_future must be larger that in time_horizon.\n'
		  'time_horizon max:   {}\ntime_future min:    {}')
		raise TemoaValidationError( msg.format(horizonh, future) )


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


def CreateCapacityFactors ( M ):
	# Steps
	#  1. Collect all possible processes
	#  2. Find the ones _not_ specified in CapacityFactor
	#  3. Set them, based on CapacityFactorDefault.

	# Shorter names, for us lazy programmer types
	CF = M.CapacityFactor

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
	unspecified_cfs = all_cfs.difference( CF.sparse_iterkeys() )

	# Step 3

	# Some hackery: We futz with _constructed because Pyomo thinks that this
	# Param is already constructed.  However, in our view, it is not yet,
	# because we're specifically targeting values that have not yet been
	# constructed, that we know are valid, and that we will need.

	if unspecified_cfs:
		CF._constructed = False
		for s, d, t, v in unspecified_cfs:
			CF[s, d, t, v] = M.CapacityFactorDefault[s, d, t]
		CF._constructed = True

	return tuple()


def CreateLifetimes ( M ):
	# Steps
	#  1. Collect all possible processes
	#  2. Find the ones _not_ specified in LifetimeTech and LifetimeLoan
	#  3. Set them, based on Lifetime*Default.

	# Shorter names, for us lazy programmer types
	LLN = M.LifetimeLoan
	LTC = M.LifetimeTech

	# Step 1
	lprocesses = set( (t, v) for t, v in M.LifetimeLoan_tv )
	processes  = set( (t, v) for t, v in M.LifetimeTech_tv )


	# Step 2
	unspecified_loan_lives = lprocesses.difference( LLN.sparse_iterkeys() )
	unspecified_tech_lives = processes.difference( LTC.sparse_iterkeys() )

	# Step 3

	# Some hackery: We futz with _constructed because Pyomo thinks that this
	# Param is already constructed.  However, in our view, it is not yet,
	# because we're specifically targeting values that have not yet been
	# constructed, that we know are valid, and that we will need.

	if unspecified_loan_lives:
		LLN._constructed = False
		for t, v in unspecified_loan_lives:
			LLN[t, v] = M.LifetimeLoanDefault[ t ]
		LLN._constructed = True

	if unspecified_tech_lives:
		LTC._constructed = False
		for t, v in unspecified_tech_lives:
			LTC[t, v] = M.LifetimeTechDefault[ t ]
		LTC._constructed = True


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
	#  1. Collect all possible cost indices (CostFixed, CostMarginal)
	#  2. Find the ones _not_ specified in CostFixed and CostMarginal
	#  3. Set them, based on Cost*VintageDefault

	# Shorter names, for us lazy programmer types
	CF = M.CostFixed
	CM = M.CostMarginal

	# Step 1
	fixed_indices = set( (p, t, v) for p, t, v in M.CostFixed_ptv )
	marg_indices  = set( (p, t, v) for p, t, v in M.CostMarginal_ptv )

	# Step 2
	unspecified_fixed_prices = fixed_indices.difference( CF.sparse_iterkeys() )
	unspecified_marg_prices  = marg_indices.difference( CM.sparse_iterkeys() )

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

	if unspecified_marg_prices:
		CM._constructed = False
		for p, t, v in unspecified_marg_prices:
			if (t, v) in M.CostMarginalVintageDefault:
				CM[p, t, v] = M.CostMarginalVintageDefault[t, v]
		CM._constructed = True


def validate_TechOutputSplit ( M ):
	msg = ('A set of output fractional values specified in TechOutputSplit do '
	  'not sum to 1.  Each item specified in TechOutputSplit represents a '
	  'fraction of the input carrier converted to the output carrier, so '
	  'they must total to 1.  Current values:\n   {}\n\tsum = {}')

	split_indices = M.TechOutputSplit.sparse_keys()

	tmp = set((i, t) for i, t, o in split_indices)
	left_side = dict({(i, t) : list() for i, t in tmp})
	for i, t, o in split_indices:
		left_side[i, t].append( o )

	for i, t in left_side:
		total = sum(
		  value( M.TechOutputSplit[i, t, o] )
		  for o in left_side[i, t]
		)

		# small enough; likely a rounding error
		if abs(total -1) < 1e-15: continue

		items = '\n   '.join(
		  "{}: {}".format(
		    str((i, t, o)),
		    value(M.TechOutputSplit[i, t, o])
		  )

		  for o in M.commodity_carrier
		  if (i, t, o) in split_indices
		)

		raise TemoaValidationError( msg.format(items, l_total) )

	return set()


def init_set_time_optimize ( M ):
	items = sorted( M.time_horizon )
	items.extend( sorted( M.time_future ) )

	return items[:-1]


def init_set_vintage_exist ( M ):
	return sorted( M.time_exist )


def init_set_vintage_future ( M ):
	return sorted( M.time_future )


def init_set_vintage_optimize ( M ):
	return sorted( M.time_optimize )


def init_set_vintage_all ( M ):
	return sorted( M.time_all )

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

	l_first_period = min( M.time_horizon )
	l_exist_indices = M.ExistingCapacity.sparse_keys()
	l_used_techs = set()

	for i, t, v, o in M.Efficiency.sparse_iterkeys():
		l_process = (t, v)
		l_lifetime = value(M.LifetimeTech[ l_process ])

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
				  'LifetimeTech parameter does not extend past the beginning of '
				  'time_horizon.  (i.e. useless parameter)'
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
				l_loan_life = value(M.LifetimeLoan[ l_process ])
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

	return set()

##############################################################################
# Sparse index creation functions

# These functions serve to create sparse index sets, so that Coopr need only
# create the parameter, variable, and constraint indices with which it will
# actually operate.  This *tremendously* cuts down on memory usage, which
# decreases time and increases the maximum specifiable problem size.

##############################################################################
# Parameters

def CapacityFactorIndices ( M ):
	indices = set(
	  (s, d, t, v)

	  for i, t, v, o in M.Efficiency.sparse_iterkeys()
	  for s in M.time_season
	  for d in M.time_of_day
	)

	return indices


def CostFixedIndices ( M ):
	return g_activeActivity_ptv


def CostMarginalIndices ( M ):
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
	for t, v in M.LifetimeLoan.sparse_iterkeys():
		l_death_year = v + value(M.LifetimeLoan[t, v])
		if l_death_year < l_max_year and l_death_year not in l_periods:
			p = max( yy for yy in M.time_optimize if yy < l_death_year )
			indices.add( (p, t, v) )

	return indices


def TechLifeFracIndices ( M ):
	"""\
Returns the set of (period, tech, vintage) tuples of processes that die between
period boundaries.  The tuple indicates the last period in which a process is
active.
"""
	l_periods = set( M.time_optimize )
	l_max_year = max( M.time_future )

	indices = set()
	for t, v in g_activeCapacity_tv:
		l_death_year = v + value(M.LifetimeTech[t, v])
		if l_death_year < l_max_year and l_death_year not in l_periods:
			p = max( yy for yy in M.time_optimize if yy < l_death_year )
			indices.add( (p, t, v) )

	return indices


def ModelTechLifeIndices ( M ):
	"""
Returns the set of (period, tech, vintage) tuples.  The tuple indicates the
periods in which a process is active, distinct from TechLifeFracIndices that
returns indices only for processes that EOL mid-period.
"""
	return g_activeActivity_ptv


def LifetimeTechIndices ( M ):
	"""\
Based on the Efficiency parameter's indices, this function returns the set of
process indices that may be specified in the LifetimeTech parameter.
"""
	indices = set(
	  (t, v)

	  for i, t, v, o in M.Efficiency.sparse_iterkeys()
	)

	return indices


def LifetimeLoanIndices ( M ):
	"""\
Based on the Efficiency parameter's indices and time_horizon parameter, this
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


def CapacityByOutputVariableIndices ( M ):
	indices = set(
	  (t, v, o)

	  for p in M.time_optimize
	  for t in M.tech_all
	  for v in ProcessVintages( p, t )
	  for o in ProcessOutputs( p, t, v )
	)

	return indices


### Reporting variables


def ActivityByPeriodTechAndVintageVarIndices ( M ):
	return g_activeActivity_ptv


def ActivityByPeriodTechAndOutputVariableIndices ( M ):
	indices = set(
	  (l_per, l_tech, l_out)

	  for l_per in M.time_optimize
	  for l_tech in M.tech_all
	  for l_vin in ProcessVintages( l_per, l_tech )
	  for l_out in ProcessOutputs( l_per, l_tech, l_vin )
	 )

	return indices


def ActivityByPeriodTechVintageAndOutputVariableIndices ( M ):
	indices = set(
	  (l_per, l_tech, l_vin, l_out)

	  for l_per in M.time_optimize
	  for l_tech in M.tech_all
	  for l_vin in ProcessVintages( l_per, l_tech )
	  for l_out in ProcessOutputs( l_per, l_tech, l_vin )
	)

	return indices


def ActivityByTechAndOutputVariableIndices ( M ):
	indices = set(
	  (l_tech, l_out)

	  for l_per, l_tech, l_vin in g_activeActivity_ptv
	  for l_out in ProcessOutputs( l_per, l_tech, l_vin )
	)

	return indices


def ActivityByInputAndTechVariableIndices ( M ):
	indices = set(
	  (l_inp, l_tech)

	  for l_per, l_tech, l_vin in g_activeActivity_ptv
	  for l_inp in ProcessInputs( l_per, l_tech, l_vin )
	)

	return indices


def ActivityByPeriodInputAndTechVariableIndices ( M ):
	indices = set(
	  (l_per, l_inp, l_tech)

	  for l_per, l_tech, l_vin in g_activeActivity_ptv
	  for l_inp in ProcessInputs( l_per, l_tech, l_vin )
	)

	return indices


def ActivityByPeriodInputTechAndVintageVariableIndices ( M ):
	indices = set(
	  (l_per, l_inp, l_tech, l_vin)

	  for l_per, l_tech, l_vin in g_activeActivity_ptv
	  for l_inp in ProcessInputs( l_per, l_tech, l_vin )
	)

	return indices


def EmissionActivityByTechVariableIndices ( M ):
	indices = set(
	  (l_emission, l_tech)

	  for l_emission, l_inp, l_tech, l_vin, l_out in M.EmissionActivity.sparse_iterkeys()
	)

	return indices

def EmissionActivityByPeriodAndTechVariableIndices ( M ):
	indices = set(
	  (l_emission, l_per, l_tech)

	  for l_emission, l_inp, l_tech, l_vin, l_out in M.EmissionActivity.sparse_iterkeys()
	  for l_per in M.time_optimize
	  if ValidActivity( l_per, l_tech, l_vin )
	)

	return indices


def EmissionActivityByTechAndVintageVariableIndices ( M ):
	indices = set(
	  (l_emission, l_tech, l_vin)

	  for l_emission, l_inp, l_tech, l_vin, l_out in M.EmissionActivity.sparse_iterkeys()
	)

	return indices


def EnergyConsumptionByTechAndOutputVariableIndices ( M ):
	indices = set(
	  (l_tech, l_out)

	  for l_inp, l_tech, l_vin, l_out in M.Efficiency.sparse_iterkeys()
	)

	return indices


def EnergyConsumptionByPeriodAndTechVariableIndices ( M ):
	indices = set(
	  (l_per, l_tech)

	  for l_inp, l_tech, l_vin, l_out in M.Efficiency.sparse_iterkeys()
	  for l_per in M.time_optimize
	  if ValidActivity( l_per, l_tech, l_vin )
	)

	return indices


def EnergyConsumptionByPeriodInputAndTechVariableIndices ( M ):
	indices = set(
	  (l_per, l_inp, l_tech)

	  for l_inp, l_tech, l_vin, l_out in M.Efficiency.sparse_iterkeys()
	  for l_per in M.time_optimize
	  if ValidActivity( l_per, l_tech, l_vin )
	)

	return indices


def EnergyConsumptionByPeriodTechAndOutputVariableIndices ( M ):
	indices = set(
	  (l_per, l_tech, l_out)

	  for l_inp, l_tech, l_vin, l_out in M.Efficiency.sparse_iterkeys()
	  for l_per in M.time_optimize
	  if ValidActivity( l_per, l_tech, l_vin )
	)

	return indices


def EnergyConsumptionByPeriodTechAndVintageVariableIndices ( M ):
	indices = set(
	  (l_per, l_tech, l_vin)

	  for l_inp, l_tech, l_vin, l_out in M.Efficiency.sparse_iterkeys()
	  for l_per in M.time_optimize
	  if ValidActivity( l_per, l_tech, l_vin )
	)

	return indices

# End variables
##############################################################################

##############################################################################
# Constraints


def CapacityByOutputConstraintIndices ( M ):
	indices = set(
	  (p, s, d, t, v, o)

	  for p in M.time_optimize
	  for t in M.tech_all
	  for v in ProcessVintages( p, t )
	  for o in ProcessOutputs( p, t, v )
	  for s in M.time_season
	  for d in M.time_of_day
	)

	return indices


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


def FractionalLifeActivityLimitConstraintIndices ( M ):
	indices = set(
	  (p, s, d, t, v, o)

	  for p, t, v in M.TechLifeFrac.sparse_iterkeys()
	  for o in ProcessOutputs( p, t, v )
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


def TechOutputSplitConstraintIndices ( M ):
	indices = set(
	  (p, s, d, i, t, v, o)

	  for i, t, o in M.TechOutputSplit.sparse_iterkeys()
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


def ProcessesByPeriodAndInput ( p, i ):
	"""\
Returns the set of processes that operate in 'period' and take 'input'.  Note
that a process is conceptually a vintage of a technology.
"""
	processes = set(
	  (t, v)

	  for p, t, v in g_processInputs
	  if p == p
	  if i in g_processInputs[p, t, v]
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


def loanIsActive ( p, t, v ):
	"""\
Return a boolean (True or False) whether a loan is still active in a period.
This is the implementation of imat in the rest of the documentation.
"""
	return (p, t, v) in g_processLoans


# End helper functions
##############################################################################

###############################################################################
# Miscellaneous routines

def parse_args ( ):
	import argparse, platform

	from coopr.opt import SolverFactory as SF
	from pyutilib.component.core import PluginGlobals

	# used for some error messages below.
	red_bold = cyan_bold = reset = ''
	if platform.system() != 'Windows' and SE.isatty():
		red_bold  = '\x1b[1;31m'
		cyan_bold = '\x1b[1;36m'
		reset     = '\x1b[0m'


	logger = PluginGlobals.env().log
	logger.disabled = True  # no need for warnings: it's what we're testing!
	available_solvers = set( solver   # name of solver; a string
	  for solver in filter( lambda x: '_' != x[0], SF.services() )
	  if SF( solver ).available( False )
	)
	logger.disabled = False

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
			default_solver = available_solvers[0]
	else:
		default_solver = 'NONE'
		SE.write('\nNOTICE: Coopr did not find any suitable solvers.  Temoa will '
		   'not be able to solve any models.  If you need help, ask on the '
		   'Temoa Project forum: http://temoaproject.org/\n\n' )

	parser = argparse.ArgumentParser()
	parser.prog = path.basename( argv[0].strip('/') )

	graphviz   = parser.add_argument_group('Graphviz Options')
	solver     = parser.add_argument_group('Solver Options')
	stochastic = parser.add_argument_group('Stochastic Options')

	parser.add_argument('dot_dat',
	  type=str,
	  nargs='*',
	  help='AMPL-format data file(s) with which to create a model instance. '
	       'e.g. "data.dat"'
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

	solver.add_argument('--symbolic_solver_labels',
	  help='When interfacing with the solver, use model-derived symbol names.  '
	       'For example, "V_Capacity(coal_plant,2000)" instead of "x(47)".  '
	       'Mainly used for debugging purposes.  [Default: use x(47) style]',
	  action='store_true',
	  dest='useSymbolLabels',
	  default=False)

	solver.add_argument('--generate_solver_lp_file',
	  help='Request that solver create an LP representation of the optimization '
	       'problem.  Mainly used for model debugging purposes.  The file name '
	       'will have the same base name as the first dot_dat file specified.  '
	       '[Default: do not create solver LP file]',
	  action='store_true',
	  dest='generateSolverLP',
	  default=False)

	solver.add_argument('--keep_coopr_lp_file',
	  help='Save the LP file as written by Pyomo.  This is distinct from the '
	       "solver's generated LP file, but /should/ represent the same model.  "
	       'Mainly used for debugging purposes.  The file name will have the '
	       'same base name as the first dot_dat file specified.  '
	       '[Default: remove Pyomo LP file]',
	  action='store_true',
	  dest='keepPyomoLP',
	  default=False)


	stochastic.add_argument('--ecg',
	  help='"Expected Cost of Guessing Wrong" -- Calculate the costs of '
	       'choosing the wrong scenario of a stochastic tree.  Specify the '
	       'path to the stochastic scenario directory.  (i.e., where to find '
	       'ScenarioStructure.dat)',
	  action='store',
	  metavar='STOCHASTIC_DIRECTORY',
	  dest='ecg',
	  default=None)

	options = parser.parse_args()

	# It would be nice if this implemented with add_mutually_exclusive_group
	# but I /also/ want them in separate groups for display.  Bummer.
	if not (options.dot_dat or options.ecg):
		usage = parser.format_usage()
		msg = ('Missing a data file to optimize (e.g., test.dat)')
		msg = '{}\n{}{}{}'.format( usage, red_bold, msg, reset )
		raise TemoaCommandLineArgumentError( msg )

	elif options.dot_dat and options.ecg:
		usage = parser.format_usage()
		msg = ('Conflicting option and arguments: --ecg and data files\n\n'
		       '--ecg is for performing an analysis on a directory of data '
		       'files, as are used in a stochastic analysis with PySP.  Please '
		       'remove either of --ecg or the data files from the command '
		       'line.')
		msg = '{}\n{}{}{}'.format( usage, red_bold, msg, reset )
		raise TemoaCommandLineArgumentError( msg )
	elif options.ecg:
		# can this be subsumed directly into the argparse module functionality?
		from os.path import isdir, isfile, join
		edir = options.ecg

		if not isdir( options.ecg ):
			msg = "{}--ecg requires a directory.{}".format( red_bold, reset )
			msg = "{}\n\nSupplied path: '{}'".format( msg, edir )
			raise TemoaCommandLineArgumentError( msg )

		structure_file = join( edir, 'ScenarioStructure.dat' )
		if not isfile( structure_file ):
			msg = "'{}{}{}' does not appear to contain a PySP stochastic program."
			msg = '{}{}{}'.format( red_bold, msg, reset )
			raise TemoaCommandLineArgumentError(
			   msg.format( reset, edir, red_bold ))

	return options

# End miscellaneous routines
###############################################################################

###############################################################################
# Direct invocation methods (when modeler runs via "python model.py ..."

def solve_perfect_foresight ( model, optimizer, options ):
	from time import clock

	from coopr.pyomo import ModelData

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

	mdata = ModelData()
	for f in dot_dats:
		if f[-4:] != '.dat':
			msg = "\n\nExpecting a dot dat (e.g., data.dat) file, found '{}'\n"
			raise SystemExit( msg.format( f ))
		mdata.add( f )
	mdata.read( model )
	SE.write( '\r[%8.2f\n' % duration() )

	SE.write( '[        ] Creating Temoa model instance.'); SE.flush()
	# Now do the solve and ...
	instance = model.create( mdata )
	SE.write( '\r[%8.2f\n' % duration() )

	SE.write( '[        ] Solving.'); SE.flush()
	if opt:
		result = opt.solve( instance )
		SE.write( '\r[%8.2f\n' % duration() )
	else:
		SE.write( '\r---------- Not solving: no available solver\n' )
		return

	SE.write( '[        ] Formatting results.' ); SE.flush()
	# ... print the easier-to-read/parse format
	updated_results = instance.update_results( result )
	formatted_results = pformat_results( instance, updated_results )
	SE.write( '\r[%8.2f\n' % duration() )
	SO.write( formatted_results )

	if options.graph_format:
		SE.write( '[        ] Creating Temoa model diagrams.' ); SE.flush()
		instance.load( result )
		CreateModelDiagrams( instance, options )
		SE.write( '\r[%8.2f\n' % duration() )


def solve_cost_of_guessing ( optimizer, options ):
	import csv

	from cStringIO import StringIO
	from collections import deque, defaultdict
	from multiprocessing import Pool, Manager
	from os import getcwd, chdir
	from os.path import isfile, abspath

	from coopr.pyomo import ModelData, Var
	from coopr.pysp.util.scenariomodels import scenario_tree_model
	from coopr.pysp.phutils import extractVariableNameAndIndex

	from pformat_results import pformat_results
	from temoa_model import temoa_create_model

	opt = optimizer    # a shorter name for us lazy programmer types

	pwd = abspath( getcwd() )
	chdir( options.ecg )
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

	# Step 2: start from the root node to find all non-anticipative nodes
	nonanticipative = [ root_node ]
	to_process.extend( sStructure.Children[ root_node ] )
	while to_process:
		node = to_process.pop()
		if sStructure.ConditionalProbability[ node ] == 1:
			nonanticipative.append( node )

	# Step 3: collect the non-anticipative variables to be set
	variables_to_fix = defaultdict(set)
	to_process.extend( nonanticipative )
	for node in to_process:
		stage = sStructure.NodeStage[ node ]
		for var_string in sStructure.StageVariables[ stage ]:
			vname, index = extractVariableNameAndIndex( var_string )
			variables_to_fix[ vname ].add( index )

	# Step 4: build the scenarios to solve
	leaf_node_keys = sStructure.ScenarioLeafNode.items()
	scenarios = dict()
	for name, node in leaf_node_keys:
		s = list()
		while node in ctpTree:
			s.append( node )
			node = ctpTree[ node ]  # the parent of node
		s.append( root_node )
		s.reverse()
		scenarios[ name ] = tuple(s)

	# Step 4.5: check that all required data files exist as expected
	for sname, nodes in scenarios.iteritems():
		for node in nodes:
			f = node + '.dat'
			if not isfile( f ):
				msg = ('Cannot complete ECGW analysis due to a missing data '
				   'file.  Either update your ScenarioStructure.dat file, or '
				   "replace the missing file.\n\n  Missing file: '{}'\n")
				raise TemoaError( msg.format( f ))

	# Step 5: Begin the solves.
	results = defaultdict(list)
	data = list()  # for CSV conversion, after processing
	for gamblers_guess, gamblers_nodes in sorted( scenarios.items() ):
		variable_values = defaultdict(list)
		total_costs = dict()

		msg = ("Solving all possible scenarios for the Gambler's guess of "
		       "scenario: '{}'\n")
		SE.write( msg.format( gamblers_guess ))

		# Step 5.1: Choose each scenario in turn as the "Gamblers Gambit", ...
		mdata = ModelData()
		for node in gamblers_nodes:
			mdata.add( node + '.dat' )
		model = temoa_create_model( "Gambit {}".format( gamblers_guess ))
		mdata.read( model )

		#  ... solve it, and ...
		the_gamble = model.create( mdata )

		sol = opt.solve( the_gamble )
		the_gamble.load( sol )

		total_costs[ gamblers_guess ] = the_gamble.TotalCost()

		for vname in the_gamble.active_components( Var ):
			var = getattr(the_gamble, vname)
			for i, v in var.iteritems():
				variable_values[ v.cname().replace("'", '') ].append((
				  gamblers_guess, v.value ))

		# Step 5.2: Save the variable values from the gambit
		fixed_values = dict()

		for vname, indices in variables_to_fix.iteritems():
			var = getattr(the_gamble, vname)
			values = list()
			for i in sorted( indices ):
				val = value(var[ i ])
				if val < 1e-9:
					val = 0
				values.append( val )
			fixed_values[ vname ] = values
			del values

		# ensure we don't mistakenly use a variable below (defensive programming)
		del mdata, model, the_gamble

		# Step 5.3: Solve every other scenario, but ...
		wrong_guesses = sorted(
		  (s, n) for s, n in scenarios.iteritems()
		  if s != gamblers_guess )
		for sname, nodes in wrong_guesses:
			SE.write( '  Solving wrong guess: {}\n'.format( sname ))

			mdata = ModelData()
			for node in nodes:
				SE.write( '    Adding file: {}\n'.format( node + '.dat' ))
				mdata.add( node + '.dat' )
			model = temoa_create_model( '{}: {}'.format( gamblers_guess, sname ))
			mdata.read( model )

			wg = model.create( mdata )     # wg = "wrong guess"

			# ... ensure that the non-anticipative variables are fixed per the
			# solution to the Gambler's Gambit.
			model_vars = list()  # save vars for later so we don't need to use ...
			for vname, indices in variables_to_fix.iteritems():
				var = getattr(wg, vname)    # ... the costly getattr twice
				for index, val in zip(sorted( indices ), fixed_values[ vname ]):
					v = var[ index ]
					model_vars.append( v )
					v.fixed = True
					v.set_value( val )
			wg.preprocess()

			# Then do the solve.
			sol = opt.solve( wg )
			wg.load( sol )
			total_costs[ sname ] = wg.TotalCost()

			for vname in wg.active_components( Var ):
				var = getattr(wg, vname)
				for i, v in var.iteritems():
					variable_values[ v.cname().replace("'", '') ].append(
					  (sname, v.value) )

			# ensure we don't make a mistake between loop iterations.
			del mdata, model, model_vars, sol, wg

		data.append( ("Gambler's Guess:", gamblers_guess) )
		data.append(tuple())

		row = ['Total Scenario Costs', gamblers_guess]
		row.extend(sname for sname, nodes in wrong_guesses)
		data.append( row )
		data.append( ['',] + [ total_costs[i] for i in row[1:]] )
		data.append(tuple())

		data.append(('Fixed variables',))
		for vname, indices in sorted(variables_to_fix.iteritems()):
			for index, val in zip(sorted(indices), fixed_values[ vname ]):
				if val < 1e-9: continue
				vfmt = ','.join('{}' for i in xrange(len(index)))
				vfmt = '{}[{}]'.format(vname, vfmt)
				# Works out to "vname[{},{},{}...]" for the length of index

				var = vfmt.format(*index)
				data.append((var, val))

		data.append(tuple())

		row = ['Variable', gamblers_guess]
		row.extend( s[0] for s in wrong_guesses )
		data.append( row )
		for v, vals in sorted( variable_values.iteritems() ):
			guess_val = filter(lambda x: x[0] == gamblers_guess, vals)[0][1]
			other_vals = filter(lambda x: x[0] != gamblers_guess, vals)

			row = [ v, guess_val ]
			row.extend( j for i, j in other_vals )
			for i, val in enumerate(row[1:]):
				if val < 1e-9:
					row[1 + i] = 0

			# if they are all 0, then there's no need to mention this variable
			if True not in ( i != 0 for i in row[1:] ): continue

			data.append( row )

		data.extend(((),()))
		del variable_values

	chdir( pwd )

	csv_data = StringIO()
	writer = csv.writer( csv_data ); writer.writerows( data )
	SO.write( csv_data.getvalue() )

	# Step 6: print the results to stdout
#	for name, result_set in results.iteritems():
#		for sname, pformatted_sol in result_set:
#			SO.write( '{}\n\n{}\n\n'.format( sname, pformatted_sol ))
#		SO.write( '-------\n' )


def temoa_solve ( model ):
	from sys import argv, version_info

	if version_info < (2, 7):
		msg = ("Temoa requires Python v2.7 to run.\n\nIf you've "
		  "installed Coopr with Python 2.6 or less, you'll need to reinstall "
		  'Coopr, taking care to install with a Python 2.7 (or greater) '
		  'executable.')
		raise SystemExit( msg )

	options = parse_args()

	from coopr.opt import SolverFactory

	opt = SolverFactory( options.solver )
	if opt:
		opt.keepFiles = options.keepPyomoLP
		opt.generateSymbolicLabels = options.useSymbolLabels

	elif options.solver != 'NONE':
		SE.write( "\nWarning: Unable to initialize solver interface for '{}'\n\n"
			.format( options.solver ))

	if options.dot_dat:
		solve_perfect_foresight( model, opt, options )
	elif options.ecg:
		solve_cost_of_guessing( opt, options )

# End direct invocation methods
###############################################################################
