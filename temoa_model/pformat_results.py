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

__all__ = ('pformat_results', 'stringify_data')

from collections import defaultdict
from cStringIO import StringIO
from sys import stderr as SE, stdout as SO
from temoa_config import TemoaConfig
import sqlite3
import os
import re
import subprocess

from pyomo.core import value

def stringify_data ( data, ostream=SO, format='plain' ):
	# data is a list of tuples of ('var_name[index]', value)
	#  data must be a list, as this function replaces each row,
	# format is currently unused, but will be utilized to implement things like
	# csv

	# This padding code is what makes the display of the output values
	# line up on the decimal point.
	for i, (v, val) in enumerate( data ):
		ipart, fpart = repr(float(val)).split('.')
		data[i] = (ipart, fpart, v)
	cell_lengths = ( map(len, l[:-1] ) for l in data )
	max_lengths = map(max, zip(*cell_lengths))   # max length of each column
	fmt = u'  {{:>{:d}}}.{{:<{:d}}}  {{}}\n'.format( *max_lengths )

	for row in data:
		ostream.write( fmt.format(*row) )



def pformat_results ( pyomo_instance, pyomo_result, options ):
	from pyomo.core import Objective, Var, Constraint

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
		return output

	objs = m.active_components( Objective )
	if len( objs ) > 1:
		msg = '\nWarning: More than one objective.  Using first objective.\n'
		SE.write( msg )

	# This awkward workaround so as to be generic.  Unfortunately, I don't
	# know how else to automatically discover the objective name
	objs = objs.items()[0]
	obj_name, obj_value = objs[0], value( objs[1]() )

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

	svars = defaultdict( lambda: defaultdict( float ))    # "solved" vars
	psvars = defaultdict( lambda: defaultdict( float ))   # "post-solve" vars
	dbvars = defaultdict( lambda: defaultdict( float ))   # "Temp" vars to populate database
	con_info = list()

	epsilon = 1e-9   # threshold for "so small it's zero"

	emission_keys = { (i, t, v, o) : e for e, i, t, v, o in m.EmissionActivity }
	P_0 = min( m.time_optimize )
	GDR = value( m.GlobalDiscountRate )
	MLL = m.ModelLoanLife
	MPL = m.ModelProcessLife
	x   = 1 + GDR    # convenience variable, nothing more

	for p, s, d, t, v in m.V_Activity:
		val = value( m.V_Activity[p, s, d, t, v] )
		if abs(val) < epsilon: continue

		svars['V_Activity'][p, s, d, t, v] = val

	for p, t, v in m.V_ActivityByPeriodAndProcess:
		val = value( m.V_ActivityByPeriodAndProcess[p, t, v] )
		if abs(val) < epsilon: continue

		svars['V_ActivityByPeriodAndProcess'][p, t, v] = val

	for t in m.V_ActivityByTech:
		val = value( m.V_ActivityByTech[t] )
		if abs(val) < epsilon: continue

		svars['V_ActivityByTech'][t] = val

	for t, v in m.V_Capacity:
		val = value( m.V_Capacity[t, v] )
		if abs(val) < epsilon: continue

		svars['V_Capacity'][t, v] = val

	for p, t in m.V_CapacityAvailableByPeriodAndTech:
		val = value( m.V_CapacityAvailableByPeriodAndTech[p, t] )
		if abs(val) < epsilon: continue

		svars['V_CapacityAvailableByPeriodAndTech'][p, t] = val

	for p, s, d, i, t, v, o in m.V_FlowIn:
		val = value( m.V_FlowIn[p, s, d, i, t, v, o] )
		if abs(val) < epsilon: continue

		svars['V_FlowIn'][p, s, d, i, t, v, o] = val

		psvars['V_EnergyConsumptionByTech'               ][ t ]     += val
		psvars['V_EnergyConsumptionByPeriodAndTech'      ][p, t]    += val
		psvars['V_EnergyConsumptionByTechAndOutput'      ][t, o]    += val
		psvars['V_EnergyConsumptionByPeriodAndProcess'   ][p, t, v] += val
		psvars['V_EnergyConsumptionByPeriodInputAndTech' ][p, i, t] += val
		psvars['V_EnergyConsumptionByPeriodTechAndOutput'][p, t, o] += val

	for p, s, d, i, t, v, o in m.V_FlowOut:
		val = value( m.V_FlowOut[p, s, d, i, t, v, o] )
		if abs(val) < epsilon: continue

		svars['V_FlowOut'][p, s, d, i, t, v, o] = val
		psvars['V_ActivityByInputAndTech'          ][i, t]       += val
		psvars['V_ActivityByPeriodAndTech'         ][p, t]       += val
		psvars['V_ActivityByTechAndOutput'         ][t, o]       += val
		psvars['V_ActivityByProcess'               ][t, v]       += val
		psvars['V_ActivityByPeriodInputAndTech'    ][p, i, t]    += val
		psvars['V_ActivityByPeriodTechAndOutput'   ][p, t, o]    += val
		psvars['V_ActivityByPeriodInputAndProcess' ][p, i, t, v] += val
		psvars['V_ActivityByPeriodProcessAndOutput'][p, t, v, o] += val

		if (i, t, v, o) not in emission_keys: continue

		e = emission_keys[i, t, v, o]
		evalue = val * m.EmissionActivity[e, i, t, v, o]

		psvars[ 'V_EmissionActivityByPeriod'           ][ p ]  += evalue
		psvars[ 'V_EmissionActivityByTech'             ][ t ]  += evalue
		psvars[ 'V_EmissionActivityByPeriodAndTech'    ][p, t] += evalue
		psvars[ 'V_EmissionActivityByProcess'          ][t, v] += evalue
		psvars[ 'V_EmissionActivityByPeriodAndProcess' ][p, e, t, v] += evalue
		
	for t, v in m.CostInvest.sparse_iterkeys():
		# CostInvest guaranteed not 0

		icost = value( m.V_Capacity[t, v] )
		if abs(icost) < epsilon: continue

		icost *= value( m.CostInvest[t, v] )
		psvars[ 'V_UndiscountedInvestmentByPeriod'  ][ v ]  += icost
		psvars[ 'V_UndiscountedInvestmentByTech'    ][ t ]  += icost
		psvars[ 'V_UndiscountedInvestmentByProcess' ][t, v] += icost
		psvars[ 'V_UndiscountedPeriodCost'          ][ v ]  += icost

		dbvars[	'Costs'	][ 'V_UndiscountedInvestmentByProcess', t, v] += icost # A small hack to make output to db easier

		icost *= value( m.LoanAnnualize[t, v] )
		icost *= (
		  value( MLL[t, v] ) if not GDR else
		    (x **(P_0 - v + 1) * (1 - x **(-value( MLL[t, v] ))) / GDR)
		)

		psvars[ 'V_DiscountedInvestmentByPeriod'  ][ v ]  += icost
		psvars[ 'V_DiscountedInvestmentByTech'    ][ t ]  += icost
		psvars[ 'V_DiscountedInvestmentByProcess' ][t, v] += icost
		psvars[ 'V_DiscountedPeriodCost'          ][ v ]  += icost

		dbvars[	'Costs'	][ 'V_DiscountedInvestmentByProcess', t, v] += icost		
		
	for p, t, v in m.CostFixed.sparse_iterkeys():
		fcost = value( m.V_Capacity[t, v] )
		if abs(fcost) < epsilon: continue

		fcost *= value( m.CostFixed[p, t, v] )
		psvars[ 'V_UndiscountedFixedCostsByPeriod'  ][ p ]  += fcost
		psvars[ 'V_UndiscountedFixedCostsByTech'    ][ t ]  += fcost
		psvars[ 'V_UndiscountedFixedCostsByVintage' ][ v ]  += fcost
		psvars[ 'V_UndiscountedFixedCostsByProcess' ][t, v] += fcost
		psvars[ 'V_UndiscountedFixedCostsByPeriodAndProcess' ][p, t, v] = fcost
		psvars[ 'V_UndiscountedPeriodCost'          ][ p ]  += fcost

		dbvars[	'Costs'	][ 'V_UndiscountedFixedCostsByProcess', t, v] += fcost
		
		fcost *= (
		  value( MPL[p, t, v] ) if not GDR else
		    (x **(P_0 - p + 1) * (1 - x **(-value( MPL[p, t, v] ))) / GDR)
		)

		psvars[ 'V_DiscountedFixedCostsByPeriod'  ][ p ]  += fcost
		psvars[ 'V_DiscountedFixedCostsByTech'    ][ t ]  += fcost
		psvars[ 'V_DiscountedFixedCostsByVintage' ][ v ]  += fcost
		psvars[ 'V_DiscountedFixedCostsByProcess' ][t, v] += fcost
		psvars[ 'V_DiscountedFixedCostsByPeriodAndProcess' ][p, t, v] = fcost
		psvars[ 'V_DiscountedPeriodCost'          ][ p ]  += fcost

		dbvars[	'Costs'	][ 'V_DiscountedFixedCostsByProcess', t, v] += fcost
		
	for p, t, v in m.CostVariable.sparse_iterkeys():
		vcost = value( m.V_ActivityByPeriodAndProcess[p, t, v] )
		if abs(vcost) < epsilon: continue

		vcost *= value( m.CostVariable[p, t, v] )
		psvars[ 'V_UndiscountedVariableCostsByPeriod'  ][ p ]  += vcost
		psvars[ 'V_UndiscountedVariableCostsByTech'    ][ t ]  += vcost
		psvars[ 'V_UndiscountedVariableCostsByVintage' ][ v ]  += vcost
		psvars[ 'V_UndiscountedVariableCostsByProcess' ][t, v] += vcost
		psvars[ 'V_UndiscountedVariableCostsByPeriodAndProcess' ][p, t, v] = vcost
		psvars[ 'V_UndiscountedPeriodCost'             ][ p ]  += vcost

		dbvars[	'Costs'	][ 'V_UndiscountedVariableCostsByProcess', t, v] += vcost

		vcost *= value( m.PeriodRate[ p ])
		psvars[ 'V_DiscountedVariableCostsByPeriod'  ][ p ]  += vcost
		psvars[ 'V_DiscountedVariableCostsByTech'    ][ t ]  += vcost
		psvars[ 'V_DiscountedVariableCostsByVintage' ][ v ]  += vcost
		psvars[ 'V_DiscountedVariableCostsByProcess' ][t, v] += vcost
		psvars[ 'V_DiscountedPeriodCost'             ][ p ]  += vcost

		dbvars[	'Costs'	][ 'V_DiscountedVariableCostsByProcess', t, v] += vcost

	collect_result_data( Cons, con_info, epsilon=1e-9 )

	msg = ( 'Model name: %s\n'
	   'Objective function value (%s): %s\n'
	   'Non-zero variable values:\n'
	)
	output.write( msg % (m.name, obj_name, obj_value) )

	def make_var_list ( variables ):
		var_list = []
		for vgroup, values in sorted( variables.iteritems() ):
			for vindex, val in sorted( values.iteritems() ):
				if isinstance( vindex, tuple ):
					vindex = ','.join( str(i) for i in vindex )
				var_list.append(( '{}[{}]'.format(vgroup, vindex), val ))
		return var_list

	if svars:
		stringify_data( make_var_list(svars), output )
	else:
		output.write( '\nAll variables have a zero (0) value.\n' )

	if psvars:
		output.write('\n"Reporting Variables" (calculated after solve)\n')
		stringify_data( make_var_list(psvars), output )

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

