from subprocess import call
from sys import argv, stderr as SE, stdout as SO
from shutil import rmtree
import argparse
import sqlite3
import os
import sys
import getopt
import re
import pandas as pd

from GraphVizUtil import *


def CreateMainResultsDiagram ( **kwargs ): #results_main	
	ifile		   = kwargs.get( 'ifile' )
	ffmt               = kwargs.get( 'image_format' )
	pp				   = kwargs.get( 'inp_period')
	scenario 		   = kwargs.get( 'scenario_name' )

	time_exist    = set()
	time_future = set()
	time_optimize   = set()
	tech_all	= set()
	commodity_emissions = set()
	commodity_carrier = set()
	Efficiency_Input = set()
	Efficiency_Output = set()

	con = sqlite3.connect(ifile)
	cur = con.cursor()   # a database cursor is a control structure that enables traversal over the records in a database
	con.text_factory = str #this ensures data is explored with the correct UTF-8 encoding

	cur.execute("SELECT t_periods FROM time_periods WHERE flag is 'e'")
	for row in cur:
		time_exist.add(int(row[0]))
	cur.execute("SELECT t_periods FROM time_periods WHERE flag is 'f'")
	for row in cur:
		time_future.add(int(row[0]))
	time_optimize = set(sorted( time_future)[:-1])
	
	
	for row in cur.execute("SELECT tech FROM technologies WHERE flag='r' OR flag='p' OR flag='pb' OR flag='ps'"):
		tech_all.add(row[0])	
	
	for row in cur.execute("SELECT comm_name FROM commodities WHERE flag is 'd' OR flag is 'p'"):
		commodity_carrier.add(row[0])
	for row in cur.execute("SELECT comm_name FROM commodities WHERE flag is 'e'"):
		commodity_emissions.add(row[0])

	for row in cur.execute('SELECT DISTINCT input_comm, tech FROM Efficiency'):
		Efficiency_Input.add((row[0], row[1]))
	for row in cur.execute('SELECT DISTINCT tech, output_comm FROM Efficiency'):
		Efficiency_Output.add((row[0], row[1]))
	
	cur.execute("SELECT tech, capacity FROM Output_CapacityByPeriodAndTech WHERE scenario == '"+scenario+"' and t_periods == '"+str(pp)+"'")
	V_Cap2 = pd.DataFrame(cur.fetchall(), columns=['tech', 'capacity'])
	
	cur.execute("SELECT input_comm, tech, SUM(vflow_in) AS flow FROM Output_VFlow_In WHERE scenario == '"+scenario+"' and t_periods == '"+str(pp)+
		"' GROUP BY input_comm, tech")
	EI2 = pd.DataFrame(cur.fetchall(), columns = ['input_comm', 'tech', 'consumption'])
		
	cur.execute("SELECT tech, output_comm, SUM(vflow_out) AS flow FROM Output_VFlow_Out WHERE scenario == '"+scenario+"' and t_periods == '"+str(pp)+
		"' GROUP BY output_comm, tech")
	EO2 = pd.DataFrame(cur.fetchall(), columns=['tech', 'output_comm', 'activity'])

	q2 = "SELECT E.emis_comm, E.tech, SUM(E.emis_act*O.vflow_out) FROM EmissionActivity E, Output_VFlow_Out O " + \
	"WHERE E.input_comm == O.input_comm AND E.tech == O.tech AND E.vintage  == O.vintage AND E.output_comm == O.output_comm AND O.scenario == '"+ scenario +"' " + \
	"and O.t_periods == '"+str(pp)+"' GROUP BY E.tech, E.emis_comm"
	cur.execute(q2)
	EmiO2 = pd.DataFrame(cur.fetchall(), columns=['emis_comm', 'tech', 'emis_activity'])
		
	cur.close()
	con.close()

	os.chdir( 'results' )

	from GraphVizFormats import results_dot_fmt

	tech_attr_fmt = 'label="%s\\nCapacity: %.2f", href="#", onclick="loadNextGraphvizGraph(\'results\', \'%s\', \'%s\')"'
	#tech_attr_fmt = 'label="%%s\\nCapacity: %%.2f", href="results_%%s_%%s.%s"'
	# tech_attr_fmt %= ffmt
	# commodity_fmt = 'href="../commodities/rc_%%s_%%s.%s"' % ffmt
	commodity_fmt = 'href="#", onclick="loadNextGraphvizGraph(\'results\', \'%s\', \'%s\')"'
	flow_fmt = 'label="%.2f"'
	

	epsilon = 0.005  

	etechs, dtechs, ecarriers, xnodes = set(), set(), set(), set()
	eemissions = set()
	eflowsi, eflowso, dflows = set(), set(), set()   # edges
	usedc, usede = set(), set()    # used carriers, used emissions

	V_Cap2.index = V_Cap2.tech
	for tech in set(tech_all) - set(V_Cap2.tech):
		dtechs.add((tech, None))

	for i in range(len(V_Cap2)):
		row = V_Cap2.iloc[i]
		etechs.add( (row['tech'], tech_attr_fmt % (row['tech'], row['capacity'], row['tech'], pp)) )
		# etechs.add( (row['tech'], tech_attr_fmt % (row['tech'], row['capacity'], row['tech'], pp)) )

	udflows = set()
	for i in range(len(EI2)):
		row = EI2.iloc[i]
		if (row['input_comm'] != 'ethos'):
			eflowsi.add((row['input_comm'], row['tech'], flow_fmt % row['consumption']))
			ecarriers.add((row['input_comm'], commodity_fmt % (row['input_comm'], pp)))
			usedc.add(row['input_comm'])
		else:
			cap = V_Cap2.ix[row['tech']].capacity
			xnodes.add((row['tech'], tech_attr_fmt % (row['tech'], cap, row['tech'], pp)))
		udflows.add((row['input_comm'], row['tech']))	

	for row in set(Efficiency_Input) - udflows:
		if row[0] != 'ethos':
			dflows.add((row[0], row[1], None))
		else:
			xnodes.add((row[1], None))

	udflows = set()
	for i in range(len(EO2)):
		row = EO2.iloc[i]
		eflowso.add((row['tech'], row['output_comm'], flow_fmt % row['activity']))
		ecarriers.add((row['output_comm'], commodity_fmt % (row['output_comm'], pp)))
		usedc.add(row['output_comm'])
		udflows.add((row['tech'], row['output_comm']))

	for row in set(Efficiency_Output) - udflows:
		dflows.add((row[0], row[1], None))

	for i in range(len(EmiO2)):
		row = EmiO2.iloc[i]
		if (row['emis_comm'] >= epsilon):
			eflowso.add((row['tech'], row['emis_comm'], flow_fmt % row['emis_activity']))
			eemissions.add((row['emis_comm'], None))
			usede.add(row['emis_comm'])

	dcarriers = set()
	demissions = set()
	for cc in commodity_carrier:
		if cc not in usedc and cc != 'ethos' :
			dcarriers.add((cc, None))
	for ee in commodity_emissions: 
		if ee not in usede:
			demissions.add((ee, None))

	dtechs     = create_text_nodes( dtechs,     indent=2 )
	etechs     = create_text_nodes( etechs,     indent=2 )
	xnodes	   = create_text_nodes( xnodes,		indent=2 )
	dcarriers  = create_text_nodes( dcarriers,  indent=2 )
	ecarriers  = create_text_nodes( ecarriers,  indent=2 )
	demissions = create_text_nodes( demissions, indent=2 )
	eemissions = create_text_nodes( eemissions, indent=2 )
	dflows     = create_text_edges( dflows,     indent=2 )
	eflowsi    = create_text_edges( eflowsi,    indent=3 )
	eflowso    = create_text_edges( eflowso,    indent=3 )

	fname = 'results%s.' % pp
	with open( fname + 'dot', 'w' ) as f:
		f.write( results_dot_fmt % dict(
		  period             = pp,
		  splinevar          = kwargs.get( 'splinevar' ),
		  arrowheadin_color  = kwargs.get( 'arrowheadin_color' ),
		  arrowheadout_color = kwargs.get( 'arrowheadout_color' ),
		  commodity_color    = kwargs.get( 'commodity_color' ),
		  tech_color         = kwargs.get( 'tech_color' ),
		  unused_color       = kwargs.get( 'unused_color' ),
		  unusedfont_color   = kwargs.get( 'unusedfont_color' ),
		  usedfont_color     = kwargs.get( 'usedfont_color' ),
		  fill_color		 = kwargs.get( 'fill_color' ),
		  font_color		 = kwargs.get( 'font_color' ),
		  dtechs     = dtechs,
		  etechs     = etechs,
		  xnodes	 = xnodes,
		  dcarriers  = dcarriers,
		  ecarriers  = ecarriers,
		  demissions = demissions,
		  eemissions = eemissions,
		  dflows     = dflows,
		  eflowsi    = eflowsi,
		  eflowso    = eflowso,
		))

	cmd = ('dot', '-T' + ffmt, '-o' + fname + ffmt, fname + 'dot')
	call( cmd )

	os.chdir( '..' )

