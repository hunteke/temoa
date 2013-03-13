#!/usr/bin/env coopr_python

"""
Temoa - Tools for Energy Model Optimization and Analysis
  linear optimization; least cost; dynamic system visualization

Copyright (C) 2011-2012  Kevin Hunter, Joseph DeCarolis

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU Affero General Public License for more details.

Developers of this script will check out a complete copy of the GNU Affero
General Public License in the file COPYING.txt.  Users uncompressing this from
an archive may not have received this license file.  If not, see
<http://www.gnu.org/licenses/>.
"""

from temoa_lib import *
from temoa_model import *

def StochasticPointObjective_rule ( M, p ):
	"""\
Stochastic objective function.

TODO: update with LaTeX version of equation.
	"""
	P_0 = min( M.time_optimize )
	GDR = value( M.GlobalDiscountRate )

	loan_costs = sum(
	    M.V_Capacity[S_t, S_v]
	  * (
	      value( M.CostInvest[S_t, S_v] )
	    * value( M.LoanAnnualize[S_t, S_v] )
	    * sum( (1 + GDR) ** -y
	        for y in range( S_v - P_0,
	                        S_v - P_0 + value( M.ModelLoanLife[S_t, S_v] ))
	      )
	  )

	  for S_t, S_v in M.CostInvest.sparse_iterkeys()
	  if S_v == p
	)

	fixed_costs = sum(
	    M.V_Capacity[S_t, S_v]
	  * (
	      value( M.CostFixed[p, S_t, S_v] )
	    * sum( (1 + GDR) ** -y
	        for y in range( p - P_0,
	                        p - P_0 + value( M.ModelTechLife[p, S_t, S_v] ))
	      )
	    )

	  for S_p, S_t, S_v in M.CostFixed.sparse_iterkeys()
	  if S_p == p
	)

	marg_costs = sum(
	    M.V_ActivityByPeriodTechAndVintage[p, S_t, S_v]
	  * (
	      value( M.CostMarginal[p, S_t, S_v] )
	    * value( M.PeriodRate[ p ] )
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