########################################################################################################################	
	tables = {"V_FlowIn" : "Output_VFlow_In", "V_FlowOut" : "Output_VFlow_Out", "V_CapacityAvailableByPeriodAndTech" : "Output_Capacity", "V_EmissionActivityByPeriodAndProcess" : "Output_Emissions", "TotalCost" : "Output_TotalCost", "Costs" : "Output_Costs"}

	if isinstance(options, TemoaConfig):	
		if not os.path.exists(options.output) :
			print "Please put the "+options.output+" file in the right Directory"
		
		con = sqlite3.connect(options.output)
		cur = con.cursor()   # a database cursor is a control structure that enables traversal over the records in a database
		con.text_factory = str #this ensures data is explored with the correct UTF-8 encoding
		
		print options.scenario
		
		for table in svars.keys() :
			if table in tables :
				cur.execute("SELECT DISTINCT scenario FROM '"+tables[table]+"'")
				for val in cur : 
					if options.scenario == val[0]:
						cur.execute("DELETE FROM "+tables[table]+" WHERE scenario is '"+options.scenario+"'") # Delete existing values if exists
				for xyz in svars[table].keys() :
					xy = str(xyz)
					xy = xy[1:-1]
					cur.execute("INSERT INTO "+tables[table]+" VALUES ('"+options.scenario+"',"+xy+","+str(svars[table][xyz])+");")
		for table in psvars.keys() :
			if table in tables :
				cur.execute("SELECT DISTINCT scenario FROM '"+tables[table]+"'")
				for val in cur : 
					if options.scenario == val[0]:
						cur.execute("DELETE FROM "+tables[table]+" WHERE scenario is '"+options.scenario+"'") # Delete existing values if exists
				for xyz in psvars[table].keys() :
					xy = str(xyz)
					xy = xy[1:-1]
					cur.execute("INSERT INTO "+tables[table]+" VALUES ('"+options.scenario+"',"+xy+","+str(psvars[table][xyz])+");")
		for table in dbvars.keys() :
			if table in tables :
				cur.execute("SELECT DISTINCT scenario FROM '"+tables[table]+"'")
				for val in cur : 
					if options.scenario == val[0]:
						cur.execute("DELETE FROM "+tables[table]+" WHERE scenario is '"+options.scenario+"'") # Delete existing values if exists
				for xyz in dbvars[table].keys() :
					xy = str(xyz)
					xy = xy[1:-1]
					cur.execute("INSERT INTO "+tables[table]+" VALUES ('"+options.scenario+"',"+xy+","+str(dbvars[table][xyz])+");")
		if obj_name in tables :
			cur.execute("SELECT DISTINCT scenario FROM '"+tables[obj_name]+"'")
			for val in cur : 
				if options.scenario == val[0]:
					cur.execute("DELETE FROM "+tables[obj_name]+" WHERE scenario is '"+options.scenario+"'") # Delete existing values if exists
			cur.execute("INSERT INTO "+tables[obj_name]+" VALUES ('"+options.scenario+"', "+str(obj_value)+");")
		con.commit()
		con.close()
		
		if options.saveEXCEL :
			os.system("python db_io"+os.sep+"DB_to_Excel.py -i \""+options.output+"\" -o db_io"+os.sep+options.scenario+" -s "+options.scenario)
	
	return output
