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

model.tech_all      = Set() # union of existing and new
model.tech_new      = Set() # contains below base, shoulder, and peak
model.tech_existing = Set()

model.tech_all_base     = Set()
model.tech_all_shoulder = Set()
model.tech_all_peak     = Set()
model.tech_new_base     = Set()
model.tech_new_shoulder = Set()
model.tech_new_peak     = Set()

model.period  = Set()
model.invest_period = Set( within=model.period, initialize=SetPeriod_Init )
model.operating_period = Set( ordered=True, within=model.period )
model.operating_period.initialize = SetMungePeriod_Init

# model.segment = Set()
# model.segment.initialize = SegmentSet_Init

# set defining demand segments as baseload, shoulder, peak
model.b_slice = Set() # base load subset
model.s_slice = Set() # shoulder load subset
model.p_slice = Set() # peak load subset
model.slice = Set()

model.inter_period = Param( model.operating_period, initialize=ParamInterPeriod_Init )
model.fuel_price = Param( model.tech_all, model.period )
model.tech_life  = Param( model.tech_all, initialize=TechLifeParam_Init )
model.loan_life  = Param( model.tech_new, initialize=LoanLifeParam_Init )
model.investment = Param( model.tech_new, model.invest_period, model.period, initialize=InvestmentPeriodParam_Init ) # imat
model.vintage    = Param( model.tech_all, model.invest_period, model.period, initialize=VintagePeriodParam_Init )    # vmat

model.co2_tot     = Param( model.period )  # Total 2100 CO2 emissions in MmtCO2
model.cost_target = Param()
model.global_discount_rate = Param()

model.hydro_max_total     = Param()
model.geo_max_total       = Param()
model.winds_on_max_total  = Param()
model.winds_off_max_total = Param()
model.solar_th_max_total  = Param()

model.power_dmd   = Param( model.period, model.slice ) # installed capacity (GW) required
model.energy_dmd  = Param( model.period, model.slice ) # electricity generation (GWh) required

model.investment_costs = Param( model.tech_new, model.invest_period, model.period, initialize=InvestmentCostsParam_Init ) # C_i "technology investment cost"
model.fixed_costs      = Param( model.tech_all, model.invest_period, model.period, initialize=FixedCostsParam_Init )      # C_f "technology fixed cost"
model.marg_costs       = Param( model.tech_all, model.invest_period, model.period, initialize=MarginalCostsParam_Init )   # C_m "technology marginal cost"
model.cf_max           = Param( model.tech_all )
model.ratio            = Param( model.tech_all )
model.co2_factors      = Param( model.tech_all )
model.discount_rate    = Param( model.tech_all )
model.thermal_eff      = Param( model.tech_all )

model.xc = Var( model.tech_new, model.invest_period,               within=NonNegativeReals )
model.xu = Var( model.tech_all, model.invest_period, model.period, within=NonNegativeReals )

# Objective function(s)

model.Total_Cost = Objective( rule=Objective_Rule, sense=minimize )


# Constraints
model.Baseload_Energy_Demand = Constraint( model.b_slice, model.operating_period, rule=Baseload_Energy_Demand )
model.Shoulder_Energy_Demand = Constraint( model.s_slice, model.operating_period, rule=Shoulder_Energy_Demand )
model.Peakload_Energy_Demand = Constraint( model.p_slice, model.operating_period, rule=Peakload_Energy_Demand )

model.Baseload_Capacity = Constraint( model.b_slice, model.operating_period, rule=Baseload_Capacity_Req )
model.Shoulder_Capacity = Constraint( model.s_slice, model.operating_period, rule=Shoulder_Capacity_Req )
model.Peakload_Capacity = Constraint( model.p_slice, model.operating_period, rule=Peakload_Capacity_Req )

model.Process_Level_Activity = Constraint( model.tech_all, model.operating_period, model.operating_period, rule=Process_Level_Activity )

model.CO2_Emissions_Constraint = Constraint( model.operating_period, rule=CO2_Emissions_Constraint )

model.Up_Hydro      = Constraint( rule=Up_Hydro )
model.Up_Geo        = Constraint( rule=Up_Geo )
model.Up_Winds_Ons  = Constraint( rule=Up_Winds_Ons )
model.Up_Winds_Offs = Constraint( rule=Up_Winds_Offs )
model.Up_Solar_Th   = Constraint( rule=Up_Solar_Th )

