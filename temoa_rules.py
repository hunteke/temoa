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

	for l_per in M.time_optimize:
		for l_tech in M.tech_all:
			for l_vin in M.vintage_optimize:
				if l_vin > l_per: continue

				if loanIsActive(l_per, l_tech, l_vin):
					l_icost = (
					    M.V_Capacity[l_tech, l_vin]
					  * ( M.CostInvest[l_tech, l_vin]
					    * M.LoanAnnualize[l_tech, l_vin]
					    + M.CostFixed[l_per, l_tech, l_vin]
					    )
					)
				else:
					l_icost = 0
					if M.CostFixed[l_per, l_tech, l_vin] > 0:
						# The if keeps the objective function cleaner in LP output
						l_icost = (
						    M.V_Capacity[l_tech, l_vin]
						  * M.CostFixed[l_per, l_tech, l_vin]
						)

			for l_vin in M.vintage_all:
				l_ucost = 0
				if M.CostMarginal[l_per, l_tech, l_vin].value > 0:
					# The if keeps the objective function cleaner in LP output
					l_ucost = sum(
					    M.V_Activity[l_per, l_season, l_time_of_day, l_tech, l_vin]
					  * M.CostMarginal[l_per, l_tech, l_vin].value

					  for l_season in M.time_season
					  for l_time_of_day in M.time_of_day
					)
				l_cost += (l_icost + l_ucost) * M.PeriodRate[ l_per ]

	return l_cost
Objective_rule = TotalCost_rule

##############################################################################
#   Initializaton rules

def ParamPeriodLength_rule ( period, M ):
	periods = list( M.time_optimize )
	periods.append( M.time_future.first() )

	i = periods.index( period )
	l_length = periods[i +1] - periods[ i ]

	return l_length


def ParamPeriodRate_rule ( period, M ):
	l_rate_multiplier = sum( [
	  (1 + M.GlobalDiscountRate.value)**(M.time_optimize.first() - y - period)

	  for y in range(0, M.PeriodLength[ period ])
	])

	return l_rate_multiplier


def ParamLoanAnnualize_rule ( A_tech, A_vintage, M ):
	l_annualized_rate = ( M.DiscountRate[ A_tech, A_vintage ].value /
	    (1 - (1 + M.DiscountRate[A_tech, A_vintage].value)
	         **(-M.LifetimeLoan[A_tech, A_vintage].value )
	))

	return l_annualized_rate

# End initialization rules
##############################################################################

##############################################################################
#   Constraint rules

def BaseloadDiurnalConstraint_rule ( A_period, A_season, A_time_of_day, A_tech, A_vintage, M ):
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
		return None

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


def EmissionsConstraint_rule ( A_period, A_emission, M ):
	pass


def MaxCarrierOutputConstraint_rule ( A_period, A_tech, A_output, M ):
	index = (A_period, A_tech, A_output)
	if M.MaxCarrierOutput[ index ] == 0:
		# if user specified 0, or did not specify a value, then there is no
		# constraint.  (The default value for this parameter is 0.)
		return None

	l_flowout = sum(
	  M.V_FlowOut[A_period, l_season, l_tod, l_inp, A_tech, l_vin, A_output]

	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	  for l_vin in M.vintage_all
	  for l_inp in ProcessInputsByOutput( (A_period, A_tech, l_vin), A_output )
	)
	expr = (l_flowout <= M.MaxCarrierOutput[ index ])
	return expr


def StorageConstraint_rule ( A_period, A_season, A_inp, A_tech, A_vintage, A_out, M ):
	"""\
	Constraint rule documentation goes here ...
"""
	if not isValidProcess( A_period, A_inp, A_tech, A_vintage, A_out ):
		return None

	l_sum_in_out = sum(
	    M.V_FlowOut[A_period, A_season, l_tod, A_inp, A_tech, A_vintage, A_out]
	  - M.V_FlowIn[A_period, A_season, l_tod, A_inp, A_tech, A_vintage, A_out]

	  for l_tod in M.time_of_day
	)

	expr = ( l_sum_in_out == 0 )
	return expr


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
	pindex = (A_period, A_tech, A_vintage)   # "process" index

	# No sense in creating a guaranteed unused constraint
	if not ProcessOutputs( *pindex ):
		return None

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


