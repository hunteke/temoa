from temoa_lib import *

##############################################################################
# Begin *_rule definitions

def TotalCost_rule ( M ):
	"""\
Objective function.

This function is currently a simple summation of all items in V_FlowOut multiplied by CommunityProductionCost.  For the time being (i.e. during development), this is intended to make development and debugging simpler.
	"""
	l_invest_indices = M.CostInvest.keys()
	l_fixed_indices  = M.CostFixed.keys()
	l_marg_indices   = M.CostMarginal.keys()

	l_loan_costs = sum(
	    M.V_Capacity[l_tech, l_vin] * M.PeriodRate[ l_per ]
	  * M.CostInvest[l_tech, l_vin]
	  * M.LoanAnnualize[l_tech, l_vin]

	  for l_per in M.time_optimize
	  for l_tech in M.tech_all
	  for l_vin in ProcessVintages( l_per, l_tech )
	  if loanIsActive( l_per, l_tech, l_vin )
	  if (l_tech, l_vin) in l_invest_indices
	  if value(M.CostInvest[l_tech, l_vin])
	)

	l_fixed_costs = sum(
	    M.V_Capacity[l_tech, l_vin]
	  * M.CostFixed[l_per, l_tech, l_vin]
	  * M.PeriodRate[ l_per ]

	  for l_per in M.time_optimize
	  for l_tech in M.tech_all
	  for l_vin in ProcessVintages( l_per, l_tech )
	  if (l_per, l_tech, l_vin) in l_fixed_indices
	  if value(M.CostFixed[l_per, l_tech, l_vin])
	)

	l_marg_costs = sum(
	    M.V_Activity[l_per, l_season, l_time_of_day, l_tech, l_vin]
	  * M.PeriodRate[ l_per ]
	  * M.CostMarginal[l_per, l_tech, l_vin]

	  for l_per in M.time_optimize
	  for l_tech in M.tech_all
	  for l_vin in ProcessVintages( l_per, l_tech )
	  if (l_per, l_tech, l_vin) in l_marg_indices
	  if value(M.CostMarginal[l_per, l_tech, l_vin])
	  for l_season in M.time_season
	  for l_time_of_day in M.time_of_day
	)

	return (l_loan_costs + l_fixed_costs + l_marg_costs)
Objective_rule = TotalCost_rule

##############################################################################
#   Initializaton rules

def ParamPeriodLength_rule ( M, period ):
	periods = list( M.time_horizon )
	periods.extend( list(M.time_future) )

	i = periods.index( period )

	# The +1 won't fail, because this rule is called over time_optimize, which
	# lacks the last period in time_future.  In fact, this is the whole point of
	# having at least one period in time_future.
	l_length = periods[i +1] - periods[ i ]

	return l_length


def ParamPeriodRate_rule ( M, period ):
	l_rate_multiplier = sum(
	  (1 + M.GlobalDiscountRate) ** (M.time_optimize.first() - y - period)

	  for y in range(0, M.PeriodLength[ period ])
	)

	return value(l_rate_multiplier)


def ParamLifetimeFrac_rule ( M, A_period, A_tech, A_vintage ):
	l_eol_year = A_vintage + value(M.LifetimeTech[A_tech, A_vintage])

	for l_inp in ProcessInputs( A_period, A_tech, A_vintage ):
		for l_out in ProcessOutputsByInput( A_period, A_tech, A_vintage, l_inp ):
			# if an efficiency exists, that's it, we're done.  Calculate
			# the fraction and return it to Pyomo
			l_frac  = l_eol_year - A_period
			l_frac /= M.PeriodLength[ A_period ]
			return value(l_frac)


def ParamLoanAnnualize_rule ( M, A_tech, A_vintage ):
	l_process = (A_tech, A_vintage)
	l_annualized_rate = (
	    M.DiscountRate[ l_process ]
	  / (1 - (1 + M.DiscountRate[ l_process ])
	         **(- M.LifetimeLoan[ l_process ])
	    )
	)

	return l_annualized_rate

# End initialization rules
##############################################################################

##############################################################################
#   Constraint rules

def BaseloadDiurnalConstraint_rule (
  M, A_period, A_season, A_time_of_day, A_tech, A_vintage
):
	"""\
Ensure that certain (electric baseload) technologies maintain equivalent output at all times during a day.

The math behind this is more computer programmatic in fashion, than
mathematical.  It involves a minor algorithm that creates an ordering of the
time_of_day set, and uses that order such that

(for each d element of time_of_day)
Activity[p,s,d,t,v] == Activity[p,s,d-1,t,v]
"""
	# Question: How do I set the different times of day equal to each other?
	# This approach is the more programmatic one, but is there a simpler
	# mathematical approach?

	l_times = list( M.time_of_day )  # convert to Python list.  (Already
	  # appropriately sorted by the 'order=True' on the Set definition.)  This
	  # this is the commonality between invocations of this method, and how
	  # to find where in the "pecking order" A_time_of_day falls.

	index = l_times.index( A_time_of_day )
	if 0 == index:
		# When index is 0, it means that we've reached the beginning of the array
		# For the algorithm, this is a terminating condition: do not create
		# an effectively useless constraint
		return Constraint.Skip

	# for the rest of the time_of_days, set them equal to the one before.  i.e.
	# create a set of constraints that look something like:
	# tod[ 2 ] == tod[ 1 ]
	# tod[ 3 ] == tod[ 2 ]
	# tod[ 4 ] == tod[ 3 ]
	# and so on ...
	l_prev_time_of_day = l_times[ index -1 ]

	aindex_1 = (A_period, A_season, A_time_of_day, A_tech, A_vintage)
	aindex_2 = (A_period, A_season, l_prev_time_of_day, A_tech, A_vintage)

	expr = (M.V_Activity[ aindex_1 ] == M.V_Activity[ aindex_2 ])
	return expr


