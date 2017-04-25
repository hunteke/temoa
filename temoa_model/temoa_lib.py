"""
Tools for Energy Model Optimization and Analysis (Temoa): 
An open source framework for energy systems optimization modeling

Copyright (C) 2015,  NC State University

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

A complete copy of the GNU General Public License v2 (GPLv2) is available 
in LICENSE.txt.  Users uncompressing this from an archive may not have 
received this license file.  If not, see <http://www.gnu.org/licenses/>.
"""

from temoa_common import *

from cStringIO import StringIO
from itertools import product as cross_product, islice, izip
from operator import itemgetter as iget
from os import path, close as os_close
from sys import argv, stderr as SE, stdout as SO
from signal import signal, SIGINT, default_int_handler
from shutil import copyfile, move

from pyomo.opt import SolverFactory as SF
from temoa_config import TemoaConfig


import errno, warnings
import re as reg_exp

import pyomo.environ
  # workaround for Coopr's brain dead signal handler
signal(SIGINT, default_int_handler)

TEMOA_GIT_VERSION  = 'HEAD'
TEMOA_RELEASE_DATE = 'Today'

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

	if abs(float(total) - 1.0) > 0.001:
		# We can't explicitly test for "!= 1.0" because of incremental rounding
		# errors associated with the specification of SegFrac by time slice, 
		# but we check to make sure it is within the specified tolerance.

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
	if abs(float(total) - 1.0) > 0.001:
		# We can't explicitly test for "!= 1.0" because of incremental rounding
		# errors associated with the specification of demand shares by time slice, 
		# but we check to make sure it is within the specified tolerance.

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

		if abs(float(total) - 1.0) > 0.001:
		# We can't explicitly test for "!= 1.0" because of incremental rounding
		# errors associated with the specification of demand shares by time slice, 
		# but we check to make sure it is within the specified tolerance.

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


def EnergyConsumptionByPeriodInputAndTechVariableIndices ( M ):
	indices = set(
	  (p, i, t)

	  for i, t, v, o in M.Efficiency.sparse_iterkeys()
	  for p in M.time_optimize
	)

	return indices
	
	
def ActivityByPeriodTechAndOutputVariableIndices ( M ):
	indices = set(
	  (p, t, o)

	  for i, t, v, o in M.Efficiency.sparse_iterkeys()
	  for p in M.time_optimize
	)

	return indices	
	
	
