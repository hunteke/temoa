from temoa_lib import *

##############################################################################
# Begin *_rule definitions

def TotalCost_rule ( M ):
	"""\
Objective function.

This function is currently a simple summation of all items in V_FlowOut multiplied by CommunityProductionCost.  For the time being (i.e. during development), this is intended to make development and debugging simpler.
	"""

	# There appears to be no other way to hook into Pyomo's model creation than
	# by "hijacking", for a time, it's first call to one of our functions.
	InitProcessParams( M )

	l_cost = 0

	for l_period in M.time_optimize:
		for l_season in M.time_season:
			for l_time_of_day in M.time_of_day:
				for l_tech in M.tech_all:
					for l_vintage in M.vintage_all:
						for l_out in M.commodity_physical:
							for l_inp in ProcessInputsByOutput( (l_period, l_tech, l_vintage), l_out ):
								l_cost += (
								    M.V_FlowOut[l_period, l_season, l_time_of_day, l_inp, l_tech, l_vintage, l_out]
								  * M.CommodityProductionCost[l_period, l_tech, l_vintage]
								)

	return l_cost
Objective_rule = TotalCost_rule


##############################################################################
#   Constraint rules

def ActivityConstraint_rule ( A_period, A_season, A_time_of_day, A_tech, A_vintage, M ):
	"""\
As V_Activity is a derived variable, the constraint sets V_Activity to the sum over input and output energy carriers of a process.

(for each period, season, time_of_day, tech, vintage)
V_Activity[p,s,d,t,v] = sum((inp,out), V_FlowOut[p,s,d,inp,t,v,out])
	"""
	pindex = (A_period, A_tech, A_vintage)
	aindex = (A_period, A_season, A_time_of_day, A_tech, A_vintage)

	# The following two lines prevent creating obviously invalid or unnecessary constraints
	# ex: a coal power plant does not consume wind and produce light.
	if not ProcessOutputs( *pindex ):
		return None

	l_activity = 0
	for l_inp in ProcessInputs( *pindex ):
		for l_out in ProcessOutputs( *pindex ):
			l_activity += M.V_FlowOut[A_period, A_season, A_time_of_day, l_inp, A_tech, A_vintage, l_out]

	expr = ( M.V_Activity[ aindex ] == l_activity )
	return expr


def CapacityConstraint_rule ( A_period, A_season, A_time_of_day, A_tech, A_vintage, M ):
	"""\
V_Capacity is a derived variable; this constraint sets V_Capacity to at least be able to handle the activity in any optimization time slice.  In effect, this sets V_Capacity[p,t,v] to the max of the activity for similar indices: max(Activity[p,*,*t,v])

(for each period, season, time_of_day, tech, vintage)
V_Capacity[t,v] * CapacityFactor[t,v] >= V_Activity[p,s,d,t,v]
	"""
	pindex = (A_period, A_tech, A_vintage)

	# No sense in creating a guaranteed unused constraint
	if not ProcessOutputs( *pindex ):
		return None

	l_vintage_activity = M.V_Activity[A_period, A_season, A_time_of_day, A_tech, A_vintage]

	cindex = (A_tech, A_vintage)
	l_capacity = M.V_Capacity[ cindex ] * M.CapacityFactor[ cindex ]

	expr = ( l_vintage_activity <= l_capacity )
	return expr


def ExistingCapacityConstraint_rule ( A_tech, A_vintage, M ):
	"""\
For vintage periods that the model is not to optimize, explicitly set the capacity values based on dat file input.

(for each tech, vintage_exist)
V_Capacity[t,v] = Param(Existingcapacity[t,v])
	"""
	index = (A_tech, A_vintage)

	# No sense in creating a guaranteed unused constraint
	ecapacity = value(M.ExistingCapacity[ index ])
	if not (ecapacity > 0):
		return None

	expr = ( M.V_Capacity[ index ] == ecapacity )
	return expr


def ResourceExtractionConstraint_rule ( A_period, A_resource, M ):
	"""\
Prevent TEMOA from extracting an endless supply of energy from "the ether".

(for each period, resource)
sum((season,time_of_day,tech,vintage),V_FlowIn[p,*,*,r,*,*r]) <= Param(ResourceBound[p,r])
	"""
	l_extract = 0
	for l_tech in M.tech_resource:
		for l_vintage in M.vintage_all:
			if isValidProcess( A_period, A_resource, l_tech, l_vintage, A_resource ):
				for l_season in M.time_season:
					for l_time_of_day in M.time_of_day:
						l_extract += M.V_FlowIn[A_period, l_season, l_time_of_day, A_resource, l_tech, l_vintage, A_resource]

	expression = (l_extract <= M.ResourceBound[A_period, A_resource])
	return expression


