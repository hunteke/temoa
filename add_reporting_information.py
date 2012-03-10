#!/usr/bin/env python

import re, sys
import pprint

from IPython import embed as II

SO = sys.stdout
SE = sys.stderr

def parse_cplex_solution ( cplex_sol_file ):

	scen_re   = r'S(?P<scen>[^_]+)'
	per_re    = r'(?P<per>\d+)'
	vint_re   = r'(?P<vint>\d+)'
	season_re = r'_*(?P<season>[^,\s]+?)_*'
	tod_re    = r'_*(?P<tod>[^,\s]+?)_*'
	inp_re    = r'_*(?P<inp>[^,\s]+?)_*'
	out_re    = r'_*(?P<out>[^,\s]+?)_*'
	tech_re   = r'_*(?P<tech>[^,\s]+?)_*'
	value_re  = r'(\d+|\d+\.\d+)'

	act_re = r'^.*{}_V_Activity\({},{},{},{},{}\).*value="{}"'
	act_re = re.compile(
	  act_re.format( scen_re, per_re, season_re, tod_re, tech_re, vint_re, value_re)
	)

	actPTV_re = r'^.*{}_V_ActivityByPeriodTechAndVintage\({},{},{}\).*value="{}"'
	actPTV_re = re.compile(
	  actPTV_re.format( scen_re, per_re, tech_re, vint_re, value_re )
	)

	cap_re = r'^.*{}_V_Capacity\({},{}\).*value="{}"'
	cap_re = re.compile( cap_re.format( scen_re, tech_re, vint_re, value_re ) )

	capPT_re = r'^.*{}_V_CapacityAvailableByPeriodAndTech\({},{}\).*value="{}"'
	capPT_re = re.compile( capPT_re.format( scen_re, per_re, tech_re, value_re ) )

	FI_re = r'^.*{}_V_FlowIn\({},{},{},{},{},{},{}\).*value="{}"'
	FI_re = re.compile(
	  FI_re.format( scen_re, per_re, season_re, tod_re, inp_re, tech_re, vint_re,
	                out_re, value_re )
	)

	FO_re = r'^.*{}_V_FlowOut\({},{},{},{},{},{},{}\).*value="{}"'
	FO_re = re.compile(
	  FO_re.format( scen_re, per_re, season_re, tod_re, inp_re, tech_re, vint_re,
	                out_re, value_re )
	)

	expected_cost_re = r'^.*EXPECTED_COST_Rs(.*?)".*value="{}"'
	expected_cost_re = re.compile( expected_cost_re.format(value_re) )

	# this 'targets' variable is a little interesting in that I use the
	# key to create a "switch" statement.  So, basically, the left side of
	# this dict must have valid Temoa variable names.  The right side is the
	# regex to parse that particular variable in the CPlex output.
	targets = dict(
	  Activity                         = act_re,
	  ActivityByPeriodTechAndVintage   = actPTV_re,
	  Capacity                         = cap_re,
	  CapacityAvailableByPeriodAndTech = capPT_re,
	#  CapacityFixed                    = capfixed_re,
	#  CapacityInvest                   = capinvest_re
	  FlowIn                           = FI_re,
	  FlowOut                          = FO_re,
	)

	scenario_vars = dict()
	switch_re = re.compile( r'.*({})\('.format( '|'.join(targets) ) )

	with open( cplex_sol_file, 'r') as f:
		master_ec_re = re.compile(r'.*objectiveValue="{}"'.format(value_re))
		for line in f:
			match = master_ec_re.match( line )
			if match:
				scenario_vars[ 'ec' ] = float( match.group(1) )
				break

		for line in f:
			# ignore constraints and variables with no value
			if ' <constraint ' in line: continue
			if ' value="0" ' in line: continue

			match = switch_re.match( line )
			if match:
				var = match.group(1)
				match = targets[ var ].match( line )
				if match:
					scen = match.group(1)
					index = match.groups()[1:-1]
					value = match.groups()[-1]
					try:
						scenario_vars[ scen ][ var ][ index ] = float( value )
					except KeyError:
						if scen not in scenario_vars: scenario_vars[ scen ] = dict()
						if var not in scenario_vars: scenario_vars[ scen ][ var ] = dict()
						scenario_vars[ scen ][ var ][ index ] = float( value )
				continue

			match = expected_cost_re.match( line )
			if match:
				scen = match.group(1)
				value = match.group(2)
				try:
					scenario_vars[ scen ][ 'cost' ] = float( value )
				except KeyError:
					if scen not in scenario_vars: scenario_vars[ scen ] = dict()
					scenario_vars[ scen ][ 'cost' ] = float( value )

	return scenario_vars


