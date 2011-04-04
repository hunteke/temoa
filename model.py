#!/usr/bin/env pyomo

__all__ = [ 'create_TEMOA_model', ]

from temoa_rules import *

def create_TEMOA_model ( ):
	M = AbstractModel('TEMOA Entire Energy System Economic Optimization Model')

	M.time_period     = Set()
	M.resource_tech   = Set()
	M.production_tech = Set()
	M.third           = Set()
	M.tech = M.resource_tech | M.production_tech  # '|' = union.

	M.vintage = M.time_period    # copy of time_period; used for technology vintaging

	M.emissions_commodity = Set()
	M.physical_commodity = Set()
	M.all_outputs = Set()
	M.demand_commodity = Set()

	# Pyomo currently has a rather large design flaw in it's implementation of set
	# unions, where it is not possible to create a union of more than two sets in
	# a single statement.  A bug report has been filed with the Coopr devs.
	#   - 24 Feb 2011
	M.tmp_set = M.physical_commodity | M.emissions_commodity
	M.all_commodities = M.tmp_set | M.demand_commodity


	M.Efficiency     = Param(M.all_commodities, M.tech, M.time_period, M.all_commodities, default=0)
	M.Lifetime       = Param(M.tech,        M.time_period,                      default=20) # 20 years
	M.Demand         = Param(M.time_period, M.demand_commodity,                 default=0)
	M.ResourceBound  = Param(M.time_period, M.physical_commodity,               default=0)
	M.CommodityProductionCost = Param(M.time_period, M.tech, M.time_period,     default=1)
	M.CapacityFactor = Param(M.time_period, M.tech, M.time_period, M.all_commodities, default=1)

	# Not yet indexed by period or incorporated into the constraints
	M.EmissionsLimit = Param(M.emissions_commodity, default=0)


	# Variables
	#   Decision variables
	M.V_FlowIn  = Var(M.time_period, M.all_commodities, M.tech, M.vintage, M.all_commodities, domain=NonNegativeReals)
	M.V_FlowOut = Var(M.time_period, M.all_commodities, M.tech, M.vintage, M.all_commodities, domain=NonNegativeReals)

	#   Calculated "dummy" variables
	M.V_Activity = Var(M.time_period, M.tech, M.vintage, M.all_commodities, domain=NonNegativeReals)
	M.V_Capacity = Var(M.time_period, M.tech, M.vintage, M.all_commodities, domain=NonNegativeReals)


	# Objective
	M.TotalCost = Objective(rule=TotalCost_rule, sense=minimize)

	# Constraints

	#   "Bookkeeping" constraints
	M.ActivityConstraint = Constraint( M.time_period, M.tech, M.vintage, M.all_commodities, rule=ActivityConstraint_rule )
	M.CapacityConstraint = Constraint( M.time_period, M.tech, M.vintage, M.all_commodities, rule=CapacityConstraint_rule )

	#   Model Constraints
	#    - in driving order.  (e.g., without Demand, none of the others are
	#      very useful.
	M.DemandConstraint             = Constraint( M.time_period, M.demand_commodity,      rule=DemandConstraint_rule )
	M.ProcessBalanceConstraint     = Constraint( M.time_period, M.all_commodities, M.tech, M.vintage, M.all_commodities, rule=ProcessBalanceConstraint_rule )
	M.CommodityBalanceConstraint   = Constraint( M.time_period, M.physical_commodity,    rule=CommodityBalanceConstraint_rule )
	M.ResourceExtractionConstraint = Constraint( M.time_period, M.physical_commodity,    rule=ResourceExtractionConstraint_rule )

	#   Constraints not yet updated
	#M.EmissionConstraint           = Constraint(M.emissions_commodity,            rule=EmissionConstraint_rule)
	#M.ResourceBalanceConstraint    = Constraint(M.physical_commodity,             rule=ResourceBalanceConstraint_rule)
	return M

model = create_TEMOA_model()


if '__main__' == __name__:
	from sys import argv, stderr

	from coopr.opt import SolverFactory
	from coopr.pyomo import ModelData

	from pformat_results import pformat_results

	SE = stderr

	if len( argv ) < 2:
		SE.write( "No data file (dot dat) specified.  Exiting.\n" )
		raise SystemExit

	opt = SolverFactory('glpk_experimental')
	opt.keepFiles = False
	# opt.options.wlp = "an.lp"    # output GLPK's LP understanding.

	# Recreate the pyomo command's ability to specify multiple "dot dat" files
	# on the command line
	mdata = ModelData()
	for f in argv[1:]:
		if f[-4:] != '.dat':
			SE.write( "Expecting a dot dat (data.dat) file, found %s\n" % f )
			raise SystemExit
		mdata.add( f )
	mdata.read( model )

	# Now do the solve and ...
	instance = model.create( mdata )
	result = opt.solve( instance )

	# ... print the easier-to-read/parse format
	print pformat_results( instance, result )
