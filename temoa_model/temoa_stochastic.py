#!/usr/bin/env coopr_python

from temoa_lib import *
from temoa_model import *

def StochasticPointObjective_rule ( M ):
	l_cost = 0

	for l_tech in M.tech_all:
		for l_vin in ProcessVintages( l_per, l_tech ):
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

			l_ucost = 0
			l_marg_cost = value(M.CostMarginal[l_per, l_tech, l_vin])
			if l_marg_cost > 0:
				# The if keeps the objective function cleaner in LP output
				l_ucost = sum(
				    M.V_Activity[l_per, l_season, l_time_of_day, l_tech, l_vin]
				  * l_marg_cost

				  for l_season in M.time_season
				  for l_time_of_day in M.time_of_day
				)
			l_cost += (l_icost + l_ucost) * M.PeriodRate[ l_per ]

	return l_cost

def Objective_rule ( M ):
	return sum( M.StochasticPointCost[ pp ] for pp in M.time_optimize )

M = model = temoa_create_model( 'TEMOA Stochastic' )

M.StochasticPointCost = Var( M.time_optimize, within=NonNegativeReals )
M.Total_Cost = Objective( rule=Objective_rule, sense=minimize )
