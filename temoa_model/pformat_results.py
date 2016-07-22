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

# ---------------------------------------------------------------------------
# This module processes model output data, which can be sent to three possible 
# locations: the shell, a user-specified database, or an Excel file. Users can
# configure the available outputs.
# ---------------------------------------------------------------------------


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
from IPython import embed as IP


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

	objs = list(m.component_data_objects( Objective ))
	if len( objs ) > 1:
		msg = '\nWarning: More than one objective.  Using first objective.\n'
		SE.write( msg )

	Cons = soln.Constraint


	def collect_result_data( cgroup, clist, epsilon):
		# cgroup = "Component group"; i.e., Vars or Cons
		# clist = "Component list"; i.e., where to store the data
		# epsilon = absolute value below which to ignore a result
		results = defaultdict(list)
		for name, data in cgroup.iteritems():
			if not (abs( data['Value'] ) > epsilon ): continue

			# name looks like "Something[some,index]"
			group, index = name[:-1].split('[')
			results[ group ].append( (name.replace("'", ''), data['Value']) )
		clist.extend( t for i in sorted( results ) for t in sorted(results[i]))

	#Create a dictionary in which to store "solved" variable values
	svars = defaultdict( lambda: defaultdict( float ))   
	
	con_info = list()
	epsilon = 1e-9   # threshold for "so small it's zero"

	emission_keys = { (i, t, v, o) : set() for e, i, t, v, o in m.EmissionActivity }
	for e, i, t, v, o in m.EmissionActivity:
		emission_keys[(i, t, v, o)].add(e)
	P_0 = min( m.time_optimize )
	GDR = value( m.GlobalDiscountRate )
	MLL = m.ModelLoanLife
	MPL = m.ModelProcessLife
	x   = 1 + GDR    # convenience variable, nothing more

	# Extract optimal decision variable values related to commodity flow:
	for p, s, d, t, v in m.V_Activity:
		val = value( m.V_Activity[p, s, d, t, v] )
		if abs(val) < epsilon: continue

		svars['V_Activity'][p, s, d, t, v] = val

	for p, t, v in m.V_ActivityByPeriodAndProcess:
		val = value( m.V_ActivityByPeriodAndProcess[p, t, v] )
		if abs(val) < epsilon: continue

		svars['V_ActivityByPeriodAndProcess'][p, t, v] = val

	for p, s, d, i, t, v, o in m.V_FlowIn:
		val = value( m.V_FlowIn[p, s, d, i, t, v, o] )
		if abs(val) < epsilon: continue

		svars['V_FlowIn'][p, s, d, i, t, v, o] = val

	for p, s, d, i, t, v, o in m.V_FlowOut:
		val = value( m.V_FlowOut[p, s, d, i, t, v, o] )
		if abs(val) < epsilon: continue

		svars['V_FlowOut'][p, s, d, i, t, v, o] = val

		if (i, t, v, o) not in emission_keys: continue

		emissions = emission_keys[i, t, v, o]
		for e in emissions:
			evalue = val * m.EmissionActivity[e, i, t, v, o]
			svars[ 'V_EmissionActivityByPeriodAndProcess' ][p, e, t, v] += evalue

	# Extract optimal decision variable values related to capacity:
	for t, v in m.V_Capacity:
		val = value( m.V_Capacity[t, v] )
		if abs(val) < epsilon: continue

		svars['V_Capacity'][t, v] = val

	for p, t in m.V_CapacityAvailableByPeriodAndTech:
		val = value( m.V_CapacityAvailableByPeriodAndTech[p, t] )
		if abs(val) < epsilon: continue
		svars['V_CapacityAvailableByPeriodAndTech'][p, t] = val

	# Calculate model costs:	
	# This is a generic workaround.  Not sure how else to automatically discover 
    # the objective name
	obj_name, obj_value = objs[0].cname(True), value( objs[0] )	
	svars[ 'Objective' ]["('"+obj_name+"')"] = obj_value

	for t, v in m.CostInvest.sparse_iterkeys():   # Returns only non-zero values
	
		icost = value( m.V_Capacity[t, v] )
		if abs(icost) < epsilon: continue
		icost *= value( m.CostInvest[t, v] )
		svars[	'Costs'	][ 'V_UndiscountedInvestmentByProcess', t, v] += icost 

		icost *= value( m.LoanAnnualize[t, v] )
		icost *= (
		  value( MLL[t, v] ) if not GDR else
		    (x **(P_0 - v + 1) * (1 - x **(-value( MLL[t, v] ))) / GDR)
		)

		svars[	'Costs'	][ 'V_DiscountedInvestmentByProcess', t, v] += icost		
		
	for p, t, v in m.CostFixed.sparse_iterkeys():
		fcost = value( m.V_Capacity[t, v] )
		if abs(fcost) < epsilon: continue

		fcost *= value( m.CostFixed[p, t, v] )
		svars[	'Costs'	][ 'V_UndiscountedFixedCostsByProcess', t, v] += fcost
		
		fcost *= (
		  value( MPL[p, t, v] ) if not GDR else
		    (x **(P_0 - p + 1) * (1 - x **(-value( MPL[p, t, v] ))) / GDR)
		)

		svars[	'Costs'	][ 'V_DiscountedFixedCostsByProcess', t, v] += fcost
		
	for p, t, v in m.CostVariable.sparse_iterkeys():
		vcost = value( m.V_ActivityByPeriodAndProcess[p, t, v] )
		if abs(vcost) < epsilon: continue

		vcost *= value( m.CostVariable[p, t, v] )
		svars[	'Costs'	][ 'V_UndiscountedVariableCostsByProcess', t, v] += vcost

		vcost *= value( m.PeriodRate[ p ])
		svars[	'Costs'	][ 'V_DiscountedVariableCostsByProcess', t, v] += vcost

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

	# -----------------------------------------------------------------
	# Write outputs stored in dictionary to the user-specified database 
	# -----------------------------------------------------------------

	# Table dictionary below maps variable names to database table names
	tables = { "V_FlowIn"   : "Output_VFlow_In",  \
			   "V_FlowOut"  : "Output_VFlow_Out", \
			   "V_Capacity" : "Output_V_Capacity",       \
			   "V_CapacityAvailableByPeriodAndTech"   : "Output_CapacityByPeriodAndTech",  \
			   "V_EmissionActivityByPeriodAndProcess" : "Output_Emissions", \
			   "Objective"  : "Output_Objective", \
			   "Costs"      : "Output_Costs" }

	if isinstance(options, TemoaConfig):	
		if not os.path.exists(options.output) :
			print "Please put the "+options.output+" file in the right Directory"
		
		con = sqlite3.connect(options.output)
		cur = con.cursor()   # A database cursor enables traversal over DB records
		con.text_factory = str # This ensures data is explored with UTF-8 encoding
		
		for table in svars.keys() :
			if table in tables :
				cur.execute("SELECT DISTINCT scenario FROM '"+tables[table]+"'")
				for val in cur : 
					if options.scenario == val[0]: # If scenario exists, delete
						cur.execute("DELETE FROM "+tables[table]+" \
									WHERE scenario is '"+options.scenario+"'") 
				for key in svars[table].keys() :
					key_str = str(key)
					key_str = key_str[1:-1] # Remove parentheses
					if table == 'Objective' : # Only table without sector info
						cur.execute("INSERT INTO "+tables[table]+" \
									VALUES('"+options.scenario+"',"+key_str+", \
									"+str(svars[table][key])+");")
					else : # First add 'NULL' for sector then update
						cur.execute("INSERT INTO "+tables[table]+ \
									" VALUES('"+options.scenario+"','NULL', \
									"+key_str+","+str(svars[table][key])+");")
						cur.execute("UPDATE "+tables[table]+" SET sector = \
									(SELECT sector FROM technologies \
									WHERE tech = "+tables[table]+".tech);")
		con.commit()
		con.close()			

		if options.saveEXCEL :
			os.system("python db_io"+os.sep+"DB_to_Excel.py -i \
					  ""+options.output+" \
					  " -o db_io"+os.sep+options.scenario+" -s "+options.scenario)
	
	return output
