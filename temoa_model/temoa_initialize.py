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

from operator import itemgetter as iget
from itertools import product as cross_product
from sys import argv, stderr as SE, stdout as SO

import IPython

# Ensure compatibility with Python 2.7 and 3
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

try:
	from pyomo.core import (
	  AbstractModel, BuildAction, Constraint, NonNegativeReals, Reals, Objective, Param,
	  Set, Var, minimize, value
	)

except:
	msg = """
Unable to find 'pyomo.core.' Check to make sure pyomo is installed, and that
you are running a version compatible with Temoa.
"""

	raise ImportError( msg )


class TemoaModel( AbstractModel ):
	def __init__( self, *args, **kwds ):
		AbstractModel.__init__( self, *args, **kwds )
		self.processInputs  = dict()
		self.processOutputs = dict()
		self.processLoans = dict()
		self.activeFlow_psditvo = None
		self.activeFlowInStorage_psditvo = None
		self.activeCurtailment_psditvo = None
		self.activeActivity_ptv = None
		self.activeCapacity_tv = None
		self.activeCapacityAvailable_pt = None

		self.commodityDStreamProcess  = dict() # The downstream process of a commodity during a period
		self.commodityUStreamProcess  = dict() # The upstream process of a commodity during a period
		self.ProcessInputsByOutput = dict()
		self.ProcessOutputsByInput = dict()
		self.processTechs = dict()
		self.processReservePeriods = dict()
		self.processVintages = dict()
		self.baseloadVintages = dict()
		self.curtailmentVintages = dict()
		self.storageVintages = dict()
		self.rampVintages = dict()
		self.inputsplitVintages = dict()
		self.outputsplitVintages = dict()
		self.ProcessByPeriodAndOutput = dict()

# ---------------------------------------------------------------
# Validation and initialization routines.
# There are a variety of functions in this section that do the following:
# Check valid indices, validate parameter specifications, and set default
# parameter values.
# ---------------------------------------------------------------

def isValidProcess ( self, p, i, t, v, o ):
	"""\
Returns a boolean (True or False) indicating whether, in any given period, a
technology can take a specified input carrier and convert it to and specified
output carrier. Not currently used.
"""
	index = (p, t, v)
	if index in self.processInputs and index in self.processOutputs:
		if i in self.processInputs[ index ]:
			if o in self.processOutputs[ index ]:
				return True

	return False

def get_str_padding ( obj ):
	return len(str( obj ))

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
		raise Exception( msg.format(
		  c, s, d, p, flow_in_expr.getvalue()
		))

def DemandConstraintErrorCheck ( supply, p, s, d, dem ):
	if int is type( supply ):
		msg = ("Error: Demand '{}' for ({}, {}, {}) unable to be met by any "
		  'technology.\n\tPossible reasons:\n'
		  ' - Is the Efficiency parameter missing an entry for this demand?\n'
		  ' - Does a tech that satisfies this demand need a longer '
		  'LifetimeProcess?\n')
		raise Exception( msg.format(dem, p, s, d) )

def validate_time ( M ):
	"""
	We check for integer status here, rather then asking Pyomo to do this via
	a 'within=Integers' clause in the definition so that we can have a very
	specific error message.  If we instead use Pyomo's mechanism, the
	python invocation of Temoa throws an error (including a traceback)
	that has proven to be scary and/or impenetrable for the typical modeler.
	"""
	for year in M.time_exist:
		if isinstance(year, int): continue

		msg = ('Set "time_exist" requires integer-only elements.\n\n  Invalid '
		  'element: "{}"')
		raise Exception( msg.format( year ))

	for year in M.time_future:
		if isinstance(year, int): continue

		msg = ('Set "time_future" requires integer-only elements.\n\n  Invalid '
		  'element: "{}"')
		raise Exception( msg.format( year ))

	if len( M.time_future ) < 2:
		msg = ('Set "time_future" needs at least 2 specified years.  Temoa '
		  'treats the integer numbers specified in this set as boundary years '
		  'between periods, and uses them to automatically ascertain the length '
		  '(in years) of each period.  Note that this means that there will be '
		  'one less optimization period than the number of elements in this set.'
		)
		raise Exception( msg )

	# Ensure that the time_exist < time_future
	max_exist    = max( M.time_exist )
	min_horizon = min( M.time_future )

	if not ( max_exist < min_horizon ):
		msg = ('All items in time_future must be larger than in time_exist.\n'
		  'time_exist max:   {}\ntime_future min: {}')
		raise Exception( msg.format(max_exist, min_horizon) )


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

		raise Exception( msg.format(items, total ))