def ExistingCapacityConstraint_rule ( A_tech, A_vintage, M ):
	"""\
For vintage periods that the model is not to optimize, explicitly set the capacity values based on dat file input.

(for each tech, vintage_exist)
V_Capacity[t,v] = Param(Existingcapacity[t,v])
	"""
	index = (A_tech, A_vintage)
	ecapacity = value(M.ExistingCapacity[ index ])

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

	if type(l_vflow_out) == type(l_vflow_in):
		if int is type(l_vflow_out):
			# Tell Pyomo not to create this constraint; it's useless because both
			# of the flows are 0.  i.e. carrier not needed and nothing makes it.
			return None

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

	  for l_tech, l_vin in ProcessesByPeriodAndOutput( A_period, A_comm, M )
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

##############################################################################
# Additional and derived (informational) variable constraints

def TechActivityByPeriodConstraint_rule ( A_per, A_tech, M ):
	l_sum = sum(
	  M.V_Activity[A_per, l_season, l_tod, A_tech, l_vin]

	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	  for l_vin in M.vintage_all
	  if l_vin <= A_per and A_per <= l_vin + M.LifetimeTech[A_tech, l_vin]
	)

	if int is type( l_sum ):
		return None

	expr = (M.V_ActivityByPeriodAndTech[A_per, A_tech] == l_sum)
	return expr


def TechActivityByPeriodAndVintageConstraint_rule ( A_per, A_tech, A_vin, M ):
	if A_per < A_vin:
		return None
	elif A_per <= A_vin or A_vin + M.LifetimeTech[A_tech, A_vin] <= A_per:
		return None

	l_sum = sum(
	  M.V_Activity[A_per, l_season, l_tod, A_tech, A_vin]

	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	)

	if int is type( l_sum ):
		return None

	expr = (M.V_ActivityByPeriodTechAndVintage[A_per, A_tech, A_vin] == l_sum)
	return expr


def CapacityByPeriodAndTechConstraint_rule ( A_per, A_tech, M ):
	l_sum = sum(
	  M.V_Capacity[A_tech, l_vin]

	  for l_vin in M.vintage_all
	  if l_vin < A_per and A_per <= M.LifetimeTech[A_tech, l_vin] + l_vin
	)

	if type( l_sum ) is int:
		return None

	expr = (M.V_CapacityByPeriodAndTech[A_per, A_tech] == l_sum)
	return expr


def InvestmentByTechConstraint_rule ( A_tech, M ):
	l_sum = sum(
	    M.V_Capacity[A_tech, l_vin]
	  * M.CostInvest[A_tech, l_vin].value

	  for l_vin in M.vintage_optimize
	  if M.CostInvest[A_tech, l_vin].value > 0
	)

	if int is type( l_sum ):
		return None

	expr = ( M.V_InvestmentByTech[ A_tech ] == l_sum)
	return expr


def InvestmentByTechAndVintageConstraint_rule ( A_tech, A_vin, M ):
	index = (A_tech, A_vin)

	l_cost = 0

	if value(M.CostInvest[ index ]) > 0:
		l_cost = M.V_Capacity[ index ] * value(M.CostInvest[ index ])

	if int is type( l_cost ):
		return None

	expr = ( M.V_InvestmentByTechAndVintage[ index ] == l_cost)
	return expr


def EmissionActivityTotalConstraint_rule ( A_emission, M ):
	l_sum = sum(
	    M.V_Activity[l_per, l_season, l_tod, l_tech, l_vin]
	  * M.EmissionActivity[A_emission, l_tech, l_vin]

	  for l_per in M.time_optimize
	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	  for l_tech in M.tech_all
	  for l_vin in M.vintage_all
	  if M.EmissionActivity[A_emission, l_tech, l_vin] > 0
	)

	if type( l_sum ) is int:
		return None

	expr = (M.V_EmissionActivityTotal[ A_emission ] == l_sum)
	return expr


def EmissionActivityByPeriodConstraint_rule ( A_emission, A_period, M ):
	l_sum = sum(
	    M.V_Activity[A_period, l_season, l_tod, l_tech, l_vin]
	  * M.EmissionActivity[A_emission, l_tech, l_vin]

	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	  for l_tech in M.tech_all
	  for l_vin in M.vintage_all
	  if M.EmissionActivity[A_emission, l_tech, l_vin] > 0
	)

	if type( l_sum ) is int:
		return None

	expr = (M.V_EmissionActivityByPeriod[A_emission, A_period] == l_sum)
	return expr


