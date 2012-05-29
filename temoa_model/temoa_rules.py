from temoa_lib import *

##############################################################################
# Begin *_rule definitions

def TotalCost_rule ( M ):
	"""\
Objective function.

This implementation of the Temoa objective function sums up all the costs
incurred in solving the system (supply energy to meet demands).

Simplistically, it is C_tot = C_loans + C_fixed + C_marginal.

Each part, in essence, is merely a summation of the costs incurred multiplied by
the time-value of money to bring it back to year 0.
"""
	partial_period_loan_indices = M.LoanLifeFrac.keys()
	partial_period_tech_indices = M.TechLifeFrac.keys()
	P_0 = M.time_optimize.first()

	loan_costs = sum(
	    M.V_CapacityInvest[S_t, S_v]
	  * value(
	      M.PeriodRate[ S_p ].value
	    * M.CostInvest[S_t, S_v].value
	    * M.LoanAnnualize[S_t, S_v].value
	  )

	  for S_t, S_v in M.CostInvest.keys()
	  for S_p in M.time_optimize
	  if (S_p, S_t, S_v) not in partial_period_loan_indices
	  if loanIsActive( S_p, S_t, S_v )
	) + sum(
	    M.V_CapacityInvest[S_t, S_v]
	  * M.CostInvest[S_t, S_v].value
	  * M.LoanAnnualize[S_t, S_v].value
	  * sum(
	      (1 + M.GlobalDiscountRate) ** (P_0 - S_p - y)
	      for y in range( 0, M.PeriodLength[ S_p ] * M.LoanLifeFrac[S_p, S_t, S_v])
	    )

	  for S_p, S_t, S_v in partial_period_loan_indices
	)

	fixed_costs = sum(
	    M.V_CapacityFixed[S_t, S_v]
	  * value(
	      M.CostFixed[S_p, S_t, S_v].value
	    * M.PeriodRate[ S_p ].value
	  )

	  for S_p, S_t, S_v in M.CostFixed.keys()
	  if (S_p, S_t, S_v) not in partial_period_tech_indices
	) + sum(
	    M.V_CapacityFixed[S_t, S_v]
	  * M.CostFixed[S_p, S_t, S_v].value
	  * sum(
	      (1 + M.GlobalDiscountRate) ** (P_0 - S_p - y)
	      for y in range( 0, M.PeriodLength[ S_p ] * M.TechLifeFrac[S_p, S_t, S_v])
	    )

	  for S_p, S_t, S_v in partial_period_tech_indices
	  if (S_p, S_t, S_v) in M.CostFixed.keys()
	)

	marg_costs = sum(
	    M.V_ActivityByPeriodTechAndVintage[S_p, S_t, S_v]
	  * value(
	      M.CostMarginal[S_p, S_t, S_v].value
	    * M.PeriodRate[ S_p ].value
	  )

	  for S_p, S_t, S_v in M.CostMarginal.keys()
	)

	return (loan_costs + fixed_costs + marg_costs)
Objective_rule = TotalCost_rule

##############################################################################
#   Initializaton rules

def ParamPeriodLength_rule ( M, p ):
	# This specifically does not use time_optimize because this function is
	# called /over/ time_optimize.
	periods = sorted( M.time_horizon )
	periods.extend( sorted(M.time_future) )

	i = periods.index( p )

	# The +1 won't fail, because this rule is called over time_optimize, which
	# lacks the last period in time_future.  In fact, this is the whole point of
	# having at least one period in time_future.
	length = periods[i +1] - periods[ i ]

	return length


def ParamPeriodRate_rule ( M, p ):
	"""\
The "Period Rate" is a multiplier against the costs incurred within a period to
bring the time-value back to the base year.  The parameter PeriodRate is not
directly specified by the modeler, but is a convenience calculation based on the
GlobalDiscountRate and the length of each period.  One may refer to this
(pseudo) parameter via M.PeriodRate[ a_period ]
"""
	rate_multiplier = sum(
	  (1 + M.GlobalDiscountRate) ** (M.time_optimize.first() - p - y)

	  for y in range(0, M.PeriodLength[ p ])
	)

	return value(rate_multiplier)