def CheckEfficiencyIndices ( M ):
	"""
	Ensure that there are no unused items in any of the Efficiency index sets.
	"""

	c_physical = set( i for i, t, v, o in M.Efficiency.sparse_iterkeys() )
	techs      = set( t for i, t, v, o in M.Efficiency.sparse_iterkeys() )
	c_outputs  = set( o for i, t, v, o in M.Efficiency.sparse_iterkeys() )

	symdiff = c_physical.symmetric_difference( M.commodity_physical )
	for i in M.commodity_emissions.keys(): #For letting emission commodities as input cmmodities in the efficiency table
		if i in symdiff:
			symdiff.remove(i)

	if symdiff:
		msg = ('Unused or unspecified physical carriers.  Either add or remove '
		  'the following elements to the Set commodity_physical.'
		  '\n\n    Element(s): {}')
		symdiff = (str(i) for i in symdiff)
		raise Exception( msg.format( ', '.join(symdiff) ))

	symdiff = techs.symmetric_difference( M.tech_all )
	if symdiff:
		msg = ('Unused or unspecified technologies.  Either add or remove '
		  'the following technology(ies) to the tech_resource or '
		  'tech_production Sets.\n\n    Technology(ies): {}')
		symdiff = (str(i) for i in symdiff)
		raise Exception( msg.format( ', '.join(symdiff) ))

	diff = M.commodity_demand - c_outputs
	if diff:
		msg = ('Unused or unspecified outputs.  Either add or remove the '
		  'following elements to the commodity_demand Set.'
		  '\n\n    Element(s): {}')
		diff = (str(i) for i in diff)
		raise Exception( msg.format( ', '.join(diff) ))


def CreateCapacityFactors ( M ):
	"""
	Steps to creating capacity factors:
	1. Collect all possible processes
	2. Find the ones _not_ specified in CapacityFactorProcess
	3. Set them, based on CapacityFactorTech.
	"""
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
		# CFP._constructed = False
		for s, d, t, v in unspecified_cfs:
			CFP[s, d, t, v] = M.CapacityFactorTech[s, d, t]
		# CFP._constructed = True


def CreateLifetimes ( M ):
	"""
	Steps to creating lifetimes:
	1. Collect all possible processes
	2. Find the ones _not_ specified in LifetimeProcess and LifetimeLoanProcess
	3. Set them, based on Lifetime*Tech.
	"""

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
		# LLN._constructed = False
		for t, v in unspecified_loan_lives:
			LLN[t, v] = M.LifetimeLoanTech[ t ]
		# LLN._constructed = True

	if unspecified_tech_lives:
		# LPR._constructed = False
		for t, v in unspecified_tech_lives:
			LPR[t, v] = M.LifetimeTech[ t ]
		# LPR._constructed = True


def CreateDemands ( M ):
	"""
	Steps to create the demand distributions
	1. Use Demand keys to ensure that all demands in commodity_demand are used
	2. Find any slices not set in DemandDefaultDistribution, and set them based
	on the associated SegFrac slice.
	3. Validate that the DemandDefaultDistribution sums to 1.
	4. Find any per-demand DemandSpecificDistribution values not set, and set
	set them from DemandDefaultDistribution.  Note that this only sets a
	distribution for an end-use demand if the user has *not* specified _any_
	anything for that end-use demand.  Thus, it is up to the user to fully
	specify the distribution, or not.  No in-between.
	 5. Validate that the per-demand distributions sum to 1.
	"""

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
		# DDD._constructed = False
		for tslice in unset_defaults:
			DDD[ tslice ] = M.SegFrac[ tslice ]
		# DDD._constructed = True

	# Step 3
	total = sum( i for i in DDD.itervalues() )
	if abs(value(total) - 1.0) > 0.001:
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

		raise Exception( msg.format(items, total) )

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
		# DSD._constructed = False
		for s, d, dem in unset_distributions:
			DSD[s, d, dem] = DDD[s, d]
		# DSD._constructed = True

	# Step 5
	for dem in used_dems:
		keys = (k for k in DSD.sparse_iterkeys() if DSD_dem_getter(k) == dem )
		total = sum( DSD[ i ] for i in keys )

		if abs(value(total) - 1.0) > 0.001:
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

			raise Exception( msg.format(dem, items, total) )