def EmissionConstraint_rule ( M, A_period, A_emission ):
	index = (A_period, A_emission)
	l_emissionlimit = M.EmissionLimit[ index ]

	l_eActivityIndices = M.EmissionActivity.keys()
	l_sum = sum(
	    M.V_FlowOut[A_period, l_season, l_tod, l_inp, l_tech, l_vin, l_out]
	  * M.EmissionActivity[A_emission, l_inp, l_tech, l_vin, l_out]

	  for l_emission, l_inp, l_tech, l_vin, l_out in M.EmissionActivity.keys()
	  if l_emission == A_emission
	  if ValidActivity( A_period, l_tech, l_vin )
	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	)

	if int is type( l_sum ):
		msg = ("Warning: No technology produces emission '%s', though limit was "
		  'specified as %s.\n')
		SE.write( msg % (A_emission, l_emissionlimit) )
		return Constraint.Skip

	expr = (l_sum <= l_emissionlimit)
	return expr


def MinCapacityConstraint_rule ( M, A_period, A_tech ):
	index = (A_period, A_tech)
	l_min = M.MinCapacity[ index ]
	expr = (M.V_CapacityAvailableByPeriodAndTech[ index ] >= l_min)
	return expr


def MaxCapacityConstraint_rule ( M, A_period, A_tech ):
	index = (A_period, A_tech)
	l_max = M.MaxCapacity[ index ]
	expr = (M.V_CapacityAvailableByPeriodAndTech[ index ] < l_max)
	return expr


def StorageConstraint_rule (
  M, A_period, A_season, A_inp, A_tech, A_vintage, A_out
):
	"""\
	Constraint rule documentation goes here ...
"""
	l_sum_in_out = sum(
	    M.V_FlowOut[A_period, A_season, l_tod, A_inp, A_tech, A_vintage, A_out]
	  - M.V_FlowIn[A_period, A_season, l_tod, A_inp, A_tech, A_vintage, A_out]
	  * M.Efficiency[A_inp, A_tech, A_vintage, A_out]

	  for l_tod in M.time_of_day
	)

	expr = ( l_sum_in_out == 0 )
	return expr


def TechOutputSplitConstraint_rule (
  M, A_period, A_season, A_time_of_day, A_input, A_tech, A_vintage, A_output
):
	split_indices = M.TechOutputSplit.keys()

	l_outputs = sorted(
	  l_out

	  for l_out in M.commodity_carrier
	  if (A_input, A_tech, l_out) in split_indices
	)

	l_index = l_outputs.index( A_output )
	if 0 == l_index:
		return Constraint.Skip

	l_prev = l_outputs[ l_index -1 ]
	l_prev_split = M.TechOutputSplit[A_input, A_tech, l_prev]
	l_split = M.TechOutputSplit[A_input, A_tech, A_output]

	expr = (
	    M.V_FlowOut[A_period, A_season, A_time_of_day, A_input, A_tech, A_vintage, A_output]
	  * l_split
	  ==
	    M.V_FlowOut[A_period, A_season, A_time_of_day, A_input, A_tech, A_vintage, l_prev]
	  * l_prev_split
	)
	return expr


def ActivityConstraint_rule (
  M, A_period, A_season, A_time_of_day, A_tech, A_vintage
):
	"""\
As V_Activity is a derived variable, the constraint sets V_Activity to the sum over input and output energy carriers of a process.

(for each period, season, time_of_day, tech, vintage)
V_Activity[p,s,d,t,v] = sum((inp,out), V_FlowOut[p,s,d,inp,t,v,out])
	"""
	pindex = (A_period, A_tech, A_vintage)
	aindex = (A_period, A_season, A_time_of_day, A_tech, A_vintage)

	l_activity = 0
	for l_inp in ProcessInputs( A_period, A_tech, A_vintage ):
		for l_out in ProcessOutputs( A_period, A_tech, A_vintage ):
			l_activity += M.V_FlowOut[A_period, A_season, A_time_of_day, l_inp, A_tech, A_vintage, l_out]

	expr = ( M.V_Activity[ aindex ] == l_activity )
	return expr