def ParamLoanLifeFraction_rule ( M, p, t, v ):
	"""\
For any technology investment loan that will end between periods (as opposed to
on a period boundary), calculate the fraction of the final period that loan
payments must still be made.

This function relies on being called only with ('period', 'tech', 'vintage')
combinations of processes that will end in 'period'.
"""
	eol_year = v + value(M.LifetimeLoan[t, v])

	  # number of years into final period loan is complete
	frac = eol_year - p

	frac /= M.PeriodLength[ p ]
	return value( frac )


def ParamTechLifeFraction_rule ( M, p, t, v ):
	"""\
For any technology that will cease operation (rust out, be decommissioned, etc.)
between periods (as opposed to on a period boundary), calculate the fraction of
the final period that the technology is still able to create useful output.

This function must be called only with ('period', 'tech', 'vintage')
combinations of processes that will end in 'period'.
"""
	eol_year = v + value(M.LifetimeTech[t, v])

	  # number of years into final period loan is complete
	frac  = eol_year - p
	frac /= M.PeriodLength[ p ]
	return value(frac)


def ParamLoanAnnualize_rule ( M, t, v ):
	process = (t, v)
	annualized_rate = (
	    M.DiscountRate[ process ]
	  / (1 - (1 + M.DiscountRate[ process ])
	         **(- M.LifetimeLoan[ process ])
	    )
	)

	return value(annualized_rate)

# End initialization rules
##############################################################################

##############################################################################
#   Constraint rules

def BaseloadDiurnalConstraint_rule ( M, p, s, d, t, v ):
	"""\
Ensure that certain (electric baseload) technologies maintain equivalent output
at all times during a day.

The math behind this is more computer programmatic in fashion, than
mathematical.  It involves a minor algorithm that creates an ordering of the
time_of_day set, and uses that order such that

(for each d element of time_of_day)
Activity[p,s,d,t,v] == Activity[p,s,d-1,t,v]
"""
	# Question: How to set the different times of day equal to each other?

	# Step 1: Acquire a "canonical" representation of the times of day
	l_times = list( M.time_of_day )  # i.e. a Python list.
	  # This is the commonality between invocations of this method.

	index = l_times.index( d )
	if 0 == index:
		# When index is 0, it means that we've reached the beginning of the array
		# For the algorithm, this is a terminating condition: do not create
		# an effectively useless constraint
		return Constraint.Skip

	# Step 2: Set the rest of the times of day equal in output to the first.
	# i.e. create a set of constraints that look something like:
	# tod[ 2 ] == tod[ 1 ]
	# tod[ 3 ] == tod[ 1 ]
	# tod[ 4 ] == tod[ 1 ]
	# and so on ...
	d_0 = l_times[ 0 ]

	# Step 3: the actual expression.  For baseload, must compute the /average/
	# activity over the segment.  By definition, average is
	#     (segment activity) / (segment length)
	# So:   (ActA / SegA) == (ActB / SegB)
	#   computationally, however, multiplication is cheaper than division, so:
	#       (ActA * SegB) == (ActB * SegA)
	expr = (
	    M.V_Activity[p, s, d, t, v]   * M.SegFrac[s, d_0]
	 ==
	    M.V_Activity[p, s, d_0, t, v] * M.SegFrac[s, d]
	)
	return expr


def EmissionConstraint_rule ( M, p, e ):
	emission_limit = M.EmissionLimit[p, e].value

	actual_emissions = sum(
	    M.V_FlowOut[p, S_s, S_d, S_i, S_t, S_v, S_o]
	  * M.EmissionActivity[e, S_i, S_t, S_v, S_o]

	  for emission, S_i, S_t, S_v, S_o in M.EmissionActivity.keys()
	  if emission == e
	  if ValidActivity( p, S_t, S_v )
	  for S_s in M.time_season
	  for S_d in M.time_of_day
	)

	if int is type( actual_emissions ):
		msg = ("Warning: No technology produces emission '%s', though limit was "
		  'specified as %s.\n')
		SE.write( msg % (e, emission_limit) )
		return Constraint.Skip

	expr = (actual_emissions <= emission_limit)
	return expr


def MinCapacityConstraint_rule ( M, p, t ):
	min_cap = M.MinCapacity[p, t]
	expr = (M.V_CapacityAvailableByPeriodAndTech[p, t] >= min_cap)
	return expr


def MaxCapacityConstraint_rule ( M, p, t ):
	max_cap = M.MaxCapacity[p, t]
	expr = (M.V_CapacityAvailableByPeriodAndTech[p, t] <= max_cap)
	return expr