def CreateCosts ( M ):
	"""
	Steps to creating fixed and variable costs:
	1. Collect all possible cost indices (CostFixed, CostVariable)
	2. Find the ones _not_ specified in CostFixed and CostVariable
	3. Set them, based on Cost*VintageDefault
	"""

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
		# CF._constructed = False
		for p, t, v in unspecified_fixed_prices:
			if (t, v) in M.CostFixedVintageDefault:
				CF[p, t, v] = M.CostFixedVintageDefault[t, v]
		# CF._constructed = True

	if unspecified_var_prices:
		# CV._constructed = False
		for p, t, v in unspecified_var_prices:
			if (t, v) in M.CostVariableVintageDefault:
				CV[p, t, v] = M.CostVariableVintageDefault[t, v]
		# CV._constructed = True


def init_set_time_optimize ( M ):
	return sorted( M.time_future )[:-1]


def init_set_vintage_exist ( M ):
	return sorted( M.time_exist )


def init_set_vintage_optimize ( M ):
	return sorted( M.time_optimize )

# ---------------------------------------------------------------
# The functions below perform the sparse matrix indexing, allowing Pyomo to only
# create the necessary parameter, variable, and constraint indices.  This
#  cuts down *tremendously* on memory usage, which decreases time and increases
# the maximum specifiable problem size.
#
# It begins below in CreateSparseDicts, which creates a set of
# dictionaries that serve as the basis of the sparse indices.
# ---------------------------------------------------------------

