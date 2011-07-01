#!/usr/bin/env coopr_python

__all__ = [ 'temoa_create_model', ]

from temoa_rules import *

def temoa_create_model ( name='TEMOA Entire Energy System Economic Optimization Model' ):
	"""\
Returns an abstract instance of the TEMOA model.  (Abstract because it will yet
need to be populated with "dot dat" file data.)

Model characteristics:

A '*' next to a Set or Parameter indicates that it is automatically deduced.
It is not possible to directly set this Set or Parameter in a "dot dat" file.

   SETS
time_exist   - the periods prior to the model.  Mainly utilized to populate the
               capacity of installed technologies prior to those the
               optimization is allowed to alter.
time_horizon - the periods of interest.  Though the model will optimize through
               time_future, Temoa will report results only for this set.
time_future  - the periods following time_horizon.
*time_optimize - the union of time_horizon and time_future, less the final
                 period.  The model will optimize over this set.
*time_report - the union of time_exist and time_horizon.
*time_all    - the union of time_optimize and time_exist
*vintage_exist  - copy of time_exist, for unambiguous contextual use
*vintage_future - copy of time_future, for unambiguous contextual use
*vintage_all - a copy of time_all, for unambiguous contextual use.

time_season  - the seasons of interest.  For example, winter might have
               different cooling demand characteristics than summer.
time_of_day  - the parts of the day of interest.  For example, the night hours
               might have a different lighting demand than the daylight hours.

tech_resource   - "base" energy resources, like imported coal, imported
                  electricity, or mined natural gas.
tech_production - technologies that convert energy, like a coal plant (coal to
                  electricity), electric boiler (electricity to heat), or
                  electric car (electricity to vehicle miles traveled)
*tech_all       - the union of tech_resource and tech_production

commodity_emissions - emission outputs of concern, like co2.
commodity_physical  - energy carriers, like coal, oil, or electricity
commodity_demand    - end use demands, like residential heating, commercial
                      lighting, or vehicle miles traveled
*commodity_all      - The union of commodity_{emissions, physical, demand}

   PARAMETERS
ExistingCapacity(tech_all, vintage_exist)
   [default: 0] ExistingCapacity allows the modeler to define any vintage of
   existing technology prior to the model optimization periods.
Efficiency(commodity_all, tech_all, vintage_all, commodity_all)
   [default: 0] Efficiency allows the modeler to define the efficiency
   associated with a particular process, identified by an input commodity,
   technology, vintage, and output commodity.
Lifetime(tech_all, vintage_all)
   [default: 0] Lifetime enables the modeler to define the usable lifetime of
   any particular
   technology or vintage of technology.
Demand(time_optimize, time_season, time_of_day, commodity_demand)
   Demand sets the exogenous amount of a commodity demand in each optimization
   time period, season, and time of day.  In some sense, this is the parameter
   that drives everything in the Temoa model.
ResourceBound(time_optimize, commodity_physical)
   [default: 0] ResourceBound enables the modeler to set limits on how much of
   a given resource the model may "mine" or "import" in any given optimization
   period.
CommodityProductionCost(time_optimize, tech_all, vintage_all)
   [default: 0] CommodityProductionCost enables the modeler to set the price
   per unit to operate a technology.  The modeler may, for example, choose to
   change the price to operate a vintage of a technology between optimization
   periods.
CapacityFactor(tech_all, vintage_all)
   [default: 0] CapacityFactor enables the modeler to set the capacity factor
   for any vintage of technology.
	"""
	M = AbstractModel( name )

	M.time_exist      = Set( ordered=True, within=Integers )
	M.time_horizon    = Set( ordered=True, within=Integers )
	M.time_future     = Set( ordered=True, within=Integers )
	M.time_optimize   = Set( ordered=True, initialize=init_set_time_optimize )
	M.time_report     = M.time_exist | M.time_horizon
	M.time_all        = M.time_exist | M.time_optimize

	# These next sets are just various copies of the time_ sets, but
	# unfortunately must be manually copied because of a few outstanding bugs
	# within Pyomo (Jul 2011)
	M.vintage_exist    = Set( ordered=True, initialize=init_set_vintage_exist)
	M.vintage_future   = Set( ordered=True, initialize=init_set_vintage_future)
	M.vintage_optimize = Set( ordered=True, initialize=init_set_vintage_optimize)
	M.vintage_all      = Set( ordered=True, initialize=init_set_vintage_all)

	# always-empty Set; hack to perform inter-Set or inter-Param validation
	M.validate_time    = Set( initialize=validate_time )

	M.time_season     = Set()
	M.time_of_day     = Set()

	M.tech_resource   = Set()
	M.tech_production = Set()
	M.tech_all = M.tech_resource | M.tech_production  # '|' = union operator
	M.tech_baseload   = Set( within=M.tech_all )
	M.tech_storage    = Set( within=M.tech_all )

	M.commodity_demand    = Set()
	M.commodity_emissions = Set()
	M.commodity_physical  = Set()

	M.commodity_carrier = M.commodity_physical | M.commodity_demand
	M.commodity_all     = M.commodity_carrier | M.commodity_emissions

	M.GlobalDiscountRate = Param( default=0 )
	M.PeriodLength = Param( M.time_optimize, initialize=ParamPeriodLength_rule )
	M.PeriodRate   = Param( M.time_optimize, initialize=ParamPeriodRate_rule )

	M.SegFrac = Param(M.time_season, M.time_of_day, default=0)
	# always-empty Set; hack to perform inter-Set or inter-Param validation
	M.validate_SegFrac = Set( initialize=validate_SegFrac )

	M.CapacityToActivity = Param( M.tech_all,  default=1 )
	M.CapacityFactor     = Param( M.tech_all,  M.vintage_all,  default=1 )

	M.ExistingCapacity = Param(M.tech_all, M.vintage_exist, default=0 )

	M.Efficiency    = Param( M.commodity_carrier,  M.tech_all,  M.vintage_all,  M.commodity_carrier,  default=0 )
	M.Demand        = Param( M.time_optimize,  M.time_season,  M.time_of_day,  M.commodity_demand,  default=0 )
	M.ResourceBound = Param( M.time_optimize,  M.commodity_physical,  default=float('+inf') )

	M.LifetimeTech = Param( M.tech_all,  M.vintage_all,  default=30 )  # in years
	M.LifetimeLoan = Param( M.tech_all,  M.vintage_optimize,  default=10 )  # in years
	M.LifetimeFrac = Param( M.time_optimize, M.tech_all,  M.vintage_all,  rule=ParamLifetimeFrac_rule )
	M.DiscountRate = Param( M.tech_all,  M.vintage_optimize,  default=0.05 )

	M.CostFixed     = Param( M.time_optimize, M.tech_all, M.vintage_all, default=0 )
	M.CostMarginal  = Param( M.time_optimize, M.tech_all, M.vintage_all, default=0 )
	M.CostInvest    = Param( M.tech_all, M.vintage_optimize, default=0 )
	M.LoanAnnualize = Param( M.tech_all, M.vintage_optimize, rule=ParamLoanAnnualize_rule )

	M.TechOutputSplit = Param( M.commodity_physical, M.tech_all, M.commodity_carrier, default=0 )
	# always-empty Set; hack to perform inter-Set or inter-Param validation
	M.validate_TechOutputSplit = Set( initialize=validate_TechOutputSplit )

	M.MinCapacity = Param( M.time_optimize, M.tech_all, default=-1 )
	M.MaxCapacity = Param( M.time_optimize, M.tech_all, default=-1 )

	# Not yet indexed by period or incorporated into the constraints
	M.EmissionLimit    = Param( M.time_optimize, M.commodity_emissions, default=float('+inf') )
	M.EmissionActivity = Param( M.commodity_emissions, M.tech_all, M.vintage_all, default=0 )

	# always empty set, like the validation hacks above.  Temoa uses a couple
	# of global variables to precalculate some oft-used results in constraint
	# generation.  This is therefore intentially placed after all Set and Param
	# definitions and initializations, but before the Var, Objectives, and
	# Constraints.
	M.IntializeProcessParameters = Set( rule=InitializeProcessParameters )

	M.FlowVarSet = Set( initialize=
	    M.time_optimize * M.time_season * M.time_of_day * M.commodity_carrier
	  * M.tech_all      * M.vintage_all * M.commodity_carrier,
	  filter = FlowVariableFilter
	)

	# Variables
	#   Base decision variables
	M.V_FlowIn  = Var( M.FlowVarSet, domain=NonNegativeReals )
	M.V_FlowOut = Var( M.FlowVarSet, domain=NonNegativeReals )

	#   Derived decision variables
	M.V_Activity = Var(M.time_optimize, M.time_season, M.time_of_day, M.tech_all, M.vintage_all, domain=NonNegativeReals)
	M.V_Capacity = Var(M.tech_all, M.vintage_all, domain=NonNegativeReals)

	AddReportingVariables( M )

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
	M.DemandCapacityConstraint     = Constraint( M.time_optimize, M.time_season, M.time_of_day, M.commodity_demand,      rule=DemandCapacityConstraint_rule )
	M.ProcessBalanceConstraint     = Constraint( M.time_optimize, M.time_season, M.time_of_day, M.commodity_physical, M.tech_all, M.vintage_all, M.commodity_carrier, rule=ProcessBalanceConstraint_rule )
	M.CommodityBalanceConstraint   = Constraint( M.time_optimize, M.time_season, M.time_of_day, M.commodity_physical,    rule=CommodityBalanceConstraint_rule )
	M.ResourceExtractionConstraint = Constraint( M.time_optimize, M.commodity_physical,    rule=ResourceExtractionConstraint_rule )

	M.BaseloadDiurnalConstraint = Constraint( M.time_optimize, M.time_season, M.time_of_day, M.tech_baseload, M.vintage_all, rule=BaseloadDiurnalConstraint_rule )

	M.StorageConstraint = Constraint( M.time_optimize, M.time_season, M.commodity_all, M.tech_storage, M.vintage_all, M.commodity_all, rule=StorageConstraint_rule )

	M.TechOutputSplitConstraint = Constraint( M.time_optimize, M.time_season, M.time_of_day, M.commodity_physical, M.tech_all, M.vintage_all, M.commodity_carrier, rule=TechOutputSplitConstraint_rule )

	M.CapacityLifetimeConstraint           = Constraint( M.time_optimize, M.commodity_carrier, rule=CapacityLifetimeConstraint_rule )
	M.CapacityFractionalLifetimeConstraint = Constraint( M.time_optimize, M.tech_all, M.vintage_all, M.commodity_carrier, rule=CapacityFractionalLifetimeConstraint_rule )

	M.MinCapacityConstraint = Constraint( M.time_optimize, M.tech_all, rule=MinCapacityConstraint_rule )
	M.MaxCapacityConstraint = Constraint( M.time_optimize, M.tech_all, rule=MaxCapacityConstraint_rule )
	#   Constraints not yet updated
	M.EmissionConstraint           = Constraint( M.time_optimize, M.commodity_emissions, rule=EmissionsConstraint_rule)


	return M


model = temoa_create_model()


if '__main__' == __name__:
	# This script was apparently invoked directly, rather than through Pyomo.
	# $ ./model.py  test.dat           # called directly
	# $ lpython  model.py  test.dat    # called directly
	# $ pyomo    model.py  test.dat    # through Pyomo

	# Calling this script directly enables a cleaner formatting than Pyomo's
	# default output, but (currently) forces the choice of solver to GLPK.
	from temoa_lib import temoa_solve
	temoa_solve( model )