def StorageConstraint_rule ( M, p, s, i, t, v, o ):
	"""\
The idea behind the Temoa storage implementation is that, on average, the amount
of energy into a storage unit (less an efficiency) is the same as the energy
coming out of it.  The "on average" is taken to be over the course of a season.
"""
	total_out_in = sum(
	    M.V_FlowOut[p, s, S_d, i, t, v, o]
	  - M.Efficiency[i, t, v, o]
	  * M.V_FlowIn[p, s, S_d, i, t, v, o]

	  for S_d in M.time_of_day
	)

	expr = ( total_out_in == 0 )
	return expr


def TechOutputSplitConstraint_rule ( M, p, s, d, i, t, v, o ):
	split_indices = M.TechOutputSplit.keys()

	outputs = sorted(
	  output

	  for output in M.commodity_carrier
	  if (i, t, output) in split_indices
	)

	index = outputs.index( o )
	if 0 == index:
		return Constraint.Skip

	prev = outputs[ index -1 ]
	prev_split = M.TechOutputSplit[i, t, prev]
	split = M.TechOutputSplit[i, t, o]

	expr = (
	    M.V_FlowOut[p, s, d, i, t, v, o]
	  * split
	  ==
	    M.V_FlowOut[p, s, d, i, t, v, prev]
	  * prev_split
	)
	return expr


def ActivityConstraint_rule ( M, p, s, d, t, v ):
	"""\
This constraint defines the convenience variable V_Activity as the sum of all
outputs of a process.  If there is more than one output, there is currently no
attempt to convert to a common unit of measurement.  (Unfortunately, this tedium
is currently left as an implicit accounting exercise for the modeler.)
"""
	activity = sum(
	  M.V_FlowOut[p, s, d, S_i, t, v, S_o]

	  for S_i in ProcessInputs( p, t, v )
	  for S_o in ProcessOutputsByInput( p, t, v, S_i )
	)

	expr = ( M.V_Activity[p, s, d, t, v] == activity )
	return expr


def CapacityLifetimeConstraint_rule ( M, A_period, A_season, A_tod, A_com ):
	demand_indices = M.Demand.keys()

	if A_com in M.commodity_demand:
		if (A_period, A_season, A_tod, A_com) not in demand_indices:
			return Constraint.Skip

		l_slice_demand = M.Demand[A_period, A_season, A_tod, A_com]
	elif A_com in M.commodity_physical:
		l_slice_demand = sum(
		  M.V_FlowIn[A_period, A_season, A_tod, A_com, l_tech, l_vin, l_out]

		  for l_tech, l_vin in ProcessesByPeriodAndInput( A_period, A_com )
		  for l_out in ProcessOutputsByInput( A_period, l_tech, l_vin, A_com )
		)

	if int is type( l_slice_demand ) and l_slice_demand == 0:
		# if there is no demand, then no need to create a constraint
		return Constraint.Skip

	l_frac_indices = M.TechLifeFrac.keys()

	l_non_dying_ability = sum(
	    M.V_Capacity[l_tech, l_vin]
	  * M.CapacityFactor[l_tech, l_vin]
	  * M.CapacityToActivity[l_tech]
	  * M.SegFrac[A_season, A_tod]

	  for l_tech, l_vin in ProcessesByPeriodAndOutput( A_period, A_com )
	  if (A_period, l_tech, l_vin) not in l_frac_indices
	)

	expr = (l_non_dying_ability >= l_slice_demand)
	return expr


def MARKAL_No_SegFrac_CapacityLifetimeConstraint_rule (
  M, A_period, A_com
):
	demand_indices = M.Demand.keys()

	if A_com in M.commodity_demand:
		l_demand = sum(
		  M.Demand[A_period, l_season, l_tod, A_com]

		  for l_per, l_season, l_tod, l_com in M.Demand.keys()
		  if l_per == A_period and l_com == A_com
		)
	elif A_com in M.commodity_physical:
		l_demand = sum(
		  M.V_FlowIn[A_period, l_season, l_tod, A_com, l_tech, l_vin, l_out]

		  for l_tech, l_vin in ProcessesByPeriodAndInput( A_period, A_com )
		  for l_out in ProcessOutputsByInput( A_period, l_tech, l_vin, A_com )
		  for l_season in M.time_season
		  for l_tod in M.time_of_day
		)

	if int is type( l_demand ) and l_demand == 0:
		# if there is no demand, then no need to create a constraint
		return Constraint.Skip

	l_frac_indices = M.TechLifeFrac.keys()

	l_non_dying_ability = sum(
	    M.V_Capacity[l_tech, l_vin]
	  * M.CapacityFactor[l_tech, l_vin]
	  * M.CapacityToActivity[l_tech]

	  for l_tech, l_vin in ProcessesByPeriodAndOutput( A_period, A_com )
	  if (A_period, l_tech, l_vin) not in l_frac_indices
	)

	expr = (l_non_dying_ability >= l_demand)
	return expr


