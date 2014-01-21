"""
Temoa - Tools for Energy Model Optimization and Analysis
  linear optimization; least cost; dynamic system visualization

Copyright (C) 2011-2014  Kevin Hunter, Joseph DeCarolis

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

__all__ = ('pformat_results', 'stringify_data')

from collections import defaultdict
from cStringIO import StringIO
from sys import stderr as SE, stdout as SO

from coopr.pyomo import value

def get_int_padding ( obj ):
	val = obj[ 1 ]         # obj is 2-tuple, with type(item[ 1 ]) == number
	return len(str(int(val)))
def get_dec_padding ( obj ):
	val = abs(obj[ 1 ])    # obj is 2-tuple, with type(item[ 1 ]) == number
	return len(str(val - int(val)))


def stringify_data ( data, ostream=SO, format='plain' ):
	# data is a list of tuples of ('var_name[index]', value)
	# this function iterates over the list multiple times, so it must at least
	# be reiterable
	# format is currently unused, but will be utilized to implement things like
	# csv

	# This padding code is what makes the display of the output values
	# line up on the decimal point.
	int_padding = max(map( get_int_padding, data ))
	dec_padding = max(map( get_dec_padding, data ))
	format = "  %%%ds%%-%ds  %%s\n" % (int_padding, dec_padding)
		# Works out to something like "%8d%-11s  %s"

	for key, val in data:
		int_part = int(abs(val))
		dec_part = str(abs(val) - int_part)[1:]  # remove (negative and) 0
		if val < 0: int_part = "-%d" % int_part
		ostream.write( format % (int_part, dec_part, key) )


def calculate_reporting_variables ( instance, ostream=SO ):
	variables = defaultdict( lambda: defaultdict( float ))
	epsilon = 1e-9   # threshold for "so small it's zero"

	m = instance   # lazy typist ...

	emission_keys = { (i, t, v, o) : e for e, i, t, v, o in m.EmissionActivity }

	for p, s, d, i, t, v, o in m.V_FlowOut:
		oval = value( m.V_FlowOut[p, s, d, i, t, v, o] )
		if abs(oval) < epsilon: continue

		variables['V_ActivityByInputAndTech'          ][i, t]       += oval
		variables['V_ActivityByPeriodAndTech'         ][p, t]       += oval
		variables['V_ActivityByTechAndOutput'         ][t, o]       += oval
		variables['V_ActivityByProcess'               ][t, v]       += oval
		variables['V_ActivityByPeriodInputAndTech'    ][p, i, t]    += oval
		variables['V_ActivityByPeriodTechAndOutput'   ][p, t, o]    += oval
		variables['V_ActivityByPeriodAndProcess'      ][p, t, v]    += oval
		variables['V_ActivityByPeriodInputAndProcess' ][p, i, t, v] += oval
		variables['V_ActivityByPeriodProcessAndOutput'][p, t, v, o] += oval

		if (i, t, v, o) not in emission_keys: continue

		e = emission_keys[i, t, v, o]
		evalue = oval * m.EmissionActivity[e, i, t, v, o]

		variables[ 'V_EmissionActivityByPeriod'         ][ p ]  += evalue
		variables[ 'V_EmissionActivityByTech'           ][ t ]  += evalue
		variables[ 'V_EmissionActivityByPeriodAndTech'  ][p, t] += evalue
		variables[ 'V_EmissionActivityByTechAndVintage' ][t, v] += evalue

	for p, s, d, i, t, v, o in m.V_FlowIn:
		ival = value( m.V_FlowIn[p, s, d, i, t, v, o] )
		if abs(ival) < epsilon: continue

		variables['V_EnergyConsumptionByTech'               ][ t ]     += ival
		variables['V_EnergyConsumptionByPeriodAndTech'      ][p, t]    += ival
		variables['V_EnergyConsumptionByTechAndOutput'      ][t, o]    += ival
		variables['V_EnergyConsumptionByPeriodAndProcess'   ][p, t, v] += ival
		variables['V_EnergyConsumptionByPeriodInputAndTech' ][p, i, t] += ival
		variables['V_EnergyConsumptionByPeriodTechAndOutput'][p, t, o] += ival

	P_0 = min( m.time_optimize )
	GDR = value( m.GlobalDiscountRate )
	for t, v in m.CostInvest.sparse_iterkeys():
		# CostInvest guaranteed not 0

		icost = value( m.V_Capacity[t, v] )
		if abs(icost) < epsilon: continue

		icost *= value( m.CostInvest[t, v] )
		variables[ 'V_UndiscountedInvestmentByPeriod'  ][ v ]  += icost
		variables[ 'V_UndiscountedInvestmentByTech'    ][ t ]  += icost
		variables[ 'V_UndiscountedInvestmentByProcess' ][t, v] += icost
		variables[ 'V_UndiscountedPeriodCost'          ][ v ]  += icost


		icost *= value( m.LoanAnnualize[t, v] )
		icost *= sum(
		  (1 + GDR) ** -y
		  for y in range( v - P_0,
		                  v - P_0 + value( m.ModelLoanLife[t, v] ))
		)
		variables[ 'V_DiscountedInvestmentByPeriod'  ][ v ]  += icost
		variables[ 'V_DiscountedInvestmentByTech'    ][ t ]  += icost
		variables[ 'V_DiscountedInvestmentByProcess' ][t, v] += icost
		variables[ 'V_DiscountedPeriodCost'          ][ v ]  += icost

	for p, t, v in m.CostFixed.sparse_iterkeys():
		fcost = value( m.V_Capacity[t, v] )
		if abs(fcost) < epsilon: continue

		fcost *= value( m.CostFixed[p, t, v] )
		variables[ 'V_UndiscountedFixedCostsByPeriod'  ][ p ]  += fcost
		variables[ 'V_UndiscountedFixedCostsByTech'    ][ t ]  += fcost
		variables[ 'V_UndiscountedFixedCostsByVintage' ][ v ]  += fcost
		variables[ 'V_UndiscountedFixedCostsByProcess' ][t, v] += fcost
		variables[ 'V_UndiscountedFixedCostsByPeriodAndProcess' ][p, t, v] = fcost
		variables[ 'V_UndiscountedPeriodCost'          ][ p ]  += fcost

		fcost *= sum(
		  (1 + GDR) ** -y
		  for y in range( p - P_0,
		                  p - P_0 + value( m.ModelTechLife[p, t, v] ))
		)
		variables[ 'V_DiscountedFixedCostsByPeriod'  ][ p ]  += fcost
		variables[ 'V_DiscountedFixedCostsByTech'    ][ t ]  += fcost
		variables[ 'V_DiscountedFixedCostsByVintage' ][ v ]  += fcost
		variables[ 'V_DiscountedFixedCostsByProcess' ][t, v] += fcost
		variables[ 'V_DiscountedFixedCostsByPeriodAndProcess' ][p, t, v] = fcost
		variables[ 'V_DiscountedPeriodCost'          ][ p ]  += fcost

	for p, t, v in m.CostVariable.sparse_iterkeys():
		vcost = value( m.V_ActivityByPeriodTechAndVintage[p, t, v] )
		if abs(vcost) < epsilon: continue

		vcost *= value( m.CostVariable[p, t, v] )
		variables[ 'V_UndiscountedVariableCostsByPeriod'  ][ p ]  += vcost
		variables[ 'V_UndiscountedVariableCostsByTech'    ][ t ]  += vcost
		variables[ 'V_UndiscountedVariableCostsByVintage' ][ v ]  += vcost
		variables[ 'V_UndiscountedVariableCostsByProcess' ][t, v] += vcost
		variables[ 'V_UndiscountedVariableCostsByPeriodAndProcess' ][p, t, v] = vcost
		variables[ 'V_UndiscountedPeriodCost'             ][ p ]  += vcost

		vcost *= value( m.PeriodRate[ p ])
		variables[ 'V_DiscountedVariableCostsByPeriod'  ][ p ]  += vcost
		variables[ 'V_DiscountedVariableCostsByTech'    ][ t ]  += vcost
		variables[ 'V_DiscountedVariableCostsByVintage' ][ v ]  += vcost
		variables[ 'V_DiscountedVariableCostsByProcess' ][t, v] += vcost
		variables[ 'V_DiscountedPeriodCost'             ][ p ]  += vcost


	var_list = []
	for vgroup, values in sorted( variables.iteritems() ):
		for vindex, val in sorted( values.iteritems() ):
			if isinstance( vindex, tuple ):
				vindex = ','.join( str(i) for i in vindex )
			var_list.append(( '{}[{}]'.format(vgroup, vindex), val ))

	ostream.write('\n"Reporting Variables" (calculated after solve)\n')
	stringify_data( var_list, ostream )


def pformat_results ( pyomo_instance, pyomo_result ):
	from coopr.pyomo import Objective, Var, Constraint

	output = StringIO()

	m = pyomo_instance            # lazy typist
	result = pyomo_result

	soln = result['Solution']
	solv = result['Solver']      # currently unused, but may want it later
	prob = result['Problem']     # currently unused, but may want it later

	optimal_solutions = (
	  'feasible', 'globallyOptimal', 'locallyOptimal', 'optimal'
	)
	if str(soln.Status) not in optimal_solutions:
		output.write( 'No solution found.' )

	objs = m.active_components( Objective )
	if len( objs ) > 1:
		msg = '\nWarning: More than one objective.  Using first objective.\n'
		SE.write( msg )

	# This awkward workaround so as to be generic.  Unfortunately, I don't
	# know how else to automatically discover the objective name
	obj_name = objs.keys()[0]
	try:
		obj_value = getattr(soln.Objective, obj_name).Value
	except AttributeError, e:
		try:
			obj_value = soln.Objective['__default_objective__'].Value
		except:
			msg = ('Unknown error collecting objective function value.  A '
			   'solution exists, but Temoa is currently unable to parse it.  '
			   'If you are inclined, please send the dat file that creates the '
			   'error to the Temoa developers.  Meanwhile, pyomo will still be '
			   'able to extract the solution.\n')
			SE.write( msg )
			raise

	Vars = soln.Variable
	Cons = soln.Constraint

	def collect_result_data( cgroup, clist, epsilon):
		# ctype = "Component group"; i.e., Vars or Cons
		# clist = "Component list"; i.e., where to store the data
		# epsilon = absolute value below which to ignore a result
		results = defaultdict(list)
		for name, data in cgroup.iteritems():
			if not (abs( data['Value'] ) > epsilon ): continue

			# name looks like "Something[some,index]"
			group, index = name[:-1].split('[')
			results[ group ].append( (name.replace("'", ''), data['Value']) )
		clist.extend( t for i in sorted( results ) for t in sorted(results[i]))

	var_info = list()
	con_info = list()

	collect_result_data( Vars, var_info, epsilon=1e-9 )
	collect_result_data( Cons, con_info, epsilon=1e-9 )

	msg = ( 'Model name: %s\n'
	   'Objective function value (%s): %s\n'
	   'Non-zero variable values:\n'
	)
	output.write( msg % (m.name, obj_name, obj_value) )

	if len( var_info ) > 0:
		stringify_data( var_info, output )
		del var_info
		calculate_reporting_variables( m, output )
	else:
		output.write( '\nAll variables have a zero (0) value.\n' )

	if len( con_info ) > 0:
		output.write( '\nBinding constraint values:\n' )
		stringify_data( con_info, output )
		del con_info
	else:
		# Since not all Coopr solvers give constraint results, must check
		msg = '\nSelected Coopr solver plugin does not give constraint data.\n'
		output.write( msg )

	output.write( '\n\nIf you use these results for a published article, '
	  "please run Temoa with the '--how_to_cite' command line argument for "
	  'citation information.\n')

	return output