def CapacityLifetimeConstraint_rule ( M, A_period, A_com ):
	demand_indices = M.Demand.keys()

	if A_com in M.commodity_demand:
		l_period_demand = sum(
		  M.Demand[A_period, l_season, l_tod, A_com]

		  for l_season in M.time_season
		  for l_tod in M.time_of_day
		  if (A_period, l_season, l_tod, A_com) in demand_indices
		)
	elif A_com in M.commodity_physical:
		l_period_demand = sum(
		  M.V_FlowIn[A_period, l_season, l_tod, A_com, l_tech, l_vin, l_out]

		  for l_tech, l_vin in ProcessesByPeriodAndInput( A_period, A_com )
		  for l_out in ProcessOutputsByInput( A_period, l_tech, l_vin, A_com )
		  for l_season in M.time_season
		  for l_tod in M.time_of_day
		)

	if int is type( l_period_demand ) and l_period_demand == 0:
		# if there is no demand, then no need to create a constraint
		return Constraint.Skip

	l_frac_indices = M.LifetimeFrac.keys()

	l_non_dying_ability = sum(
	    M.V_Capacity[l_tech, l_vin]
	  * M.CapacityFactor[l_tech, l_vin]
	  * M.CapacityToActivity[l_tech]
	  * M.PeriodLength[ A_period ]

	  for l_tech, l_vin in ProcessesByPeriodAndOutput( A_period, A_com )
	  if (A_period, l_tech, l_vin) not in l_frac_indices
	)

	expr = (l_non_dying_ability >= l_period_demand)
	return expr


def CapacityFractionalLifetimeConstraint_rule (
  M, A_period, A_tech, A_vintage, A_com
):
	l_max_output = (
	    M.V_Capacity[A_tech, A_vintage]
	  * M.CapacityFactor[A_tech, A_vintage]
	  * M.CapacityToActivity[A_tech]
	  * M.LifetimeFrac[A_period, A_tech, A_vintage]
	  * M.PeriodLength[ A_period ]
	)

	l_output = sum(
	  M.V_FlowOut[A_period, l_season, l_tod, l_inp, A_tech, A_vintage, A_com]

	  for l_inp in ProcessInputsByOutput( A_period, A_tech, A_vintage, A_com )
	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	)

	expr = (l_output <= l_max_output)
	return expr


def CapacityConstraint_rule (
  M, A_period, A_season, A_time_of_day, A_tech, A_vintage
):
	"""\
V_Capacity is a derived variable; this constraint sets V_Capacity to at least be able to handle the activity in any optimization time slice.  In effect, this sets V_Capacity[p,t,v] to the max of the activity for similar indices: max(Activity[p,*,*t,v])

(for each period, season, time_of_day, tech, vintage)
V_Capacity[t,v] * CapacityFactor[t,v] >= V_Activity[p,s,d,t,v]
	"""
	pindex = (A_period, A_tech, A_vintage)   # "process" index

	l_vintage_activity = (
	  M.V_Activity[A_period, A_season, A_time_of_day, A_tech, A_vintage]
	)

	cindex = (A_tech, A_vintage)   # "capacity" index
	l_capacity = (
	    M.V_Capacity[ cindex ]
	  * M.CapacityFactor[ cindex ]
	  * M.SegFrac[A_season, A_time_of_day]
	  * M.CapacityToActivity[ A_tech ]
	)

	expr = ( l_vintage_activity <= l_capacity )
	return expr


def ExistingCapacityConstraint_rule ( M, A_tech, A_vintage ):
	"""\
For vintage periods (that the model is not to optimize), explicitly set the capacity values.

(for each tech, vintage_exist)
V_Capacity[t,v] = Param(Existingcapacity[t,v])
	"""
	index = (A_tech, A_vintage)
	ecapacity = M.ExistingCapacity[ index ]

	expr = ( M.V_Capacity[ index ] == ecapacity )
	return expr


def ResourceExtractionConstraint_rule ( M, A_period, A_resource ):
	"""\
Prevent TEMOA from extracting an endless supply of energy from "the ether".

(for each period, resource)
sum((season,time_of_day,tech,vintage),V_FlowIn[p,*,*,e,*,*,r]) <= Param(ResourceBound[p,r])
	"""
	index = (A_period, A_resource)
	max_resource = M.ResourceBound[ index ]

	l_extract = sum(
	  M.V_FlowIn[A_period, l_season, l_tod, l_inp, l_tech, l_vin, A_resource]

	  for l_tech, l_vin in ProcessesByPeriodAndOutput( A_period, A_resource )
	  for l_inp in ProcessInputsByOutput( A_period, l_tech, l_vin, A_resource )
	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	)

	expression = (l_extract <= max_resource)
	return expression


def CommodityBalanceConstraint_rule ( M, A_period, A_season, A_time_of_day, A_carrier ):
	"""\
Ensure that the FlowOut of a produced energy carrier at least meets the demand of the needed FlowIn of that energy carrier.  That is, this constraint maintains energy flows between processes.

(for each period, season, time_of_day, energy_carrier)
sum((inp,tech,vintage),V_FlowOut[p,s,t,*,*,*,c]) >= sum((tech,vintage,out),V_FlowIn[p,s,t,c,*,*,*])
sum((inp,tech,vintage),V_FlowOut[period,season,time_of_day,*,*,*,carrier]) >= sum((tech,vintage,out),V_FlowIn[period,season,time_of_day,carrier,*,*,*])
	"""
	if A_carrier in M.commodity_demand:
		return Constraint.Skip

	l_vflow_in = sum(
	  M.V_FlowIn[A_period, A_season, A_time_of_day, A_carrier, l_tech, l_vin, l_out]

	  for l_tech in M.tech_production
	  for l_vin in M.vintage_all
	  for l_out in ProcessOutputsByInput( A_period, l_tech, l_vin, A_carrier )
	)

	l_vflow_out = sum(
	  M.V_FlowOut[A_period, A_season, A_time_of_day, l_inp, l_tech, l_vin, A_carrier]

	  for l_tech in M.tech_all
	  for l_vin in M.vintage_all
	  for l_inp in ProcessInputsByOutput( A_period, l_tech, l_vin, A_carrier )
	)

	CommodityBalanceConstraintErrorCheck(
	  l_vflow_out, l_vflow_in, A_carrier, A_season, A_time_of_day, A_period
	)

	expression = (l_vflow_out >= l_vflow_in)
	return expression


