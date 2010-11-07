"""
    TEMOA (Tools for Energy Model Optimization and Analysis)
    Copyright (C) 2010 TEMOA Developer Team

    This file is part of TEMOA.
    TEMOA is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    TEMOA is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with TEMOA.  If not, see <http://www.gnu.org/licenses/>.
"""

from coopr.pyomo import *

import debug as D
from set_init    import *
from param_init  import *
from constraints import *
from objective   import *


#D.LEVEL = D.DEBUG
D.LEVEL = D.INFO
#D.LEVEL = D.NORMAL

model = Model( name='TEMOA ELC' )

# Set and parameter declarations
model.segment = Set() # demand segments, currently baseload, shoulder, and peak

model.tech_new      = Set() # only tech model can build.
model.tech_existing = Set() # only tech already "there" when model begins
model.tech_all      = model.tech_new | model.tech_existing

model.tech_all_by_seg = Set( model.segment )
model.tech_new_by_seg = Set( model.segment )
model.tech_existing_by_seg = Set( model.segment )

model.period  = Set()

model.invest_period    = Set( ordered=True, within=model.period, initialize=SetOperatingPeriod_Init )
model.operating_period = Set( ordered=True, within=model.period, initialize=SetOperatingPeriod_Init )

model.inter_period = Param( model.operating_period, initialize=ParamInterPeriod_Init )
model.urn_price    = Param( model.operating_period )
model.coal_price   = Param( model.operating_period )
model.diesel_price = Param( model.operating_period )
model.ng_price     = Param( model.operating_period )

model.tech_life  = Param( model.tech_all, initialize=TechLifeParam_Init )
model.loan_life  = Param( model.tech_new, initialize=LoanLifeParam_Init )

model.investment = Set( initialize=SetInvestmentPeriod_Init, dimen=3 ) # imat
model.vintage    = Param( model.tech_all, model.invest_period, model.operating_period, initialize=VintagePeriodParam_Init )    # vmat

model.co2_tot     = Param( model.operating_period )  # Total annual CO2 emissions in MmtCO2
model.cost_target = Param()
model.global_discount_rate = Param()

model.hydro_max_total     = Param()
model.geo_max_total       = Param()
model.winds_on_max_total  = Param()
model.winds_off_max_total = Param()
model.solar_th_max_total  = Param()


model.power_dmd   = Param( model.operating_period, model.segment ) # installed capacity (GW) required
model.energy_dmd  = Param( model.operating_period, model.segment ) # electricity generation (GWh) required

model.investment_costs = Param( model.tech_new, model.invest_period, model.operating_period, default=0 )     # C_i "technology investment cost"
model.fixed_costs      = Param( model.tech_all, model.invest_period, model.operating_period, default=0 )      # C_f "technology fixed cost"
model.marg_costs       = Param( model.tech_all, model.operating_period, initialize=MarginalCostsParam_Init ) # C_m "technology marginal cost"
model.cf_max           = Param( model.tech_all )
model.ratio            = Param( model.tech_all )
model.co2_factors      = Param( model.tech_all )
model.discount_rate    = Param( model.tech_all )
model.thermal_eff      = Param( model.tech_all )
model.t0_capacity      = Param( model.operating_period, model.tech_existing )

model.loan_cost     = Param( model.tech_new, rule=ParamLoanCost_Init )
model.period_spread = Param( model.operating_period, rule=ParamPeriodSpread_Init )

model.xc = Var( model.tech_new, model.invest_period,                         within=NonNegativeReals, bounds=(0, 1e50) )
model.xu = Var( model.tech_all, model.invest_period, model.operating_period, within=NonNegativeReals, bounds=(0, 1e50) )

model.PeriodCost = Var( model.operating_period, within=NonNegativeReals )

# Objective function(s)
def TotalCost ( model ):
	return sum( model.PeriodCost[ p ] for p in model.operating_period )
model.Total_Cost = Objective( rule=TotalCost, sense=minimize )



# Constraints
model.Energy_Demand = Constraint( model.segment, model.operating_period, rule=Energy_Demand )
model.Capacity      = Constraint( model.segment, model.operating_period, rule=Capacity_Req )

model.Process_Level_Activity = Constraint( model.tech_all, model.invest_period, model.operating_period, rule=Process_Level_Activity )

model.CO2_Emissions_Constraint = Constraint( model.operating_period, rule=CO2_Emissions_Constraint )

model.Up_Hydro      = Constraint( rule=Up_Hydro )
model.Up_Geo        = Constraint( rule=Up_Geo )
model.Up_Winds_Ons  = Constraint( rule=Up_Winds_Ons )
model.Up_Winds_Offs = Constraint( rule=Up_Winds_Offs )
model.Up_Solar_Th   = Constraint( rule=Up_Solar_Th )

###################################################

def setAnnualCosts ( per, model ):
	return model.PeriodCost[ per ] == AnnualCost( per, model )

model.ComputeAnnualCosts = Constraint( model.operating_period, rule=setAnnualCosts)

#                                 Debugging Additions                         #
###############################################################################
if D.LEVEL == D.INFO:
	model.curr_capacity = Var( model.segment, model.invest_period )
	model.INFO_Current_Capacity = Constraint( model.segment, model.invest_period, rule=INFO_Current_Capacity )

	model.total_curr_capacity = Var( model.invest_period )
	model.INFO_Total_Current_Capacity = Constraint( model.invest_period, rule=INFO_Total_Current_Capacity )

	model.new_capacity_per = Var( model.operating_period )
	model.INFO_new_capacity_per = Constraint( model.operating_period, rule=INFO_new_capacity_per )

	model.CO2_seg_per = Var( model.segment, model.invest_period, within=NonNegativeReals )
	model.INFO_CO2_seg_per = Constraint( model.segment, model.invest_period, rule=INFO_CO2_seg_per )

	model.CO2_per = Var( model.invest_period, within=NonNegativeReals )
	model.INFO_CO2_per = Constraint( model.invest_period, rule=INFO_CO2_per )

	model.total_CO2 = Var( within=NonNegativeReals )
	model.INFO_total_CO2 = Constraint( rule=INFO_total_CO2 )

	model.xu_summed_invest = Var( model.tech_all, model.operating_period, within=NonNegativeReals )
	model.INFO_xu_summed_invest = Constraint( model.tech_all, model.operating_period, rule=INFO_xu_summed_invest )
