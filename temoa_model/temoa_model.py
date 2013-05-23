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

__all__ = ( 'temoa_create_model', )

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
time_horizon - the year boundaries of the periods of interest.
*time_optimize - time_horizon less the final (largest) year.  The model will
                 optimize over this set.
*vintage_exist  - copy of time_exist, for unambiguous contextual use
*vintage_all - the union of time_optimize and time_exist

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
	M.time_optimize   = Set( ordered=True, initialize=init_set_time_optimize )

	# These next sets are just various copies of the time_ sets, but
	# unfortunately must be manually copied because of a few outstanding bugs
	# within Pyomo (Jul 2011)
	M.vintage_exist    = Set( ordered=True, initialize=init_set_vintage_exist)
	M.vintage_optimize = Set( ordered=True, initialize=init_set_vintage_optimize)
	M.vintage_all      = M.time_exist | M.time_optimize

	# perform some basic validation on the time sets as a whole.
	M.validate_time    = BuildAction( rule=validate_time )

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
	M.PeriodLength = Param( M.time_optimize, initialize=ParamPeriodLength )
	M.PeriodRate   = Param( M.time_optimize, initialize=ParamPeriodRate )

	M.SegFrac = Param( M.time_season, M.time_of_day )

	# Ensure that all the time slices specified in SegFrac sum to 1
	M.validate_SegFrac = BuildAction( rule=validate_SegFrac )

	M.CapacityToActivity = Param( M.tech_all,  default=1 )

	M.ExistingCapacity = Param( M.tech_all, M.vintage_exist )
	M.Efficiency   = Param( M.commodity_physical, M.tech_all, M.vintage_all, M.commodity_carrier )

	M.CapacityFactorDefault = Param( M.time_season, M.time_of_day, M.tech_all, default=1 )
	M.CapacityFactor_sdtv   = Set( dimen=4, rule=CapacityFactorIndices )
	M.CapacityFactor        = Param( M.CapacityFactor_sdtv )

	M.initialize_CapacityFactor = Set( rule=CreateCapacityFactors )

	M.LifetimeTechDefault = Param( M.tech_all, default=30 )
	M.LifetimeLoanDefault = Param( M.tech_all, default=10 )
	M.LifetimeTech_tv = Set( dimen=2, rule=LifetimeTechIndices )
	M.LifetimeLoan_tv = Set( dimen=2, rule=LifetimeLoanIndices )
	M.LifetimeTech = Param( M.LifetimeTech_tv )  # in years
	M.LifetimeLoan = Param( M.LifetimeLoan_tv )  # in years

	M.initialize_Lifetimes = BuildAction( rule=CreateLifetimes )

	# always empty set, like the validation hacks above.  Temoa uses a couple
	# of global variables to precalculate some oft-used results in constraint
	# generation.  This is therefore intentially placed after all Set and Param
	# definitions and initializations, but before the Var, Objectives, and
	# Constraints.
	M.IntializeProcessParameters = Set( rule=InitializeProcessParameters )

	M.DemandDefaultDistribution  = Param( M.time_season, M.time_of_day )
	M.DemandSpecificDistribution = Param( M.time_season, M.time_of_day, M.commodity_demand )
	M.Demand        = Param( M.time_optimize,  M.commodity_demand )

	M.initialize_Demands = BuildAction( rule=CreateDemands )

	M.ResourceBound = Param( M.time_optimize,  M.commodity_physical )

	M.CostFixed_ptv    = Set( dimen=3, rule=CostFixedIndices )
	M.CostMarginal_ptv = Set( dimen=3, rule=CostMarginalIndices )
	M.CostInvest_tv    = Set( dimen=2, rule=CostInvestIndices )
	M.CostFixedVintageDefault_tv = Set( dimen=2,
	   rule=lambda M: set((t, v) for p, t, v in M.CostFixed_ptv ) )
	M.CostMarginalVintageDefault_tv = Set( dimen=2,
	   rule=lambda M: set((t, v) for p, t, v in M.CostMarginal_ptv ) )

	M.CostFixedVintageDefault    = Param( M.CostFixedVintageDefault_tv )
	M.CostMarginalVintageDefault = Param( M.CostMarginalVintageDefault_tv )
	M.CostFixed    = Param( M.CostFixed_ptv )
	M.CostMarginal = Param( M.CostMarginal_ptv )
	M.CostInvest   = Param( M.CostInvest_tv )

	M.initialize_Costs = BuildAction( rule=CreateCosts )

	M.Loan_tv           = Set( dimen=2, rule=lambda M: M.CostInvest.keys() )
	M.ModelLoanLife_tv  = Set( dimen=2, rule=lambda M: M.CostInvest.keys() )
	M.ModelTechLife_ptv = Set( dimen=3, rule=ModelTechLifeIndices )
	M.ModelLoanLife = Param( M.ModelLoanLife_tv,  initialize=ParamModelLoanLife_rule )
	M.ModelTechLife = Param( M.ModelTechLife_ptv, initialize=ParamModelTechLife_rule )

	M.DiscountRate_tv = Set( dimen=2, rule=lambda M: M.CostInvest.keys() )
	M.LoanLifeFrac_ptv = Set( dimen=3, rule=LoanLifeFracIndices )
	M.TechLifeFrac_ptv = Set( dimen=3, rule=ModelTechLifeIndices )

	M.DiscountRate  = Param( M.DiscountRate_tv, default=0.05 )
	M.TechLifeFrac  = Param( M.TechLifeFrac_ptv, initialize=ParamTechLifeFraction_rule )
	M.LoanAnnualize = Param( M.Loan_tv, initialize=ParamLoanAnnualize_rule )

	M.TechOutputSplit = Param( M.commodity_physical, M.tech_all, M.commodity_carrier )
	# always-empty Set; hack to perform inter-Set or inter-Param validation
	M.validate_TechOutputSplit = Set( initialize=validate_TechOutputSplit )

	M.MinCapacity = Param( M.time_optimize, M.tech_all )
	M.MaxCapacity = Param( M.time_optimize, M.tech_all )

	M.EmissionLimit    = Param( M.time_optimize, M.commodity_emissions )
	M.EmissionActivity_eitvo = Set( dimen=5, rule=EmissionActivityIndices )
	M.EmissionActivity = Param( M.EmissionActivity_eitvo )

	M.ActivityVar_psdtv = Set( dimen=5, rule=ActivityVariableIndices )
	M.ActivityByPeriodTechAndVintageVar_ptv = Set(
	  dimen=3, rule=ActivityByPeriodTechAndVintageVarIndices )

	M.CapacityVar_tv = Set( dimen=2, rule=CapacityVariableIndices )
	M.CapacityAvailableVar_pt = Set(
	  dimen=2, rule=CapacityAvailableVariableIndices )

	M.FlowVar_psditvo = Set( dimen=7, rule=FlowVariableIndices )

	# Variables
	#   Base decision variables
	M.V_FlowIn  = Var( M.FlowVar_psditvo, domain=NonNegativeReals )
	M.V_FlowOut = Var( M.FlowVar_psditvo, domain=NonNegativeReals )

	#   Derived decision variables
	M.V_Activity = Var( M.ActivityVar_psdtv, domain=NonNegativeReals )

	M.V_Capacity         = Var( M.CapacityVar_tv,       domain=NonNegativeReals )

	M.V_ActivityByPeriodTechAndVintage = Var(
	  M.ActivityByPeriodTechAndVintageVar_ptv,
	  domain=NonNegativeReals
	)

	M.V_CapacityAvailableByPeriodAndTech = Var(
	  M.CapacityAvailableVar_pt,
	  domain=NonNegativeReals
	)

	AddReportingVariables( M )

	M.BaseloadDiurnalConstraint_psdtv = Set(
	  dimen=5, rule=BaseloadDiurnalConstraintIndices )
	M.CommodityBalanceConstraint_psdc = Set(
	  dimen=4, rule=CommodityBalanceConstraintIndices )
	M.DemandConstraint_psdc = Set( dimen=4, rule=DemandConstraintIndices )
	M.DemandActivityConstraint_psdtv_dem_s0d0 = Set( dimen=8, rule=DemandActivityConstraintIndices )
	M.ExistingCapacityConstraint_tv = Set(
	  dimen=2, rule=lambda M: M.ExistingCapacity.sparse_iterkeys() )
	M.MaxCapacityConstraint_pt = Set(
	  dimen=2, rule=lambda M: M.MaxCapacity.sparse_iterkeys() )
	M.MinCapacityConstraint_pt = Set(
	  dimen=2, rule=lambda M: M.MinCapacity.sparse_iterkeys() )
	M.ProcessBalanceConstraint_psditvo = Set(
	  dimen=7, rule=ProcessBalanceConstraintIndices )
	M.ResourceConstraint_pr = Set(
	  dimen=2, rule=lambda M: M.ResourceBound.sparse_iterkeys() )
	M.StorageConstraint_psitvo = Set( dimen=6, rule=StorageConstraintIndices )
	M.TechOutputSplitConstraint_psditvo = Set(
	  dimen=7, rule=TechOutputSplitConstraintIndices )

	M.EmissionLimitConstraint_pe = Set(
	  dimen=2, rule=lambda M: M.EmissionLimit.sparse_iterkeys() )

	# Objective
	M.TotalCost = Objective(rule=TotalCost_rule, sense=minimize)

	# Constraints

	#   "Bookkeeping" constraints
	M.ActivityConstraint = Constraint( M.ActivityVar_psdtv, rule=Activity_Constraint )
	M.ActivityByPeriodTechAndVintageConstraint = Constraint( M.ActivityByPeriodTechAndVintageVar_ptv, rule=ActivityByPeriodTechAndVintage_Constraint )

	M.CapacityConstraint = Constraint( M.ActivityVar_psdtv, rule=Capacity_Constraint )

	M.ExistingCapacityConstraint = Constraint( M.ExistingCapacityConstraint_tv, rule=ExistingCapacity_Constraint )

	# M.CapacityInvestConstraint = Constraint( M.CapacityVar_tv, rule=CapacityInvest_Constraint )
	# M.CapacityFixedConstraint  = Constraint( M.CapacityVar_tv, rule=CapacityFixed_Constraint )

	#   Model Constraints
	#    - in driving order.  (e.g., without Demand, none of the others are
	#      very useful.)
	M.DemandConstraint           = Constraint( M.DemandConstraint_psdc,  rule=Demand_Constraint )
	M.DemandActivityConstraint   = Constraint( M.DemandActivityConstraint_psdtv_dem_s0d0, rule=DemandActivity_Constraint )
	M.ProcessBalanceConstraint   = Constraint( M.ProcessBalanceConstraint_psditvo, rule=ProcessBalance_Constraint )
	M.CommodityBalanceConstraint = Constraint( M.CommodityBalanceConstraint_psdc,  rule=CommodityBalance_Constraint )

	M.ResourceExtractionConstraint = Constraint( M.ResourceConstraint_pr,  rule=ResourceExtraction_Constraint )

	M.BaseloadDiurnalConstraint = Constraint( M.BaseloadDiurnalConstraint_psdtv,  rule=BaseloadDiurnal_Constraint )

	M.StorageConstraint = Constraint( M.StorageConstraint_psitvo, rule=Storage_Constraint )

	M.TechOutputSplitConstraint = Constraint( M.TechOutputSplitConstraint_psditvo, rule=TechOutputSplit_Constraint )

	M.CapacityAvailableByPeriodAndTechConstraint = Constraint( M.CapacityAvailableVar_pt, rule=CapacityAvailableByPeriodAndTech_Constraint )

	M.MinCapacityConstraint = Constraint( M.MinCapacityConstraint_pt, rule=MinCapacity_Constraint )
	M.MaxCapacityConstraint = Constraint( M.MaxCapacityConstraint_pt, rule=MaxCapacity_Constraint )

	M.EmissionLimitConstraint = Constraint( M.EmissionLimitConstraint_pe, rule=EmissionLimit_Constraint)


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

