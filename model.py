#!/usr/bin/env python

__all__ = [ 'create_TEMOA_model', ]

from temoa_rules import *

def create_TEMOA_model ( ):
	M = AbstractModel('TEMOA Entire Energy System Economic Optimization Model')

	M.time_period     = Set( ordered=True, within=Integers )
	M.time_season     = Set()
	M.time_of_day     = Set()
	M.resource_tech   = Set()
	M.production_tech = Set()
	M.tech = M.resource_tech | M.production_tech  # '|' = union.

	M.window_period         = Param( Set(initialize=['begin', 'final'] ), within=M.time_period )
	M.exist_period          = Set( ordered=True, within=M.time_period, initialize=init_exist_set )
	M.future_period         = Set( ordered=True, within=M.time_period, initialize=init_future_set )
	M.beyond_horizon_period = Set( ordered=True, within=M.time_period, initialize=init_future_set )

	M.vintage    = M.time_period    # intentional copy of time_period, for easier bookkeeping
	M.exist_vintage  = M.exist_period
	M.future_vintage = M.vintage - M.exist_vintage

	M.optimize_period = M.future_period | M.beyond_horizon_period

	M.emissions_commodity = Set()
	M.physical_commodity = Set()
	M.demand_commodity = Set()

	# Pyomo currently has a rather large design flaw in it's implementation of set
	# unions, where it is not possible to create a union of more than two sets in
	# a single statement.  A bug report has been filed with the Coopr devs.
	#   - 24 Feb 2011
	M.tmp_set = M.physical_commodity | M.emissions_commodity
	M.all_commodities = M.tmp_set | M.demand_commodity


	M.ExistingCapacity = Param(M.tech, M.exist_vintage, default=0)
	M.Efficiency       = Param(M.all_commodities, M.tech, M.vintage, M.all_commodities, default=0)
	M.Lifetime         = Param(M.tech,        M.vintage,                  default=20) # 20 years
	M.Demand           = Param(M.time_period, M.time_season, M.time_of_day, M.demand_commodity,   default=0)
	M.ResourceBound    = Param(M.time_period, M.physical_commodity,       default=0)
	M.CommodityProductionCost = Param(M.time_period, M.tech, M.vintage,   default=1)
	M.CapacityFactor   = Param(M.tech, M.vintage,                         default=1)


	# Not yet indexed by period or incorporated into the constraints
	M.EmissionsLimit = Param(M.emissions_commodity, default=0)


	# Variables
	#   Decision variables
	M.V_FlowIn  = Var(M.time_period, M.time_season, M.time_of_day, M.all_commodities, M.tech, M.vintage, M.all_commodities, domain=NonNegativeReals)
	M.V_FlowOut = Var(M.time_period, M.time_season, M.time_of_day, M.all_commodities, M.tech, M.vintage, M.all_commodities, domain=NonNegativeReals)

	#   Calculated "dummy" variables
	M.V_Activity = Var(M.optimize_period, M.time_season, M.time_of_day, M.tech, M.vintage, domain=NonNegativeReals)
	M.V_Capacity = Var(M.tech, M.vintage, domain=NonNegativeReals)


	# Objective
	M.TotalCost = Objective(rule=TotalCost_rule, sense=minimize)

	# Constraints

	#   "Bookkeeping" constraints
	M.ActivityConstraint = Constraint( M.optimize_period, M.time_season, M.time_of_day, M.tech, M.vintage, rule=ActivityConstraint_rule )
	M.CapacityConstraint = Constraint( M.optimize_period, M.time_season, M.time_of_day, M.tech, M.vintage, rule=CapacityConstraint_rule )

	M.ExistingCapacityConstraint = Constraint( M.optimize_period, M.tech, M.exist_vintage, rule=ExistingCapacityConstraint_rule )

	#   Model Constraints
	#    - in driving order.  (e.g., without Demand, none of the others are
	#      very useful.)
	M.DemandConstraint             = Constraint( M.time_period, M.time_season, M.time_of_day, M.demand_commodity,      rule=DemandConstraint_rule )
	M.ProcessBalanceConstraint     = Constraint( M.time_period, M.time_season, M.time_of_day, M.all_commodities, M.tech, M.vintage, M.all_commodities, rule=ProcessBalanceConstraint_rule )
	M.CommodityBalanceConstraint   = Constraint( M.time_period, M.time_season, M.time_of_day, M.physical_commodity,    rule=CommodityBalanceConstraint_rule )
	M.ResourceExtractionConstraint = Constraint( M.time_period, M.physical_commodity,    rule=ResourceExtractionConstraint_rule )

	#   Constraints not yet updated
	#M.EmissionConstraint           = Constraint(M.emissions_commodity,            rule=EmissionConstraint_rule)
	#M.ResourceBalanceConstraint    = Constraint(M.physical_commodity,             rule=ResourceBalanceConstraint_rule)
	return M

model = create_TEMOA_model()


if '__main__' == __name__:
	from sys import argv, stderr, stdout

	from coopr.opt import SolverFactory
	from coopr.pyomo import ModelData

	from pformat_results import pformat_results

	SE, SO = stderr.write, stdout.write

	if len( argv ) < 2:
		SE( "No data file (dot dat) specified.  Exiting.\n" )
		raise SystemExit

	opt = SolverFactory('glpk_experimental')
	opt.keepFiles = False
	# opt.options.wlp = "temoa_model.lp"  # output GLPK LP understanding of model

	# Recreate the pyomo command's ability to specify multiple "dot dat" files
	# on the command line
	mdata = ModelData()
	for f in argv[1:]:
		if f[-4:] != '.dat':
			SE( "Expecting a dot dat (data.dat) file, found %s\n" % f )
			raise SystemExit
		mdata.add( f )
	mdata.read( model )

	# Now do the solve and ...
	instance = model.create( mdata )
	result = opt.solve( instance )

	# ... print the easier-to-read/parse format
	SO( pformat_results( instance, result ) )
