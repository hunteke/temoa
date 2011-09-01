#!/usr/bin/env coopr_python

from temoa_lib import *
from temoa_model import *

def StochasticPointObjective_rule ( M, A_period ):
	l_cost = 0
	"""\
Objective function.

This function is currently a simple summation of all items in V_FlowOut multiplied by CommunityProductionCost.  For the time being (i.e. during development), this is intended to make development and debugging simpler.
	"""
	l_invest_indices = M.CostInvest.keys()
	l_fixed_indices  = M.CostFixed.keys()
	l_marg_indices   = M.CostMarginal.keys()

	l_loan_costs = sum(
	    M.V_Capacity[l_tech, l_vin] * M.PeriodRate[ A_period ]
	  * M.CostInvest[l_tech, l_vin]
	  * M.LoanAnnualize[l_tech, l_vin]

	  for l_tech in M.tech_all
	  for l_vin in ProcessVintages( A_period, l_tech )
	  if loanIsActive( A_period, l_tech, l_vin )
	  if (l_tech, l_vin) in l_invest_indices
	  if value(M.CostInvest[l_tech, l_vin])
	)

	l_fixed_costs = sum(
	    M.V_Capacity[l_tech, l_vin]
	  * M.CostFixed[A_period, l_tech, l_vin]
	  * M.PeriodRate[ A_period ]

	  for l_tech in M.tech_all
	  for l_vin in ProcessVintages( A_period, l_tech )
	  if (A_period, l_tech, l_vin) in l_fixed_indices
	  if value(M.CostFixed[A_period, l_tech, l_vin])
	)

	l_marg_costs = sum(
	    M.V_Activity[A_period, l_season, l_time_of_day, l_tech, l_vin]
	  * M.PeriodRate[ A_period ]
	  * M.CostMarginal[A_period, l_tech, l_vin]

	  for l_tech in M.tech_all
	  for l_vin in ProcessVintages( A_period, l_tech )
	  if (A_period, l_tech, l_vin) in l_marg_indices
	  if value(M.CostMarginal[A_period, l_tech, l_vin])
	  for l_season in M.time_season
	  for l_time_of_day in M.time_of_day
	)

	expr = (M.StochasticPointCost[ A_period ] == l_cost)
	return expr

def Objective_rule ( M ):
	return sum( M.StochasticPointCost[ pp ] for pp in M.time_optimize )

M = model = temoa_create_model( 'TEMOA Stochastic' )

M.StochasticPointCost = Var( M.time_optimize, within=NonNegativeReals )
M.StochasticPointCostConstraint = Constraint( M.time_optimize, rule=StochasticPointObjective_rule )

M.Total_Cost = Objective( rule=Objective_rule, sense=minimize )