# Needs some small fixing - cases where no input but output is there. # Check sample graphs
def CreateTechResultsDiagrams ( **kwargs ): # tech results
	
	ifile		   = kwargs.get( 'ifile' )
	ffmt               = kwargs.get( 'image_format' )
	per 			   = kwargs.get( 'inp_period' )
	tech 			   = kwargs.get( 'inp_technology' )
	scenario 		   = kwargs.get( 'scenario_name' )
	
	os.chdir( 'results' )

	from GraphVizFormats import tech_results_dot_fmt

	# enode_attr_fmt = 'href="../commodities/rc_%%s_%%s.%s"' % ffmt
	# vnode_attr_fmt = 'href="results_%%s_p%%sv%%s_segments.%s", ' % ffmt
	# vnode_attr_fmt += 'label="%s\\nCap: %.2f"'
	enode_attr_fmt = 'href="#", onclick="loadNextGraphvizGraph(\'results\', \'%s\', \'%s\')"'
	vnode_attr_fmt = 'href="#", onclick="loadNextGraphvizGraph(\'%s\', \'%s\', \'%s\')"'
	vnode_attr_fmt += 'label="%s\\nCap: %.2f"'

	con = sqlite3.connect(ifile)
	cur = con.cursor()   # a database cursor is a control structure that enables traversal over the records in a database
	con.text_factory = str #this ensures data is explored with the correct UTF-8 encoding

	cur.execute("SELECT capacity FROM Output_CapacityByPeriodAndTech WHERE scenario == '"+scenario+"' and tech is '"+tech+"' and t_periods is '"+str(per)+"'" )
	total_cap = cur.fetchone()[0]

	cur.execute("SELECT OF.input_comm, OF.output_comm, OF.vintage, SUM(vflow_in), SUM(vflow_out), OC.capacity FROM Output_VFlow_In OF, Output_VFlow_Out OFO, Output_V_Capacity OC "+
		"WHERE OF.t_periods is '"+str(per)+"' and OF.tech is '"+tech+"' and OF.scenario is '"+scenario+"' and OC.scenario == OF.scenario and OC.tech is '"+tech+
		"' and OFO.t_periods is '"+str(per)+"' and OF.tech is '"+tech+"' and OFO.scenario is '"+scenario+
		"' and OF.vintage == OC.vintage and OF.input_comm == OFO.input_comm and OF.output_comm == OFO.output_comm and OF.vintage == OFO.vintage and OF.t_day == OFO.t_day"+
		" and OF.t_season == OFO.t_season GROUP BY OF.input_comm, OF.output_comm, OF.vintage")

	flows = pd.DataFrame(cur.fetchall(), columns=['input_comm', 'output_comm', 'vintage', 'flow_in', 'flow_out', 'capacity'])

	cur.close()
	con.close()

	# energy/vintage nodes, in/out edges
	enodes, vnodes, iedges, oedges = set(), set(), set(), set()

	for i in range(len(flows)):
		row = flows.iloc[i]
		vnode = str(row['vintage'])
		vnodes.add( (vnode, vnode_attr_fmt %
			(tech, per, row['vintage'], row['vintage'], row['capacity']) ) )

		if row['input_comm'] != 'ethos':
			enodes.add( (row['input_comm'], enode_attr_fmt % (row['input_comm'], per)) )
			iedges.add( (row['input_comm'], vnode, 'label="%.2f"' % row['flow_in']) )
		enodes.add( (row['output_comm'], enode_attr_fmt % (row['output_comm'], per)) )
		oedges.add( (vnode, row['output_comm'], 'label="%.2f"' % row['flow_out']) )

	print flows, total_cap

	#cluster_vintage_url = "results%s.%s" % (per, ffmt)
	cluster_vintage_url = "#"

	if vnodes:
		print "Generating graph"
		enodes = create_text_nodes( enodes, indent=2 )
		vnodes = create_text_nodes( vnodes, indent=2 )
		iedges = create_text_edges( iedges, indent=2 )
		oedges = create_text_edges( oedges, indent=2 )

		fname = 'results_%s_%s.' % (tech, per)
		with open( fname + 'dot', 'w' ) as f:
			f.write( tech_results_dot_fmt % dict(
			  cluster_vintage_url = cluster_vintage_url,
			  tech            = tech,
			  period          = per,
			  ffmt            = ffmt,
			  commodity_color = kwargs.get( 'commodity_color' ),
			  usedfont_color  = kwargs.get( 'usedfont_color' ),
			  home_color      = kwargs.get( 'home_color' ),
			  input_color     = kwargs.get( 'arrowheadin_color' ),
			  output_color    = kwargs.get( 'arrowheadout_color' ),
			  vintage_cluster_color = kwargs.get( 'sb_vpbackg_color' ),
			  font_color	  = kwargs.get( 'font_color' ),
			  fill_color	  = kwargs.get( 'fill_color' ),
			  vintage_color   = kwargs.get( 'sb_vp_color' ),
			  splinevar       = kwargs.get( 'splinevar' ),
			  total_cap       = total_cap,
			  vnodes          = vnodes,
			  enodes          = enodes,
			  iedges          = iedges,
			  oedges          = oedges,
			))
		cmd = ('dot', '-T' + ffmt, '-o' + fname + ffmt, fname + 'dot')
		call( cmd )

	os.chdir( '..' )