def FractionalLifeActivityLimit_Constraint ( M, p, s, d, t, v, o ):
	max_output = (
	    M.V_Capacity[t, v]
	  * M.CapacityFactor[t, v]
	  * M.CapacityToActivity[t]
	  * M.TechLifeFrac[p, t, v]
	  * M.SegFrac[s, d]
	)

	actual_output = sum(
	  M.V_FlowOut[p, s, d, S_i, t, v, o]

	  for S_i in ProcessInputsByOutput( p, t, v, o )
	)

	expr = (actual_output <= max_output)
	return expr


def CapacityByOutputConstraint_rule ( M, p, s, d, t, v, o ):
	actual_activity = sum(
	  M.V_FlowOut[p, s, d, S_i, t, v, o]
	  for S_i in ProcessInputs( p, t, v )
	)

	min_output = (
	    M.V_CapacityByOutput[t, v, o]
	  * M.CapacityFactor[t, v]
	  * M.SegFrac[s, d]
	  * M.CapacityToActivity[ t ]
	)

	expr = ( min_output >= actual_activity )
	return expr


def CapacityConstraint_rule ( M, t, v ):
	capacity = sum(
	  M.V_CapacityByOutput[t, v, o]

	  for t_i, v_i, o in M.V_CapacityByOutput.keys()
	  if t_i == t and v_i == v
	)

	return M.V_Capacity[t, v] == capacity


def MARKAL_No_SegFrac_CapacityConstraint_rule ( M, p, t, v ):
	"""\
V_Capacity is a derived variable; this constraint sets V_Capacity to at least be able to handle the activity in any optimization time slice.  In effect, this sets V_Capacity[p,t,v] to the max of the activity for similar indices: max(Activity[p,*,*t,v])

(for each period, season, time_of_day, tech, vintage)
V_Capacity[t,v] * CapacityFactor[t,v] >= V_Activity[p,s,d,t,v]
	"""
	vintage_activity = sum(
	  M.V_Activity[p, s, d, t, v]

	  for s in M.time_season
	  for d in M.time_of_day
	)

	max_output = (
	    M.V_Capacity[t, v]
	  * M.CapacityFactor[t, v]
	  * M.CapacityToActivity[ t ]
	)

	expr = ( vintage_activity <= max_output )
	return expr


def CapacityInvestConstraint_rule ( M, t, v ):
	return  M.V_Capacity[t, v] == M.V_CapacityInvest[t, v]


def CapacityFixedConstraint_rule ( M, t, v ):
	return  M.V_Capacity[t, v] == M.V_CapacityFixed[t, v]


def ExistingCapacityConstraint_rule ( M, t, v ):
	"""\
For vintage periods (that the model is not to optimize), explicitly set the capacity values.

(for each tech, vintage_exist)
V_Capacity[t,v] = Param(Existingcapacity[t,v])
	"""
	expr = ( M.V_Capacity[t, v] == M.ExistingCapacity[t, v] )
	return expr


def ResourceExtractionConstraint_rule ( M, p, c ):
	"""\
Prevent TEMOA from extracting an endless supply of energy from "the ether".

(for each period, resource)
sum((season,time_of_day,tech,vintage),V_FlowIn[p,*,*,e,*,*,r]) <= Param(ResourceBound[p,r])
	"""
	max_resource = M.ResourceBound[p, c]

	collected = sum(
	  M.V_FlowIn[p, S_s, S_d, S_i, S_t, S_v, c]

	  for S_t, S_v in ProcessesByPeriodAndOutput( p, c )
	  for S_i in ProcessInputsByOutput( p, S_t, S_v, c )
	  for S_s in M.time_season
	  for S_d in M.time_of_day
	)

	expression = (collected <= max_resource)
	return expression