def EmissionActivityByTechConstraint_rule ( A_emission, A_tech, M ):
	l_sum = sum(
	    M.V_Activity[l_per, l_season, l_tod, A_tech, l_vin]
	  * M.EmissionActivity[A_emission, A_tech, l_vin]

	  for l_per in M.time_optimize
	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	  for l_vin in M.vintage_all
	  if M.EmissionActivity[A_emission, A_tech, l_vin] > 0
	)

	if type( l_sum ) is int:
		return None

	expr = (M.V_EmissionActivityByTech[A_emission, A_tech] == l_sum)
	return expr


def EmissionActivityByPeriodAndTechConstraint_rule ( A_emission, A_period, A_tech, M ):
	l_sum = sum(
	    M.V_Activity[A_period, l_season, l_tod, A_tech, l_vin]
	  * M.EmissionActivity[A_emission, A_tech, l_vin]

	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	  for l_vin in M.vintage_all
	  if M.EmissionActivity[A_emission, A_tech, l_vin] > 0
	)

	if type( l_sum ) is int:
		return None

	index = (A_emission, A_period, A_tech)
	expr = (M.V_EmissionActivityByPeriodAndTech[ index ] == l_sum)
	return expr


def EmissionActivityByTechAndVintageConstraint_rule ( A_emission, A_tech, A_vintage, M ):
	l_sum = sum(
	    M.V_Activity[l_per, l_season, l_tod, A_tech, A_vintage]
	  * M.EmissionActivity[A_emission, A_tech, A_vintage]

	  for l_per in M.time_optimize
	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	  if M.EmissionActivity[A_emission, A_tech, A_vintage] > 0
	)

	if type( l_sum ) is int:
		return None

	index = (A_emission, A_tech, A_vintage)
	expr = (M.V_EmissionActivityByTechAndVintage[ index ] == l_sum)
	return expr


def EnergyConsumptionByTechConstraint_rule ( A_tech, M ):
	l_sum = sum(
	  M.V_FlowIn[l_per, l_season, l_tod, l_inp, A_tech, l_vin, l_out]

	  for l_per in M.time_optimize
	  for l_inp in M.commodity_physical
	  for l_vin in M.vintage_all
	  for l_out in ProcessOutputsByInput( (l_per, A_tech, l_vin), l_inp )
	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	)

	expr = (M.V_EnergyConsumptionByTech[ A_tech ] == l_sum)
	return expr


def EnergyConsumptionByTechAndOutputConstraint_rule ( A_tech, A_out, M ):
	l_sum = sum(
	  M.V_FlowIn[l_per, l_season, l_tod, l_inp, A_tech, l_vin, A_out]

	  for l_per in M.time_optimize
	  for l_vin in M.vintage_all
	  for l_inp in ProcessInputsByOutput( (l_per, A_tech, l_vin), A_out )
	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	)

	expr = (M.V_EnergyConsumptionByTechAndOutput[A_tech, A_out] == l_sum)
	return expr

def EnergyConsumptionByPeriodAndTechConstraint_rule ( A_period, A_tech, M ):
	l_sum = sum(
	  M.V_FlowIn[A_period, l_season, l_tod, l_inp, A_tech, l_vin, l_out]

	  for l_inp in M.commodity_physical
	  for l_vin in M.vintage_all
	  for l_out in ProcessOutputsByInput( (A_period, A_tech, l_vin), l_inp )
	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	)

	expr = (M.V_EnergyConsumptionByPeriodAndTech[A_period, A_tech] == l_sum)
	return expr


def EnergyConsumptionByPeriodTechAndOutputConstraint_rule ( A_period, A_tech, A_out, M ):
	l_sum = sum(
	  M.V_FlowIn[A_period, l_season, l_tod, l_inp, A_tech, l_vin, A_out]

	  for l_vin in M.vintage_all
	  for l_inp in ProcessInputsByOutput( (A_period, A_tech, l_vin), A_out )
	  for l_season in M.time_season
	  for l_tod in M.time_of_day
	)

	index = (A_period, A_tech, A_out)
	expr = (M.V_EnergyConsumptionByPeriodTechAndOutput[ index ] == l_sum)
	return expr


def EnergyConsumptionByPeriodTechAndVintageConstraint_rule ( A_period, A_tech, A_vintage, M ):
	l_sum = sum(
	  M.V_FlowIn[A_period, l_season, l_tod, l_inp, A_tech, A_vintage, l_out]

	  for l_inp in M.commodity_physical
	  for l_out in ProcessOutputsByInput( (A_period, A_tech, A_vintage), l_inp )
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
