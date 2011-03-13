#!/usr/bin/env lpython

from coopr.pyomo import *

# Global Variables (dictionaries to cache parsing of Efficiency parameter)
g_processInputs  = dict()
g_processOutputs = dict()


##############################################################################
# Begin helper functions

def ProcessProduces ( A_period, A_tech, A_vintage, A_output ):
	"""\
Return the set of input energy carriers used by a technology (A_tech) to
produce a given output carrier (A_output).
"""
	index = (A_period, A_tech, A_vintage)
	if index in g_processOutputs:
		if A_output in g_processOutputs[ index ]:
			return g_processInputs[ index ]

	return set()


def ProcessConsumes ( A_period, A_tech, A_vintage, A_input ):
	"""\
Return the set of output energy carriers used by a technology (A_tech) to
produce a given input carrier (A_output).
"""
	index = (A_period, A_tech, A_vintage)
	if index in g_processInputs:
		if A_input in g_processInputs[ index ]:
			return g_processOutputs[ index ]

	return set()


def InitProcessParams ( M ):
	global g_processInputs
	global g_processOutputs

	for l_vintage in M.time_period:
		for l_tech in M.tech:
			for l_inp in M.physical_commodity:
				for l_out in M.all_commidities:
					eindex = (l_inp, l_tech, l_vintage, l_out)
					if M.Efficiency[eindex] > 0:
						for l_period in M.time_period:
							if l_period < l_vintage: continue

							if value(M.Lifetime[l_tech, l_vintage]) > l_period - l_vintage:
								pindex = (l_period, l_tech, l_vintage)
								if pindex not in g_processInputs:
									g_processInputs[  pindex ] = set()
									g_processOutputs[ pindex ] = set()
								g_processInputs[ pindex ].add( l_inp )
								g_processOutputs[pindex ].add( l_out )


def isValidProcess( A_period, A_inp, A_tech, A_vintage, A_out ):
	"""\
Returns a boolean indicating whether, in any given period, a technology can take a specified input carrier and convert it to and specified output carrier.
"""
	index = (A_period, A_tech, A_vintage)
	if index in g_processInputs and index in g_processOutputs:
		if A_inp in g_processInputs[ index ]:
			if A_out in g_processOutputs[ index ]:
				return True

	return False

# End helper functions
##############################################################################

##############################################################################
# Begin *_rule definitions

def TotalCost_rule ( M ):
	"""
	Objective function.
	"""

	# There appears to be no other way to hook into Pyomo's model creation than
	# by "hijacking", for a time, it's first call to one of our functions.
	InitProcessParams( M )

	l_cost = 0

	for l_period in M.time_period:
		for l_tech in M.tech:
			for l_vintage in M.time_period:
				for l_out in M.physical_commodity:
					for l_inp in ProcessProduces( l_period, l_tech, l_vintage, l_out ):
						l_cost += (
						    M.V_FlowOut[l_period, l_inp, l_tech, l_vintage, l_out]
						  * M.CommodityProductionCost[l_period, l_tech, l_vintage]
						)

	return l_cost
Objective_rule = TotalCost_rule


##############################################################################
#   Constraint rules

def ActivityConstraint_rule ( A_period, A_tech, A_vintage, A_output, M ):
	l_activity = 0
	for l_inp in ProcessProduces( A_period, A_tech, A_vintage, A_output ):
		l_activity += M.V_FlowOut[A_period, l_inp, A_tech, A_vintage, A_output]

	expr = ( M.V_Activity[A_period, A_tech, A_vintage, A_output] == l_activity )
	return expr


def CapacityConstraint_rule ( A_period, A_tech, A_vintage, A_output, M ):
	l_cf = (
	    M.V_Capacity[A_period, A_tech, A_vintage, A_output]
	  * M.CapacityFactor[A_period, A_tech, A_vintage, A_output]
	)

	expr = ( M.V_Activity[A_period, A_tech, A_vintage, A_output] == l_cf )
	return expr


def ResourceExtractionConstraint_rule ( A_period, A_resource, M ):
	l_extract = 0
	for l_tech in M.resource_tech:
		for l_vintage in M.time_period:
			if isValidProcess( A_period, A_resource, l_tech, l_vintage, A_resource ):
				l_extract += M.V_FlowIn[A_period, A_resource, l_tech, l_vintage, A_resource]

	expression = (l_extract <= M.ResourceBound[A_period, A_resource])
	return expression


def CommodityBalanceConstraint_rule ( A_period, A_carrier, M ):
	l_vflow_out = l_vflow_in = 0

	for l_tech in M.tech:
		for l_vintage in M.time_period:
			for l_inp in ProcessProduces( A_period, l_tech, l_vintage, A_carrier ):
				l_vflow_out += M.V_FlowOut[A_period, l_inp, l_tech, l_vintage, A_carrier]

	for l_tech in M.production_tech:
		for l_vintage in M.time_period:
			for l_out in ProcessConsumes( A_period, l_tech, l_vintage, A_carrier ):
				l_vflow_in += M.V_FlowIn[A_period, A_carrier, l_tech, l_vintage, l_out]

	if type(l_vflow_out) == type(l_vflow_in):
		if int is type(l_vflow_out):
			# Tell Pyomo not to create this constraint; it's useless because both
			# of the flows are 0.  i.e. carrier not requested; nothing makes it.
			return None
	elif int is type(l_vflow_out):
		msg = "Unable to meet an interprocess '%s' transfer in '%s'.\n"         \
		  "No flow out.  Constraint flow in:\n   %s\n"                          \
		  "Possible reasons:\n"                                                 \
		  " - Is there a missing tech in set 'resource_tech'?\n"                \
		  " - Is there a missing tech in set 'production_tech'?\n"              \
		  " - Is there a missing commodity in set 'physical_commodity'?\n"      \
		  " - Are there missing entries in the Efficiency parameter?\n"         \
		  " - Does a tech need a longer Lifetime parameter setting?"
		raise ValueError, msg % (A_carrier, A_period, l_vflow_in)

	expression = (l_vflow_out >= l_vflow_in)
	return expression


def ProcessBalanceConstraint_rule ( A_period, A_inp, A_tech, A_vintage, A_out, M ):
	if not isValidProcess(A_period, A_inp, A_tech, A_vintage, A_out):
		# No sense in creating a guaranteed unused constraint
		return None

	expr = (
	    M.V_FlowOut[A_period, A_inp, A_tech, A_vintage, A_out]
	      <=
	    M.V_FlowIn[A_period, A_inp, A_tech, A_vintage, A_out]
	  * M.Efficiency[A_inp, A_tech, A_vintage, A_out]
	)

	return expr


def DemandConstraint_rule ( A_period, A_comm, M ):
	l_supply = 0

	if not (M.Demand[A_period, A_comm] > 0):
		# nothing to be met: don't create a useless constraint like X >= 0
		return None

	for l_tech in M.tech:
		for l_vintage in M.time_period:
			for l_input in ProcessProduces( A_period, l_tech, l_vintage, A_comm ):
				l_supply += M.V_FlowOut[A_period, l_input, l_tech, l_vintage, A_comm]

	if int is type( l_supply ):
		msg = "Error: Demand '%s' in '%s' unable to be met by any technology." \
		  "\n\tPossible reasons:\n"                                            \
		  " - Is the Efficiency parameter missing an entry for this demand?\n" \
		  " - Does a tech that satisfies this demand need a longer Lifetime?\n"
		raise ValueError, msg % (A_comm, A_period)

	expression = (l_supply >= M.Demand[A_period, A_comm])
	return expression

# End constraint rules
##############################################################################

# End *_rule definitions
##############################################################################