def CommodityBalanceConstraint_rule ( M, p, s, d, c ):
	"""\
Ensure that the FlowOut of a produced energy carrier at least meets the demand of the needed FlowIn of that energy carrier.  That is, this constraint maintains energy flows between processes.

(for each period, season, time_of_day, energy_carrier)
sum((inp,tech,vintage),V_FlowOut[p,s,t,*,*,*,c]) >= sum((tech,vintage,out),V_FlowIn[p,s,t,c,*,*,*])
sum((inp,tech,vintage),V_FlowOut[period,season,time_of_day,*,*,*,carrier]) >= sum((tech,vintage,out),V_FlowIn[period,season,time_of_day,carrier,*,*,*])
	"""
	if c in M.commodity_demand:
		return Constraint.Skip

	commodity_flow_in = sum(
	  M.V_FlowIn[p, s, d, c, S_t, S_v, S_o]

	  for S_t in M.tech_production
	  for S_v in M.vintage_all
	  for S_o in ProcessOutputsByInput( p, S_t, S_v, c )
	)

	commodity_flow_out = sum(
	  M.V_FlowOut[p, s, d, S_i, S_t, S_v, c]

	  for S_t in M.tech_all
	  for S_v in M.vintage_all
	  for S_i in ProcessInputsByOutput( p, S_t, S_v, c )
	)

	CommodityBalanceConstraintErrorCheck(
	  p, s, d, c, commodity_flow_out, commodity_flow_in
	)

	expr = (commodity_flow_out >= commodity_flow_in)
	return expr


def ProcessBalanceConstraint_rule ( M, p, s, d, i, t, v, o ):
	"""\
Analogous to CommodityBalance, this constraint ensures that the amount of
energy leaving a process is not more than the amount entering it.

(for each period, season, time_of_day, inp_carrier, vintage, out_carrier)
V_FlowOut[p,s,d,t,v,o] <= V_FlowIn[p,s,d,t,v,o] * Efficiency[i,t,v,o]
	"""
	expr = (
	    M.V_FlowOut[p, s, d, i, t, v, o]
	      <=
	    M.V_FlowIn[p, s, d, i, t, v, o]
	  * M.Efficiency[i, t, v, o]
	)

	return expr


def DemandActivityConstraint_rule ( M, p, s, d, t, v, dem, s_0, d_0 ):

	"""\
For end-use demands, it is unreasonable to let the optimizer only allow use in a
single time slice.  For instance, if household A buys a natural gas furnace
while household B buys an electric furnace, then both units should be used
through the year.  Without this constraint, the model might choose to only use
the electric during the day, and the natural gas during the night.

Mathematically, this constraint ensures that the ratio of the Activity to demand
is constant for all time slices.  The multiplication trick here is analogous to
what is performed in the Baseload constraint.
"""

	act_a = sum(
	  M.V_FlowOut[p, s_0, d_0, S_i, t, v, dem]

	  for S_i in ProcessInputsByOutput( p, t, v, dem )
	)
	act_b = sum(
	  M.V_FlowOut[p, s, d, S_i, t, v, dem]

	  for S_i in ProcessInputsByOutput( p, t, v, dem )
	)

	expr = (
	  act_a * M.Demand[p, s, d, dem].value
	     ==
	  act_b * M.Demand[p, s_0, d_0, dem].value
	)
	return expr


def DemandConstraint_rule ( M, p, s, d, dem ):
	"""\
The driving constraint, this rule ensures that supply at least equals demand.

(for each period, season, time_of_day, commodity)
sum((inp,tech,vintage),V_FlowOut[p,s,d,*,*,*,commodity]) >= Demand[p,s,d,commodity]
	"""
	index = (p, s, d, dem)
	if not (M.Demand[ index ] > 0):
		# User must have supplied a 0 demand: no need to create a useless
		# constraint like X >= 0
		return Constraint.Skip

	supply = sum(
	  M.V_FlowOut[p, s, d, S_i, S_t, S_v, dem]

	  for S_t in M.tech_all
	  for S_v in M.vintage_all
	  for S_i in ProcessInputsByOutput( p, S_t, S_v, dem )
	)

	DemandConstraintErrorCheck ( p, s, d, supply, dem )

	expr = (supply >= M.Demand[ index ])
	return expr

# End constraint rules
##############################################################################

##############################################################################
# Additional and derived (informational) variable constraints