def EmissionActivityByPeriodAndTechVariableIndices ( M ):
	indices = set(
	  (e, p, t)

	  for e, i, t, v, o in M.EmissionActivity.sparse_iterkeys()
	  for p in M.time_optimize
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

def RampConstraintDayIndices ( M ):
	indices = set(
	  (p, s, d, t, v)

	  for p in M.time_optimize
	  for s in M.time_season
	  for d in M.time_of_day
	  for t in M.tech_ramping
	  for v in ProcessVintages( p, t )
	)

	return indices

def RampConstraintSeasonIndices ( M ):
	indices = set(
	  (p, s, t, v)

	  for p in M.time_optimize
	  for s in M.time_season	  
	  for t in M.tech_ramping
	  for v in ProcessVintages( p, t )
	)

	return indices

def RampConstraintPeriodIndices ( M ):
	indices = set(
	  (p, t, v)

	  for p in M.time_optimize
	  for t in M.tech_ramping
	  for v in ProcessVintages( p, t )
	)

	return indices

def ReserveMarginIndices ( M ):
		indices = set(
			(p, c)

			for p in M.time_optimize
			for c in M.commodity_demand
			if M.ReserveMargin[c] >= 1e-3
			)
		return indices

def TechInputSplitConstraintIndices ( M ):
	indices = set(
	  (p, s, d, i, t, v)

	  for p, i, t in M.TechInputSplit.sparse_iterkeys()
	  for p in M.time_optimize
	  for v in ProcessVintages( p, t )
	  for s in M.time_season
	  for d in M.time_of_day
	)

	return indices


def TechOutputSplitConstraintIndices ( M ):
	indices = set(
	  (p, s, d, t, v, o)

	  for p, t, o in M.TechOutputSplit.sparse_iterkeys()
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


def version ( options ):
	from sys import stdout as SO
	from os.path import basename, dirname
	import os

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
Copyright (C) 2015 NC State University

We provide Temoa -- the model and associated scripts -- "as-is" with no express
or implied warranty for accuracy or accessibility.  Temoa is a research tool,
given in good faith to the community (anyone who uses Temoa for any purpose) as
free software under the terms of the GNU General Public License, version 2.
"""

	try:
		txt_file = open(options.path_to_logs+os.sep+"Complete_OutputLog.log", "w")
	except BaseException as io_exc:
		SE.write("Log file cannot be opened. Please check path. Trying to find:\n"+options.path_to_logs+" folder\n")
		txt_file = open("Complete_OutputLog.log", "w")

	txt_file.write( msg )
	SO.write( msg.format( *args ))
	#raise SystemExit


def bibliographicalInformation ( options ):
	from sys import stdout as SO
	import os

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

	try:
		txt_file = open(options.path_to_logs+os.sep+"Complete_OutputLog.log", "w")
	except BaseException as io_exc:
		SE.write("Log file cannot be opened. Please check path. Trying to find:\n"+options.path_to_logs+" folder\n")
		txt_file = open("Complete_OutputLog.log", "w")

	txt_file.write( msg )
	SO.write( msg )
	#raise SystemExit



# End miscellaneous routines
###############################################################################

###############################################################################
# Direct invocation methods (when modeler runs via "python model.py ..."

def MGA ( model, optimizer, options, epsilon=1e-6 ):
	from collections import defaultdict
	from time import clock
	import sys, os, gc

	from pyomo.environ import DataPortal

	from temoa_rules import TotalCost_rule
	from pformat_results import pformat_results

	opt = optimizer              # for us lazy programmer types
	dot_dats = options.dot_dat

	scenario_names = []
	scenario_names.append(options.scenario)
	
	def ActivityObj_rule ( M, prev_act_t ):
		new_act = 0
		for t in M.V_ActivityByTech:
			if t in prev_act_t:
				new_act += prev_act_t[ t ] * M.V_ActivityByTech[t]
		return new_act

	def SlackedObjective_rule ( M, prev_cost ):
		# It is important that this function name *not* match its constraint name
		# plus '_rule', else Pyomo will attempt to be too smart.  That is, at the
		# first implementation, the associated constraint name is
		# 'PreviousSlackedObjective', for which Pyomo searches the namespace for
		# 'PreviousSlackedObjective_rule'.  We decidedly do not want Pyomo
		# trying to call this function because it is not aware of the second arg.
		slackcost = (1 + options.mga) * prev_cost 
		oldobjective = TotalCost_rule( M )
		expr = ( slackcost >= oldobjective )
		return expr

	def PreviousAct_rule ( instance ):
		#   The version below weights each technology by its previous cumulative
		#   activity. However, different sectors may be tracked in different units and 
		#   have activities of very different magnitudes. Can also modify the code 
		#   changing 'val' to 1 to implement a integer-based weight to address this non-uniform
		#   weighting issue.
		if options.mga_weight == 'integer':
			for t in instance_1.V_ActivityByTech:
				if t in instance.tech_mga:
					val = value( instance.V_ActivityByTech[t] )
					if abs(val) < epsilon: continue
					prev_activity_t[ t ] += 1.0   #val
                	return prev_activity_t
                
		#   The version below calculates activity by sector and normalized technology-
		#   specific activity by the total activity for the sector. Currently accounts
		#   for electric and transport sectors, but others can be added to the block below.
		elif options.mga_weight == 'normalized':
			sectors = set(['electric', 'transport', 'industrial', 'commercial', 'residential'])
			act     = dict()
			techs   = {'electric':    instance.tech_electric,
			           'transport':   instance.tech_transport,
			           'industrial':  instance.tech_industrial,
			           'commercial':  instance.tech_commercial,
			           'residential': instance.tech_residential}
			for s in sectors:
				if len(techs[s]) > 0:
					act[s] = sum(
			  		value( instance.V_ActivityByTech[S_t] )
			  		for S_t in techs[s]
					)
       	
			for t in instance_1.V_ActivityByTech:
				for s in sectors:
					if t in techs[s]:
						val = value( instance.V_ActivityByTech[t] )
						if abs(val) < epsilon: continue
						prev_activity_t[ t ] += val / act[s]
                	return prev_activity_t


	# The MGA algorithm uses different objectives per iteration, so the first
	# step is to remove the original objective function
	model.del_component( 'TotalCost' )

	
	try:
		txt_file = open(options.path_to_logs+os.sep+"Complete_OutputLog.log", "w")
	except BaseException as io_exc:
		SE.write("Log file cannot be opened. Please check path. Trying to find:\n"+options.path_to_logs+" folder\n")
		txt_file = open("Complete_OutputLog.log", "w")
		txt_file.write("Log file cannot be opened. Please check path. Trying to find:\n"+options.path_to_logs+" folder\n")
	
	try:
		
		if options.keepPyomoLP:
			SE.write('\nSolver will write file: {}\n\n'.format( options.scenario + '.lp' ))
			txt_file.write('\nSolver will write file: {}\n\n'.format( options.scenario + '.lp' ))

		SE.write( '[        ] Reading data files.'); SE.flush()
		txt_file.write( 'Reading data files.')
		begin = clock()
		duration = lambda: clock() - begin

		mdata = DataPortal( model=model )
		for fname in dot_dats:
			if fname[-4:] != '.dat':
				msg = "\n\nExpecting a dot dat (e.g., data.dat) file, found '{}'\n"
				raise TemoaValidationError( msg.format( fname ))
			mdata.load( filename=fname )
		SE.write( '\r[%8.2f\n' % duration() )
		txt_file.write( '\r[%8.2f]\n' % duration() )

		SE.write( '[        ] Creating Temoa model instance.'); SE.flush()
		txt_file.write( 'Creating Temoa model instance.')

		# Create concrete model
		instance_1 = model.create_instance( mdata )

		# Now add in and objective function, like we earlier removed; note that name
		# we choose here (FirstObj) will be copied to the output file.
		instance_1.FirstObj = Objective( rule=TotalCost_rule, sense=minimize )
		instance_1.preprocess()

		SE.write( '\r[%8.2f\n' % duration() )
		txt_file.write( '\r[%8.2f]\n' % duration() )

		SE.write( '[        ] Solving first model instance.'); SE.flush()
		txt_file.write( 'Solving first model instance.')

		if opt:
			result_1 = opt.solve( instance_1, 
								  load_solutions=False, 
								  keepfiles=options.keepPyomoLP, 
								  symbolic_solver_labels = options.keepPyomoLP )
			instance_1.solutions.load_from(result_1, delete_symbol_map=False)

			SE.write( '\r[%8.2f\n' % duration() )
			txt_file.write( '\r[%8.2f]\n' % duration() )

			instance_1.solutions.load_from(result_1)
			formatted_results = pformat_results( instance_1, result_1, options )  
			SO.write( formatted_results.getvalue() )
			txt_file.write( formatted_results.getvalue() )
			txt_file.flush()


			# using value() converts the now-load()ed results into a single number,
			# which we'll use with our slightly unusual SlackedObjective_rule below
			# (but defined above).
			Perfect_Foresight_Obj = value( instance_1.FirstObj )
			
			# Create a new parameter that stores the MGA objective function weights
			prev_activity_t = defaultdict( int )		
			prev_activity_t = PreviousAct_rule( instance_1 )		

			if isinstance(options, TemoaConfig) and options.saveTEXTFILE:
				for inpu in options.dot_dat:
					file_ty = reg_exp.search(r"\b([\w-]+)\.(\w+)\b", inpu)
				
				new_dir = options.path_to_db_io+os.sep+file_ty.group(1)+'_'+options.scenario+'_model'
				
				if path.isfile(options.path_to_logs+os.sep+'Complete_OutputLog.log') and path.exists(new_dir):
					copyfile(options.path_to_logs+os.sep+'Complete_OutputLog.log', new_dir+os.sep+options.scenario+'_OutputLog.log')

			
			if isinstance(options, TemoaConfig) and options.keepPyomoLP:
				for inpu in options.dot_dat:
					file_ty = reg_exp.search(r"\b([\w-]+)\.(\w+)\b", inpu)
				
				new_dir = options.path_to_db_io+os.sep+file_ty.group(1)+'_'+options.scenario+'_model'
				
				for files in os.listdir(options.path_to_lp_files):
					if files.endswith(".lp"):
						lpfile = files
					else:
						if files == "README.txt":
							continue
						os.remove(options.path_to_lp_files+os.sep+files)
				
				if path.exists(new_dir):
					move(options.path_to_lp_files+os.sep+lpfile, new_dir+os.sep+options.scenario+'.lp')
			
			
			#Perform 5 MGA iterations
			while options.next_mga():
				instance_mga = model.create_instance( mdata )


				try:
					txt_file_mga = open(options.path_to_logs+os.sep+"OutputLog_MGA_last.log", "w")
				except BaseException as io_exc:
					SE.write("MGA Log file cannot be opened. Please check path. Trying to find:\n"+options.path_to_logs+" folder\n")
					txt_file_mga = open("OutputLog_MGA_last.log", "w")
				
				#scenario_names.append(options.scenario)
				
				# Update second instance with the new MGA-specific objective function
				# and constraint.
				instance_mga.SecondObj = Objective(
				expr=ActivityObj_rule( instance_mga, prev_activity_t ),
				noruleinit=True,
				sense=minimize
				)
				instance_mga.PreviousSlackedObjective = Constraint(
				rule=None,
				expr=SlackedObjective_rule( instance_mga, Perfect_Foresight_Obj ),
				noruleinit=True
				)
				instance_mga.preprocess()

				if options.keepPyomoLP:
					SE.write('\nSolver will write file: {}\n\n'.format( options.scenario + '.lp' ))
					txt_file.write('\nSolver will write file: {}\n\n'.format( options.scenario + '.lp' ))

				SE.write( '[        ] Solving {}.'.format(options.scenario)); SE.flush()
				txt_file.write( 'Solving {}.'.format(options.scenario)); SE.flush()
				txt_file_mga.write( 'Solving {}.'.format(options.scenario)); SE.flush()
				
				result_mga = opt.solve( instance_mga, 
										load_solutions=False, 
										keepfiles=options.keepPyomoLP, 
										symbolic_solver_labels = options.keepPyomoLP )

				SE.write( '\r[%8.2f\n' % duration() )
				txt_file.write( '\r[%8.2f]\n' % duration() )
				txt_file_mga.write( '\r[%8.2f]\n' % duration() )


				instance_mga.solutions.load_from(result_mga, delete_symbol_map=False)
				formatted_results = pformat_results( instance_mga, result_mga, options )
				SO.write( formatted_results.getvalue() )
				txt_file.write( formatted_results.getvalue() )
				txt_file_mga.write( formatted_results.getvalue() )

				txt_file_mga.flush()
				
				#Keep adding activity from latest iteration to MGA Obj function
				prev_activity_t = PreviousAct_rule( instance_mga )

				# return signal handlers to defaults, again
				signal(SIGINT, default_int_handler)
				
				txt_file_mga.close()
			
				if isinstance(options, TemoaConfig) and options.saveTEXTFILE:
					for inpu in options.dot_dat:
						file_ty = reg_exp.search(r"\b([\w-]+)\.(\w+)\b", inpu)
					
					new_dir = options.path_to_db_io+os.sep+file_ty.group(1)+'_'+options.scenario+'_model'
					
					if path.isfile(options.path_to_logs+os.sep+'OutputLog_MGA_last.log') and path.exists(new_dir):
						copyfile(options.path_to_logs+os.sep+'OutputLog_MGA_last.log', new_dir+os.sep+options.scenario+'_OutputLog.log')


				if isinstance(options, TemoaConfig) and options.keepPyomoLP:
					for inpu in options.dot_dat:
						file_ty = reg_exp.search(r"\b([\w-]+)\.(\w+)\b", inpu)
					
					new_dir = options.path_to_db_io+os.sep+file_ty.group(1)+'_'+options.scenario+'_model'
					
					for files in os.listdir(options.path_to_lp_files):
						if files.endswith(".lp"):
							lpfile = files
						else:
							if files == "README.txt":
								continue
							os.remove(options.path_to_lp_files+os.sep+files)
					
					if path.exists(new_dir):
						move(options.path_to_lp_files+os.sep+lpfile, new_dir+os.sep+options.scenario+'.lp')

						
			txt_file.flush()
			txt_file.close()
		else:
			SE.write( '\r---------- Not solving: no available solver\n' )
			txt_file.write( '\r---------- Not solving: no available solver\n' )
			txt_file.close()
			#return
			
	except BaseException as model_exc:
		SE.write("exception found in MGA()\n")
		txt_file.write("exception found in MGA()\n")
		SE.write(str(model_exc))
		txt_file.write(str(model_exc))
		txt_file.close()
		
	if isinstance(options, TemoaConfig) and options.saveTEXTFILE:
		for inpu in options.dot_dat:
			file_ty = reg_exp.search(r"\b([\w-]+)\.(\w+)\b", inpu)
		
		for sc in scenario_names:
			new_dir = options.path_to_db_io+os.sep+file_ty.group(1)+'_'+sc+'_model'
			
			if path.isfile(options.path_to_logs+os.sep+'Complete_OutputLog.log') and path.exists(new_dir):
				copyfile(options.path_to_logs+os.sep+'Complete_OutputLog.log', new_dir+os.sep+'Complete_OutputLog.log')

		
def solve_perfect_foresight ( model, optimizer, options ):
	from time import clock
	import sys, os, gc

	from pyomo.core import DataPortal

	from pformat_results import pformat_results
	
	try:
		txt_file = open(options.path_to_logs+os.sep+"Complete_OutputLog.log", "w")
	except BaseException as io_exc:
		SE.write("Log file cannot be opened. Please check path. Trying to find:\n"+options.path_to_logs+" folder\n")
		txt_file = open("Complete_OutputLog.log", "w")
		txt_file.write("Log file cannot be opened. Please check path. Trying to find:\n"+options.path_to_logs+" folder\n")
	
	try:
	
		opt = optimizer              # for us lazy programmer types
		dot_dats = options.dot_dat

		if options.keepPyomoLP:
			SE.write('\nSolver will write file: {}\n\n'.format( options.scenario + '.lp' ))
			txt_file.write('\nSolver will write file: {}\n\n'.format( options.scenario + '.lp' ))

		SE.write( '[        ] Reading data files.'); SE.flush()
		txt_file.write( 'Reading data files.')
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
		SE.write( '\r[%8.2f]\n' % duration() )
		txt_file.write( '[%8.2f]\n' % duration() )

		SE.write( '[        ] Creating Temoa model instance.'); SE.flush()
		txt_file.write( 'Creating Temoa model instance.')
		instance = model.create_instance( modeldata )
		SE.write( '\r[%8.2f\n' % duration() )
		txt_file.write( '[%8.2f]\n' % duration() )

		# Now do the solve
		SE.write( '[        ] Solving.'); SE.flush()
		txt_file.write( 'Solving.')
		if opt:
			result = opt.solve( instance , 
								keepfiles=options.keepPyomoLP, 
								symbolic_solver_labels=options.keepPyomoLP )
			SE.write( '\r[%8.2f\n' % duration() )
			txt_file.write( '[%8.2f]\n' % duration() )

			# return signal handlers to defaults, again
			signal(SIGINT, default_int_handler)

		else:
			SE.write( '\r---------- Not solving: no available solver\n' )
			txt_file.write( '\r---------- Not solving: no available solver\n' )
			return

		# ... print the easier-to-read/parse format
		msg = '[        ] Calculating reporting variables and formatting results.'
		SE.write( msg ); SE.flush()
		txt_file.write( 'Calculating reporting variables and formatting results.')
		instance.solutions.store_to(result)
		formatted_results = pformat_results( instance, result, options )
		SE.write( '\r[%8.2f\n' % duration() )
		txt_file.write( '[%8.2f]\n' % duration() )

		SO.write( formatted_results.getvalue() )
		txt_file.write( formatted_results.getvalue() )
		txt_file.close()
	except BaseException as model_exc:
		SE.write("exception found in solve_perfect_foresight\n")
		txt_file.write("exception found in solve_perfect_foresight\n")
		SE.write(str(model_exc))
		txt_file.write(str(model_exc))
		txt_file.close()

	if isinstance(options, TemoaConfig) and options.saveTEXTFILE:
		for inpu in options.dot_dat:
			file_ty = reg_exp.search(r"\b([\w-]+)\.(\w+)\b", inpu)
		
		new_dir = options.path_to_db_io+os.sep+file_ty.group(1)+'_'+options.scenario+'_model'
		
		if path.isfile(options.path_to_logs+os.sep+'Complete_OutputLog.log') and path.exists(new_dir):
			copyfile(options.path_to_logs+os.sep+'Complete_OutputLog.log', new_dir+os.sep+options.scenario+'_OutputLog.log')

	if isinstance(options, TemoaConfig) and options.keepPyomoLP:
		for inpu in options.dot_dat:
			file_ty = reg_exp.search(r"\b([\w-]+)\.(\w+)\b", inpu)
		
		new_dir = options.path_to_db_io+os.sep+file_ty.group(1)+'_'+options.scenario+'_model'
		
		for files in os.listdir(options.path_to_lp_files):
			if files.endswith(".lp"):
				lpfile = files
			else:
				if files == "README.txt":
					continue
				os.remove(options.path_to_lp_files+os.sep+files)
		
		if path.exists(new_dir):
			move(options.path_to_lp_files+os.sep+lpfile, new_dir+os.sep+options.scenario+'.lp')

def get_solvers():
	
	from logging import getLogger
	
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
		SE.write('\nNOTICE: Pyomo did not find any suitable solvers.  Temoa will '
		   'not be able to solve any models.  If you need help, ask on the '
		   'Temoa Project forum: http://temoaproject.org/\n\n' )

	return (available_solvers, default_solver)



def parse_args ( ):
	
	import argparse, platform, sys
	import os, re
	from os.path import dirname, abspath

	# used for some error messages below.
	red_bold = cyan_bold = reset = ''
	if platform.system() != 'Windows' and SE.isatty():
		red_bold  = '\x1b[1;31m'
		cyan_bold = '\x1b[1;36m'
		reset     = '\x1b[0m'

	

	available_solvers, default_solver = get_solvers()
	
	parser = argparse.ArgumentParser()
	parser.prog = path.basename( argv[0].strip('/') )

	solver      = parser.add_argument_group('Solver Options')
	stochastic  = parser.add_argument_group('Stochastic Options')
	postprocess = parser.add_argument_group('Postprocessing Options')
	mga         = parser.add_argument_group('MGA Options')

	parser.add_argument('dot_dat',
	  type=str,
	  nargs='*',
	  help='AMPL-format data file(s) with which to create a model instance. '
	       'e.g. "data.dat"'
	)

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
	
	parser.add_argument( '--path_to_logs',
	  help='Path to where debug logs will be generated by default. See folder debug_logs in db_io.',
	  action='store',
	  dest='path_to_logs',
	  default=re.sub('temoa_model$', 'db_io', dirname(abspath(__file__)))+os.sep+"debug_logs"
	)
	
	parser.add_argument( '--config',
	 help='Path to file containing configuration information.',
	 action='store',
	 dest='config',
	 default=None
	 )

	solver.add_argument('--solver',
	  help="Which backend solver to use.  See 'pyomo --help-solvers' for a list "
	       'of solvers with which Coopr can interface.  The list shown here is '
	       'what Coopr can currently find on this system.  [Default: {}]'
	       .format(default_solver),
	  action='store',
	  choices=sorted(available_solvers),
	  dest='solver',
	  default=default_solver)

	solver.add_argument('--keep_pyomo_lp_file',
	  help='Save the LP file as written by Pyomo.  This is distinct from the '
	       "solver's generated LP file, but /should/ represent the same model.  "
	       'Mainly used for debugging purposes.  '
	       '[Default: remove Pyomo LP file]',
	  action='store_true',
	  dest='keepPyomoLP',
	  default=False)

	#An optional argument with the ability to take a flag (--MGA) and a
	#numeric slack value
	mga.add_argument('--mga',
	  help='Include the flag --MGA and supply a slack-value and recieve a '
	    'Modeling to generate alternatives solution',
	  dest='mga',
	  type=float)

	options = parser.parse_args()
	#print options
	#Namespace(config='config_sample', dot_dat=[], generateSolverLP=False, how_to_cite=False, keepPyomoLP=False, mga=None, solver='mpec_nlp', version=False)

	# Use the Temoa configuration file to overwrite Kevin's argument parser
	if options.config:
		try:
			temoa_config = TemoaConfig(d_solver=default_solver)
			temoa_config.build(config=options.config)
			SE.write(repr(temoa_config))
			options = temoa_config
			SE.write('\nPlease press enter to continue or Ctrl+C to quit.\n')
			#raw_input() # Give the user a chance to confirm input
			if options.abort_temoa:
				return
		except KeyboardInterrupt:
			SE.write('\n\nUser requested quit.  Exiting Temoa ...\n')
			raise SystemExit()

	# First, the options that exit or do not perform any "real" computation
	if options.version:
		version(options)
		# this function exits
		return

	if options.how_to_cite:
		bibliographicalInformation(options)
		# this function exits.
		return
		
	if options.mga:
		msg = 'MGA specified (slack value: {})\n'.format( options.mga )
		SE.write( msg )

	s_choice = str( options.solver ).upper()
	SE.write('Notice: Using the {} solver interface.\n'.format( s_choice ))
	SE.flush()
	
	SE.write("Continue Operation? [Press enter to continue or CTRL+C to abort]\n")
	SE.flush()
	raw_input() # Give the user a chance to confirm input

	return options


def temoa_solve_ui ( model, config_filename ):
	from os import sep
	
	available_solvers, default_solver = get_solvers()

	temoa_config = TemoaConfig(d_solver=default_solver)
	temoa_config.build(config=config_filename)
	options = temoa_config
	
	global temp_lp_dest
	temp_lp_dest = '/srv/thirdparty/temoa/db_io/'

	from pyutilib.services import TempfileManager
	options.path_to_lp_files = options.path_to_logs + sep + "lp_files"
	TempfileManager.tempdir = options.path_to_lp_files	
	
	#FIXME: Put logic from parse_args() here that are not covered in
	#temoa_config.py. Like --how_to_cite & --version options.
	if options.version:
		version(options)
		# this function exits
		return

	if options.how_to_cite:
		bibliographicalInformation(options)
		# this function exits.
		return
	
	if options.abort_temoa:
		return
	
	run_solve(model, options)


def temoa_solve ( model ):
	
	from argparse import Namespace
	from os import sep

	options = parse_args()

	if options is None:
		return
	
	global temp_lp_dest
	temp_lp_dest = ''
	
	from pyutilib.services import TempfileManager
	options.path_to_lp_files = options.path_to_logs + sep + "lp_files"
	TempfileManager.tempdir = options.path_to_lp_files
	
	run_solve(model,options)

	

	

def run_solve(model,options):
	from sys import argv, version_info, exit
	from shutil import rmtree
	import os
	
	if version_info < (2, 7):
		msg = ("Temoa requires Python v2.7 to run.\n\nIf you've "
		  "installed Coopr with Python 2.6 or less, you'll need to reinstall "
		  'Coopr, taking care to install with a Python 2.7 (or greater) '
		  'executable.')
		raise SystemExit( msg )


	from pyomo.opt import SolverFactory

	opt = SolverFactory( options.solver )
	if opt:
		pass
		#if options.keepPyomoLP:
		# 	opt.keepfiles = True
		# 	opt.symbolic_solver_labels = True

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
			if options.mga:
				for inpu in options.dot_dat:
					file_ty = reg_exp.search(r"\b([\w-]+)\.(\w+)\b", inpu)
			
				options.path_to_db_io += os.sep+file_ty.group(1)+'_'+options.scenario+'_model'
				
				if os.path.exists( options.path_to_db_io ):
					rmtree( options.path_to_db_io )
				os.mkdir(options.path_to_db_io)
				
				MGA( model, opt, options )
			else:
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