def CreateCommodityPartialResults ( **kwargs ): 
	
	ifile		= kwargs.get( 'ifile' )
	ffmt            = kwargs.get( 'image_format' )
	per 			= kwargs.get( 'inp_period' )
	comm 			= kwargs.get( 'inp_commodity' )
	scenario 		= kwargs.get( 'scenario_name' )
	
	os.chdir( 'commodities' )

	from GraphVizFormats import commodity_dot_fmt

	con = sqlite3.connect(ifile)
	cur = con.cursor()
	con.text_factory = str

	cur.execute("SELECT DISTINCT tech FROM Efficiency WHERE output_comm is '"+comm+"'")
	input_total = set(pd.DataFrame(cur.fetchall(), columns=['tech'])['tech'])

	cur.execute("SELECT DISTINCT tech FROM Efficiency WHERE input_comm is '"+comm+"'")
	output_total = set(pd.DataFrame(cur.fetchall(), columns=['tech'])['tech'])

	cur.execute("SELECT DISTINCT tech, SUM(vflow_in) FROM Output_VFlow_In WHERE input_comm is '"+comm+"' and scenario is '"+scenario+"' and t_periods is '"+str(per)+"' GROUP BY tech")
	flow_in = pd.DataFrame(cur.fetchall(), columns=['input_techs', 'flow_in'])
	otechs = set(flow_in['input_techs'])

	cur.execute("SELECT DISTINCT tech, SUM(vflow_out) FROM Output_VFlow_Out WHERE output_comm is '"+comm+"' and scenario is '"+scenario+"' and t_periods is '"+str(per)+"' and input_comm != 'ethos' GROUP BY tech")
	flow_out = pd.DataFrame(cur.fetchall(), columns=['output_techs', 'flow_out'])
	itechs = set(flow_out['output_techs'])

	cur.close()
	con.close()

	period_results_url_fmt = '../results/results%%s.%s' % ffmt
	# node_attr_fmt = 'href="../results/results_%%s_%%s.%s"' % ffmt
	# rc_node_fmt = 'color="%s", href="%s", shape="circle", fillcolor="%s", fontcolor="black"'

	node_attr_fmt = 'href="#", onclick="loadNextGraphvizGraph(\'results\', \'%s\', \'%s\')"'
	rc_node_fmt = 'color="%s", href="%s", shape="circle", fillcolor="%s", fontcolor="black"'

	# url = period_results_url_fmt % per
	url = '#'
	enodes, dnodes, eedges, dedges = set(), set(), set(), set()

	rcnode = ((comm, rc_node_fmt % (kwargs.get( 'commodity_color' ), url, kwargs.get( 'fill_color' ))),)

	for i in range(len(flow_in)):
		t = flow_in.iloc[i]['input_techs']
		f = flow_in.iloc[i]['flow_in']
		enodes.add( (t, node_attr_fmt % (t, per)) )
		eedges.add( (comm, t, 'label="%.2f"' % f) )
	for t in output_total - otechs:
		dnodes.add( (t, None) )
		dedges.add( (comm, t, None) )
	for i in range(len(flow_out)):
		t = flow_out.iloc[i]['output_techs']
		f = flow_out.iloc[i]['flow_out']
		enodes.add( (t, node_attr_fmt % (t, per)) )
		eedges.add( (t, comm, 'label="%.2f"' % f) )
	for t in input_total - itechs:
		dnodes.add( (t, None) )
		dedges.add( (t, comm, None) )

	rcnode = create_text_nodes( rcnode )
	enodes = create_text_nodes( enodes, indent=2 )
	dnodes = create_text_nodes( dnodes, indent=2 )
	eedges = create_text_edges( eedges, indent=2 )
	dedges = create_text_edges( dedges, indent=2 )
	
	fname = 'rc_%s_%s.' % (comm, per)
	with open( fname + 'dot' ,'w') as f:
		f.write( commodity_dot_fmt % dict(
		  home_color     = kwargs.get( 'home_color' ),
		  usedfont_color = kwargs.get( 'usedfont_color' ),
		  sb_arrow_color = kwargs.get( 'sb_arrow_color' ),
		  tech_color     = kwargs.get( 'tech_color' ),
		  commodity      = comm,
		  period         = per,
		  unused_color   = kwargs.get( 'unused_color' ),
		  font_color	 = kwargs.get( 'font_color' ),
		  resource_node  = rcnode,
		  used_nodes     = enodes,
		  unused_nodes   = dnodes,
		  used_edges     = eedges,
		  unused_edges   = dedges,
		))

	cmd = ('dot', '-T' + ffmt, '-o' + fname + ffmt, fname + 'dot')
	call( cmd )

	os.chdir( '..' )

