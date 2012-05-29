#!/usr/bin/env coopr_python

from temoa_lib import *
from temoa_model import *

def StochasticPointObjective_rule ( M, p ):
	l_cost = 0
	"""\
Objective function.

This function is currently a simple summation of all items in V_FlowOut multiplied by CommunityProductionCost.  For the time being (i.e. during development), this is intended to make development and debugging simpler.
	"""
	partial_period_loan_indices = M.LoanLifeFrac.keys()
	partial_period_tech_indices = M.TechLifeFrac.keys()
	P_0 = M.time_optimize.first()

	loan_costs = sum(
	    M.V_Capacity[S_t, S_v]
	  * (
	      M.PeriodRate[ p ].value
	    * M.CostInvest[S_t, S_v].value
	    * M.LoanAnnualize[S_t, S_v].value
	  )

	  for S_t, S_v in M.CostInvest.keys()
	  if (p, S_t, S_v) not in partial_period_loan_indices
	  if loanIsActive( p, S_t, S_v )
	) + sum(
	    M.V_CapacityInvest[S_t, S_v]
	  * M.CostInvest[S_t, S_v].value
	  * M.LoanAnnualize[S_t, S_v].value
	  * sum(
	      (1 + M.GlobalDiscountRate) ** (P_0 - S_p - y)
	      for y in range( 0, M.PeriodLength[ S_p ] * M.LoanLifeFrac[S_p, S_t, S_v])
	    )

	  for S_p, S_t, S_v in partial_period_loan_indices
	  if S_p == p
	)

	fixed_costs = sum(
	    M.V_Capacity[S_t, S_v]
	  * (
	      M.CostFixed[p, S_t, S_v].value
	    * M.PeriodRate[ p ].value
	  )

	  for S_p, S_t, S_v in M.CostFixed.keys()
	  if S_p == p
	  if (S_p, S_t, S_v) not in partial_period_tech_indices
	) + sum(
	    M.V_CapacityFixed[S_t, S_v]
	  * M.CostFixed[S_p, S_t, S_v].value
	  * sum(
	      (1 + M.GlobalDiscountRate) ** (P_0 - S_p - y)
	      for y in range( 0, M.PeriodLength[ S_p ] * M.TechLifeFrac[S_p, S_t, S_v])
	    )

	  for S_p, S_t, S_v in partial_period_tech_indices
	  if S_p == p
	  if (S_p, S_t, S_v) in M.CostFixed.keys()
	)

	marg_costs = sum(
	    M.V_ActivityByPeriodTechAndVintage[S_p, S_t, S_v]
	  * value(
	      M.CostMarginal[S_p, S_t, S_v].value
	    * M.PeriodRate[ S_p ].value
	  )

	  for S_p, S_t, S_v in M.CostMarginal.keys()
	  if S_p == p
	)

	costs = (loan_costs + fixed_costs + marg_costs)
	expr = (M.StochasticPointCost[ p ] == costs)
	return expr

def Objective_rule ( M ):
	return sum( M.StochasticPointCost[ pp ] for pp in M.time_optimize )

M = model = temoa_create_model( 'TEMOA Stochastic' )

M.StochasticPointCost = Var( M.time_optimize, within=NonNegativeReals )
M.StochasticPointCostConstraint = Constraint( M.time_optimize, rule=StochasticPointObjective_rule )

M.TotalCost = Objective( rule=Objective_rule, sense=minimize )

