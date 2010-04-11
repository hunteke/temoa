from coopr.pyomo import *

import debug as D
from set_init    import *
from param_init  import *
from constraints import *
from objective   import *


#D.LEVEL = D.INFO
D.LEVEL = D.NORMAL

model = Model()

# Set and parameter declarations
model.segment = Set() # demand segments, currently baseload, shoulder, and peak

model.tech_new      = Set() # only tech model can build.
model.tech_existing = Set() # only tech already "there" when model begins
model.tech_all      = model.tech_new | model.tech_existing

model.tech_all_by_seg = Set( model.segment )
model.tech_new_by_seg = Set( model.segment )

model.period  = Set()

model.invest_period = Set( within=model.period, initialize=SetPeriod_Init )
model.operating_period = Set( ordered=True, within=model.period, initialize=SetOperatingPeriod_Init )

model.inter_period = Param( model.operating_period, initialize=ParamInterPeriod_Init )
model.fuel_price = Param( model.tech_all, model.period )
model.tech_life  = Param( model.tech_all, initialize=TechLifeParam_Init )
model.loan_life  = Param( model.tech_new, initialize=LoanLifeParam_Init )

model.investment = Set( initialize=SetInvestmentPeriod_Init, dimen=3 ) # imat
model.vintage    = Param( model.tech_all, model.invest_period, model.period, initialize=VintagePeriodParam_Init )    # vmat

model.co2_tot     = Param( model.period )  # Total annual CO2 emissions in MmtCO2
model.cost_target = Param()
model.global_discount_rate = Param()

model.hydro_max_total     = Param()
model.geo_max_total       = Param()
model.winds_on_max_total  = Param()
model.winds_off_max_total = Param()
model.solar_th_max_total  = Param()


model.power_dmd   = Param( model.period, model.segment ) # installed capacity (GW) required
model.energy_dmd  = Param( model.period, model.segment ) # electricity generation (GWh) required

model.investment_costs = Param( model.tech_new, model.invest_period, model.period, initialize=InvestmentCostsParam_Init ) # C_i "technology investment cost"
model.fixed_costs      = Param( model.tech_all, model.invest_period, model.period, initialize=FixedCostsParam_Init )      # C_f "technology fixed cost"
model.marg_costs       = Param( model.tech_all, model.invest_period, model.period, initialize=MarginalCostsParam_Init )   # C_m "technology marginal cost"
model.cf_max           = Param( model.tech_all )
model.ratio            = Param( model.tech_all )
model.co2_factors      = Param( model.tech_all )
model.discount_rate    = Param( model.tech_all )
model.thermal_eff      = Param( model.tech_all )

model.loan_cost     = Param( model.tech_new, rule=ParamLoanCost_Init )
model.period_spread = Param( model.operating_period, rule=ParamPeriodSpread_Init )

model.xc = Var( model.tech_new, model.invest_period,               within=NonNegativeReals )
model.xu = Var( model.tech_all, model.invest_period, model.period, within=NonNegativeReals )

# Objective function(s)

model.Total_Cost = Objective( rule=Objective_Rule, sense=minimize )


# Constraints
model.Energy_Demand = Constraint( model.segment, model.operating_period, rule=Energy_Demand )
model.Capacity      = Constraint( model.segment, model.operating_period, rule=Capacity_Req )

model.Process_Level_Activity = Constraint( model.tech_all, model.operating_period, model.operating_period, rule=Process_Level_Activity )

model.CO2_Emissions_Constraint = Constraint( model.operating_period, rule=CO2_Emissions_Constraint )

model.Up_Hydro      = Constraint( rule=Up_Hydro )
model.Up_Geo        = Constraint( rule=Up_Geo )
model.Up_Winds_Ons  = Constraint( rule=Up_Winds_Ons )
model.Up_Winds_Offs = Constraint( rule=Up_Winds_Offs )
model.Up_Solar_Th   = Constraint( rule=Up_Solar_Th )