def ActivityByPeriodTechConstraint_rule ( M, p, t ):
	activity = sum(
	  M.V_Activity[p, S_s, S_d, t, S_v]

	  for S_v in ProcessVintages( p, t )
	  for S_s in M.time_season
	  for S_d in M.time_of_day
	)

	if int is type( activity ):
		return Constraint.Skip

	expr = (M.V_ActivityByPeriodAndTech[p, t] == activity)
	return expr


def ActivityByPeriodTechAndVintageConstraint_rule ( M, p, t, v ):
	if p < v or v not in ProcessVintages( p, t ):
		return Constraint.Skip

	activity = sum(
	  M.V_Activity[p, S_s, S_d, t, v]

	  for S_s in M.time_season
	  for S_d in M.time_of_day
	)

	if int is type( activity ):
		return Constraint.Skip

	expr = (M.V_ActivityByPeriodTechAndVintage[p, t, v] == activity)
	return expr


def ActivityByPeriodTechAndOutputConstraint_rule ( M, p, t, o ):
	activity = sum(
	  M.V_FlowOut[p, S_s, S_d, S_i, t, S_v, o]

	  for S_v in ProcessVintages( p, t )
	  for S_i in ProcessInputsByOutput( p, t, S_v, o )
	  for S_s in M.time_season
	  for S_d in M.time_of_day
	)

	if int is type( activity ):
		return Constraint.Skip

	expr = (M.V_ActivityByPeriodTechAndOutput[p, t, o] == activity)
	return expr


def ActivityByPeriodTechVintageAndOutputConstraint_rule ( M, p, t, v, o ):
	activity = sum(
	  M.V_FlowOut[p, S_s, S_d, S_i, t, v, o]

	  for S_i in ProcessInputsByOutput( p, t, v, o )
	  for S_s in M.time_season
	  for S_d in M.time_of_day
	)

	if int is type( activity ):
		return Constraint.Skip

	expr = (M.V_ActivityByPeriodTechVintageAndOutput[p, t, v, o] == activity)
	return expr

def ActivityByTechAndOutputConstraint_rule ( M, t, o ):
	activity = sum(
	  M.V_FlowOut[S_p, S_s, S_d, S_i, t, S_v, o]

	  for S_p in M.time_optimize
	  for S_v in ProcessVintages( S_p, t )
	  for S_i in ProcessInputsByOutput( S_p, t, S_v, o )
	  for S_s in M.time_season
	  for S_d in M.time_of_day
	)

	if int is type( activity ):
		return Constraint.Skip

	expr = (M.V_ActivityByTechAndOutput[t, o] == activity)
	return expr


def ActivityByInputAndTechConstraint_rule ( M, i, t ):
	activity = sum(
	  M.V_FlowOut[S_p, S_s, S_d, i, t, S_v, S_o]

	  for S_p in M.time_optimize
	  for S_v in ProcessVintages( S_p, t )
	  for S_o in ProcessOutputsByInput( S_p, t, S_v, i )
	  for S_s in M.time_season
	  for S_d in M.time_of_day
	)

	if int is type( activity ):
		return Constraint.Skip

	expr = (M.V_ActivityByInputAndTech[i, t] == activity)
	return expr


def ActivityByPeriodInputAndTechConstraint_rule ( M, p, i, t ):
	activity = sum(
	  M.V_FlowIn[p, S_s, S_d, i, t, S_v, S_o]

	  for S_v in ProcessVintages( p, t )
	  for S_o in ProcessOutputsByInput( p, t, S_v, i )
	  for S_s in M.time_season
	  for S_d in M.time_of_day
	)

	if int is type( activity ):
		return Constraint.Skip

	index = (p, i, t)
	expr = (M.V_ActivityByPeriodInputAndTech[p, i, t] == activity)
	return expr


def ActivityByPeriodInputTechAndVintageConstraint_rule ( M, p, i, t, v ):
	activity = sum(
	  M.V_FlowIn[p, S_s, S_d, i, t, v, S_o]

	  for S_o in ProcessOutputsByInput( p, t, v, i )
	  for S_s in M.time_season
	  for S_d in M.time_of_day
	)

	if int is type( activity ):
		return Constraint.Skip

	expr = (M.V_ActivityByPeriodInputTechAndVintage[p, i, t, v] == activity)
	return expr


