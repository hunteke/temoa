#!/usr/bin/env pyomo

from coopr.pyomo import *

##############################################################################
# Model methods
#

def TotalCost_rule ( M ):
	"""
An objective function.  For now, a simple summation of the ProcessUse variable
and associated costs.
"""
	cost = 0
	for l_process in M.AllProcesses:
		cost += M.V_ProcessUse[ l_process ] * M.ProcessCost[ l_process ]

	return cost

# not strictly necessary, but allows referencing it by another name
Objective_rule = TotalCost_rule

def DemandConstraint_rule ( A_process, M ):
	""" Constraint
One of 3 core constraints, this one setting the end-use demands per the datum.
The other core constraints are ProcessConstraint and DemandProcessConstraint.
"""

	l_demand = 0
	for l_output_process in M.EnergySink:
		l_demand += M.V_EnergyFlow[A_process, l_output_process]

	expression = ( l_demand >= M.Demand[ A_process ] )
	return expression

def DemandProcessConstraint_rule ( A_demand, M ):
	""" Constraint
One of 3 core constraints, this one ensuring that end-use demands are met.  The
other two core constraints are ProcessConstraint and DemandConstraint.
"""

	l_units_in = l_units_out = 0
	for l_carrier in M.EnergyCarrier:
		if 1 == M.ProcessConsumes[A_demand, l_carrier]:
			for l_source in M.InputProcess:
				if 1 == M.ProcessProduces[l_source, l_carrier]:
					l_units_in += M.V_EnergyFlow[l_source, A_demand]

	for l_sink in M.EnergySink:
		l_units_out += M.V_EnergyFlow[A_demand, l_sink]

	expression = ( l_units_in >= l_units_out )
	return expression

def ProcessConstraint_rule ( A_process, M ):
	""" Constraint
One of 2 constraints, this one ensuring that the total amount of energy
carriers entering a process at least meets what is leaving.
"""

	l_units_in = l_units_out = 0
	for l_carrier in M.EnergyCarrier:
		if 1 == M.ProcessConsumes[A_process, l_carrier]:
			for l_source in M.AllProcesses:
				if 1 == M.ProcessProduces[l_source, l_carrier]:
					l_units_in += M.V_EnergyFlow[l_source, A_process]

	for l_carrier in M.EnergyCarrier:
		if 1 == M.ProcessProduces[A_process, l_carrier]:
			for l_sink in M.AllProcesses:
				if 1 == M.ProcessConsumes[l_sink, l_carrier]:
					l_units_out += M.V_EnergyFlow[A_process, l_sink]

	expression = ( l_units_in >= l_units_out )
	return expression


def ProcessUseConstraint_rule ( A_process, M ):
	""" Constraint
Set ProcessUse[ process ] equal to the amount of incoming energy carrier.  This
allows us to use ProcessUse[ process ] as a proxy for each process.
"""

	l_units = 0
	for l_carrier in M.EnergyCarrier:
		if 1 == M.ProcessProduces[A_process, l_carrier]:
			for l_output_process in M.AllProcesses:
				if 1 == M.ProcessConsumes[l_output_process, l_carrier]:
					l_units += M.V_EnergyFlow[A_process, l_output_process]

	expression = ( l_units == M.V_ProcessUse[ A_process ] )
	return expression

def ResourceConstraint_rule ( A_process, M ):
	""" Constraint
For each (physical) resource, ensure that no more than an exogenously decided
amount may be mined, harvested, drilled.  For example, if there is only 500
barrels of oil in a well, it is impossible harvest 1000 barrels from it.
"""

	l_res_production = 0
	for l_input_process in M.EnergySource:
		l_res_production += M.V_EnergyFlow[l_input_process, A_process]

	expression = ( l_res_production <= M.ResourceBound[ A_process ] )
	return expression



##############################################################################
# Model definition

model = AbstractModel( name='TEMOA, Entire Energy System' )
M = model  # Coopr expects to see 'model', but I'm lazy;
           # a capital emm 'M' = less typing.  :-)

# Set definitions
M.EnergySource  = Set()
M.EnergySink    = Set()
M.EnergyCarrier = Set()
M.ResourceProcess = Set()
M.MiddleProcess = Set()
M.DemandProcess = Set()

M.InputProcess  = M.MiddleProcess | M.ResourceProcess
M.OutputProcess = M.MiddleProcess | M.DemandProcess
M.AllProcesses  = M.OutputProcess | M.InputProcess
M.AllProcesses.add('SINK')    # Hack; not sure how to add to a Set.
M.AllProcesses.add('SOURCE')  # ditto.  (See dot dat file's EnergySource/Sink)

# Variable definitions
M.V_EnergyFlow = Var( M.AllProcesses, M.AllProcesses, domain=NonNegativeReals )
M.V_ProcessUse = Var( M.AllProcesses, domain=NonNegativeReals )

# Parameter definitions
M.ResourceBound = Param( M.ResourceProcess, default=1000 )
M.ProcessCost   = Param( M.AllProcesses, default=10 )
M.Efficiency    = Param( M.AllProcesses, M.AllProcesses, default=0 )
M.Demand        = Param( M.DemandProcess, default=1 )

 # Binary matrixes, enabling what a process exports.  Unless otherwise stated
 # (in the data), a process does not export any energy carrier.  (Default=0)
M.ProcessConsumes = Param( M.AllProcesses, M.EnergyCarrier, default=0 )
M.ProcessProduces = Param( M.AllProcesses, M.EnergyCarrier, default=0 )

# An objective is all Pyomo needs to write a legal LP file
M.TotalCost = Objective( rule=TotalCost_rule, sense=minimize )

M.ProcessUseConstraint = Constraint( M.AllProcesses,    rule=ProcessUseConstraint_rule )
M.ResourceConstraint   = Constraint( M.ResourceProcess, rule=ResourceConstraint_rule )
M.DemandConstraint     = Constraint( M.DemandProcess,   rule=DemandConstraint_rule )
M.ProcessConstraint    = Constraint( M.MiddleProcess,   rule=ProcessConstraint_rule )
M.DemandProcessConstraint = Constraint( M.DemandProcess, rule=DemandProcessConstraint_rule )
