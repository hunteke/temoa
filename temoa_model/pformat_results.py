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
from shutil import rmtree
import sqlite3
import os
import re
import subprocess
import sys

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
	P_e = m.time_future.last()
	GDR = value( m.GlobalDiscountRate )
	MLL = m.ModelLoanLife
	MPL = m.ModelProcessLife
	LLN = m.LifetimeLoanProcess
	x   = 1 + GDR    # convenience variable, nothing more

	# Extract optimal decision variable values related to commodity flow:
	for p, s, d, t, v in m.V_Activity:
		val = value( m.V_Activity[p, s, d, t, v] )
		if abs(val) < epsilon: continue

		svars['V_Activity'][p, s, d, t, v] = val

		#Added to output storage values
	for p, s, d, t in m.V_HourlyStorage:
		val = value( m.V_HourlyStorage[p, s, d, t] )
		if abs(val) < epsilon: continue

		svars['V_HourlyStorage'][p, s, d, t] = val		
		
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
		icost *= value( m.CostInvest[t, v] )*(
			(
				1 -  x**( -min( value(m.LifetimeProcess[t, v]), P_e - v ) )
			)/(
				1 -  x**( -value( m.LifetimeProcess[t, v] ) ) 
			)
		)
		svars[	'Costs'	][ 'V_UndiscountedInvestmentByProcess', t, v] += icost

		icost *= value( m.LoanAnnualize[t, v] )
		icost *= (
		  value( LLN[t, v] ) if not GDR else
		    (x **(P_0 - v + 1) * (1 - x **(-value( LLN[t, v] ))) / GDR)
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

		vcost *= (
		  value( MPL[p, t, v] ) if not GDR else
		    (x **(P_0 - p + 1) * (1 - x **(-value( MPL[p, t, v] ))) / GDR)
		  )
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
			   "Costs"      : "Output_Costs", \
			   "V_HourlyStorage"   :  "Output_HourlyStorage"}
	
	db_tables = ['time_periods', 'time_season', 'time_of_day', 'technologies', 'commodities',\
				'LifetimeTech', 'LifetimeProcess', 'Efficiency', 'EmissionActivity', 'ExistingCapacity']

	
	if isinstance(options, TemoaConfig):	
		if not options.output:
			if options.saveTEXTFILE or options.keepPyomoLP:
				for inpu in options.dot_dat:
					print inpu
					file_ty = re.search(r"\b([\w-]+)\.(\w+)\b", inpu)
				new_dir = options.path_to_db_io+os.sep+file_ty.group(1)+'_'+options.scenario+'_model'
				if os.path.exists( new_dir ):
					rmtree( new_dir )
				os.mkdir(new_dir)
			print "No Output File specified."
			return output
	
		if not os.path.exists(options.output) :
			print "Please put the "+options.output+" file in the right Directory"
			return output


		con = sqlite3.connect(options.output)
		cur = con.cursor()   # A database cursor enables traversal over DB records
		con.text_factory = str # This ensures data is explored with UTF-8 encoding

		### Copy tables from Input File to DB file.
		# IF output file is empty database.
		cur.execute("SELECT * FROM technologies")
		is_db_empty = False #False for empty db file
		for elem in cur:
			is_db_empty = True #True for non-empty db file
			break
		
		
		if is_db_empty: #This file could be schema with populated results from previous run. Or it could be a normal db file.
			cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='input_file';")
			does_input_file_table_exist = False
			for i in cur: # This means that the 'input_file' table exists in db.
				does_input_file_table_exist = True
			if does_input_file_table_exist: #This block distinguishes normal database from schema.
				#This is schema file. 
				cur.execute("SELECT file FROM input_file WHERE id is '1';")
				for i in cur:
					tagged_file = i[0]
				tagged_file = re.sub('["]', "", tagged_file)

				if tagged_file == options.dot_dat[0]:
					#If Input_file name matches, add output and check tech/comm
					dat_to_db(options.dot_dat[0], con)
				else:
					#If not a match, delete output tables and update input_file. Call dat_to_db
					for i in db_tables:
						cur.execute("DELETE FROM "+i+";")
						cur.execute("VACUUM;")		
					
					for i in tables.keys():
						cur.execute("DELETE FROM "+tables[i]+";")
						cur.execute("VACUUM;")
						
					for i in options.dot_dat:
						cur.execute("DELETE FROM input_file WHERE id=1;")
						cur.execute("INSERT INTO input_file VALUES(1, '"+i+"');")
						break
					dat_to_db(i, con)
			
		else: #empty schema db file
			cur.execute("CREATE TABLE IF NOT EXISTS input_file ( id integer PRIMARY KEY, file varchar(30));")
			
			for i in tables.keys():
				cur.execute("DELETE FROM "+tables[i]+";")
				cur.execute("VACUUM;")
			
			for i in options.dot_dat:
				cur.execute("DELETE FROM input_file WHERE id=1;")
				cur.execute("INSERT INTO input_file(id, file) VALUES(?, ?);", (1,  '"'+i+'"'))
				break
			dat_to_db(i, con)
		

		
		for table in svars.keys() :
			if table in tables :
				cur.execute("SELECT DISTINCT scenario FROM '"+tables[table]+"'")
				for val in cur : 
					if options.scenario == val[0]: # If scenario exists, delete
						cur.execute("DELETE FROM "+tables[table]+" \
									WHERE scenario is '"+options.scenario+"'") 
				if table == 'Objective' : # Only table without sector info
					for key in svars[table].keys():
						key_str = str(key) # only 1 row to write
						key_str = key_str[1:-1] # Remove parentheses
						cur.execute("INSERT INTO "+tables[table]+" \
									VALUES('"+options.scenario+"',"+key_str+", \
									"+str(svars[table][key])+");")

				else : # First add 'NULL' for sector then update
					for key in svars[table].keys() : # Need to loop over keys (rows)
						key_str = str(key)
						key_str = key_str[1:-1] # Remove parentheses
						cur.execute("INSERT INTO "+tables[table]+ \
									" VALUES('"+options.scenario+"','NULL', \
									"+key_str+","+str(svars[table][key])+");")
					cur.execute("UPDATE "+tables[table]+" SET sector = \
								(SELECT technologies.sector FROM technologies \
								WHERE "+tables[table]+".tech = technologies.tech);")
		con.commit()
		con.close()			
		
		if options.saveEXCEL or options.saveTEXTFILE or options.keepPyomoLP:
			for inpu in options.dot_dat:
				file_ty = re.search(r"\b([\w-]+)\.(\w+)\b", inpu)
			new_dir = options.path_to_db_io+os.sep+file_ty.group(1)+'_'+options.scenario+'_model'
			if os.path.exists( new_dir ):
				rmtree( new_dir )
			os.mkdir(new_dir)
			
			if options.saveEXCEL:
				file_type = re.search(r"([\w-]+)\.(\w+)\b", options.output)
				file_n = file_type.group(1)
				from DB_to_Excel import make_excel
				temp_scenario = set()
				temp_scenario.add(options.scenario)
				make_excel(options.output, new_dir+os.sep+options.scenario, temp_scenario)
				#os.system("python data_processing"+os.sep+"DB_to_Excel.py -i \
				#		  ""+options.output+" \
				#		  " -o data_files"+os.sep+options.scenario+" -s "+options.scenario)
	
	return output
	