def ProcessBalanceConstraint_rule (
  M, A_period, A_season, A_time_of_day, A_inp, A_tech, A_vintage, A_out
):
	"""\
Analogous to CommodityBalance, this constraint ensures that the amount of
energy leaving a process is not more than the amount entering it.

(for each period, season, time_of_day, inp_carrier, vintage, out_carrier)
V_FlowOut[p,s,d,t,v,o] <= V_FlowIn[p,s,d,t,v,o] * Efficiency[i,t,v,o]
	"""
	aindex = (A_period, A_season, A_time_of_day, A_inp, A_tech, A_vintage, A_out)

	expr = (
	    M.V_FlowOut[ aindex ]
	      <=
	    M.V_FlowIn[ aindex ]
	  * M.Efficiency[A_inp, A_tech, A_vintage, A_out]
	)

	return expr


def DemandCapacityConstraint_rule (
  M, A_period, A_season, A_time_of_day, A_comm
):
	"""\
"""

	l_capacity = sum(
	  M.V_Capacity[l_tech, l_vin]

	  for l_tech, l_vin in ProcessesByPeriodAndOutput( A_period, A_comm )
	)

	dindex = (A_period, A_season, A_time_of_day, A_comm)
	sindex = (A_season, A_time_of_day)

	expression = (l_capacity * M.SegFrac[ sindex ] >= M.Demand[ dindex ])
	return expression


def DemandConstraint_rule ( M, A_period, A_season, A_time_of_day, A_comm ):
	"""\
The driving constraint, this rule ensures that supply at least equals demand.

(for each period, season, time_of_day, commodity)
sum((inp,tech,vintage),V_FlowOut[p,s,d,*,*,*,commodity]) >= Demand[p,s,d,commodity]
	"""
	index = (A_period, A_season, A_time_of_day, A_comm)
	if not (M.Demand[ index ] > 0):
		# User must have supplied a 0 demand: no need to create a useless
		# constraint like X >= 0
		return Constraint.Skip

	l_supply = sum(
	  M.V_FlowOut[A_period, A_season, A_time_of_day, l_inp, l_tech, l_vin, A_comm]

	  for l_tech in M.tech_all
	  for l_vin in M.vintage_all
	  for l_inp in ProcessInputsByOutput( A_period, l_tech, l_vin, A_comm )
	)

	DemandConstraintErrorCheck (
	  l_supply, A_comm, A_period, A_season, A_time_of_day
	)

	expression = (l_supply >= M.Demand[ index ])
	return expression

# End constraint rules
##############################################################################

##############################################################################
# Additional and derived (informational) variable constraints

def ActivityByPeriodTechConstraint_rule ( M, A_per, A_tech ):
	l_sum = sum(
	  M.V_Activity[A_per, l_season, l_tod, A_tech, l_vin]

	  for l_vin in ProcessVintages( A_per, A_tech )
	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	)

	if int is type( l_sum ):
		return Constraint.Skip

	expr = (M.V_ActivityByPeriodAndTech[A_per, A_tech] == l_sum)
	return expr


def ActivityByPeriodTechAndVintageConstraint_rule ( M, A_per, A_tech, A_vin ):
	if A_per < A_vin or A_vin not in ProcessVintages( A_per, A_tech ):
		return Constraint.Skip

	l_sum = sum(
	  M.V_Activity[A_per, l_season, l_tod, A_tech, A_vin]

	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	)

	if int is type( l_sum ):
		return Constraint.Skip

	expr = (M.V_ActivityByPeriodTechAndVintage[A_per, A_tech, A_vin] == l_sum)
	return expr


def ActivityByPeriodTechAndOutputConstraint_rule ( M, A_period, A_tech, A_output ):
	l_sum = sum(
	  M.V_FlowOut[A_period, l_season, l_tod, l_inp, A_tech, l_vin, A_output]

	  for l_vin in ProcessVintages( A_period, A_tech )
	  for l_inp in ProcessInputsByOutput( A_period, A_tech, l_vin, A_output )
	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	)

	if int is type( l_sum ):
		return Constraint.Skip

	index = (A_period, A_tech, A_output)
	expr = (M.V_ActivityByPeriodTechAndOutput[ index ] == l_sum)
	return expr


def ActivityByPeriodTechVintageAndOutputConstraint_rule (
  M, A_period, A_tech, A_vintage, A_output
):
	l_sum = sum(
	  M.V_FlowOut[A_period, l_season, l_tod, l_inp, A_tech, A_vintage, A_output]

	  for l_inp in ProcessInputsByOutput( A_period, A_tech, A_vintage, A_output )
	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	)

	if int is type( l_sum ):
		return Constraint.Skip

	index = (A_period, A_tech, A_vintage, A_output)
	expr = (M.V_ActivityByPeriodTechVintageAndOutput[ index ] == l_sum)
	return expr