def compute_reporting_variables ( solution_info ):
	costs = list()
	ec = solution_info[ 'ec' ]
	del solution_info[ 'ec' ]

	# hard coded to the model.  This is one of those to-be-updated values.
	# I told you this was a "quick and dirty" script!
	periods = ('2010', '2015', '2020', '2025', '2030', '2035')

	# slen = "scenario_length"; i.e. the number of stages
	slen = max( len(i.split('s')) for i in solution_info.keys() )
	all_scenarios = sorted(
	  i for i in solution_info.keys() if len( i.split('s') ) == slen )

	# This section creates a table of incurred costs for each scenario,
	# separated by the period to which those costs were attributed.
	sub_costs = list()
	for s in all_scenarios:
		sub_scenarios = s.split('s')
		sub = sub_scenarios.pop(0)
		costs = [ solution_info[ sub ][ 'cost' ] ]
		for decision in sub_scenarios:
			sub += 's' + decision
			costs.append( solution_info[ sub ][ 'cost' ] )

		sub_costs.append( [sub, ec] + costs + [ec + sum(costs)] )

	# sort by the total cost
	sub_costs.sort( key=lambda x: x[-1] )

	data = list()
	data.append(['Scenario Total Costs',])
	data.append(['',] + list(periods) +['Total'])
	data.extend( sub_costs )
	data.append(list())

	for s in all_scenarios:
	# After trial and error, comment out the above line and uncomment the
	# following line, with the specific scenarios you want to look at.
	#for s in ('0s0s5s1s0', '0s0s5s2s2', '0s0s4s0s0'):
		variables = solution_info[ s ]
		cap_avail = variables[ 'CapacityAvailableByPeriodAndTech' ]
		cap       = variables[ 'Capacity' ]

		data.append(['Total Capacity Available', '(%s)' % s])
		data.append(['',] + list(periods))
		techs = set(t for p, t in cap_avail.keys() )
		for t in sorted( techs ):
			line = [t,]
			for p in periods:
				if (p, t) in cap_avail:
					line.append(cap_avail[p, t])
				else:
					line.append(0)
			data.append(line)
		data.append(list())

		data.append(['New Capacity', '(%s)' % s])
		data.append(['',] + list( periods ))
		techs = set(t for t, v in cap.keys() )
		for t in sorted( techs ):
			line = [t,]
			for v in periods:
				if (t, v) in cap:
					line.append(cap[t, v])
				else:
					line.append( 0 )
			data.append( line )
		data.append( list() )

	import csv, cStringIO
	csvdata = cStringIO.StringIO()
	writer = csv.writer( csvdata ); writer.writerows( data )
	print csvdata.getvalue()



def usage ( ):
	SE.write("""
This is a very "quick and dirty" script.  It's basic functionality is to
convert a CPlex solution of a stochastic Temoa problem into a set of tables
within a CSV file.

It is a temporary measure before we settle on a more robust method of turning
solutions into usable results.  Currently, there are a few minor issues
preventing us from immediately using the Coopr version of solutions, but the
honking not-so-minor issue is Coopr's love of memory.  For any sizeable
problem, Coopr uses most (if not all) of our cluster's memory.  This leaves
little for the solver to work with, not to mention doling it back out into a
form we can digest with other tools.

Also, a friendly reminder for how to make CPlex solve your LP filed:

$ cplex   # start cplex
cplex> read  your_model.lp
cplex> optimize
 ...
cplex> write  your_model.sol

synopsis: coopr_python  {0}  <options_to_import.py>  <your_model.sol>  >  your_model.csv

Example: coopr_python  {0} \
  options/utopia_coal_vs_nuc.py \
  utopia_coal_vs_nuc.sol  >  utopia_coal_vs_nuc.csv

""".format(sys.argv[0]))

	raise SystemExit


def inform ( x ):
	global verbose
	if verbose:
		SE.write( x )
		SE.flush()


def main ( ):
	import os
	from time import clock

	if len(sys.argv) < 3:
		usage()
	module_name = sys.argv[1][:-3].replace('/', '.')  # remove the '.py'

	try:
		__import__(module_name)
		opts = sys.modules[ module_name ]

	except ImportError:
		msg = ('Unable to import {}.\n\nRun this script with no arguments for '
		       'more information.\n')
		SE.write( msg.format( sys.argv[1] ) )
		raise

	try:
		opts.dirname
	except AttributeError:
		opts.dirname = module_name.split('.')[-1]

	global verbose
	verbose = opts.verbose

	begin = clock()
	duration = lambda: clock() - begin

	inform( '[      ] Parsing CPlex solution file (%s)' % sys.argv[2] )
	solution_info = parse_cplex_solution( sys.argv[2] )
	inform( '\r[%6.2f\n' % duration() )


	inform( '[      ] Computing report variable information.' )
	compute_reporting_variables( solution_info )
	inform( '\r[%6.2f\n' % duration() )



if '__main__' == __name__:
	main()