def dat_to_db(input_file, output_schema, run_partial=False):

	def traverse_dat(dat_filename, search_tablename):
		
		result_string = ""
		table_found_flag = False
		
		with open(dat_filename) as f:
			for line in f:
				line = re.sub("[#].*$", " ", line)

				if table_found_flag:
					result_string += line
					if re.search(";\s*$", line):
						break
					
				if re.search(""+search_tablename+"\s*[:][=]", line):
					result_string += line
					table_found_flag = True
					if re.search(";\s*$", line):
						break
										
		return result_string	
	
	#####Code Starts here	
	tables_single_value = [	'time_exist', 'time_future', 'time_season', 'time_of_day', \
				'tech_baseload', 'tech_resource', 'tech_production', 'tech_storage', 'tech_hourlystorage', \
				'commodity_physical', 'commodity_demand', 'commodity_emissions']
	
	partial_run_tech = ['tech_baseload', 'tech_resource', 'tech_production', 'tech_storage', 'tech_hourlystorage']

	partial_run_comm = ['commodity_physical', 'commodity_demand', 'commodity_emissions']
	
	tables_multiple_value = ['ExistingCapacity', 'Efficiency', 'LifetimeTech', \
								'LifetimeProcess', 'EmissionActivity']
							
	parsed_data = {}
	
	#if db_or_dat_flag: #This is an input db file
	#	import pdb; pdb.set_trace()
	#	output_schema.execute("ATTACH DATABASE ? AS db2;", "'"+input_file+"'")
	#	for i in db_tables:
	#		output_schema.execute("INSERT INTO "+i+" SELECT * FROM db2."+i+";")
	
	if run_partial:
		comm_set = set()
		tech_set = set()
		for i in partial_run_comm:
			raw_string = traverse_dat(input_file, i)
			raw_string = re.sub("\s+", " ", raw_string)
			raw_string = re.sub("^.*[:][=]", "", raw_string)
			raw_string = re.sub(";\s*$", "", raw_string)
			raw_string = re.sub("^\s+|\s+$", "", raw_string)
			parsed_data[i] = re.split(" ", raw_string)
			for datas in parsed_data[i]:
				if datas == '':
					continue
				comm_set.add(datas)
		
		for i in partial_run_tech:
			raw_string = traverse_dat(input_file, i)
			raw_string = re.sub("\s+", " ", raw_string)
			raw_string = re.sub("^.*[:][=]", "", raw_string)
			raw_string = re.sub(";\s*$", "", raw_string)
			raw_string = re.sub("^\s+|\s+$", "", raw_string)
			parsed_data[i] = re.split(" ", raw_string)
			for datas in parsed_data[i]:
				if datas == '':
					continue
				tech_set.add(datas)
				
		return comm_set, tech_set
	
	#This is an input dat file
	for i in tables_single_value:
		raw_string = traverse_dat(input_file, i)
		raw_string = re.sub("\s+", " ", raw_string)
		raw_string = re.sub("^.*[:][=]", "", raw_string)
		raw_string = re.sub(";\s*$", "", raw_string)
		raw_string = re.sub("^\s+|\s+$", "", raw_string)
		parsed_data[i] = re.split(" ", raw_string)

	for i in tables_multiple_value:
		raw_string = traverse_dat(input_file, i)
		raw_string = re.sub("\n", ",", raw_string)
		raw_string = re.sub("\s+", " ", raw_string)
		raw_string = re.sub("^.*[:][=]\s*,", "", raw_string)
		raw_string = re.sub(",?;\s*,?$", "", raw_string)
		raw_string = re.sub("^\s+|\s+$", "", raw_string)
		raw_string = re.sub("\s?,\s?", ",", raw_string)
		raw_string = re.sub(",+", ",", raw_string)
		parsed_data[i] = re.split(",", raw_string)

	#Fill time_periods
	for i in parsed_data['time_exist']:
		if i is '': 
			continue
		output_schema.execute("INSERT OR REPLACE INTO time_periods VALUES("+i+", 'e');")
	for i in parsed_data['time_future']:
		if i is '':
			continue
		output_schema.execute("INSERT OR REPLACE INTO time_periods VALUES("+i+", 'f');")
	
	#Fill time_season
	for i in parsed_data['time_season']:
		if i is '':
			continue
		output_schema.execute("INSERT OR REPLACE INTO time_season VALUES('"+i+"');")
	
	#Fill time_of_day
	for i in parsed_data['time_of_day']:
		if i is '':
			continue
		output_schema.execute("INSERT OR REPLACE INTO time_of_day VALUES('"+i+"');")
	
	#Fill technologies
	for i in parsed_data['tech_baseload']:
		if i is '':
			continue
		output_schema.execute("INSERT OR REPLACE INTO technologies VALUES('"+i+"', 'pb', '', '');")
	for i in parsed_data['tech_storage']:
		if i is '':
			continue
		output_schema.execute("INSERT OR REPLACE INTO technologies VALUES('"+i+"', 'ps', '', '');")
	for i in parsed_data['tech_hourlystorage']:
		if i is '':
			continue
		output_schema.execute("INSERT OR REPLACE INTO technologies VALUES('"+i+"', 'ph', '', '');")		
	for i in parsed_data['tech_production']:
		if i is '':
			continue
		if i in parsed_data['tech_storage']:
			continue
		if i in parsed_data['tech_hourlystorage']:
			continue			
		if i in parsed_data['tech_baseload']:
			continue
		output_schema.execute("INSERT OR REPLACE INTO technologies VALUES('"+i+"', 'p', '', '');")
	for i in parsed_data['tech_resource']:
		if i is '':
			continue
		output_schema.execute("INSERT OR REPLACE INTO technologies VALUES('"+i+"', 'r', '', '');")
	
	#Fill commodities
	for i in parsed_data['commodity_demand']:
		if i is '':
			continue
		output_schema.execute("INSERT OR REPLACE INTO commodities VALUES('"+i+"', 'd', '');")
	for i in parsed_data['commodity_physical']:
		if i is '':
			continue
		output_schema.execute("INSERT OR REPLACE INTO commodities VALUES('"+i+"', 'p', '');")
	for i in parsed_data['commodity_emissions']:
		if i is '':
			continue
		output_schema.execute("INSERT OR REPLACE INTO commodities VALUES('"+i+"', 'e', '');")

		
	#Fill ExistingCapacity
	for i in parsed_data['ExistingCapacity']:
		if i is '':
			continue
		row_data = re.split(" ", i)
		row_data.append('')
		row_data.append('')
		output_schema.execute("INSERT OR REPLACE INTO ExistingCapacity VALUES(?, ?, ?, ?, ?);", row_data)
	
	#Fill Efficiency
	for i in parsed_data['Efficiency']:
		if i is '':
			continue
		row_data = re.split(" ", i)
		row_data.append('')
		output_schema.execute("INSERT OR REPLACE INTO Efficiency VALUES(?, ?, ?, ?, ?, ?);", row_data)		
		
	#Fill LifetimeTech
	for i in parsed_data['LifetimeTech']:
		if i is '':
			continue
		row_data = re.split(" ", i)
		row_data.append('')
		output_schema.execute("INSERT OR REPLACE INTO LifetimeTech VALUES(?, ?, ?);", row_data)		
	
	#Fill LifetimeProcess
	for i in parsed_data['LifetimeProcess']:
		if i is '':
			continue
		row_data = re.split(" ", i)
		row_data.append('')
		output_schema.execute("INSERT OR REPLACE INTO LifetimeProcess VALUES(?, ?, ?, ?);", row_data)		
	
	#Fill EmissionActivity
	for i in parsed_data['EmissionActivity']:
		if i is '':
			continue
		row_data = re.split(" ", i)
		row_data.append('')
		if len(row_data) is 7:
			row_data.append('')
		output_schema.execute("INSERT OR REPLACE INTO EmissionActivity VALUES(?, ?, ?, ?, ?, ?, ?, ?);", row_data)
			