def ActivityByTechAndOutputConstraint_rule ( M, A_tech, A_output ):
	l_sum = sum(
	  M.V_FlowOut[l_per, l_season, l_tod, l_inp, A_tech, l_vin, A_output]

	  for l_per in M.time_optimize
	  for l_vin in ProcessVintages( l_per, A_tech )
	  for l_inp in ProcessInputsByOutput( l_per, A_tech, l_vin, A_output )
	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	)

	if int is type( l_sum ):
		return Constraint.Skip

	index = (A_tech, A_output)
	expr = (M.V_ActivityByTechAndOutput[ index ] == l_sum)
	return expr


def ActivityByInputAndTechConstraint_rule ( M, A_input, A_tech ):
	l_sum = sum(
	  M.V_FlowOut[l_per, l_season, l_tod, A_input, A_tech, l_vin, l_out]

	  for l_per in M.time_optimize
	  for l_vin in ProcessVintages( l_per, A_tech )
	  for l_out in ProcessOutputsByInput( l_per, A_tech, l_vin, A_input )
	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	)

	if int is type( l_sum ):
		return Constraint.Skip

	index = (A_input, A_tech)
	expr = (M.V_ActivityByInputAndTech[ index ] == l_sum)
	return expr


def ActivityByPeriodInputAndTechConstraint_rule (
  M, A_period, A_input, A_tech
):
	l_sum = sum(
	  M.V_FlowIn[A_period, l_season, l_tod, A_input, A_tech, l_vin, l_out]

	  for l_vin in ProcessVintages( A_period, A_tech )
	  for l_out in ProcessOutputsByInput( A_period, A_tech, l_vin, A_input )
	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	)

	if int is type( l_sum ):
		return Constraint.Skip

	index = (A_period, A_input, A_tech)
	expr = (M.V_ActivityByPeriodInputAndTech[ index ] == l_sum)
	return expr


def ActivityByPeriodInputTechAndVintageConstraint_rule (
  M, A_period, A_input, A_tech, A_vintage
):
	l_sum = sum(
	  M.V_FlowIn[A_period, l_season, l_tod, A_input, A_tech, A_vintage, l_out]

	  for l_out in ProcessOutputsByInput( A_period, A_tech, A_vintage, A_input )
	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	)

	if int is type( l_sum ):
		return Constraint.Skip

	index = (A_period, A_input, A_tech, A_vintage)
	expr = (M.V_ActivityByPeriodInputTechAndVintage[ index ] == l_sum)
	return expr



def CapacityAvailableByPeriodAndTechConstraint_rule ( M, A_per, A_tech ):
	l_sum = sum(
	  M.V_Capacity[A_tech, l_vin]

	  for l_vin in ProcessVintages( A_per, A_tech )
	)

	expr = (M.V_CapacityAvailableByPeriodAndTech[A_per, A_tech] == l_sum)
	return expr


def InvestmentByTechConstraint_rule ( M, A_tech ):
	l_sum = sum(
	    M.V_Capacity[A_tech, l_vin]
	  * value( M.CostInvest[A_tech, l_vin] )

	  for l_tech, l_vin in M.CostInvest.keys()
	  if l_tech == A_tech
	)

	if int is type( l_sum ):
		return Constraint.Skip

	expr = ( M.V_InvestmentByTech[ A_tech ] == l_sum)
	return expr


def InvestmentByTechAndVintageConstraint_rule ( M, A_tech, A_vin ):
	index = (A_tech, A_vin)

	if index in M.CostInvest.keys():
		l_cost = M.V_Capacity[ index ] * value(M.CostInvest[ index ])
	else:
		return Constraint.Skip

	expr = ( M.V_InvestmentByTechAndVintage[ index ] == l_cost)
	return expr


def EmissionActivityTotalConstraint_rule ( M, A_emission ):
	l_sum = sum(
	    M.V_FlowOut[l_per, l_season, l_tod, l_inp, l_tech, l_vin, l_out]
	  * M.EmissionActivity[A_emission, l_inp, l_tech, l_vin, l_out]

	  for l_emission, l_inp, l_tech, l_vin, l_out in M.EmissionActivity.keys()
	  if l_emission == A_emission
	  for l_per in M.time_optimize
	  if ValidActivity( l_per, l_tech, l_vin )
	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	)

	if type( l_sum ) is int:
		return Constraint.Skip

	expr = (M.V_EmissionActivityTotal[ A_emission ] == l_sum)
	return expr


def EmissionActivityByPeriodConstraint_rule ( M, A_emission, A_period ):
	l_sum = sum(
	    M.V_FlowOut[A_period, l_season, l_tod, l_inp, l_tech, l_vin, l_out]
	  * M.EmissionActivity[A_emission, l_inp, l_tech, l_vin, l_out]

	  for l_emission, l_inp, l_tech, l_vin, l_out in M.EmissionActivity.keys()
	  if l_emission == A_emission
	  if ValidActivity( A_period, l_tech, l_vin )
	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	)

	if type( l_sum ) is int:
		return Constraint.Skip

	expr = (M.V_EmissionActivityByPeriod[A_emission, A_period] == l_sum)
	return expr