def CapacityAvailableByPeriodAndTechConstraint_rule ( M, p, t ):
	"""
This constraint sets V_CapacityAvailableByPeriodAndTech, a variable
nominally for reporting, but also used in the Max and Min constraint
calculations.  For any process with an end-of-life on a period boundary, all of
its capacity is available for use.  However, for any process with an EOL that
falls between periods, Temoa makes the simplifying assumption that the available
capacity from the dying technology is available through the *whole period*, but
only as much percentage as its lifespan through the period.  For example, if a
period is 8 years, and a process dies 3 years into the period, then only 3/8 of
the installed capacity is available for use for the period.
"""
	dying_vintages = set( v

	  for T_p, T_t, v in M.TechLifeFrac.keys()
	  if T_p == p and T_t == t
	)
	non_dying = ProcessVintages( p, t ) - dying_vintages

	total_cap = sum( M.V_Capacity[t, S_v] for S_v in non_dying )
	total_cap += sum(
	    M.V_Capacity[t, S_v]
	  * M.TechLifeFrac[p, t, S_v].value

	  for S_v in dying_vintages
	)

	expr = (M.V_CapacityAvailableByPeriodAndTech[p, t] == total_cap)
	return expr


def InvestmentByTechConstraint_rule ( M, t ):
	investment = sum(
	    M.V_Capacity[t, S_v]
	  * value( M.CostInvest[t, S_v] )

	  for S_t, S_v in M.CostInvest.keys()
	  if S_t == t
	)

	if int is type( investment ):
		return Constraint.Skip

	expr = ( M.V_InvestmentByTech[ t ] == investment)
	return expr


def InvestmentByTechAndVintageConstraint_rule ( M, t, v ):
	if (t, v) not in M.CostInvest.keys():
		return Constraint.Skip

	investment = M.V_Capacity[t, v] * value(M.CostInvest[t, v])

	expr = ( M.V_InvestmentByTechAndVintage[t, v] == investment)
	return expr


def EmissionActivityTotalConstraint_rule ( M, e ):
	emission_total = sum(
	    M.V_FlowOut[S_p, S_s, S_d, S_i, S_t, S_v, S_o]
	  * M.EmissionActivity[e, S_i, S_t, S_v, S_o]

	  for emission, S_i, S_t, S_v, S_o in M.EmissionActivity.keys()
	  if emission == e
	  for S_p in M.time_optimize
	  if ValidActivity( S_p, S_t, S_v )
	  for S_s in M.time_season
	  for S_d in M.time_of_day
	)

	if type( emission_total ) is int:
		return Constraint.Skip

	expr = (M.V_EmissionActivityTotal[ e ] == emission_total)
	return expr


def EmissionActivityByPeriodConstraint_rule ( M, e, p ):
	emission_total = sum(
	    M.V_FlowOut[p, S_s, S_d, S_i, S_t, S_v, S_o]
	  * M.EmissionActivity[e, S_i, S_t, S_v, S_o]

	  for T_e, S_i, S_t, S_v, S_o in M.EmissionActivity.keys()
	  if T_e == e
	  if ValidActivity( p, S_t, S_v )
	  for S_s in M.time_season
	  for S_d in M.time_of_day
	)

	if type( emission_total ) is int:
		return Constraint.Skip

	expr = (M.V_EmissionActivityByPeriod[e, p] == emission_total)
	return expr


def EmissionActivityByTechConstraint_rule ( M, e, t ):
	emission_total = sum(
	    M.V_FlowOut[S_p, S_s, S_d, S_i, t, S_v, S_o]
	  * M.EmissionActivity[e, S_i, t, S_v, S_o]

	  for T_e, S_i, S_t, S_v, S_o in M.EmissionActivity.keys()
	  if T_e == e and S_t == t
	  for S_p in M.time_optimize
	  if ValidActivity( S_p, S_t, S_v )
	  for S_s in M.time_season
	  for S_d in M.time_of_day
	)

	if type( emission_total ) is int:
		return Constraint.Skip

	expr = (M.V_EmissionActivityByTech[e, t] == emission_total)
	return expr


def EmissionActivityByPeriodAndTechConstraint_rule ( M, e, p, t ):
	emission_total = sum(
	    M.V_FlowOut[p, S_s, S_d, S_i, t, S_v, S_o]
	  * M.EmissionActivity[e, S_i, t, S_v, S_o]

	  for T_e, S_i, S_t, S_v, S_o in M.EmissionActivity.keys()
	  if T_e == e and S_t == t
	  if ValidActivity( p, S_t, S_v )
	  for S_s in M.time_season
	  for S_d in M.time_of_day
	)

	if type( emission_total ) is int:
		return Constraint.Skip

	expr = (M.V_EmissionActivityByPeriodAndTech[e, p, t] == emission_total)
	return expr