def CreateSparseDicts ( M ):
	"""
	This function creates customized dictionaries with only the key / value pairs
	defined in the associated datafile. The dictionaries defined here are used to
	do the sparse matrix indexing for all parameters, variables, and constraints
	in the model. The function works by looping over the sparse indices in the
	Efficiency table. For each iteration of the loop, the appropriate key / value
	pairs are defined as appropriate for each dictionary.
	"""
	l_first_period = min( M.time_future )
	l_exist_indices = M.ExistingCapacity.sparse_keys()
	l_used_techs = set()

	# The basis for the dictionaries are the sparse keys defined in the
	# Efficiency table.
	for i, t, v, o in M.Efficiency.sparse_iterkeys():
		l_process = (t, v)
		l_lifetime = value(M.LifetimeProcess[ l_process ])
		# Do some error checking for the user.
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

		# Add in the period (p) index, since it's not included in the efficiency
		# table.
		for p in M.time_optimize:
			# Can't build a vintage before it's been invented
			if p < v: continue

			pindex = (p, t, v)

			if v in M.time_optimize:
				l_loan_life = value(M.LifetimeLoanProcess[ l_process ])
				if v + l_loan_life >= p:
					M.processLoans[ pindex ] = True

			# if tech is no longer active, don't include it
			if v + l_lifetime <= p: continue

			# Here we utilize the indices in a given iteration of the loop to
			# create the dictionary keys, and initialize the associated values
			# to an empty set.
			if pindex not in M.processInputs:
				M.processInputs[  pindex ] = set()
				M.processOutputs[ pindex ] = set()
			if (p, i) not in M.commodityDStreamProcess:
				M.commodityDStreamProcess[p, i] = set()
			if (p, o) not in M.commodityUStreamProcess:
				M.commodityUStreamProcess[p, o] = set()
			if (p, t, v, i) not in M.ProcessOutputsByInput:
				M.ProcessOutputsByInput[p, t, v, i] = set()
			if (p, t, v, o) not in M.ProcessInputsByOutput:
				M.ProcessInputsByOutput[p, t, v, o] = set()
			if t not in M.processTechs:
					M.processTechs[t] = set()
			# While the dictionary just above indentifies the vintage (v)
			# associated with each (p,t) we need to do the same below for various
			# technology subsets.
			if (p, t) not in M.processVintages:
				M.processVintages[p, t] = set()
			if t in M.tech_curtailment and (p, t) not in M.curtailmentVintages:
				M.curtailmentVintages[p, t] = set()
			if t in M.tech_baseload and (p, t) not in M.baseloadVintages:
				M.baseloadVintages[p, t] = set()
			if t in M.tech_storage and (p,t) not in M.storageVintages:
				M.storageVintages[p,t] = set()
			if t in M.tech_ramping and (p,t) not in M.rampVintages:
				M.rampVintages[p,t] = set()
			if (p, i, t) in M.TechInputSplit.sparse_iterkeys() and (p, i, t) not in M.inputsplitVintages:
				M.inputsplitVintages[p,i,t] = set()
			if (p, t, o) in M.TechOutputSplit.sparse_iterkeys() and (p, t, o) not in M.outputsplitVintages:
				M.outputsplitVintages[p,t,o] = set()
			if t in M.tech_resource and (p,o) not in M.ProcessByPeriodAndOutput:
				M.ProcessByPeriodAndOutput[p,o] = set()
			if t in M.tech_reserve and p not in M.processReservePeriods:
					M.processReservePeriods[p] = set()

			# Now that all of the keys have been defined, and values initialized
			# to empty sets, we fill in the appropriate values for each
			# dictionary.
			M.processInputs[ pindex ].add( i )
			M.processOutputs[pindex ].add( o )
			M.commodityDStreamProcess[p, i].add( (t, v) )
			M.commodityUStreamProcess[p, o].add( (t, v) )
			M.ProcessOutputsByInput[p, t, v, i].add( o )
			M.ProcessInputsByOutput[p, t, v, o].add( i )
			M.processTechs[t].add( (p, v) )
			M.processVintages[p, t].add( v )
			if t in M.tech_curtailment:
				M.curtailmentVintages[p, t].add( v )
			if t in M.tech_baseload:
				M.baseloadVintages[p, t].add( v )
			if t in M.tech_storage:
				M.storageVintages[p, t].add( v )
			if t in M.tech_ramping:
				M.rampVintages[p , t].add( v )
			if (p, i, t) in M.TechInputSplit.sparse_iterkeys():
				M.inputsplitVintages[p,i,t].add( v )
			if (p, t, o) in M.TechOutputSplit.sparse_iterkeys():
				M.outputsplitVintages[p,t,o].add( v )
			if t in M.tech_resource:
				M.ProcessByPeriodAndOutput[p,o].add(( i,t,v ))
			if t in M.tech_reserve:
				M.processReservePeriods[p].add( (t,v) )


	l_unused_techs = M.tech_all - l_used_techs
	if l_unused_techs:
		msg = ("Notice: '{}' specified as technology, but it is not utilized in "
		       'the Efficiency parameter.\n')
		for i in sorted( l_unused_techs ):
			SE.write( msg.format( i ))

	M.activeFlow_psditvo = set(
	  (p, s, d, i, t, v, o)

	  for p,t in M.processVintages.keys()
	  for v in M.processVintages[ p, t ]
	  for i in M.processInputs[ p, t, v ]
	  for o in M.ProcessOutputsByInput[ p, t, v, i ]
	  for s in M.time_season
	  for d in M.time_of_day
	)

	M.activeFlowInStorage_psditvo = set(
	  (p, s, d, i, t, v, o)

	  for p,t in M.processVintages.keys() if t in M.tech_storage
	  for v in M.processVintages[ p, t ]
	  for i in M.processInputs[ p, t, v ]
	  for o in M.ProcessOutputsByInput[ p, t, v, i ]
	  for s in M.time_season
	  for d in M.time_of_day
	)



	M.activeCurtailment_psditvo = set(
	   (p, s, d, i, t, v, o)

	  for p,t in M.curtailmentVintages.keys()
	  for v in M.curtailmentVintages[ p, t ]
	  for i in M.processInputs[ p, t, v ]
	  for o in M.ProcessOutputsByInput[ p, t, v, i ]
	  for s in M.time_season
	  for d in M.time_of_day
	)

	M.activeActivity_ptv = set(
	  (p, t, v)

	  for p,t in M.processVintages.keys()
	  for v in M.processVintages[ p, t ]
	)

	M.activeCapacity_tv = set(
	  (t, v)

	  for p,t in M.processVintages.keys()
	  for v in M.processVintages[ p, t ]
	)

	M.activeCapacityAvailable_pt = set(
	  (p, t)

	  for p,t in M.processVintages.keys()
	  if M.processVintages[ p, t ]
	)

# ---------------------------------------------------------------
# Create sparse parameter indices.
# These functions are called from temoa_model.py and use the sparse keys 
# associated with specific parameters.
# ---------------------------------------------------------------

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
	return M.activeActivity_ptv

def CostVariableIndices ( M ):
	return M.activeActivity_ptv