def EmissionActivityByTechConstraint_rule ( M, A_emission, A_tech ):
	l_sum = sum(
	    M.V_FlowOut[l_per, l_season, l_tod, l_inp, A_tech, l_vin, l_out]
	  * M.EmissionActivity[A_emission, l_inp, A_tech, l_vin, l_out]

	  for l_emission, l_inp, l_tech, l_vin, l_out in M.EmissionActivity.keys()
	  if l_emission == A_emission and l_tech == A_tech
	  for l_per in M.time_optimize
	  if ValidActivity( l_per, l_tech, l_vin )
	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	)

	if type( l_sum ) is int:
		return Constraint.Skip

	expr = (M.V_EmissionActivityByTech[A_emission, A_tech] == l_sum)
	return expr


def EmissionActivityByPeriodAndTechConstraint_rule (
  M, A_emission, A_period, A_tech
):
	l_sum = sum(
	    M.V_FlowOut[A_period, l_season, l_tod, l_inp, A_tech, l_vin, l_out]
	  * M.EmissionActivity[A_emission, l_inp, A_tech, l_vin, l_out]

	  for l_emission, l_inp, l_tech, l_vin, l_out in M.EmissionActivity.keys()
	  if l_emission == A_emission and l_tech == A_tech
	  if ValidActivity( A_period, l_tech, l_vin )
	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	)

	if type( l_sum ) is int:
		return Constraint.Skip

	index = (A_emission, A_period, A_tech)
	expr = (M.V_EmissionActivityByPeriodAndTech[ index ] == l_sum)
	return expr


def EmissionActivityByTechAndVintageConstraint_rule (
  M, A_emission, A_tech, A_vintage
):
	l_sum = sum(
	    M.V_FlowOut[l_per, l_season, l_tod, l_inp, A_tech, A_vintage, l_out]
	  * M.EmissionActivity[A_emission, l_inp, A_tech, A_vintage, l_out]

	  for l_emission, l_inp, l_tech, l_vin, l_out in M.EmissionActivity.keys()
	  if l_emission == A_emission and l_tech == A_tech and l_vin == A_vintage
	  for l_per in M.time_optimize
	  if ValidActivity( l_per, l_tech, l_vin )
	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	)

	if type( l_sum ) is int:
		return Constraint.Skip

	index = (A_emission, A_tech, A_vintage)
	expr = (M.V_EmissionActivityByTechAndVintage[ index ] == l_sum)
	return expr


def EnergyConsumptionByTechConstraint_rule ( M, A_tech ):
	l_sum = sum(
	  M.V_FlowIn[l_per, l_season, l_tod, l_inp, A_tech, l_vin, l_out]

	  for l_per in M.time_optimize
	  for l_vin in ProcessVintages( l_per, A_tech )
	  for l_inp in ProcessInputs( l_per, A_tech, l_vin )
	  for l_out in ProcessOutputsByInput( l_per, A_tech, l_vin, l_inp )
	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	)

	expr = (M.V_EnergyConsumptionByTech[ A_tech ] == l_sum)
	return expr


def EnergyConsumptionByTechAndOutputConstraint_rule ( M, A_tech, A_out ):
	l_sum = sum(
	  M.V_FlowIn[l_per, l_season, l_tod, l_inp, A_tech, l_vin, A_out]

	  for l_per in M.time_optimize
	  for l_vin in ProcessVintages( l_per, A_tech )
	  for l_inp in ProcessInputsByOutput( l_per, A_tech, l_vin, A_out )
	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	)

	expr = (M.V_EnergyConsumptionByTechAndOutput[A_tech, A_out] == l_sum)
	return expr

def EnergyConsumptionByPeriodAndTechConstraint_rule ( M, A_period, A_tech ):
	l_sum = sum(
	  M.V_FlowIn[A_period, l_season, l_tod, l_inp, A_tech, l_vin, l_out]

	  for l_vin in ProcessVintages( A_period, A_tech )
	  for l_inp in ProcessInputs( A_period, A_tech, l_vin )
	  for l_out in ProcessOutputsByInput( A_period, A_tech, l_vin, l_inp )
	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	)

	expr = (M.V_EnergyConsumptionByPeriodAndTech[A_period, A_tech] == l_sum)
	return expr


def EnergyConsumptionByPeriodInputAndTechConstraint_rule (
  M, A_period, A_inp, A_tech
):
	l_sum = sum(
	  M.V_FlowIn[A_period, l_season, l_tod, A_inp, A_tech, l_vin, l_out]

	  for l_vin in ProcessVintages( A_period, A_tech )
	  for l_out in ProcessOutputsByInput( A_period, A_tech, l_vin, A_inp )
	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	)

	index = (A_period, A_inp, A_tech)
	expr = (M.V_EnergyConsumptionByPeriodInputAndTech[ index ] == l_sum)
	return expr


def EnergyConsumptionByPeriodTechAndOutputConstraint_rule (
  M, A_period, A_tech, A_out
):
	l_sum = sum(
	  M.V_FlowIn[A_period, l_season, l_tod, l_inp, A_tech, l_vin, A_out]

	  for l_vin in ProcessVintages( A_period, A_tech )
	  for l_inp in ProcessInputsByOutput( A_period, A_tech, l_vin, A_out )
	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	)

	index = (A_period, A_tech, A_out)
	expr = (M.V_EnergyConsumptionByPeriodTechAndOutput[ index ] == l_sum)
	return expr