def createCompleteInputGraph( **kwargs ) : # Call this function if the input file is a database.
	ifile		   = kwargs.get( 'ifile' )
	q_flag			   = kwargs.get( 'q_flag' )
	quick_name 		   = kwargs.get( 'quick_name' )
	scenario_name	   = kwargs.get( 'scenario_name' )
	ffmt               = kwargs.get( 'image_format' )
	arrowheadin_color  = kwargs.get( 'arrowheadin_color' )
	arrowheadout_color = kwargs.get( 'arrowheadout_color' )
	commodity_color    = kwargs.get( 'commodity_color' )
	tech_color         = kwargs.get( 'tech_color' )
	unused_color       = kwargs.get( 'unused_color' )
	unusedfont_color   = kwargs.get( 'unusedfont_color' )
	usedfont_color     = kwargs.get( 'usedfont_color' )
	fill_color		   = kwargs.get( 'fill_color' )
	font_color		   = kwargs.get( 'font_color' )
	inp_comm		   = kwargs.get( 'inp_commodity' )
	inp_tech		   = kwargs.get( 'inp_technology' )
	
	nodes, tech, ltech, to_tech, from_tech = set(), set(), set(), set(), set()
	if q_flag:
		# Specify the Input and Output Commodities to choose from. Default puts all commodities in the Graph.
		if inp_comm is None and inp_tech is None :
			inp_comm = "NOT NULL"
			inp_tech = "NOT NULL"
		else :
			if inp_comm is None :
				inp_comm = "NULL"
			else :
				inp_comm = "'"+inp_comm+"'"
			if inp_tech is None :
				inp_tech = "NULL"
			else :
				inp_tech = "'"+inp_tech+"'"
		
		#connect to the database
		con = sqlite3.connect(ifile)
		cur = con.cursor()   # a database cursor is a control structure that enables traversal over the records in a database
		con.text_factory = str #this ensures data is explored with the correct UTF-8 encoding

		print ifile, inp_comm, inp_tech

		cur.execute("SELECT input_comm, tech, output_comm FROM Efficiency WHERE input_comm is "+inp_comm+" or output_comm is "+inp_comm+" or tech is "+inp_tech)
		for row in cur:
			if row[0] != 'ethos':
				nodes.add(row[0])
			else :
				ltech.add(row[1])
			nodes.add(row[2])
			tech.add(row[1])
			# Now populate the dot file with the concerned commodities
			if row[0] != 'ethos':
				to_tech.add('"%s"' % row[0] + '\t->\t"%s"' % row[1]) 
			from_tech.add('"%s"' % row[1] + '\t->\t"%s"' % row[2])

		cur.close()
		con.close()
		
	else:
		# Specify the Input and Output Commodities to choose from. Default puts all commodities in the Graph.
		if inp_comm is None and inp_tech is None :
			inp_comm = "\w+"
			inp_tech = "\w+"
		else :
			if inp_comm is None :
				inp_comm = "\W+"
			if inp_tech is None :
				inp_tech = "\W+"

		eff_flag = False
		#open the text file
		with open (ifile) as f :
			for line in f:
				if eff_flag is False and re.search("^\s*param\s+efficiency\s*[:][=]", line, flags = re.I) : 
					#Search for the line param Efficiency := (The script recognizes the commodities specified in this section)
					eff_flag = True
				elif eff_flag :
					line = re.sub("[#].*$", " ", line)
					if re.search("^\s*;\s*$", line)	:
						break #  Finish searching this section when encounter a ';'
					if re.search("^\s+$", line)	:
						continue
					line = re.sub("^\s+|\s+$", "", line)
					row = re.split("\s+", line)
					if not re.search(inp_comm, row[0]) and not re.search(inp_comm, row[3]) and not re.search(inp_tech, row[1]) :
						continue
					if row[0] != 'ethos':
						nodes.add(row[0])
					else :
						ltech.add(row[1])
					nodes.add(row[3])
					tech.add(row[1])
					# Now populate the dot file with the concerned commodities
					if row[0] != 'ethos':
						to_tech.add('"%s"' % row[0] + '\t->\t"%s"' % row[1])
					from_tech.add('"%s"' % row[1] + '\t->\t"%s"' % row[3])
							
		if eff_flag is False :	
			print ("Error: The Efficiency Parameters cannot be found in the specified file - "+ifile)
			sys.exit(2)
	
	print "Creating Diagrams...\n"

	from GraphVizFormats import quick_run_dot_fmt

	with open( quick_name + '.dot', 'w' ) as f:
		f.write( quick_run_dot_fmt % dict(
		  arrowheadin_color  = arrowheadin_color,
		  arrowheadout_color = arrowheadout_color,
		  commodity_color    = commodity_color,
		  tech_color         = tech_color,
		  font_color         = font_color,
		  fill_color         = fill_color,
		  enodes             = "".join('"%s";\n\t\t' % x for x in nodes),
		  tnodes             = "".join('"%s";\n\t\t' % x for x in tech),
		  iedges             = "".join('%s;\n\t\t' % x for x in to_tech),
		  oedges             = "".join('%s;\n\t\t' % x for x in from_tech),
		  snodes             = ";".join('"%s"' %x for x in ltech),
		))
	del nodes, tech, to_tech, from_tech
	cmd = ('dot', '-T' + ffmt, '-o' + quick_name+'.' + ffmt, quick_name+'.dot')
	call( cmd )