def EmissionActivityByTechAndVintageConstraint_rule ( M, e, t, v ):
	emission_total = sum(
	    M.V_FlowOut[S_p, S_s, S_d, S_i, t, v, S_o]
	  * M.EmissionActivity[e, S_i, t, v, S_o]

	  for T_e, S_i, S_t, S_v, S_o in M.EmissionActivity.keys()
	  if T_e == e and S_t == t and S_v == v
	  for S_p in M.time_optimize
	  if ValidActivity( S_p, S_t, S_v )
	  for S_s in M.time_season
	  for S_d in M.time_of_day
	)

	if type( emission_total ) is int:
		return Constraint.Skip

	expr = (M.V_EmissionActivityByTechAndVintage[e, t, v] == emission_total)
	return expr


def EnergyConsumptionByTechConstraint_rule ( M, t ):
	energy_used = sum(
	  M.V_FlowIn[S_p, S_s, S_d, S_i, t, S_v, S_o]

	  for S_p in M.time_optimize
	  for S_v in ProcessVintages( S_p, t )
	  for S_i in ProcessInputs( S_p, t, S_v )
	  for S_o in ProcessOutputsByInput( S_p, t, S_v, S_i )
	  for S_s in M.time_season
	  for S_d in M.time_of_day
	)

	expr = (M.V_EnergyConsumptionByTech[ t ] == energy_used)
	return expr


def EnergyConsumptionByTechAndOutputConstraint_rule ( M, t, o ):
	energy_used = sum(
	  M.V_FlowIn[S_p, S_s, S_d, S_i, t, S_v, o]

	  for S_p in M.time_optimize
	  for S_v in ProcessVintages( S_p, t )
	  for S_i in ProcessInputsByOutput( S_p, t, S_v, o )
	  for S_s in M.time_season
	  for S_d in M.time_of_day
	)

	expr = (M.V_EnergyConsumptionByTechAndOutput[t, o] == energy_used)
	return expr

def EnergyConsumptionByPeriodAndTechConstraint_rule ( M, p, t ):
	energy_used = sum(
	  M.V_FlowIn[p, S_s, S_d, S_i, t, S_v, S_o]

	  for S_v in ProcessVintages( p, t )
	  for S_i in ProcessInputs( p, t, S_v )
	  for S_o in ProcessOutputsByInput( p, t, S_v, S_i )
	  for S_s in M.time_season
	  for S_d in M.time_of_day
	)

	expr = (M.V_EnergyConsumptionByPeriodAndTech[p, t] == energy_used)
	return expr


def EnergyConsumptionByPeriodInputAndTechConstraint_rule ( M, p, i, t ):
	energy_used = sum(
	  M.V_FlowIn[p, S_s, S_d, i, t, S_v, S_o]

	  for S_v in ProcessVintages( p, t )
	  for S_o in ProcessOutputsByInput( p, t, S_v, i )
	  for S_s in M.time_season
	  for S_d in M.time_of_day
	)

	expr = (M.V_EnergyConsumptionByPeriodInputAndTech[p, i, t] == energy_used)
	return expr


def EnergyConsumptionByPeriodTechAndOutputConstraint_rule ( M, p, t, o ):
	energy_used = sum(
	  M.V_FlowIn[p, S_s, S_d, S_i, t, S_v, o]

	  for S_v in ProcessVintages( p, t )
	  for S_i in ProcessInputsByOutput( p, t, S_v, o )
	  for S_s in M.time_season
	  for S_d in M.time_of_day
	)

	index = (p, t, o)
	expr = (M.V_EnergyConsumptionByPeriodTechAndOutput[p, t, o] == energy_used)
	return expr


def EnergyConsumptionByPeriodTechAndVintageConstraint_rule ( M, p, t, v ):
	energy_used = sum(
	  M.V_FlowIn[p, S_s, S_d, S_i, t, v, S_o]

	  for S_i in ProcessInputs( p, t, v )
	  for S_o in ProcessOutputsByInput( p, t, v, S_i )
	  for S_s in M.time_season
	  for S_d in M.time_of_day
	)

	expr = (M.V_EnergyConsumptionByPeriodTechAndVintage[p, t, v] == energy_used)
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