def EnergyConsumptionByPeriodTechAndVintageConstraint_rule (
  M, A_period, A_tech, A_vintage
):
	l_sum = sum(
	  M.V_FlowIn[A_period, l_season, l_tod, l_inp, A_tech, A_vintage, l_out]

	  for l_inp in ProcessInputs( A_period, A_tech, A_vintage )
	  for l_out in ProcessOutputsByInput( A_period, A_tech, A_vintage, l_inp )
	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	)

	index = (A_period, A_tech, A_vintage)
	expr = (M.V_EnergyConsumptionByPeriodTechAndVintage[ index ] == l_sum)
	return expr

# End additional and derived (informational) variable constraints
##############################################################################

# End *_rule definitions
##############################################################################

##############################################################################
# Miscellaneous related functions

def AddReportingVariables ( M ):
	# Additional and derived variables, mainly for reporting purposes.  As
	# these are basically used to export information for modeler consumption,
	# these could be taken out of here and put in a post-processing step.  This
	# is in fact what we'll likely want to do as we grow because Coopr remains
	# fairly inefficient, and each Variable represents a fair chunk of memory,
	# among other resources.  Luckily, all told, these are cheap, compared
	# to the computational cost of the other constraints.
	M.ActivityByPeriodTechAndVintageVarIndices = Set(
	  dimen=3, rule=ActivityByPeriodTechAndVintageVarIndices )
	M.ActivityByPeriodTechAndOutputVarIndices = Set(
	  dimen=3, rule=ActivityByPeriodTechAndOutputVariableIndices )
	M.ActivityByPeriodTechVintageAndOutputVarIndices = Set(
	  dimen=4, rule=ActivityByPeriodTechVintageAndOutputVariableIndices )

	M.ActivityByTechAndOutputVarIndices = Set(
	  dimen=2, rule=ActivityByTechAndOutputVariableIndices )
	M.ActivityByInputAndTechVarIndices = Set(
	  dimen=2, rule=ActivityByInputAndTechVariableIndices )

	M.ActivityByPeriodInputAndTechVarIndices = Set(
	  dimen=3, rule=ActivityByPeriodInputAndTechVariableIndices )
	M.ActivityByPeriodInputTechAndVintageVarIndices = Set(
	  dimen=4, rule=ActivityByPeriodInputTechAndVintageVariableIndices )

	M.EmissionActivityByTechVarIndices = Set(
	  dimen=2, rule=EmissionActivityByTechVariableIndices )
	M.EmissionActivityByPeriodAndTechVarIndices = Set(
	  dimen=3, rule=EmissionActivityByPeriodAndTechVariableIndices )
	M.EmissionActivityByTechAndVintageVarIndices = Set(
	  dimen=3, rule=EmissionActivityByTechAndVintageVariableIndices )

	M.EnergyConsumptionByTechAndOutputVarIndices = Set(
	  dimen=2, rule=EnergyConsumptionByTechAndOutputVariableIndices )
	M.EnergyConsumptionByPeriodAndTechVarIndices = Set(
	  dimen=2, rule=EnergyConsumptionByPeriodAndTechVariableIndices )
	M.EnergyConsumptionByPeriodInputAndTechVarIndices = Set(
	  dimen=3, rule=EnergyConsumptionByPeriodInputAndTechVariableIndices )
	M.EnergyConsumptionByPeriodTechAndOutputVarIndices = Set(
	  dimen=3, rule=EnergyConsumptionByPeriodTechAndOutputVariableIndices )
	M.EnergyConsumptionByPeriodTechAndVintageVarIndices = Set(
	  dimen=3, rule=EnergyConsumptionByPeriodTechAndVintageVariableIndices )

	M.V_ActivityByPeriodAndTech              = Var( M.time_optimize, M.tech_all,                      domain=NonNegativeReals )
	M.V_ActivityByPeriodTechAndVintage       = Var( M.ActivityByPeriodTechAndVintageVarIndices,       domain=NonNegativeReals )
	M.V_ActivityByPeriodTechAndOutput        = Var( M.ActivityByPeriodTechAndOutputVarIndices,        domain=NonNegativeReals )
	M.V_ActivityByPeriodTechVintageAndOutput = Var( M.ActivityByPeriodTechVintageAndOutputVarIndices, domain=NonNegativeReals )

	M.V_ActivityByTechAndOutput = Var( M.ActivityByTechAndOutputVarIndices, domain=NonNegativeReals )
	M.V_ActivityByInputAndTech  = Var( M.ActivityByInputAndTechVarIndices,  domain=NonNegativeReals )

	M.V_ActivityByPeriodInputAndTech        = Var( M.ActivityByPeriodInputAndTechVarIndices,        domain=NonNegativeReals )
	M.V_ActivityByPeriodInputTechAndVintage = Var( M.ActivityByPeriodInputTechAndVintageVarIndices, domain=NonNegativeReals )

	M.V_InvestmentByTech           = Var( M.tech_all,                     domain=NonNegativeReals )
	M.V_InvestmentByTechAndVintage = Var( M.tech_all, M.vintage_optimize, domain=NonNegativeReals )

	M.V_EmissionActivityTotal            = Var( M.commodity_emissions,                        domain=Reals )
	M.V_EmissionActivityByPeriod         = Var( M.commodity_emissions, M.time_optimize,       domain=Reals )
	M.V_EmissionActivityByTech           = Var( M.EmissionActivityByTechVarIndices,           domain=Reals )
	M.V_EmissionActivityByPeriodAndTech  = Var( M.EmissionActivityByPeriodAndTechVarIndices,  domain=Reals )
	M.V_EmissionActivityByTechAndVintage = Var( M.EmissionActivityByTechAndVintageVarIndices, domain=Reals )

	M.V_EnergyConsumptionByTech                 = Var( M.tech_all, domain=NonNegativeReals )
	M.V_EnergyConsumptionByTechAndOutput        = Var( M.EnergyConsumptionByTechAndOutputVarIndices, domain=NonNegativeReals )
	M.V_EnergyConsumptionByPeriodAndTech        = Var( M.EnergyConsumptionByPeriodAndTechVarIndices, domain=NonNegativeReals )
	M.V_EnergyConsumptionByPeriodInputAndTech   = Var( M.EnergyConsumptionByPeriodInputAndTechVarIndices, domain=NonNegativeReals )
	M.V_EnergyConsumptionByPeriodTechAndOutput  = Var( M.EnergyConsumptionByPeriodTechAndOutputVarIndices, domain=NonNegativeReals )
	M.V_EnergyConsumptionByPeriodTechAndVintage = Var( M.EnergyConsumptionByPeriodTechAndVintageVarIndices, domain=NonNegativeReals )

	#   The requisite constraints to set the derived variables above.

	M.ActivityByPeriodTechConstraint                 = Constraint( M.time_optimize, M.tech_all,                      rule=ActivityByPeriodTechConstraint_rule )
	M.ActivityByPeriodTechAndVintageConstraint       = Constraint( M.ActivityByPeriodTechAndVintageVarIndices,       rule=ActivityByPeriodTechAndVintageConstraint_rule )
	M.ActivityByPeriodTechAndOutputConstraint        = Constraint( M.ActivityByPeriodTechAndOutputVarIndices,        rule=ActivityByPeriodTechAndOutputConstraint_rule )
	M.ActivityByPeriodTechVintageAndOutputConstraint = Constraint( M.ActivityByPeriodTechVintageAndOutputVarIndices, rule=ActivityByPeriodTechVintageAndOutputConstraint_rule )

	M.ActivityByTechAndOutputConstraint = Constraint( M.ActivityByTechAndOutputVarIndices, rule=ActivityByTechAndOutputConstraint_rule )
	M.ActivityByInputAndTechConstraint  = Constraint( M.ActivityByInputAndTechVarIndices,  rule=ActivityByInputAndTechConstraint_rule )

	M.ActivityByPeriodInputAndTechConstraint        = Constraint( M.ActivityByPeriodInputAndTechVarIndices,        rule=ActivityByPeriodInputAndTechConstraint_rule )
	M.ActivityByPeriodInputTechAndVintageConstraint = Constraint( M.ActivityByPeriodInputTechAndVintageVarIndices, rule=ActivityByPeriodInputTechAndVintageConstraint_rule )

	M.InvestmentByTechConstraint           = Constraint( M.tech_all, rule=InvestmentByTechConstraint_rule )
	M.InvestmentByTechAndVintageConstraint = Constraint( M.tech_all, M.vintage_optimize, rule=InvestmentByTechAndVintageConstraint_rule )

	M.EmissionActivityTotalConstraint            = Constraint( M.commodity_emissions, rule=EmissionActivityTotalConstraint_rule )
	M.EmissionActivityByPeriodConstraint         = Constraint( M.commodity_emissions, M.time_optimize, rule=EmissionActivityByPeriodConstraint_rule )
	M.EmissionActivityByTechConstraint           = Constraint( M.EmissionActivityByTechVarIndices, rule=EmissionActivityByTechConstraint_rule )
	M.EmissionActivityByPeriodAndTechConstraint  = Constraint( M.EmissionActivityByPeriodAndTechVarIndices, rule=EmissionActivityByPeriodAndTechConstraint_rule )
	M.EmissionActivityByTechAndVintageConstraint = Constraint( M.EmissionActivityByTechAndVintageVarIndices, rule=EmissionActivityByTechAndVintageConstraint_rule )

	M.EnergyConsumptionByTechConstraint                 = Constraint( M.tech_all, rule=EnergyConsumptionByTechConstraint_rule )
	M.EnergyConsumptionByTechAndOutputConstraint        = Constraint( M.EnergyConsumptionByTechAndOutputVarIndices, rule=EnergyConsumptionByTechAndOutputConstraint_rule )
	M.EnergyConsumptionByPeriodAndTechConstraint        = Constraint( M.EnergyConsumptionByPeriodAndTechVarIndices, rule=EnergyConsumptionByPeriodAndTechConstraint_rule )
	M.EnergyConsumptionByPeriodInputAndTechConstraint   = Constraint( M.EnergyConsumptionByPeriodInputAndTechVarIndices, rule=EnergyConsumptionByPeriodInputAndTechConstraint_rule )
	M.EnergyConsumptionByPeriodTechAndOutputConstraint  = Constraint( M.EnergyConsumptionByPeriodTechAndOutputVarIndices, rule=EnergyConsumptionByPeriodTechAndOutputConstraint_rule )
	M.EnergyConsumptionByPeriodTechAndVintageConstraint = Constraint( M.EnergyConsumptionByPeriodTechAndVintageVarIndices, rule=EnergyConsumptionByPeriodTechAndVintageConstraint_rule )

# End miscellaneous related functions
##############################################################################