def CreateModelDiagrams (kwargs):

	if not kwargs['quick_flag']:
		images_dir = kwargs['quick_name'] + "_" + kwargs['scenario_name']
		if os.path.exists( images_dir ):
			rmtree( images_dir )
		os.mkdir( images_dir )
		os.chdir( images_dir )
		os.makedirs( 'commodities' )
		os.makedirs( 'processes' )
		os.makedirs( 'results' )
	else:
		images_dir = kwargs['quick_name']
		if os.path.exists( images_dir ):
			rmtree( images_dir )
		os.mkdir( images_dir )
		os.chdir( images_dir )

	print "Created output folders"
	
	if (kwargs['quick_flag'] == True):
		print "Generating createCompleteInputGraph"
		createCompleteInputGraph(**kwargs)
	elif (kwargs['inp_technology'] is None and kwargs['inp_commodity'] is None):
		print "Generating CreateMainResultsDiagram"
		CreateMainResultsDiagram(**kwargs)
	elif (kwargs['inp_commodity'] is None):
		print "Generating CreateTechResultsDiagrams"
		CreateTechResultsDiagrams(**kwargs)
	elif (kwargs['inp_technology'] is None):
		print "Generating CreateCommodityPartialResults"
		CreateCommodityPartialResults(**kwargs)

	os.chdir( '..' )
	
