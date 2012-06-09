#!/usr/bin/env coopr_python

from temoa_lib import *
from temoa_model import *

def StochasticPointObjective_rule ( M, p ):
	"""\
Stochastic objective function.

TODO: update with LaTeX version of equation.
	"""
	P_0 = min( M.time_optimize )

	loan_costs = sum(
	    M.V_CapacityInvest[S_t, S_v]
	  * (
	      M.CostInvest[S_t, S_v].value
	    * M.LoanAnnualize[S_t, S_v].value
	    * sum( (1 + M.GlobalDiscountRate.value) ** -y
	        for y in range( S_v - P_0,
	                        S_v - P_0 + M.ModelLoanLife[S_t, S_v].value )
	      )
	  )

	  for S_t, S_v in M.CostInvest.sparse_iterkeys()
	  if S_v == p
	)

	fixed_costs = sum(
	    M.V_CapacityFixed[S_t, S_v]
	  * (
	      M.CostFixed[p, S_t, S_v].value
	    * sum( (1 + M.GlobalDiscountRate.value) ** -y
	        for y in range( p - P_0,
	                        p - P_0 + M.ModelTechLife[p, S_t, S_v].value )
	      )
	    )

	  for S_p, S_t, S_v in M.CostFixed.sparse_iterkeys()
	  if S_p == p
	)

	marg_costs = sum(
	    M.V_ActivityByPeriodTechAndVintage[p, S_t, S_v]
	  * (
	      M.CostMarginal[p, S_t, S_v].value
	    * M.PeriodRate[ p ].value
	  )

	  for S_p, S_t, S_v in M.CostMarginal.sparse_iterkeys()
	  if S_p == p
	)

	sp_cost = (loan_costs + fixed_costs + marg_costs)

	expr = (M.StochasticPointCost[ p ] == sp_cost)
	return expr

def Objective_rule ( M ):
	return sum( M.StochasticPointCost[ pp ] for pp in M.time_optimize )

M = model = temoa_create_model( 'TEMOA Stochastic' )

M.StochasticPointCost = Var( M.time_optimize, within=NonNegativeReals )
M.StochasticPointCostConstraint = Constraint( M.time_optimize, rule=StochasticPointObjective_rule )

M.TotalCost = Objective( rule=Objective_rule, sense=minimize )