def CostInvestIndices ( M ):
	indices = set(
	  (t, v)

	  for p, t, v in M.processLoans
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
	return M.activeActivity_ptv

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

# ---------------------------------------------------------------
# Create sparse indices for decision variables.
# These functions are called from temoa_model.py and use the dictionaries
# created above in CreateSparseDicts()
# ---------------------------------------------------------------

def CapacityVariableIndices ( M ):
	return M.activeCapacity_tv

def CapacityAvailableVariableIndices ( M ):
	return M.activeCapacityAvailable_pt

def FlowVariableIndices ( M ):
	return M.activeFlow_psditvo

def FlowInStorageVariableIndices ( M ):
	return M.activeFlowInStorage_psditvo


def CurtailmentVariableIndices ( M ):
	return M.activeCurtailment_psditvo

def ActivityVariableIndices ( M ):
	activity_indices = set(
	  (p, s, d, t, v)

	  for p, t, v in M.activeActivity_ptv
	  for s in M.time_season
	  for d in M.time_of_day
	)

	return activity_indices

def ActivityByPeriodAndProcessVarIndices ( M ):
	return M.activeActivity_ptv

# ---------------------------------------------------------------
# Create sparse indices for constraints.
# These functions are called from temoa_model.py and use the dictionaries
# created above in CreateSparseDicts()
# ---------------------------------------------------------------

def DemandActivityConstraintIndices ( M ):
	"""\
This function returns a set of sparse indices that are used in the
DemandActivity constraint. It returns a tuple of the form:
(p,s,d,t,v,dem,first_s,first_d) where "dem" is a demand commodity, and "first_s"
and "first_d" are the reference season and time-of-day, respectively used to
ensure demand activity remains consistent across time slices.
"""
	first_s = M.time_season.first()
	first_d = M.time_of_day.first()
	for p,t,v,dem in M.ProcessInputsByOutput.keys():
		if dem in M.commodity_demand:
			for s in M.time_season:
				for d in M.time_of_day:
					if s != first_s or d != first_d:
						yield (p,s,d,t,v,dem,first_s,first_d)

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

	  for p,t in M.baseloadVintages.keys()
	  for v in M.baseloadVintages[ p, t ]
	  for s in M.time_season
	  for d in M.time_of_day
	)

	return indices

def CommodityBalanceConstraintIndices ( M ):
	# We only consider those commodities that have both upstream and downstream
	# processes during a specific period.
	period_commodity_with_up = set( M.commodityUStreamProcess.keys() )
	period_commodity_with_dn = set( M.commodityDStreamProcess.keys() )
	period_commodity = period_commodity_with_up.intersection( period_commodity_with_dn )
	indices = set(
	  (p, s, d, o)

	  for p, o in period_commodity
	  for t, v in M.commodityUStreamProcess[ p, o ]
	  if t not in M.tech_storage
	  for s in M.time_season
	  for d in M.time_of_day
	)

	return indices

def StorageVariableIndices ( M ):
	indices = set(
		(p, s, d, t, v)
		
		for p,t in M.storageVintages.keys()
		for s in M.time_season
		for d in M.time_of_day		
		for v in M.storageVintages[ p, t ]

	)

	return indices
	
def RampConstraintDayIndices ( M ):
	indices = set(
	  (p, s, d, t, v)

	  for p,t in M.rampVintages.keys()
	  for s in M.time_season
	  for d in M.time_of_day
	  for v in M.rampVintages[ p, t ]
	)

	return indices

def RampConstraintSeasonIndices ( M ):
	indices = set(
	  (p, s, t, v)

	  for p,t in M.rampVintages.keys()
	  for s in M.time_season	  
	  for v in M.rampVintages[ p, t ]
	)

	return indices

def RampConstraintPeriodIndices ( M ):
	indices = set(
	  (p, t, v)

	  for p,t in M.rampVintages.keys()
	  for v in M.rampVintages[ p, t ]	)

	return indices

def ReserveMarginIndices ( M ):
	indices = set(
		(p , s , d )

	   for p in M.time_optimize
	   for s in M.time_season
	   for d in M.time_of_day
	)
	return indices

def TechInputSplitConstraintIndices ( M ):
	indices = set(
	  (p, s, d, i, t, v)

	  for p, i, t in M.inputsplitVintages.keys()
	  for v in M.inputsplitVintages[ p, i, t ]
	  for s in M.time_season
	  for d in M.time_of_day
	)

	return indices

def TechOutputSplitConstraintIndices ( M ):
	indices = set(
	  (p, s, d, t, v, o)

	  for p, t, o in M.outputsplitVintages.keys()
	  for v in M.outputsplitVintages[ p, t, o ]
	  for s in M.time_season
	  for d in M.time_of_day
	)

	return indices