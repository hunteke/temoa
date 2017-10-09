#!/usr/bin/env python

"""
Tools for Energy Model Optimization and Analysis (Temoa): 
An open source framework for energy systems optimization modeling

Copyright (C) 2015,  NC State University

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

A complete copy of the GNU General Public License v2 (GPLv2) is available 
in LICENSE.txt.  Users uncompressing this from an archive may not have 
received this license file.  If not, see <http://www.gnu.org/licenses/>.
"""

from temoa_rules import *
from temoa_initialize import *
from temoa_run import *

def temoa_create_model ( name='The Temoa Energy System Model' ):
    """\
    Returns an abstract instance of the TEMOA model -- Abstract because it needs
    to be populated with a "dot dat" file in order to create a specific model
    instantiation.
  """
    M = TemoaModel( name )
    
    # Define Sets---------------------------------------------------------------
    M.time_exist    = Set( ordered=True )  # check for integerness performed
    M.time_future   = Set( ordered=True )  # (with reasoning) in temoa_lib
    M.time_optimize = Set( ordered=True, initialize=init_set_time_optimize )
    
    # These next sets are just various copies of the time_ sets, but
    # unfortunately must be manually copied because of a few outstanding bugs
    # within Pyomo (Jul 2011)
    M.vintage_exist    = Set( ordered=True, initialize=init_set_vintage_exist)
    M.vintage_optimize = Set( ordered=True, initialize=init_set_vintage_optimize)
    M.vintage_all      = M.time_exist | M.time_optimize
    
    # Perform some basic validation on the time sets as a whole.
    M.validate_time    = BuildAction( rule=validate_time )
    
    M.time_season     = Set( ordered=True )
    M.time_of_day     = Set( ordered=True )
    
    M.tech_resource   = Set()
    M.tech_production = Set()
    M.tech_all = M.tech_resource | M.tech_production  # '|' = union operator
    
    M.tech_baseload   = Set( within=M.tech_all )
    M.tech_storage    = Set( within=M.tech_all )
    M.tech_hourlystorage = Set( within=M.tech_all) 
    M.tech_ramping    = Set( within=M.tech_all )
    M.tech_reserve    = Set( within=M.tech_all )
    M.tech_capacity_min   = Set( within=M.tech_all ) 
    M.tech_capacity_max   = Set( within=M.tech_all ) 
    
    # Technology sets used for sector-specific MGA weights
    M.tech_mga         = Set( within=M.tech_all )
    M.tech_electric    = Set( within=M.tech_all )
    M.tech_transport   = Set( within=M.tech_all )
    M.tech_industrial  = Set( within=M.tech_all )
    M.tech_commercial  = Set( within=M.tech_all )
    M.tech_residential = Set( within=M.tech_all )
    
    M.commodity_demand    = Set()
    M.commodity_emissions = Set()
    M.commodity_physical  = Set()
    
    M.commodity_carrier = M.commodity_physical | M.commodity_demand
    M.commodity_all     = M.commodity_carrier | M.commodity_emissions
    
    # Define Parameters---------------------------------------------------------
    
    # Note: In order to increase model efficiency, we use sparse indexing of 
    # of parameters, variables, and equations to prevent the creation of indices 
    # for which no data exists. While basic model sets are defined above, sparse 
    # index sets are defined below adjacent to the appropriate parameter, 
    # variable, or constraint and all are initialized in temoa_lib.py.
    
    M.GlobalDiscountRate = Param()
    M.PeriodLength = Param( M.time_optimize, initialize=ParamPeriodLength )
    M.PeriodRate   = Param( M.time_optimize, initialize=ParamPeriodRate )
    M.SegFrac = Param( M.time_season, M.time_of_day )  
    M.validate_SegFrac = BuildAction( rule=validate_SegFrac )
    M.CapacityToActivity = Param( M.tech_all,  default=1 )
    M.ExistingCapacity = Param( M.tech_all, M.vintage_exist )
    M.Efficiency = Param( M.commodity_physical, M.tech_all, M.vintage_all, 
                      M.commodity_carrier )
    M.validate_UsedEfficiencyIndices = BuildAction( rule=CheckEfficiencyIndices )   
    M.CapacityFactor_sdtv = Set( dimen=4, initialize=CapacityFactorProcessIndices )
    M.CapacityFactorProcess = Param( M.CapacityFactor_sdtv )
    M.CapacityFactor_sdt  = Set( dimen=3, initialize=CapacityFactorTechIndices )
    M.CapacityFactorTech    = Param( M.CapacityFactor_sdt, default=1 )
    M.initialize_CapacityFactors = BuildAction( rule=CreateCapacityFactors )
    M.LifetimeTech           = Param( M.tech_all, default=30 )    # in years
    M.LifetimeLoanTech       = Param( M.tech_all, default=10 )    # in years
    M.LifetimeProcess_tv     = Set( dimen=2, initialize=LifetimeProcessIndices )
    M.LifetimeProcess        = Param( M.LifetimeProcess_tv )      # in years
    M.LifetimeLoanProcess_tv = Set( dimen=2, initialize=LifetimeLoanProcessIndices )
    M.LifetimeLoanProcess    = Param( M.LifetimeLoanProcess_tv )  # in years
    M.initialize_Lifetimes = BuildAction( rule=CreateLifetimes )
    M.GrowthRateMax = Param( M.tech_all )
    M.GrowthRateSeed = Param( M.tech_all )
    
    # Temoa uses a couple of global variables to precalculate some frequently 
    # used results in constraint generation.  This is therefore intentially 
    # placed before the Var, Objectives, and Constraints.
    M.initialize_ProcessParameters = BuildAction( rule=InitializeProcessParameters )
    
    M.DemandDefaultDistribution  = Param( M.time_season, M.time_of_day )
    M.DemandSpecificDistribution = Param( M.time_season, M.time_of_day, 
                                      M.commodity_demand )
    M.Demand = Param( M.time_optimize, M.commodity_demand )
    M.initialize_Demands = BuildAction( rule=CreateDemands )
    M.ResourceBound = Param( M.time_optimize,  M.commodity_physical )
    M.CostFixed_ptv    = Set( dimen=3, initialize=CostFixedIndices )
    M.CostFixed    = Param( M.CostFixed_ptv )
    M.CostFixedVintageDefault_tv = Set( dimen=2, 
       initialize=lambda M: set((t, v) for p, t, v in M.CostFixed_ptv ) )
    M.CostFixedVintageDefault    = Param( M.CostFixedVintageDefault_tv )
    M.CostInvest_tv    = Set( dimen=2, initialize=CostInvestIndices )
    M.CostInvest   = Param( M.CostInvest_tv )  
    M.CostVariable_ptv = Set( dimen=3, initialize=CostVariableIndices )
    M.CostVariable = Param( M.CostVariable_ptv ) 
    M.CostVariableVintageDefault_tv = Set( dimen=2,
       initialize=lambda M: set((t, v) for p, t, v in M.CostVariable_ptv ) )
    M.CostVariableVintageDefault = Param( M.CostVariableVintageDefault_tv )
    M.initialize_Costs = BuildAction( rule=CreateCosts )
    M.DiscountRate_tv = Set( dimen=2, initialize=lambda M: M.CostInvest.keys() )
    M.DiscountRate  = Param( M.DiscountRate_tv, default=0.05 )
    M.Loan_tv           = Set( dimen=2, initialize=lambda M: M.CostInvest.keys() )
    M.LoanAnnualize = Param( M.Loan_tv, initialize=ParamLoanAnnualize_rule )
    M.SalvageRate   = Param( M.Loan_tv, initialize=ParamSalvageRate_rule )
    M.ModelLoanLife_tv  = Set( dimen=2, initialize=lambda M: M.CostInvest.keys() )
    M.ModelLoanLife     = Param( M.ModelLoanLife_tv,  
                             initialize=ParamModelLoanLife_rule )
    M.ModelProcessLife_ptv = Set( dimen=3, initialize=ModelProcessLifeIndices )
    M.ModelProcessLife  = Param( M.ModelProcessLife_ptv, 
                             initialize=ParamModelProcessLife_rule )
    M.LoanLifeFrac_ptv = Set( dimen=3, initialize=LoanLifeFracIndices )
    M.ProcessLifeFrac_ptv = Set( dimen=3, initialize=ModelProcessLifeIndices )
    M.ProcessLifeFrac  = Param( M.ProcessLifeFrac_ptv, 
       initialize=ParamProcessLifeFraction_rule )
    
    #Parameters for user-defined constraints
    M.MinCapacity = Param( M.time_optimize, M.tech_all )
    M.MaxCapacity = Param( M.time_optimize, M.tech_all )
    M.MinCapacitySum = Param( M.time_optimize )   #minimum capacity for all techs within tech_capacity  
    M.MaxCapacitySum = Param( M.time_optimize )   #maximum capacity for all techs within tech_capacity  
    M.MaxActivity = Param( M.time_optimize, M.tech_all )
    M.MinActivity = Param( M.time_optimize, M.tech_all )
    M.EmissionLimit    = Param( M.time_optimize, M.commodity_emissions )
    M.EmissionActivity_eitvo = Set( dimen=5, initialize=EmissionActivityIndices )
    M.EmissionActivity = Param( M.EmissionActivity_eitvo )
    M.TechInputSplit  = Param( M.time_optimize, M.commodity_physical, M.tech_all )
    M.TechOutputSplit = Param( M.time_optimize, M.tech_all, M.commodity_carrier )

    #Parameters for Ramping Up and Ramping Down Constraints ARQ 22/07/16
    M.RampUp   = Param( M.tech_ramping )
    M.RampDown = Param( M.tech_ramping )

    # Parameters for reserve margin constraints.
    M.CapacityCredit = Param( M.tech_reserve, default=1 )
    M.ReserveMargin  = Param( M.commodity_demand, default=0.0 )

    # Decision Variables--------------------------------------------------------
    #   Base decision variables
    M.FlowVar_psditvo = Set( dimen=7, initialize=FlowVariableIndices )
    M.V_FlowIn  = Var( M.FlowVar_psditvo, domain=NonNegativeReals )
    M.V_FlowOut = Var( M.FlowVar_psditvo, domain=NonNegativeReals )
    
    # Derived decision variables
    M.ActivityVar_psdtv = Set( dimen=5, initialize=ActivityVariableIndices )
    M.V_Activity = Var( M.ActivityVar_psdtv, domain=NonNegativeReals )
    
    M.CapacityVar_tv = Set( dimen=2, initialize=CapacityVariableIndices )    
    M.V_Capacity = Var( M.CapacityVar_tv,    domain=NonNegativeReals )
        
    M.ActivityByPeriodAndProcessVar_ptv = Set(
      dimen=3, initialize=ActivityByPeriodAndProcessVarIndices )     
    M.V_ActivityByPeriodAndProcess = Var( M.ActivityByPeriodAndProcessVar_ptv,
                                          domain=NonNegativeReals )
    M.CapacityAvailableVar_pt = Set(
      dimen=2, initialize=CapacityAvailableVariableIndices )    
    M.V_CapacityAvailableByPeriodAndTech = Var( M.CapacityAvailableVar_pt,
                                            domain=NonNegativeReals )

    M.EnergyConsumptionByPeriodInputAndTech_pit = Set(
      dimen=3, initialize=EnergyConsumptionByPeriodInputAndTechVariableIndices )
    M.V_EnergyConsumptionByPeriodInputAndTech = Var(
      M.EnergyConsumptionByPeriodInputAndTech_pit, 
      domain=NonNegativeReals )

    M.ActivityByPeriodTechAndOutput_pto = Set(
      dimen=3, initialize=ActivityByPeriodTechAndOutputVariableIndices )
    M.V_ActivityByPeriodTechAndOutput = Var( M.ActivityByPeriodTechAndOutput_pto, 
                                             domain=NonNegativeReals )

    M.EmissionActivityByPeriodAndTech_ept = Set(
      dimen=3, initialize=EmissionActivityByPeriodAndTechVariableIndices )    
    M.V_EmissionActivityByPeriodAndTech = Var( 
      M.EmissionActivityByPeriodAndTech_ept, domain=Reals )

    # This derived decision variable is used in MGA objective function:
    M.V_ActivityByTech = Var(M.tech_all, domain=NonNegativeReals )

    # Decision variable for hourly storage
    M.HourlyStorage_psdt = Set (dimen=4, initialize=HourlyStorageVariableIndices )
    M.V_HourlyStorage = Var( M.HourlyStorage_psdt, domain=NonNegativeReals )

    # Objective Function--------------------------------------------------------
    M.TotalCost = Objective(rule=TotalCost_rule, sense=minimize)
    
    
    # Constraints---------------------------------------------------------------

    # Constraints to calculate derived decision variables
    M.ActivityConstraint = Constraint( 
      M.ActivityVar_psdtv, 
      rule=Activity_Constraint )
    
    M.ActivityByPeriodAndProcessConstraint = Constraint( 
      M.ActivityByPeriodAndProcessVar_ptv, 
      rule=ActivityByPeriodAndProcess_Constraint )

    M.EnergyConsumptionByPeriodInputAndTechConstraint = Constraint( 
      M.EnergyConsumptionByPeriodInputAndTech_pit, 
      rule=EnergyConsumptionByPeriodInputAndTech_Constraint )
    
    M.ActivityByPeriodTechAndOutputConstraint = Constraint( 
      M.ActivityByPeriodTechAndOutput_pto, 
      rule=ActivityByPeriodTechAndOutput_Constraint )

    M.ActivityByTechConstraint = Constraint(
      M.tech_all, 
      rule=ActivityByTech_Constraint )

    M.CapacityConstraint = Constraint( 
      M.ActivityVar_psdtv, 
      rule=Capacity_Constraint )
    
    M.CapacityAvailableByPeriodAndTechConstraint = Constraint( 
      M.CapacityAvailableVar_pt, 
      rule=CapacityAvailableByPeriodAndTech_Constraint )

    M.ExistingCapacityConstraint_tv = Set(
      dimen=2, initialize=lambda M: M.ExistingCapacity.sparse_iterkeys() )
    M.ExistingCapacityConstraint = Constraint( 
      M.ExistingCapacityConstraint_tv, 
      rule=ExistingCapacity_Constraint )

    M.EmissionActivityByPeriodAndTechConstraint = Constraint( 
      M.EmissionActivityByPeriodAndTech_ept, 
      rule=EmissionActivityByPeriodAndTech_Constraint )

    #   Model Constraints
    #   In driving order, starting with the need to meet end-use demands

    M.DemandConstraint_psdc = Set( dimen=4, initialize=DemandConstraintIndices )
    M.DemandConstraint           = Constraint( 
      M.DemandConstraint_psdc,  
      rule=Demand_Constraint )

    M.DemandActivityConstraint_psdtv_dem_s0d0 = Set( 
       dimen=8, initialize=DemandActivityConstraintIndices )
    M.DemandActivityConstraint   = Constraint( 
      M.DemandActivityConstraint_psdtv_dem_s0d0, 
      rule=DemandActivity_Constraint )

    M.ProcessBalanceConstraint_psditvo = Set(
      dimen=7, initialize=ProcessBalanceConstraintIndices )
    M.ProcessBalanceConstraint   = Constraint( 
      M.ProcessBalanceConstraint_psditvo, 
      rule=ProcessBalance_Constraint )

    M.CommodityBalanceConstraint_psdc = Set(
      dimen=4, initialize=CommodityBalanceConstraintIndices )
    M.CommodityBalanceConstraint = Constraint( 
      M.CommodityBalanceConstraint_psdc,  
      rule=CommodityBalance_Constraint )

    M.ResourceConstraint_pr = Set(
      dimen=2, initialize=lambda M: M.ResourceBound.sparse_iterkeys() )
    M.ResourceExtractionConstraint = Constraint( 
      M.ResourceConstraint_pr,  
      rule=ResourceExtraction_Constraint )

    M.BaseloadDiurnalConstraint_psdtv = Set(
      dimen=5, initialize=BaseloadDiurnalConstraintIndices )
    M.BaseloadDiurnalConstraint = Constraint( 
      M.BaseloadDiurnalConstraint_psdtv,  
      rule=BaseloadDiurnal_Constraint )

    M.StorageConstraint_psitvo = Set( 
      dimen=6, initialize=StorageConstraintIndices )
    M.StorageConstraint = Constraint( 
      M.StorageConstraint_psitvo, 
      rule=Storage_Constraint )

    #Hourly Storage     
    
    # Hourly Storage constraint   
    M.HourlyStorageConstraint_psdt = Set( 
      dimen=4, initialize=HourlyStorageConstraintIndices )
    M.HourlyStorageConstraint = Constraint( 
      M.HourlyStorageConstraint_psdt, 
      rule=HourlyStorage_Constraint )   
    
    # Hourly Storage Upper Bound
    M.HourlyStorageUpperBoundConstraint_psdt = Set( 
      dimen=4, initialize=HourlyStorageBoundConstraintIndices )
    M.HourlyStorageUpperBoundConstraint = Constraint( 
      M.HourlyStorageUpperBoundConstraint_psdt, 
      rule=HourlyStorage_UpperBound )   
    # Hourly Storage Lower Bound
    M.HourlyStorageLowerBoundConstraint_psdt = Set( 
      dimen=4, initialize=HourlyStorageBoundConstraintIndices )
    M.HourlyStorageLowerBoundConstraint = Constraint( 
      M.HourlyStorageLowerBoundConstraint_psdt, 
      rule=HourlyStorage_LowerBound )       
    
    # Hourly Storage Upper Bound on Charging
    M.HourlyStorageChargeUpperBoundConstraint_psdt = Set( 
      dimen=4, initialize=HourlyStorageBoundConstraintIndices )
    M.HourlyStorageChargeUpperBoundConstraint = Constraint( 
      M.HourlyStorageChargeUpperBoundConstraint_psdt, 
      rule=HourlyStorageCharge_UpperBound )   
    # Hourly Storage Lower Bound on Discharging
    M.HourlyStorageDischargeLowerBoundConstraint_psdt = Set( 
      dimen=4, initialize=HourlyStorageBoundConstraintIndices )
    M.HourlyStorageDischargeLowerBoundConstraint = Constraint( 
      M.HourlyStorageDischargeLowerBoundConstraint_psdt, 
      rule=HourlyStorageCharge_LowerBound )           
    
    #-----------------    

    M.RampUpConstraintDay_psdtv = Set( 
      dimen=5, initialize=RampConstraintDayIndices )
    M.RampUpConstraintDay = Constraint( 
      M.RampUpConstraintDay_psdtv, 
      rule=RampUpDay_Constraint )

    M.RampUpConstraintSeason_pstv = Set( 
      dimen=4, initialize=RampConstraintSeasonIndices )
    M.RampUpConstraintSeason = Constraint( 
      M.RampUpConstraintSeason_pstv, 
      rule=RampUpSeason_Constraint )

    M.RampUpConstraintPeriod_ptv = Set( 
      dimen=3, initialize=RampConstraintPeriodIndices )
    M.RampUpConstraintPeriod = Constraint( 
      M.RampUpConstraintPeriod_ptv, 
      rule=RampUpPeriod_Constraint )

    M.RampDownConstraintDay_psdtv = Set( 
      dimen=5, initialize=RampConstraintDayIndices )
    M.RampDownConstraintDay = Constraint( 
      M.RampDownConstraintDay_psdtv, 
      rule=RampDownDay_Constraint )

    M.RampDownConstraintSeason_pstv = Set( 
      dimen=4, initialize=RampConstraintSeasonIndices )
    M.RampDownConstraintSeason = Constraint( 
      M.RampDownConstraintSeason_pstv, 
      rule=RampDownSeason_Constraint )

    M.RampDownConstraintPeriod_ptv = Set( 
      dimen=3, initialize=RampConstraintPeriodIndices )
    M.RampDownConstraintPeriod = Constraint( 
      M.RampDownConstraintPeriod_ptv, 
      rule=RampDownPeriod_Constraint )

    M.ReserveMargin_pc = Set(
      dimen = 2, initialize=ReserveMarginIndices )
    M.ReserveMarginConstraint = Constraint(
      M.ReserveMargin_pc,
      rule=ReserveMargin_Constraint)

    # Constraints for user-defined limits
    M.EmissionLimitConstraint_pe = Set(
      dimen=2, initialize=lambda M: M.EmissionLimit.sparse_iterkeys() )
    M.EmissionLimitConstraint = Constraint( 
      M.EmissionLimitConstraint_pe, 
      rule=EmissionLimit_Constraint)

    from itertools import product
    M.GrowthRateMaxConstraint_tv = Set(
      dimen=2, initialize=lambda M: set(product( M.time_optimize, 
      M.GrowthRateMax.sparse_iterkeys() )) )
    M.GrowthRateConstraint = Constraint( 
      M.GrowthRateMaxConstraint_tv, 
      rule=GrowthRateConstraint_rule )

    M.MaxActivityConstraint_pt = Set(
      dimen=2, initialize=lambda M: M.MaxActivity.sparse_iterkeys() )
    M.MaxActivityConstraint = Constraint( 
      M.MaxActivityConstraint_pt, 
      rule=MaxActivity_Constraint )

    M.MinActivityConstraint_pt = Set(
      dimen=2, initialize=lambda M: M.MinActivity.sparse_iterkeys() ) 
    M.MinActivityConstraint = Constraint( 
      M.MinActivityConstraint_pt, 
      rule=MinActivity_Constraint )    

    M.MaxCapacityConstraint_pt = Set(
      dimen=2, initialize=lambda M: M.MaxCapacity.sparse_iterkeys() )
    M.MaxCapacityConstraint = Constraint( 
      M.MaxCapacityConstraint_pt, 
      rule=MaxCapacity_Constraint )

    M.MinCapacityConstraint_pt = Set(
      dimen=2, initialize=lambda M: M.MinCapacity.sparse_iterkeys() )
    M.MinCapacityConstraint = Constraint( 
      M.MinCapacityConstraint_pt, 
      rule=MinCapacity_Constraint )

    M.MinCapacitySetConstraint_p = Set(
      dimen=1, initialize=lambda M: M.MinCapacitySum.sparse_iterkeys() )
    M.MinCapacitySetConstraint = Constraint( 
      M.MinCapacitySetConstraint_p, 
      rule=MinCapacitySet_Constraint )    
    
    M.MaxCapacitySetConstraint_p = Set(
      dimen=1, initialize=lambda M: M.MaxCapacitySum.sparse_iterkeys() )
    M.MaxCapacitySetConstraint = Constraint( 
      M.MaxCapacitySetConstraint_p, 
      rule=MaxCapacitySet_Constraint )      
    
    M.TechInputSplitConstraint_psditv = Set(
      dimen=6, initialize=TechInputSplitConstraintIndices
      )
    M.TechInputSplitConstraint  = Constraint( 
      M.TechInputSplitConstraint_psditv,  
      rule=TechInputSplit_Constraint )

    M.TechOutputSplitConstraint_psdtvo = Set(
      dimen=6, initialize=TechOutputSplitConstraintIndices )
    M.TechOutputSplitConstraint = Constraint( 
      M.TechOutputSplitConstraint_psdtvo, 
      rule=TechOutputSplit_Constraint )


    return M



def runModelUI(config_filename):
    """This function launches the model run from the Temoa GUI"""

    model = temoa_create_model()
    solver = TemoaSolver(model, config_filename)
    for k in solver.createAndSolve():
        yield k
        #yield " " * 1024


def runModel():
    """This function launches the model run, and is invoked when called from
    __main__.py"""

    model = temoa_create_model()
    dummy = ''  # If calling from command line, send empty string  
    solver = TemoaSolver(model, dummy)
    for k in solver.createAndSolve():
        pass


if '__main__' == __name__:

    dummy = ''  # If calling from command line, send empty string 
    model = temoa_create_model()
    solver = TemoaSolver(model, dummy)
    solver.createAndSolve()
    # this code only invoked when called this file is invoked directly from the
    # command line as follows:
    # $ python temoa_model/temoa_model.py path/to/dat/file