def createGraphBasedOnInput(inputs):
	
	inputs = processInputArgs(inputs)
	grey_flag = inputs['grey_flag']

	kwargs = dict(
	  images_dir         = '%s_%s' % (inputs['quick_name'], inputs['scenario_name']),
	  image_format       = inputs['image_format'].lower(),

	  tech_color         = 'darkseagreen' if grey_flag else 'black',
	  commodity_color    = 'lightsteelblue' if grey_flag else 'black',
	  unused_color       = 'powderblue' if grey_flag else 'gray75',
	  arrowheadout_color = 'forestgreen' if grey_flag else 'black',
	  arrowheadin_color  = 'firebrick' if grey_flag else 'black',
	  usedfont_color     = 'black',
	  unusedfont_color   = 'chocolate' if grey_flag else 'gray75',
	  menu_color         = 'hotpink',
	  home_color         = 'gray75',
	  font_color	     = 'black' if grey_flag else 'white',
	  fill_color	     = 'lightsteelblue' if grey_flag else 'white',

	  #MODELDETAILED,
	  md_tech_color      = 'hotpink',

	  sb_incom_color     = 'lightsteelblue' if grey_flag else 'black',
	  sb_outcom_color    = 'lawngreen' if grey_flag else 'black',
	  sb_vpbackg_color   = 'lightgrey',
	  sb_vp_color        = 'white',
	  sb_arrow_color     = 'forestgreen' if grey_flag else 'black',

	  #SUBGRAPH 1 ARROW COLORS
	  color_list = ('red', 'orange', 'gold', 'green', 'blue', 'purple',
	                'hotpink', 'cyan', 'burlywood', 'coral', 'limegreen',
	                'black', 'brown') if grey_flag else ('black', 'black'),
	)

	kwargs.update(inputs)

	print "Reading File %s ..." %inputs['ifile'] 

	if inputs['res_dir'] is None:
		inputs['res_dir'] = "current directory"
	else:
		os.chdir(inputs['res_dir'])
	print "CreateModelDiagrams with quick_flag = ", inputs['quick_flag']

	CreateModelDiagrams (kwargs)

	print "Done. Look for results in %s" %inputs['res_dir']


if __name__ == "__main__":	
	
	argv = sys.argv[1:]
	
	createGraphBasedOnInput(argv)