def CommodityBalanceConstraint_rule ( A_period, A_season, A_time_of_day, A_carrier, M ):
	"""\
Ensure that the FlowOut of a produced energy carrier at least meets the demand of the needed FlowIn of that energy carrier.  That is, this constraint maintains energy flows between processes.

(for each period, season, time_of_day, energy_carrier)
sum((inp,tech,vintage),V_FlowOut[p,s,t,*,*,*,c]) >= sum((tech,vintage,out),V_FlowIn[p,s,t,c,*,*,*])
sum((inp,tech,vintage),V_FlowOut[period,season,time_of_day,*,*,*,carrier]) >= sum((tech,vintage,out),V_FlowIn[period,season,time_of_day,carrier,*,*,*])
	"""
	l_vflow_out = l_vflow_in = 0

	for l_tech in M.tech_all:
		for l_vintage in M.vintage_all:
			for l_inp in ProcessInputsByOutput( (A_period, l_tech, l_vintage), A_carrier ):
				l_vflow_out += M.V_FlowOut[A_period, A_season, A_time_of_day, l_inp, l_tech, l_vintage, A_carrier]

	for l_tech in M.tech_production:
		for l_vintage in M.vintage_all:
			for l_out in ProcessOutputsByInput( (A_period, l_tech, l_vintage), A_carrier ):
				l_vflow_in += M.V_FlowIn[A_period, A_season, A_time_of_day, A_carrier, l_tech, l_vintage, l_out]

	CommodityBalanceConstraintErrorCheck(
	  l_vflow_out, l_vflow_in, A_carrier, A_season, A_time_of_day, A_period
	)

	expression = (l_vflow_out >= l_vflow_in)
	return expression


def ProcessBalanceConstraint_rule ( A_period, A_season, A_time_of_day, A_inp, A_tech, A_vintage, A_out, M ):
	"""\
Analogous to CommodityBalance, this constraint ensures that the amount of energy leaving a process is not more than the amount entering it.

(for each period, season, time_of_day, inp_carrier, vintage, out_carrier)
V_FlowOut[p,s,d,t,v,o] <= V_FlowIn[p,s,d,t,v,o] * Efficiency[i,t,v,o]
	"""
	index = (A_period, A_inp, A_tech, A_vintage, A_out)
	if not isValidProcess( *index ):
		# No sense in creating a guaranteed unused constraint
		return None

	aindex = (A_period, A_season, A_time_of_day, A_inp, A_tech, A_vintage, A_out)

	expr = (
	    M.V_FlowOut[ aindex ]
	      <=
	    M.V_FlowIn[ aindex ]
	  * M.Efficiency[A_inp, A_tech, A_vintage, A_out]
	)

	return expr


def DemandCapacityConstraint_rule ( A_period, A_season, A_time_of_day, A_comm, M ):
	"""\
"""

	l_capacity = sum(
	  M.V_Capacity[ l_tech, l_vin ]

	  for l_tech, l_vin in ProcessesByPeriodDemand( A_period, A_comm, M )
	)

	dindex = (A_period, A_season, A_time_of_day, A_comm)
	sindex = (A_season, A_time_of_day)

	l_demandfrac = M.Demand[ dindex ] / M.SegFrac[ sindex ]

	expression = (l_capacity >= l_demandfrac)
	return expression


def DemandConstraint_rule ( A_period, A_season, A_time_of_day, A_comm, M ):
	"""\
The driving constraint, this rule ensures that supply at least equals demand.

(for each period, season, time_of_day, commodity)
sum((inp,tech,vintage),V_FlowOut[p,s,d,*,*,*,commodity]) >= Demand[p,s,d,commodity]
	"""
	index = (A_period, A_season, A_time_of_day, A_comm)
	if not (M.Demand[ index ] > 0):
		# nothing to be met: don't create a useless constraint like X >= 0
		return None

	l_supply = 0
	for l_tech in M.tech_all:
		for l_vintage in M.vintage_all:
			for l_input in ProcessInputsByOutput( (A_period, l_tech, l_vintage), A_comm ):
				l_supply += M.V_FlowOut[A_period, A_season, A_time_of_day, l_input, l_tech, l_vintage, A_comm]

	DemandConstraintErrorCheck (
	  l_supply, A_comm, A_period, A_season, A_time_of_day
	)

	expression = (l_supply >= M.Demand[ index ])
	return expression

# End constraint rules
##############################################################################

# End *_rule definitions
##############################################################################
