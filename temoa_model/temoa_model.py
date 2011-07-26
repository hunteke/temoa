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

	M.GlobalDiscountRate = Param()
	M.PeriodLength = Param( M.time_optimize, initialize=ParamPeriodLength_rule )
	M.PeriodRate   = Param( M.time_optimize, initialize=ParamPeriodRate_rule )

	M.SegFrac = Param( M.time_season, M.time_of_day )
	# always-empty Set; hack to perform inter-Set or inter-Param validation
	M.validate_SegFrac = Set( initialize=validate_SegFrac )

	M.CapacityToActivity = Param( M.tech_all,  default=1 )
	M.CapacityFactor     = Param( M.tech_all,  M.vintage_all,  default=1 )

	M.ExistingCapacity = Param( M.tech_all, M.vintage_exist )
	M.Efficiency   = Param( M.commodity_carrier, M.tech_all, M.vintage_all, M.commodity_carrier )
	M.LifetimeTech = Param( M.tech_all,  M.vintage_all,  default=30 )  # in years
	M.LifetimeLoan = Param( M.tech_all,  M.vintage_optimize,  default=10 )  # in years

	# always empty set, like the validation hacks above.  Temoa uses a couple
	# of global variables to precalculate some oft-used results in constraint
	# generation.  This is therefore intentially placed after all Set and Param
	# definitions and initializations, but before the Var, Objectives, and
	# Constraints.
	M.IntializeProcessParameters = Set( rule=InitializeProcessParameters )

	M.Demand        = Param( M.time_optimize,  M.time_season,  M.time_of_day,  M.commodity_demand )
	M.ResourceBound = Param( M.time_optimize,  M.commodity_physical )

	M.CostFixedIndices    = Set( dimen=3, rule=CostFixedIndices )
	M.CostMarginalIndices = Set( dimen=3, rule=CostMarginalIndices )
	M.CostInvestIndices   = Set( dimen=2, rule=CostInvestIndices )
	M.CostFixed    = Param( M.CostFixedIndices )
	M.CostMarginal = Param( M.CostMarginalIndices )
	M.CostInvest   = Param( M.CostInvestIndices )

	M.DiscountRateIndices = Set( dimen=2, rule=DiscountRateIndices )
	M.LifetimeFracIndices = Set( dimen=3, rule=LifetimeFracIndices )
	M.LoanIndices         = Set( dimen=2, rule=LoanIndices )

	M.DiscountRate  = Param( M.DiscountRateIndices, default=0.05 )
	M.LifetimeFrac  = Param( M.LifetimeFracIndices, rule=ParamLifetimeFrac_rule )
	M.LoanAnnualize = Param( M.LoanIndices, rule=ParamLoanAnnualize_rule )

	M.TechOutputSplit = Param( M.commodity_physical, M.tech_all, M.commodity_carrier )
	# always-empty Set; hack to perform inter-Set or inter-Param validation
	M.validate_TechOutputSplit = Set( initialize=validate_TechOutputSplit )

	M.MinCapacity = Param( M.time_optimize, M.tech_all )
	M.MaxCapacity = Param( M.time_optimize, M.tech_all )

	M.EmissionLimit    = Param( M.time_optimize, M.commodity_emissions )
	M.EmissionActivityIndices = Set( dimen=5, rule=EmissionActivityIndices )
	M.EmissionActivity = Param( M.EmissionActivityIndices )

	M.ActivityVarIndices = Set( dimen=5, rule=ActivityVariableIndices )
	M.CapacityVarIndices = Set( dimen=2, rule=CapacityVariableIndices )
	M.CapacityAvailableVarIndices = Set(
	  dimen=2, rule=CapacityAvailableVariableIndices )
	M.FlowVarIndices = Set( dimen=7, rule=FlowVariableIndices )

	M.BaseloadDiurnalConstraintIndices = Set(
	  dimen=5, rule=BaseloadDiurnalConstraintIndices )
	M.CapacityFractionalLifetimeConstraintIndices = Set(
	  dimen=4, rule=CapacityFractionalLifetimeConstraintIndices )
	M.CapacityLifetimeConstraintIndices = Set(
	  dimen=2, rule=CapacityLifetimeConstraintIndices )
	M.CommodityBalanceConstraintIndices = Set(
	  dimen=4, rule=CommodityBalanceConstraintIndices )
	M.DemandConstraintIndices = Set( dimen=4, rule=DemandConstraintIndices )
	M.ExistingCapacityConstraintIndices = Set(
	  dimen=2, rule=ExistingCapacityConstraintIndices )
	M.MaxCapacityConstraintIndices = Set(
	  dimen=2, rule=MaxCapacityConstraintIndices )
	M.MinCapacityConstraintIndices = Set(
	  dimen=2, rule=MinCapacityConstraintIndices )
	M.ProcessBalanceConstraintIndices = Set(
	  dimen=7, rule=ProcessBalanceConstraintIndices )
	M.ResourceConstraintIndices = Set( dimen=2, rule=ResourceConstraintIndices )
	M.StorageConstraintIndices = Set( dimen=6, rule=StorageConstraintIndices )
	M.TechOutputSplitConstraintIndices = Set(
	  dimen=7, rule=TechOutputSplitConstraintIndices )

	M.EmissionConstraintIndices = Set( dimen=2, rule=EmissionConstraintIndices )

	# Variables
	#   Base decision variables
	M.V_FlowIn  = Var( M.FlowVarIndices, domain=NonNegativeReals )
	M.V_FlowOut = Var( M.FlowVarIndices, domain=NonNegativeReals )

	#   Derived decision variables
	M.V_Activity = Var( M.ActivityVarIndices, domain=NonNegativeReals )
	M.V_Capacity = Var( M.CapacityVarIndices, domain=NonNegativeReals )

	M.V_CapacityAvailableByPeriodAndTech = Var(
	  M.CapacityAvailableVarIndices,
	  domain=NonNegativeReals
	)

	AddReportingVariables( M )

	# Objective
	M.TotalCost = Objective(rule=TotalCost_rule, sense=minimize)

	# Constraints

	#   "Bookkeeping" constraints
	M.ActivityConstraint = Constraint( M.ActivityVarIndices, rule=ActivityConstraint_rule )
	M.CapacityConstraint = Constraint( M.ActivityVarIndices, rule=CapacityConstraint_rule )

	M.ExistingCapacityConstraint = Constraint( M.ExistingCapacityConstraintIndices, rule=ExistingCapacityConstraint_rule )

	#   Model Constraints
	#    - in driving order.  (e.g., without Demand, none of the others are
	#      very useful.)
	M.DemandConstraint           = Constraint( M.DemandConstraintIndices,  rule=DemandConstraint_rule )
	M.DemandCapacityConstraint   = Constraint( M.DemandConstraintIndices,  rule=DemandCapacityConstraint_rule )
	M.ProcessBalanceConstraint   = Constraint( M.ProcessBalanceConstraintIndices, rule=ProcessBalanceConstraint_rule )
	M.CommodityBalanceConstraint = Constraint( M.CommodityBalanceConstraintIndices,  rule=CommodityBalanceConstraint_rule )

	M.ResourceExtractionConstraint = Constraint( M.ResourceConstraintIndices,  rule=ResourceExtractionConstraint_rule )

	M.BaseloadDiurnalConstraint = Constraint( M.BaseloadDiurnalConstraintIndices,  rule=BaseloadDiurnalConstraint_rule )

	M.StorageConstraint = Constraint( M.StorageConstraintIndices, rule=StorageConstraint_rule )

	M.TechOutputSplitConstraint = Constraint( M.TechOutputSplitConstraintIndices, rule=TechOutputSplitConstraint_rule )

	M.CapacityAvailableByPeriodAndTechConstraint = Constraint( M.CapacityAvailableVarIndices, rule=CapacityAvailableByPeriodAndTechConstraint_rule )

	M.CapacityLifetimeConstraint           = Constraint( M.CapacityLifetimeConstraintIndices, rule=CapacityLifetimeConstraint_rule )
	M.CapacityFractionalLifetimeConstraint = Constraint( M.CapacityFractionalLifetimeConstraintIndices, rule=CapacityFractionalLifetimeConstraint_rule )

	M.MinCapacityConstraint = Constraint( M.MinCapacityConstraintIndices, rule=MinCapacityConstraint_rule )
	M.MaxCapacityConstraint = Constraint( M.MaxCapacityConstraintIndices, rule=MaxCapacityConstraint_rule )

	M.EmissionConstraint = Constraint( M.EmissionConstraintIndices, rule=EmissionConstraint_rule)


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

