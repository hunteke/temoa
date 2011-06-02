#!/usr/bin/env lpython

__all__ = [ 'temoa_create_model', ]

from temoa_rules import *

def temoa_create_model ( ):
	M = AbstractModel('TEMOA Entire Energy System Economic Optimization Model')

	M.time_exist      = Set( ordered=True, within=Integers )
	M.time_horizon    = Set( ordered=True, within=Integers )
	M.time_future     = Set( ordered=True, within=Integers )
	M.time_validation = Set( initialize=validate_periods )
	M.time_optimize   = Set( ordered=True, initialize=init_set_time_optimize )
	M.time_all        = M.time_exist | M.time_optimize
	M.vintage_exist   = M.time_exist   # intentional copy, for unambiguous use
	M.vintage_future  = M.time_future  # intentional copy, for unambiguous use
	M.vintage_all     = M.time_all     # intentional copy, for unambiguous use

	M.time_season     = Set()
	M.time_of_day     = Set()

	M.tech_resource   = Set()
	M.tech_production = Set()
	M.tech_all = M.tech_resource | M.tech_production  # '|' = union operator

	M.commodity_emissions = Set()
	M.commodity_physical  = Set()
	M.commodity_demand    = Set()

	# Pyomo currently has a rather large design flaw in it's implementation of set
	# unions, where it is not possible to create a union of more than two sets in
	# a single statement.  A bug report has been filed with the Coopr devs.
	#   - 24 Feb 2011
	M.tmp_set = M.commodity_physical | M.commodity_emissions
	M.commodity_all = M.tmp_set | M.commodity_demand


	M.ExistingCapacity = Param(M.tech_all, M.vintage_exist, default=0)
	M.Efficiency       = Param(M.commodity_all,  M.tech_all,  M.vintage_all,  M.commodity_all,  default=0)
	M.Lifetime         = Param(M.tech_all,  M.vintage_all,  default=20)         # 20 years
	M.Demand           = Param(M.time_optimize,  M.time_season,  M.time_of_day,  M.commodity_demand,  default=0)
	M.ResourceBound    = Param(M.time_optimize,  M.commodity_physical,  default=0)
	M.CommodityProductionCost = Param(M.time_optimize,  M.tech_all,  M.vintage_all,  default=1)
	M.CapacityFactor   = Param(M.tech_all,  M.vintage_all,  default=1)


	# Not yet indexed by period or incorporated into the constraints
	M.EmissionsLimit = Param(M.commodity_emissions, default=0)


	# Variables
	#   Decision variables
	M.V_FlowIn  = Var(M.time_optimize, M.time_season, M.time_of_day, M.commodity_all, M.tech_all, M.vintage_all, M.commodity_all, domain=NonNegativeReals)
	M.V_FlowOut = Var(M.time_optimize, M.time_season, M.time_of_day, M.commodity_all, M.tech_all, M.vintage_all, M.commodity_all, domain=NonNegativeReals)

	#   Derived variables
	M.V_Activity = Var(M.time_optimize, M.time_season, M.time_of_day, M.tech_all, M.vintage_all, domain=NonNegativeReals)
	M.V_Capacity = Var(M.tech_all, M.vintage_all, domain=NonNegativeReals)


	# Objective
	M.TotalCost = Objective(rule=TotalCost_rule, sense=minimize)

	# Constraints

	#   "Bookkeeping" constraints
	M.ActivityConstraint = Constraint( M.time_optimize, M.time_season, M.time_of_day, M.tech_all, M.vintage_all, rule=ActivityConstraint_rule )
	M.CapacityConstraint = Constraint( M.time_optimize, M.time_season, M.time_of_day, M.tech_all, M.vintage_all, rule=CapacityConstraint_rule )

	M.ExistingCapacityConstraint = Constraint( M.tech_all, M.vintage_exist, rule=ExistingCapacityConstraint_rule )

	#   Model Constraints
	#    - in driving order.  (e.g., without Demand, none of the others are
	#      very useful.)
	M.DemandConstraint             = Constraint( M.time_optimize, M.time_season, M.time_of_day, M.commodity_demand,      rule=DemandConstraint_rule )
	M.ProcessBalanceConstraint     = Constraint( M.time_optimize, M.time_season, M.time_of_day, M.commodity_all, M.tech_all, M.vintage_all, M.commodity_all, rule=ProcessBalanceConstraint_rule )
	M.CommodityBalanceConstraint   = Constraint( M.time_optimize, M.time_season, M.time_of_day, M.commodity_physical,    rule=CommodityBalanceConstraint_rule )
	M.ResourceExtractionConstraint = Constraint( M.time_optimize, M.commodity_physical,    rule=ResourceExtractionConstraint_rule )

	#   Constraints not yet updated
	#M.EmissionConstraint           = Constraint(M.commodity_emissions,            rule=EmissionConstraint_rule)
	#M.ResourceBalanceConstraint    = Constraint(M.commodity_physical,             rule=ResourceBalanceConstraint_rule)
	return M

model = temoa_create_model()


if '__main__' == __name__:
	# Figure out whether this script was called directly, or through Pyomo:
	# $ ./model.py  test.dat           # called directly
	# $ lpython  model.py  test.dat    # called directly
	# $ pyomo    model.py  test.dat    # through Pyomo

	# Calling this script directly enables a cleaner formatting than Pyomo's
	# default output, but (currently) forces the choice of solver to GLPK.
	from temoa_lib import temoa_solve
	temoa_solve( model )