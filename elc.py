import sys


sys.path = ['', '/home/kevin/ram/coopr/lib/python2.6/site-packages/setuptools-0.6c11-py2.6.egg', '/home/kevin/ram/coopr/lib/python2.6/site-packages/pip-0.6.3-py2.6.egg', '/home/kevin/ram/coopr/lib/python2.6/site-packages/virtualenv-1.4.5-py2.6.egg', '/home/kevin/ram/coopr/lib/python2.6/site-packages/nose-0.11.3-py2.6.egg', '/home/kevin/ram/coopr/lib/python2.6/site-packages/unittest2-0.3.0-py2.6.egg', '/home/kevin/ram/coopr/lib/python2.6/site-packages/bidict-0.1.1-py2.6.egg', '/home/kevin/ram/coopr/lib/python2.6/site-packages/ply-3.3-py2.6.egg', '/home/kevin/ram/coopr/src/pyutilib.common', '/home/kevin/ram/coopr/src/pyutilib.th', '/home/kevin/ram/coopr/src/pyutilib.enum', '/home/kevin/ram/coopr/src/pyutilib.excel', '/home/kevin/ram/coopr/src/pyutilib.math', '/home/kevin/ram/coopr/src/pyutilib.misc', '/home/kevin/ram/coopr/src/pyutilib.ply', '/home/kevin/ram/coopr/src/pyutilib.pyro', '/home/kevin/ram/coopr/src/pyutilib.R', '/home/kevin/ram/coopr/src/pyutilib.component.core', '/home/kevin/ram/coopr/src/pyutilib.component.config', '/home/kevin/ram/coopr/src/pyutilib.component.executables', '/home/kevin/ram/coopr/src/pyutilib.component.app', '/home/kevin/ram/coopr/src/pyutilib.component.loader', '/home/kevin/ram/coopr/src/pyutilib.services', '/home/kevin/ram/coopr/src/pyutilib.virtualenv', '/home/kevin/ram/coopr/src/pyutilib.subprocess', '/home/kevin/ram/coopr/src/pyutilib.dev', '/home/kevin/ram/coopr/src/coopr.misc', '/home/kevin/ram/coopr/src/coopr.opt', '/home/kevin/ram/coopr/src/coopr.colin', '/home/kevin/ram/coopr/src/coopr.plugins', '/home/kevin/ram/coopr/src/coopr.pyomo', '/home/kevin/ram/coopr/src/coopr.pysos', '/home/kevin/ram/coopr/src/coopr.pysp', '/home/kevin/ram/coopr/src/coopr.sucasa', '/home/kevin/ram/coopr/src/coopr', '/home/kevin/devel/djangologging', '/home/kevin/devel/mathtex', '/home/kevin/.local/lib/python2.6/site-packages', '/home/kevin/ram/coopr/lib/python2.6', '/home/kevin/ram/coopr/lib/python2.6/plat-linux2', '/home/kevin/ram/coopr/lib/python2.6/lib-tk', '/home/kevin/ram/coopr/lib/python2.6/lib-old', '/home/kevin/ram/coopr/lib/python2.6/lib-dynload', '/usr/lib/python2.6', '/usr/lib64/python2.6', '/usr/lib/python2.6/plat-linux2', '/usr/lib/python2.6/lib-tk', '/usr/lib64/python2.6/lib-tk', '/home/kevin/ram/coopr/lib/python2.6/site-packages', '/usr/bin', '/usr/local/lib/python2.6/dist-packages/VTK-5.4.2-py2.6.egg', '/home/kevin/devel/djangologging', '/home/kevin/devel/mathtex', '/home/kevin/.local/lib/python2.6/site-packages', '/usr/lib/python2.6', '/usr/lib/python2.6/plat-linux2', '/usr/lib/python2.6/lib-tk', '/usr/lib/python2.6/lib-old', '/usr/lib/python2.6/lib-dynload', '/usr/lib/python2.6/dist-packages', '/usr/lib/python2.6/dist-packages/PIL', '/usr/lib/python2.6/dist-packages/gst-0.10', '/usr/lib/pymodules/python2.6', '/usr/lib/python2.6/dist-packages/gtk-2.0', '/usr/lib/pymodules/python2.6/gtk-2.0', '/usr/lib/python2.6/dist-packages/wx-2.8-gtk2-unicode', '/usr/local/lib/python2.6/dist-packages', '/usr/lib/pymodules/python2.6/IPython/Extensions', u'/home/kevin/.ipython']
#from IPython.Shell import IPShellEmbed
#ipshell = IPShellEmbed()

from coopr.pyomo import *

import debug as D
from set_init    import *
from param_init  import *
from constraints import *
from objective   import *


#Debugging
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
model.invest_period = Set( within=model.period )
model.munge_period = Set( ordered=True, within=model.period )
model.munge_period.initialize = SetMungePeriod_Init

#model.invest_period.initialize = PeriodSet_Init

# model.segment = Set()
# model.segment.initialize = SegmentSet_Init

# set defining demand segments as baseload, shoulder, peak
model.b_slice = Set() # base load subset
model.s_slice = Set() # shoulder load subset
model.p_slice = Set() # peak load subset
model.slice = Set()

model.inter_period = Param( model.munge_period, initialize=ParamInterPeriod_Init )
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
model.Baseload_Energy_Demand = Constraint( model.b_slice, model.munge_period, rule=Baseload_Energy_Demand )
model.Shoulder_Energy_Demand = Constraint( model.s_slice, model.munge_period, rule=Shoulder_Energy_Demand )
model.Peakload_Energy_Demand = Constraint( model.p_slice, model.munge_period, rule=Peakload_Energy_Demand )

model.Baseload_Capacity = Constraint( model.b_slice, model.munge_period, rule=Baseload_Capacity_Req )
model.Shoulder_Capacity = Constraint( model.s_slice, model.munge_period, rule=Shoulder_Capacity_Req )
model.Peakload_Capacity = Constraint( model.p_slice, model.munge_period, rule=Peakload_Capacity_Req )

model.Process_Level_Activity = Constraint( model.tech_all, model.munge_period, model.munge_period, rule=Process_Level_Activity )

model.CO2_Emissions_Constraint = Constraint( model.munge_period, rule=CO2_Emissions_Constraint )

model.Up_Hydro      = Constraint( rule=Up_Hydro )
model.Up_Geo        = Constraint( rule=Up_Geo )
model.Up_Winds_Ons  = Constraint( rule=Up_Winds_Ons )
model.Up_Winds_Offs = Constraint( rule=Up_Winds_Offs )
model.Up_Solar_Th   = Constraint( rule=Up_Solar_Th )

