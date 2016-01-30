from subprocess import call
from sys import argv, stderr as SE, stdout as SO
from shutil import rmtree
import argparse
import sqlite3
import os
import sys
import getopt
import re

ifile = None
graph_format = 'svg'
show_capacity = False
graph_type = 'separate_vintages'
splinevar = False
quick_flag = False
quick_name = None
grey_flag = True
scenario = None
res_dir = None
inp_comm = None
out_comm = None
db_dat_flag = None

# Global Variables (dictionaries to cache parsing of Efficiency parameter)
g_processInputs  = dict()
g_processOutputs = dict()
g_processVintages = dict()
g_processLoans = dict()
epsilon = 1e-9

time_exist    = set()
time_future   = set()
time_optimize   = set()
tech_all	= set()
vintage_exist    = set()
vintage_all = set()
ExistingCapacity = dict()
vintage_optimize = set()
commodity_demand    = set()
commodity_emissions = set()
commodity_physical  = set()
commodity_carrier = set()
Efficiency = dict()
time_season     = set()
time_of_day     = set()
LifetimeProcess = dict()
EmissionActivity = dict()
V_Capacity = dict()
V_CapacityAvailableByPeriodAndTech = dict()
V_ActivityByPeriodAndProcess = dict()
V_FlowOut = dict()
V_FlowIn = dict()
V_EnergyConsumptionByPeriodInputAndTech = {}
V_ActivityByPeriodTechAndOutput = dict()
V_EmissionActivityByPeriodAndTech = dict()

def InitializeProcessParameters ():
	global g_processInputs
	global g_processOutputs
	global g_processVintages
	global g_processLoans
	global g_activeFlow_psditvo
	global g_activeActivity_ptv
	global g_activeCapacity_tv
	global g_activeCapacityAvailable_pt

	l_first_period = min( time_future )
	l_exist_indices = ExistingCapacity.keys()

	for i, t, v, o in Efficiency.iterkeys():
		l_process = (t, v)
		l_lifetime = LifetimeProcess[ l_process ]
		for p in time_optimize:
			# can't build a vintage before it's been invented
			if p < v: continue

			pindex = (p, t, v)

			if v + l_lifetime <= p: continue

			if pindex not in g_processInputs:
				g_processInputs[  pindex ] = set()
				g_processOutputs[ pindex ] = set()
			if (p, t) not in g_processVintages:
				g_processVintages[p, t] = set()

			g_processVintages[p, t].add( v )
			g_processInputs[ pindex ].add( i )
			g_processOutputs[pindex ].add( o )
	
	g_activeFlow_psditvo = set(
	  (p, s, d, i, t, v, o)

	  for p in time_optimize
	  for t in tech_all
	  for v in g_processVintages[ p, t ]
	  for i in g_processInputs[ p, t, v ]
	  for o in g_processOutputs[ p, t, v ]
	  for s in time_season
	  for d in time_of_day
	)
	g_activeActivity_ptv = set(
	  (p, t, v)

	  for p in time_optimize
	  for t in tech_all
	  for v in g_processVintages[ p, t ]
	)
	g_activeCapacity_tv = set(
	  (t, v)

	  for p in time_optimize
	  for t in tech_all
	  for v in g_processVintages[ p, t ]
	)
	g_activeCapacityAvailable_pt = set(
	  (p, t)

	  for p in time_optimize
	  for t in tech_all
	  if g_processVintages[ p, t ]
	)

	
def calc_intermediates (ifile):
	global V_EnergyConsumptionByPeriodInputAndTech
	global V_ActivityByPeriodTechAndOutput
	global V_EmissionActivityByPeriodAndTech
	global V_Capacity
	global V_CapacityAvailableByPeriodAndTech
	global V_ActivityByPeriodAndProcess
	global V_FlowOut
	global V_FlowIn
	
	emission_keys = { (i, t, v, o) : e for e, i, t, v, o in EmissionActivity.iterkeys() }
	
	con = sqlite3.connect(ifile)
	cur = con.cursor()   # a database cursor is a control structure that enables traversal over the records in a database
	con.text_factory = str #this ensures data is explored with the correct UTF-8 encoding
	
	for x,y in g_activeCapacity_tv:
		V_Capacity[x,y] = 0
		for row in cur.execute("SELECT capacity FROM V_Capacity WHERE tech is '"+x+"' and vintage is '"+str(y)+"'"):
			V_Capacity[x,y] = row[0]

###########FIXME########################################
	for x,y in g_activeCapacityAvailable_pt:
		V_CapacityAvailableByPeriodAndTech[x,y] = 0
		for row in cur.execute("SELECT capacity FROM Output_Capacity WHERE t_periods is '"+str(x)+"' and tech is '"+y+"'"):
			V_CapacityAvailableByPeriodAndTech[x,y] = row[0]
	
	for x,y,z in g_activeActivity_ptv:
		V_ActivityByPeriodAndProcess[x,y,z] = 0
		for row in cur.execute("SELECT activity FROM V_ActivityByPeriodAndProcess WHERE t_periods is '"+str(x)+"' and tech is '"+y+"' and vintage is '"+str(z)+"'"):
			V_ActivityByPeriodAndProcess[x,y,z] = row[0]
	
	for a,b,c,d,e,f,g in g_activeFlow_psditvo:
		V_FlowIn[a,b,c,d,e,f,g] = 0
		V_FlowOut[a,b,c,d,e,f,g] = 0
		for row in cur.execute("SELECT vflow_in FROM Output_VFlow_In WHERE t_periods is '"+str(a)+"' and t_season is '"+b+"' and t_day is '"+c+"' and input_comm is '"+d+"' and tech is '"+e+"' and vintage is '"+str(f)+"' and output_comm is '"+g+"'"):
			V_FlowIn[a,b,c,d,e,f,g] = row[0]
		for row in cur.execute("SELECT vflow_out FROM Output_VFlow_Out WHERE t_periods is '"+str(a)+"' and t_season is '"+b+"' and t_day is '"+c+"' and input_comm is '"+d+"' and tech is '"+e+"' and vintage is '"+str(f)+"' and output_comm is '"+g+"'"):
			V_FlowOut[a,b,c,d,e,f,g] = row[0]
######################################################
	
	for p, s, d, i, t, v, o in V_FlowIn.iterkeys():
		val = V_FlowIn[p, s, d, i, t, v, o]
		#V_EnergyConsumptionByPeriodInputAndTech[p, i, t] = 0		
		if abs(val) < epsilon: continue
		if (p,i,t) not in V_EnergyConsumptionByPeriodInputAndTech.keys() :
			V_EnergyConsumptionByPeriodInputAndTech[p, i, t] = val
		else :
			V_EnergyConsumptionByPeriodInputAndTech[p, i, t] += val
		
	for p, s, d, i, t, v, o in V_FlowOut:
		val = V_FlowOut[p, s, d, i, t, v, o]
		#V_ActivityByPeriodTechAndOutput[p, t, o]    = 0
		#V_EmissionActivityByPeriodAndTech[p, t] = 0
					
		if abs(val) < epsilon: continue
		if (p,t,o) not in V_ActivityByPeriodTechAndOutput.keys() :
			V_ActivityByPeriodTechAndOutput[p, t, o]    = val
		else :
			V_ActivityByPeriodTechAndOutput[p, t, o]    += val

		if (i, t, v, o) not in emission_keys: continue

		e = emission_keys[i, t, v, o]
		evalue = val * EmissionActivity[e, i, t, v, o]
		if (p,t) not in V_EmissionActivityByPeriodAndTech.keys() :
			V_EmissionActivityByPeriodAndTech[p, t] = evalue
		else:
			V_EmissionActivityByPeriodAndTech[p, t] += evalue
		
	cur.close()
	con.close()


def db_file(ifile) : # Call this function if the input file is a database.
	global time_exist    
	global time_future   
	global time_optimize 
	global tech_all	
	global vintage_exist 
	global vintage_all 
	global ExistingCapacity 
	global vintage_optimize 
	global commodity_demand   
	global commodity_emissions
	global commodity_physical
	global commodity_carrier
	global Efficiency
	global time_season   
	global time_of_day   
	global LifetimeProcess
	global EmissionActivity
	
	#connect to the database
	con = sqlite3.connect(ifile)
	cur = con.cursor()   # a database cursor is a control structure that enables traversal over the records in a database
	con.text_factory = str #this ensures data is explored with the correct UTF-8 encoding
		
	cur.execute("SELECT t_periods FROM time_periods WHERE flag is 'e'")
	for row in cur:
		time_exist.add(int(row[0]))
	cur.execute("SELECT t_periods FROM time_periods WHERE flag is 'f'")
	for row in cur:
		time_future.add(int(row[0]))
	for x in sorted( time_future)[:-1]:
		time_optimize.add(x)
	
	cur.execute("SELECT tech FROM technologies WHERE flag='r' OR flag='p' OR flag='pb' OR flag='ps'")
	for row in cur:
		tech_all.add(row[0])
	for x in sorted( time_exist ):
		vintage_exist.add(x)
	for x,y in [(a,b) for a in tech_all for b in vintage_exist]:
		cur.execute("SELECT exist_cap FROM ExistingCapacity WHERE tech is '"+x+"' and vintage is '"+str(y)+"'")
		for row in cur:
			ExistingCapacity[x,y] = row[0]
	for x in sorted(time_optimize) :
		vintage_optimize.add(x)
	vintage_all      = time_exist.union(time_optimize)

	cur.execute("SELECT comm_name FROM commodities WHERE flag is 'd'")
	for row in cur:
		commodity_demand.add(row[0])
	cur.execute("SELECT comm_name FROM commodities WHERE flag is 'p'")
	for row in cur:
		commodity_physical.add(row[0])
	cur.execute("SELECT comm_name FROM commodities WHERE flag is 'e'")
	for row in cur:
		commodity_emissions.add(row[0])
	commodity_carrier = commodity_physical.union(commodity_demand)
	for w,x,y,z in [(a,b,c,d) for a in commodity_physical for b in tech_all for c in vintage_all for d in commodity_carrier]:
		for row in cur.execute("SELECT efficiency FROM Efficiency WHERE input_comm is '"+w+"' and tech is '"+x+"' and vintage is '"+str(y)+"' and output_comm is '"+z+"'"):
			Efficiency[w,x,y,z] = row[0]

################FIND Default values when not specified########################
	for x,y in set( (t, v) for i, t, v, o in Efficiency.iterkeys()):
		for row in cur.execute("SELECT life FROM LifetimeTech WHERE tech is '"+x+"'"):
			LifetimeProcess[x,y] = row[0]
		for row in cur.execute("SELECT life_process FROM LifetimeProcess WHERE tech is '"+x+"' and vintage is '"+str(y)+"'"):
			LifetimeProcess[x,y] = row[0]
		if row[0] is None:
			LifetimeProcess[x,y] = 30 # Default no of years
####################FIXME########################################
	
	for v,w,x,y,z in set(	(e, i, t, v, o) for i, t, v, o in Efficiency.iterkeys() for e in commodity_emissions ):
		for row in cur.execute("SELECT emis_act FROM EmissionActivity WHERE emis_comm is '"+v+"' and input_comm is '"+w+"' and tech is '"+x+"' and vintage is '"+str(y)+"' and output_comm is '"+z+"'"):
			EmissionActivity[v,w,x,y,z] = row[0]
	
	cur.execute("SELECT t_season FROM time_season")
	for row in cur:
		time_season.add(row[0])
	cur.execute("SELECT t_day FROM time_of_day")
	for row in cur:
		time_of_day.add(row[0])

	cur.close()
	con.close()



###################################

def _getLen ( key ):
	def wrapped ( obj ):
		return len(obj[ key ])
	return wrapped


def create_text_nodes ( nodes, indent=1 ):
	"""\
Return a set of text nodes in Graphviz DOT format, optimally padded for easier
reading and debugging.

nodes: iterable of (id, attribute) node tuples
       e.g. [(node1, attr1), (node2, attr2), ...]

indent: integer, number of tabs with which to indent all Dot node lines
"""
	if not nodes: return '// no nodes in this section'

	# guarantee basic structure of nodes arg
	assert( len(nodes) == sum( 1 for a, b in nodes ) )

	# Step 1: for alignment, get max item length in node list
	maxl = max(map(_getLen(0), nodes)) + 2 # account for two extra quotes

	# Step 2: prepare a text format based on max node size that pads all
	#         lines with attributes
	nfmt_attr = '{0:<%d} [ {1} ] ;' % maxl      # node text format
	nfmt_noa  = '{0} ;'

	# Step 3: create each node, and place string representation in a set to
	#         guarantee uniqueness
	q = '"%s"' # enforce quoting for all nodes
	gviz = set( nfmt_attr.format( q % n, a ) for n, a in nodes if a )
	gviz.update( nfmt_noa.format( q % n ) for n, a in nodes if not a )

	# Step 4: return a sorted version of nodes, as a single string
	indent = '\n' + '\t' *indent
	return indent.join(sorted( gviz ))


def create_text_edges ( edges, indent=1 ):
	"""\
Return a set of text edge definitions in Graphviz DOT format, optimally padded
for easier reading and debugging.

edges: iterable of (from, to, attribute) edge tuples
       e.g. [(inp1, tech1, attr1), (inp2, tech2, attr2), ...]

indent: integer, number of tabs with which to indent all Dot edge lines
"""
	if not edges: return '// no edges in this section'

	# guarantee basic structure of edges arg
	assert( len(edges) == sum( 1 for a, b, c in edges ) )

	# Step 1: for alignment, get max length of items on left and right side of
	# graph operator token ('->')
	maxl, maxr = max(map(_getLen(0), edges)), max(map(_getLen(1), edges))
	maxl += 2  # account for additional two quotes
	maxr += 2  # account for additional two quotes

	# Step 2: prepare format to be "\n\tinp+PADDING -> out+PADDING [..."
	efmt_attr = '{0:<%d} -> {1:<%d} [ {2} ] ;' % (maxl, maxr) # with attributes
	efmt_noa  = '{0:<%d} -> {1} ;' % maxl                     # no attributes

	# Step 3: add each edge to a set (to guarantee unique entries only)
	q = '"%s"' # enforce quoting for all tokens
	gviz = set( efmt_attr.format( q % i, q % t, a ) for i, t, a in edges if a )
	gviz.update( efmt_noa.format( q % i, q % t ) for i, t, a in edges if not a )

	# Step 4: return a sorted version of the edges, as a single string
	indent = '\n' + '\t' *indent
	return indent.join(sorted( gviz ))


def CreateCompleteEnergySystemDiagram ( **kwargs ): #all_vintages_model
	"""\
These first couple versions of CreateModelDiagram do not fully work, and should
be thought of merely as "proof of concept" code.  They create Graphviz DOT files
and equivalent PDFs, but the graphics are not "correct" representations of the
model.  Specifically, there are currently a few artifacts and missing pieces:

Artifacts:
 * Though the graph is "roughly" a left-right DAG, certain pieces currently a
   swapped around, especially on the left-hand side of the image.  This makes
   the graph a bit harder to visually follow.
 * Especially with the birth of energy, there are a few cycles.  For example,
   with the way the model currently creates energy, the graph makes it seem as
   if 'imp_coal' also receives coal, when it should only export coal.

Initially known missing pieces:
 * How should the graph represent the notion of periods?
 * How should the graph represent the vintages?
 * Should the graph include time slices? (e.g. day, season)

Notes:
* For _any_ decently sized system, displaying this type of graph of the entire
  model will be infeasible, or effectively unusable.  We need a way to
  dynamically look at only subsections of the graph, while still giving a 10k'
  foot view of the overall system.

* We need to create a system that puts results into a database, or common result
  format, such that we can archive them for later.  In this manner, directly
  creating graphs at the point of model instantiation and running is not the
  right place.  Creating graphs needs to be a post processing action, and less
  tightly coupled (not coupled at all!) to the internal Pyomo data structure.
"""

	ffmt            = kwargs.get( 'image_format' )
	commodity_color = kwargs.get( 'commodity_color' )
	input_color     = kwargs.get( 'arrowheadin_color' )
	output_color    = kwargs.get( 'arrowheadout_color' )
	tech_color      = kwargs.get( 'tech_color' )
	font_color      = kwargs.get( 'font_color' )
	fill_color      = kwargs.get( 'fill_color' )

	data = """\
// This file is generated by the --graph_format option of the Temoa model.  It
// is a Graphviz DOT language text description of a Temoa model instance.  For
// the curious, Graphviz will read this file to create an equivalent image in
// a number of formats, including SVG, PNG, GIF, and PDF.  For example, here
// is how one might invoke Graphviz to create an SVG image from the dot file.
//
// dot -Tsvg -o model.svg model.dot
//
// For more information, see the Graphviz homepage: http://graphviz.org/

strict digraph TemoaModel {
	rankdir = "LR";       // The direction of the graph goes from Left to Right

	node [ style="filled" ] ;
	edge [ arrowhead="vee", label="   " ] ;


	subgraph technologies {
		node [ color="%(tech_color)s", shape="box", fontcolor="%(font_color)s" ] ;

		%(techs)s
	}

	subgraph energy_carriers {
		node [ color="%(carrier_color)s", shape="circle", fillcolor="%(fill_color)s" ] ;

		%(carriers)s
	}

	subgraph inputs {
		edge [ color="%(input_color)s" ] ;

		%(inputs)s
	}

	subgraph outputs {
		edge [ color="%(output_color)s" ];

		%(outputs)s
	}
	{rank = same; %(xnodes)s}
}
"""

	carriers, techs, xnodes = set(), set(), set()
	inputs, outputs = set(), set()

	p_fmt = '%s, %s'   # "Process format"

	for l_per, l_tech, l_vin in g_activeActivity_ptv:
		techs.add( (p_fmt % (l_per, l_tech), None) )
		for l_inp in g_processInputs[ l_per, l_tech, l_vin ]:
			if l_inp == 'ethos':
				xnodes.add((p_fmt % (l_per, l_tech), None))
			else:
				carriers.add( (l_inp, None) )
				inputs.add( (l_inp, p_fmt % (l_per, l_tech), None) )
		for l_out in g_processOutputs[ l_per, l_tech, l_vin ]:
			carriers.add( (l_out, None) )
			outputs.add( (p_fmt % (l_per, l_tech), l_out, None) )

	techs    = create_text_nodes( techs,    indent=2 )
	carriers = create_text_nodes( carriers, indent=2 )
	xnodes   = create_text_nodes( xnodes,   indent=2 )
	inputs   = create_text_edges( inputs,   indent=2 )
	outputs  = create_text_edges( outputs,  indent=2 )

	fname = 'all_vintages_model.'
	with open( fname + 'dot', 'w' ) as f:
		f.write( data % dict(
		  input_color   = input_color,
		  output_color  = output_color,
		  carrier_color =  commodity_color,
		  tech_color    = tech_color,
		  font_color    = font_color,
		  fill_color	= fill_color,
		  techs    = techs,
		  carriers = carriers,
		  inputs   = inputs,
		  outputs  = outputs,
		  xnodes   = xnodes,
		))

	# Outsource to Graphviz via the old Unix standby: temporary files
	cmd = ('dot', '-T' + ffmt, '-o' + fname + ffmt, fname + 'dot')
	print cmd
	call( cmd )


def CreateCommodityPartialGraphs ( **kwargs ):#commodities
	
	images_dir      = kwargs.get( 'images_dir' )
	ffmt            = kwargs.get( 'image_format' )
	commodity_color = kwargs.get( 'commodity_color' )
	input_color     = kwargs.get( 'arrowheadin_color' )
	output_color    = kwargs.get( 'arrowheadout_color' )
	home_color      = kwargs.get( 'home_color' )
	usedfont_color  = kwargs.get( 'usedfont_color' )
	tech_color      = kwargs.get( 'tech_color' )
	fill_color      = kwargs.get( 'fill_color' )
	font_color      = kwargs.get( 'font_color' )

	os.chdir( 'commodities' )

	commodity_file_format = """\
// This file is generated by the --graph_format option of the Temoa model.  It
// is a Graphviz DOT language text description of a Temoa model instance.  For
// the curious, Graphviz will read this file to create an equivalent image in
// a number of formats, including SVG, PNG, GIF, and PDF.  For example, here
// is how one might invoke Graphviz to create an SVG image from the dot file.
//
// dot -Tsvg -o model.svg model.dot
//
// For more information, see the Graphviz homepage: http://graphviz.org/

// This particular file is the dot language description of the flow of energy
// via the carrier '%(graph_label)s'.

strict digraph Temoa_energy_carrier {
	label = "%(graph_label)s"

	color       = "black";
	compound    = "True";
	concentrate = "True";
	rankdir     = "LR";
	splines     = "True";

	// Default node attributes
	node [ style="filled" ] ;

	// Default edge attributes
	edge [
	  arrowhead      = "vee",
	  fontsize       = "8",
	  label          = "   ",
	  labelfloat     = "false",
	  len            = "2",
	  weight         = "0.5",
	] ;


	// Define individual nodes (and non-default characteristics)
	subgraph techs {
		node [ color="%(tech_color)s", shape="box", fontcolor="%(font_color)s" ] ;

		%(tnodes)s
	}

	subgraph energy_carriers {
		node [ color="%(commodity_color)s", shape="circle", fillcolor="%(fill_color)s" ] ;

		%(enodes)s
	}

	// Define individual edges (and non-default characteristics)
	subgraph outputs {
		edge [ color="%(output_color)s" ] ;

		%(oedges)s
	}

	subgraph inputs {
		edge [ color="%(input_color)s" ] ;

		%(iedges)s
	}
}
"""

	# Step 0: define the Graphviz Dot file format (above)

	model_url = 'href="../simple_model.%s"' % ffmt
	node_attr_fmt = 'href="../processes/process_%%s.%s"' % ffmt

	# Step 1: Define what to do for each energy carrier
	def createImages ( carriers ):
		# Step 1a: Create dot file for each item
		#   The basic gist is to create a set of nodes and edges, and then format
		#   them nicely in case a human needs to investigate the Dot file.
		for l_carrier in sorted( carriers ):
			# energy/tech nodes, in/out edges
			enodes, tnodes, iedges, oedges = set(), set(), set(), set()

			# Step 1b: populate nodes and edges sets with data
			enodes.add( (l_carrier, model_url) )

			for l_per, l_tech, l_vin in g_processInputs:
				if l_carrier in g_processInputs[ l_per, l_tech, l_vin ]:
					tnodes.add( (l_tech, node_attr_fmt % l_tech) )
					iedges.add( (l_carrier, l_tech, None) )
			for l_per, l_tech, l_vin in g_processOutputs:
				if l_carrier in g_processOutputs[ l_per, l_tech, l_vin ]:
					tnodes.add( (l_tech, node_attr_fmt % l_tech) )
					oedges.add( (l_tech, l_carrier, None) )

			# Step 1c: convert the populated nodes and edges to Graphviz format
			tnodes = create_text_nodes( tnodes, indent=2 )
			enodes = create_text_nodes( enodes, indent=2 )
			iedges = create_text_edges( iedges, indent=2 )
			oedges = create_text_edges( oedges, indent=2 )

			# Step 1d: write out the Dot file for later Graphviz work
			with open( 'commodity_%s.dot' % l_carrier, 'w') as f:
				f.write( commodity_file_format % dict(
				  graph_label     = l_carrier,
				  images_dir      = images_dir,
				  commodity_color = commodity_color,
				  home_color      = home_color,
				  input_color     = input_color,
				  output_color    = output_color,
				  tech_color      = tech_color,
				  usedfont_color  = usedfont_color,
				  font_color	  = font_color,
				  fill_color	  = fill_color,
				  tnodes          = tnodes,
				  enodes          = enodes,
				  iedges          = iedges,
				  oedges          = oedges
				))

			# Step 1e: finally, have Graphviz actually create an image
			cmd = (
			  'dot',
			  '-T' + ffmt,
			  '-ocommodity_%s.%s' % (l_carrier, ffmt),
			  'commodity_%s.dot' % l_carrier
			)
			call( cmd )

	# Step 2: find the parts of the energy system this set of graphs address
	l_carriers = set()
	for index in g_processInputs:
		l_carriers.update( l_carrier for l_carrier in g_processInputs[ index ] if l_carrier != 'ethos' )
		l_carriers.update( l_carrier for l_carrier in g_processOutputs[index ] )

	# sorting is not strictly necessary, but if there is some error, it lets
	# the user know on exactly which carrier it failed in terms of what has
	# (not) been written to disk.

	# Step 3: actually do the work
	createImages( sorted(l_carriers) )

	os.chdir('..')


def CreateProcessPartialGraphs ( **kwargs ): #processes
	"""\
A new subgraph is created for every technology in the tech_all set.  Subgraphs
are named model_<tech>.<format>
"""
	
	ffmt               = kwargs.get( 'image_format' )
	arrowheadin_color  = kwargs.get( 'arrowheadin_color' )
	arrowheadout_color = kwargs.get( 'arrowheadout_color' )
	commodity_color    = kwargs.get( 'commodity_color' )
	sb_vp_color        = kwargs.get( 'sb_vp_color' )
	sb_vpbackg_color   = kwargs.get( 'sb_vpbackg_color' )
	color_list         = kwargs.get( 'color_list' )
	sb_incom_color     = kwargs.get( 'sb_incom_color' )
	sb_outcom_color    = kwargs.get( 'sb_outcom_color' )
	images_dir         = kwargs.get( 'images_dir' )
	usedfont_color     = kwargs.get( 'usedfont_color' )
	home_color         = kwargs.get( 'home_color' )
	tech_color         = kwargs.get( 'tech_color' )
	fill_color         = kwargs.get( 'fill_color' )
	
	os.chdir( 'processes' )

	VintageCap = V_Capacity
	PeriodCap  = V_CapacityAvailableByPeriodAndTech

	url_fmt  = '../commodities/commodity_%%s.%s' % ffmt
	dummystr = '   '
	fname = 'process_%s.%s'

	def _create_separate ( l_tech ):
		# begin/end/period/vintage nodes
		bnodes, enodes, pnodes, vnodes = set(), set(), set(), set()
		eedges, vedges = set(), set()

		periods  = set()  # used to obtain the first vintage/period, so that
		vintages = set()  #   all connections can point to a common point
		for l_per, tmp, l_vin in g_processInputs:
			if tmp != l_tech: continue
			periods.add(l_per)
			vintages.add(l_vin)

		if not (periods and vintages):
			# apparently specified a technology in tech_resource, but never used
			# it in efficiency.
			return None

		mid_period  = sorted(periods)[ len(periods)  //2 ] # // is 'floordiv'
		mid_vintage = sorted(vintages)[len(vintages) //2 ]
		del periods, vintages

		p_fmt = 'p_%s'
		v_fmt = 'v_%s'
		niattr = 'color="%s", href="%s"' % (sb_incom_color, url_fmt)  # inp node
		noattr = 'color="%s", href="%s"' % (sb_outcom_color, url_fmt) # out node
		eattr = 'color="%s"'    # edge attribute
		pattr = None            # period node attribute
		vattr = None            # vintage node attribute
		  # "cluster-in attribute", "cluster-out attribute"
		ciattr = 'color="%s", lhead="cluster_vintage"' % arrowheadin_color
		coattr = 'color="%s", ltail="cluster_period"'  % arrowheadout_color

		if show_capacity:
			pattr_fmt = 'label="p%s\\nTotal Capacity: %.2f"'
			vattr_fmt = 'label="v%s\\nCapacity: %.2f"'

		j = 0
		for l_per, tmp, l_vin in g_processInputs:
			if tmp != l_tech: continue

			if show_capacity:
				pattr = pattr_fmt % (l_per, PeriodCap[l_per, l_tech] )
				vattr = vattr_fmt % (l_vin, VintageCap[l_tech, l_vin] )
			pnodes.add( (p_fmt % l_per, pattr) )
			vnodes.add( (v_fmt % l_vin, vattr) )

			for l_inp in g_processInputs[ l_per, l_tech, l_vin ]:
				for l_out in g_processOutputs[ l_per, l_tech, l_vin ]:
					# use color_list for the option 1 subgraph arrows 1, so as to
					# more easily delineate the connections in the graph.
					rainbow = color_list[j]
					j = (j +1) % len(color_list)

					if l_inp != 'ethos':
						enodes.add( (l_inp, niattr % l_inp) )
						eedges.add( (l_inp, v_fmt % mid_vintage, ciattr) )
					bnodes.add( (l_out, noattr % l_out) )
					vedges.add( (v_fmt % l_vin, p_fmt % l_per, eattr % rainbow) )
					eedges.add( (p_fmt % mid_period, '%s' % l_out, coattr) )

		bnodes = create_text_nodes( bnodes, indent=2 ) # beginning nodes
		enodes = create_text_nodes( enodes, indent=2 ) # ending nodes
		pnodes = create_text_nodes( pnodes, indent=2 ) # period nodes
		vnodes = create_text_nodes( vnodes, indent=2 ) # vintage nodes
		eedges = create_text_edges( eedges, indent=2 ) # external edges
		vedges = create_text_edges( vedges, indent=2 ) # vintage edges

		dot_fname = fname % (l_tech, 'dot')
		with open( dot_fname, 'w' ) as f:
			f.write( model_dot_fmt % dict(
			  cluster_url = '../simple_model.%s' % ffmt,
			  graph_label = l_tech,
			  dummy       = dummystr,
			  images_dir  = images_dir,
			  splinevar   = splinevar,
			  clusternode_color = sb_vp_color,
			  period_color      = sb_vpbackg_color,
			  vintage_color     = sb_vpbackg_color,
			  usedfont_color    = usedfont_color,
			  home_color        = home_color,
			  fill_color		= fill_color,
			  bnodes = bnodes,
			  enodes = enodes,
			  pnodes = pnodes,
			  vnodes = vnodes,
			  eedges = eedges,
			  vedges = vedges,
			))
		return dot_fname


	def _create_explicit ( l_tech ):
		v_fmt = 'p%s_v%s'

		nattr = 'color="%s", href="%s"' % (commodity_color, url_fmt)
		vattr = 'color="%s", href="model.%s"' % (tech_color, ffmt)
		etattr = 'color="%s", sametail="%%s"' % arrowheadin_color
		efattr = 'color="%s", samehead="%%s"' % arrowheadout_color

		if show_capacity:
			vattr = 'color="%s", label="p%%(p)s_v%%(v)s\\n' \
		           'Capacity = %%(val).2f", href="model.%s"' % (tech_color, ffmt)

		# begin/end/vintage nodes
		bnodes, enodes, vnodes, edges = set(), set(), set(), set()

		for l_per, tmp, l_vin in g_processInputs:
			if tmp != l_tech: continue

			for l_inp in g_processInputs[ l_per, l_tech, l_vin ]:
				for l_out in g_processOutputs[ l_per, l_tech, l_vin ]:
					if l_inp != 'ethos':
						bnodes.add( (l_inp, nattr % l_inp) )
					enodes.add( (l_out, nattr % l_out) )

					attr_args = dict()
					if show_capacity:
						val = VintageCap[l_tech, l_vin] 
						attr_args.update(p=l_per, v=l_vin, val=val)
					vnodes.add( (v_fmt % (l_per, l_vin),
					  vattr % attr_args ) )
					if l_inp != 'ethos':
						edges.add( (l_inp, v_fmt % (l_per, l_vin),
						etattr % l_inp) )
					edges.add( (v_fmt % (l_per, l_vin), l_out, efattr % l_out) )

		if not (bnodes and enodes and vnodes and edges):
			# apparently specified a technology in tech_resource, but never used
			# it in efficiency.
			return None

		bnodes = create_text_nodes( bnodes, indent=2 )
		enodes = create_text_nodes( enodes, indent=2 )
		vnodes = create_text_nodes( vnodes )
		edges  = create_text_edges( edges )

		dot_fname = fname % (l_tech, 'dot')
		with open( fname, 'w' ) as f:
			f.write( model_dot_fmt % dict(
			  tech           = l_tech,
			  images_dir     = images_dir,
			  home_color     = home_color,
			  usedfont_color = usedfont_color,
			  fill_color	 = fill_color,
			  dummy          = dummystr,
			  bnodes         = bnodes,
			  enodes         = enodes,
			  vnodes         = vnodes,
			  edges          = edges,
			))
		return dot_fname


	if graph_type == 'separate_vintages':
		create_dot_file = _create_separate
		model_dot_fmt = """\
strict digraph model {
	label = "%(graph_label)s" ;

	bgcolor     = "transparent" ;
	color       = "black" ;
	compound    = "True" ;
	concentrate = "True" ;
	rankdir     = "LR" ;
	splines     = "%(splinevar)s" ;

	node [ shape="box", style="filled" ];

	edge [
	  arrowhead  = "vee",
	  decorate   = "True",
	  dir        = "both",
	  fontsize   = "8",
	  label      = "%(dummy)s",
	  labelfloat = "false",
	  labelfontcolor = "lightgreen",
	  len        = "2",
	  weight     = "0.5"
	];

	subgraph cluster_vintage {
		label = "Vintages" ;

		color = "%(vintage_color)s" ;
		style = "filled";
		href  = "%(cluster_url)s" ;

		node [ color="%(clusternode_color)s" ]

		%(vnodes)s
	}

	subgraph cluster_period {
		label = "Period" ;
		color = "%(period_color)s" ;
		style = "filled" ;
		href  = "%(cluster_url)s" ;

		node [ color="%(clusternode_color)s" ]

		%(pnodes)s
	}

	subgraph energy_carriers {
		node [ shape="circle", fillcolor="%(fill_color)s" ] ;

	  // Beginning nodes
		%(bnodes)s

	  // Ending nodes
		%(enodes)s
	}

	subgraph external_edges {
		edge [ arrowhead="normal", dir="forward" ] ;

		%(eedges)s
	}

	subgraph internal_edges {
		// edges between vintages and periods
		%(vedges)s
	}
}
"""
	elif graph_type == 'explicit_vintages':
		create_dot_file = _create_explicit
		model_dot_fmt = """\
strict digraph model {
	label = "%(tech)s" ;

	color       = "black" ;
	concentrate = "True" ;
	rankdir     = "LR" ;

	node [ shape="box", style="filled" ];

	edge [
	  arrowhead = "vee",
	  decorate  = "True",
	  label     = "%(dummy)s",
	  labelfontcolor = "lightgreen"
	];

	subgraph energy_carriers {
		node [ shape="circle", fillcolor="%(fill_color)s" ] ;

	  // Input nodes
		%(bnodes)s

	  // Output nodes
		%(enodes)s
	}

		// Vintage nodes
	%(vnodes)s

	// Define edges and any specific edge attributes
	%(edges)s
}
"""

	# Now actually do the work
	#  Sorting is not necessary, but gives a clue to user about where to look
	#  if some sort of processing error occurs.

	for t in sorted( tech_all ):
		dot_fname = create_dot_file( t )
		if dot_fname:
			cmd = (
			  'dot',
			  '-T' + ffmt,
			  '-o' + fname % (t, ffmt),
			  fname % (t, 'dot')
			)
			call( cmd )

	os.chdir('..')


def CreateMainModelDiagram ( **kwargs ): #simple_model

	ffmt               = kwargs.get( 'image_format' )
	images_dir         = kwargs.get( 'images_dir' )
	arrowheadin_color  = kwargs.get( 'arrowheadin_color' )
	arrowheadout_color = kwargs.get( 'arrowheadout_color' )
	commodity_color    = kwargs.get( 'commodity_color' )
	home_color         = kwargs.get( 'home_color' )
	tech_color         = kwargs.get( 'tech_color' )
	usedfont_color     = kwargs.get( 'usedfont_color' )
	fill_color         = kwargs.get( 'fill_color' )
	font_color         = kwargs.get( 'font_color' )
	
	fname = 'simple_model.'

	model_dot_fmt = """\
strict digraph model {
	rankdir = "LR" ;

	// Default node and edge attributes
	node [ style="filled" ] ;
	edge [ arrowhead="vee", labelfontcolor="lightgreen" ] ;

	// Define individual nodes
	subgraph techs {
		node [ color="%(tech_color)s", shape="box", fontcolor="%(font_color)s" ] ;

		%(tnodes)s
	}

	subgraph energy_carriers {
		node [ color="%(commodity_color)s", shape="circle", fillcolor="%(fill_color)s" ] ;

		%(enodes)s
	}

	// Define edges and any specific edge attributes
	subgraph inputs {
		edge [ color="%(arrowheadin_color)s" ] ;

		%(iedges)s
	}

	subgraph outputs {
		edge [ color="%(arrowheadout_color)s" ] ;

		%(oedges)s
	}
	{rank = same; %(xnodes)s}
}
"""

	tech_attr_fmt    = 'href="processes/process_%%s.%s"' % ffmt
	carrier_attr_fmt = 'href="commodities/commodity_%%s.%s"' % ffmt

	# edge/tech nodes, in/out edges
	enodes, tnodes, iedges, oedges, xnodes = set(), set(), set(), set(), set()

	for l_per, l_tech, l_vin in g_processInputs:
		tnodes.add( (l_tech, tech_attr_fmt % l_tech) )
		for l_inp in g_processInputs[ l_per, l_tech, l_vin ]:
			if l_inp != 'ethos':
				enodes.add( (l_inp, carrier_attr_fmt % l_inp) ) 
			for l_out in g_processOutputs[ l_per, l_tech, l_vin ]:
				enodes.add( (l_out, carrier_attr_fmt % l_out) )
				if l_inp == 'ethos':
					xnodes.add((l_tech, None))
				else:
					iedges.add( (l_inp, l_tech, None) ) 
				oedges.add( (l_tech, l_out, None) )

	enodes = create_text_nodes( enodes, indent=2 )
	tnodes = create_text_nodes( tnodes, indent=2 )
	iedges = create_text_edges( iedges, indent=2 )
	oedges = create_text_edges( oedges, indent=2 )
	xnodes = create_text_nodes( xnodes, indent=2 )

	with open( fname + 'dot', 'w' ) as f:
		f.write( model_dot_fmt % dict(
		  images_dir         = images_dir,
		  arrowheadin_color  = arrowheadin_color,
		  arrowheadout_color = arrowheadout_color,
		  commodity_color    = commodity_color,
		  home_color         = home_color,
		  tech_color         = tech_color,
		  usedfont_color     = usedfont_color,
		  font_color		 = font_color,
		  fill_color		 = fill_color,
		  enodes             = enodes,
		  tnodes             = tnodes,
		  iedges             = iedges,
		  oedges             = oedges,
		  xnodes             = xnodes,
		))
	del enodes, tnodes, iedges, oedges

	cmd = ('dot', '-T' + ffmt, '-o' + fname + ffmt, fname + 'dot')
	call( cmd )

def CreateTechResultsDiagrams ( **kwargs ): #results

	ffmt               = kwargs.get( 'image_format' )
	images_dir         = kwargs.get( 'images_dir' )
	arrowheadin_color  = kwargs.get( 'arrowheadin_color' )
	arrowheadout_color = kwargs.get( 'arrowheadout_color' )
	sb_vpbackg_color   = kwargs.get( 'sb_vpbackg_color' )
	sb_vp_color        = kwargs.get( 'sb_vp_color' )
	commodity_color    = kwargs.get( 'commodity_color' )
	home_color         = kwargs.get( 'home_color' )
	tech_color         = kwargs.get( 'tech_color' )
	fill_color		   = kwargs.get( 'fill_color' )
	font_color		   = kwargs.get( 'font_color' )
	usedfont_color     = kwargs.get( 'usedfont_color' )
	
	os.chdir( 'results' )

	model_dot_fmt = """\
strict digraph model {
	label = "Results for %(tech)s in %(period)s" ;

	compound    = "True" ;
	concentrate = "True";
	rankdir     = "LR" ;
	splines     = "%(splinevar)s" ;

	node [ style="filled" ] ;
	edge [ arrowhead="vee" ] ;

	subgraph cluster_vintages {
		label = "Vintages\\nCapacity: %(total_cap).2f" ;

		href  = "results%(period)s.%(ffmt)s" ;
		style = "filled"
		color = "%(vintage_cluster_color)s"

		node [ color="%(vintage_color)s", shape="box", fontcolor="%(usedfont_color)s" ] ;

		%(vnodes)s
	}

	subgraph energy_carriers {
		node [
		  color     = "%(commodity_color)s",
		  fontcolor = "%(usedfont_color)s",
		  shape     = "circle",
		  fillcolor = "%(fill_color)s"
		] ;

		%(enodes)s
	}

	subgraph inputs {
		edge [ color="%(input_color)s" ] ;

		%(iedges)s
	}

	subgraph outputs {
		edge [ color="%(output_color)s" ] ;

		%(oedges)s
	}
}
"""
	enode_attr_fmt = 'href="../commodities/rc_%%s_%%s.%s"' % ffmt
	vnode_attr_fmt = 'href="results_%%s_p%%sv%%s_segments.%s", ' % ffmt
	vnode_attr_fmt += 'label="%s\\nCap: %.2f"'

	for per, tech in g_activeCapacityAvailable_pt:
		total_cap = V_CapacityAvailableByPeriodAndTech[per, tech]

		# energy/vintage nodes, in/out edges
		enodes, vnodes, iedges, oedges = set(), set(), set(), set()

		for l_vin in g_processVintages[ per, tech ]:
			if (per, tech, l_vin) in V_ActivityByPeriodAndProcess.keys():
				pass
			else:
				continue

			cap = V_Capacity[tech, l_vin]
			if not cap: continue
			vnode = str(l_vin)
			flowin = 0
			flowout = 0
			for l_inp in g_processInputs[ per, tech, l_vin ]:
				for l_out in g_processOutputs[ per, tech, l_vin ]:
					for ssn in time_season:
						for tod in time_of_day:
							flowin  += V_FlowIn[per, ssn, tod, l_inp, tech, l_vin, l_out]
							flowout += V_FlowOut[per, ssn, tod, l_inp, tech, l_vin, l_out]
					index = (per, l_inp, tech, l_vin)

					vnodes.add( (vnode, vnode_attr_fmt %
					  (tech, per, l_vin, l_vin, cap)) )
					if l_inp != 'ethos' :
						enodes.add( (l_inp, enode_attr_fmt % (l_inp, per)) )
						iedges.add( (l_inp, vnode, 'label="%.2f"' % flowin) )
					enodes.add( (l_out, enode_attr_fmt % (l_out, per)) )
					oedges.add( (vnode, l_out, 'label="%.2f"' % flowout) )

		if not vnodes: continue

		enodes = create_text_nodes( enodes, indent=2 )
		vnodes = create_text_nodes( vnodes, indent=2 )
		iedges = create_text_edges( iedges, indent=2 )
		oedges = create_text_edges( oedges, indent=2 )

		fname = 'results_%s_%s.' % (tech, per)
		with open( fname + 'dot', 'w' ) as f:
			f.write( model_dot_fmt % dict(
			  images_dir      = images_dir,
			  tech            = tech,
			  period          = per,
			  ffmt            = ffmt,
			  commodity_color = commodity_color,
			  usedfont_color  = usedfont_color,
			  home_color      = home_color,
			  input_color     = arrowheadin_color,
			  output_color    = arrowheadout_color,
			  vintage_cluster_color = sb_vpbackg_color,
			  font_color	  = font_color,
			  fill_color	  = fill_color,
			  vintage_color   = sb_vp_color,
			  splinevar       = splinevar,
			  total_cap       = total_cap,
			  vnodes          = vnodes,
			  enodes          = enodes,
			  iedges          = iedges,
			  oedges          = oedges,
			))
		cmd = ('dot', '-T' + ffmt, '-o' + fname + ffmt, fname + 'dot')
		call( cmd )

	os.chdir( '..' )


def CreatePartialSegmentsDiagram ( **kwargs ): #results_segment

	ffmt               = kwargs.get( 'image_format' )
	arrowheadin_color  = kwargs.get( 'arrowheadin_color' )
	arrowheadout_color = kwargs.get( 'arrowheadout_color' )
	sb_vpbackg_color   = kwargs.get( 'sb_vpbackg_color' )
	sb_vp_color        = kwargs.get( 'sb_vp_color' )
	commodity_color    = kwargs.get( 'commodity_color' )
	home_color         = kwargs.get( 'home_color' )
	tech_color         = kwargs.get( 'tech_color' )
	usedfont_color     = kwargs.get( 'usedfont_color' )
	fill_color		   = kwargs.get( 'fill_color' )
	font_color		   = kwargs.get( 'font_color' )
	
	os.chdir( 'results' )

	slice_dot_fmt = """\
strict digraph model {
	label = "Activity split of process %(tech)s, %(vintage)s in year %(period)s" ;

	compound    = "True" ;
	concentrate = "True";
	rankdir     = "LR" ;
	splines     = "%(splinevar)s" ;

	node [ style="filled" ] ;
	edge [ arrowhead="vee" ] ;

	subgraph cluster_slices {
		label = "%(vintage)s Capacity: %(total_cap).2f" ;

		color = "%(vintage_cluster_color)s" ;
		rank  = "same" ;
		style = "filled" ;

		node [ color="%(vintage_color)s", shape="box", fontcolor="%(usedfont_color)s" ] ;

		%(snodes)s
	}

	subgraph energy_carriers {
		node [
		  color     = "%(commodity_color)s",
		  fontcolor = "%(usedfont_color)s",
		  shape     = "circle",
		  fillcolor = "%(fill_color)s"
		] ;

		%(enodes)s
	}

	subgraph inputs {
		edge [ color="%(input_color)s" ] ;

		%(iedges)s
	}

	subgraph outputs {
		edge [ color="%(output_color)s" ] ;

		%(oedges)s
	}
}
"""
	enode_attr_fmt = 'href="../commodities/rc_%%s_%%s.%s"' % ffmt

	for p, t in g_activeCapacityAvailable_pt:
		total_cap = V_CapacityAvailableByPeriodAndTech[p, t]

		for v in g_processVintages[ p, t ]:
			if (p,t,v) in V_ActivityByPeriodAndProcess.keys():
				pass
			else :
				continue

			cap = V_Capacity[t, v]
			vnode = str( v )
			for i in g_processInputs[ p, t, v ]:
				for o in g_processOutputs[ p, t, v ]:
					# energy/vintage nodes, in/out edges
					snodes, enodes, iedges, oedges = set(), set(), set(), set()
					for s in time_season:
						for d in time_of_day:
							flowin = V_FlowIn[p, s, d, i, t, v, o]
							if not flowin: continue
							flowout = V_FlowOut[p, s, d, i, t, v, o]
							snode = "%s, %s" % (s, d)
							snodes.add( (snode, None) )
							if i != 'ethos' :
								enodes.add( (i, enode_attr_fmt % (i, p)) )
								iedges.add( (i, snode, 'label="%.2f"' % flowin) )
							oedges.add( (snode, o, 'label="%.2f"' % flowout) )
							enodes.add( (o, enode_attr_fmt % (o, p)) )

					if not snodes: continue

					snodes = create_text_nodes( snodes, indent=2 )
					enodes = create_text_nodes( enodes, indent=2 )
					iedges = create_text_edges( iedges, indent=2 )
					oedges = create_text_edges( oedges, indent=2 )

					fname = 'results_%s_p%sv%s_segments.' % (t, p, v)
					with open( fname + 'dot', 'w' ) as f:
						f.write( slice_dot_fmt % dict(
						  period          = p,
						  tech            = t,
						  vintage         = v,
						  ffmt            = ffmt,
						  commodity_color = commodity_color,
						  usedfont_color  = usedfont_color,
						  home_color      = home_color,
						  input_color     = arrowheadin_color,
						  output_color    = arrowheadout_color,
						  vintage_cluster_color = sb_vpbackg_color,
						  vintage_color   = sb_vp_color,
						  font_color	  =	font_color,
						  fill_color 	  = fill_color,
						  splinevar       = splinevar,
						  total_cap       = total_cap,
						  snodes          = snodes,
						  enodes          = enodes,
						  iedges          = iedges,
						  oedges          = oedges,
						))
					cmd = ('dot', '-T' + ffmt, '-o' + fname + ffmt, fname + 'dot')
					call( cmd )

	os.chdir( '..' )


def CreateCommodityPartialResults ( **kwargs ): #partial commodities

	ffmt            = kwargs.get( 'image_format' )
	images_dir      = kwargs.get( 'images_dir' )
	sb_arrow_color  = kwargs.get( 'sb_arrow_color' )
	commodity_color = kwargs.get( 'commodity_color' )
	home_color      = kwargs.get( 'home_color' )
	tech_color      = kwargs.get( 'tech_color' )
	usedfont_color  = kwargs.get( 'usedfont_color' )
	unused_color    = kwargs.get( 'unused_color' )
	fill_color	    = kwargs.get( 'fill_color' )
	font_color	    = kwargs.get( 'font_color' )
	
	os.chdir( 'commodities' )

	commodity_dot_fmt = """\
strict digraph result_commodity_%(commodity)s {
	label       = "%(commodity)s - %(period)s" ;

	compound    = "True" ;
	concentrate = "True" ;
	rankdir     = "LR" ;
	splines     = "True" ;

	node [ shape="box", style="filled", fontcolor="%(font_color)s" ] ;
	edge [
	  arrowhead  = "vee",
	  fontsize   = "8",
	  label      = "   ",
	  labelfloat = "False",
	  labelfontcolor = "lightgreen"
	  len        = "2",
	  weight     = "0.5",
	] ;

	%(resource_node)s

	subgraph used_techs {
		node [ color="%(tech_color)s" ] ;

		%(used_nodes)s
	}

	subgraph used_techs {
		node [ color="%(unused_color)s" ] ;

		%(unused_nodes)s
	}

	subgraph in_use_flows {
		edge [ color="%(sb_arrow_color)s" ] ;

		%(used_edges)s
	}

	subgraph unused_flows {
		edge [ color="%(unused_color)s" ] ;

		%(unused_edges)s
	}
}
"""

	FI = V_FlowIn
	FO = V_FlowOut
	used_carriers, used_techs = set(), set()

	for p, t, v in g_processInputs:
		for i in g_processInputs[ p, t, v ]:
			if i == 'ethos':
				continue
			for o in g_processOutputs[ p, t, v ]:
				flowin = sum(
				  FI[p, s, d, i, t, v, o]
				  for s in time_season
				  for d in time_of_day
				)
				if flowin:
					flowout = sum(
					  FO[p, s, d, i, t, v, o]
					  for s in time_season
					  for d in time_of_day
					)
					used_carriers.update( g_processInputs[p, t, v] )
					used_carriers.update( g_processOutputs[p, t, v] )
					used_techs.add( t )

	period_results_url_fmt = '../results/results%%s.%s' % ffmt
	node_attr_fmt = 'href="../results/results_%%s_%%s.%s"' % ffmt
	rc_node_fmt = 'color="%s", href="%s", shape="circle", fillcolor="%s", fontcolor="black"'

	for l_per in time_future:
		url = period_results_url_fmt % l_per
		for l_carrier in used_carriers:
			# enabled/disabled nodes/edges
			enodes, dnodes, eedges, dedges = set(), set(), set(), set()

			rcnode = ((l_carrier, rc_node_fmt % (commodity_color, url, fill_color)),)

			for l_period, l_tech, l_vin in g_processInputs:
				if l_carrier in g_processInputs[l_period, l_tech, l_vin]:
					if l_tech in used_techs and l_period is l_per:
						enodes.add( (l_tech, node_attr_fmt % (l_tech, l_per)) )
						eedges.add( (l_carrier, l_tech, None) )
					else:
						dnodes.add( (l_tech, None) )
						dedges.add( (l_carrier, l_tech, None) )
			for l_period, l_tech, l_vin in g_processOutputs:
				if l_carrier in g_processOutputs[l_period, l_tech, l_vin]:
					if l_tech in used_techs and l_period is l_per:
						enodes.add( (l_tech, node_attr_fmt % (l_tech, l_per)) )
						eedges.add( (l_tech, l_carrier, None) )
					else:
						dnodes.add( (l_tech, None) )
						dedges.add( (l_tech, l_carrier, None) )

			rcnode = create_text_nodes( rcnode )
			enodes = create_text_nodes( enodes, indent=2 )
			dnodes = create_text_nodes( dnodes, indent=2 )
			eedges = create_text_edges( eedges, indent=2 )
			dedges = create_text_edges( dedges, indent=2 )
			
			fname = 'rc_%s_%s.' % (l_carrier, l_per)
			with open( fname + 'dot' ,'w') as f:
				f.write( commodity_dot_fmt % dict(
				  images_dir     = images_dir,
				  home_color     = home_color,
				  usedfont_color = usedfont_color,
				  sb_arrow_color = sb_arrow_color,
				  tech_color     = tech_color,
				  commodity      = l_carrier,
				  period         = l_per,
				  unused_color   = unused_color,
				  font_color	 = font_color,
				  resource_node  = rcnode,
				  used_nodes     = enodes,
				  unused_nodes   = dnodes,
				  used_edges     = eedges,
				  unused_edges   = dedges,
				))

			cmd = ('dot', '-T' + ffmt, '-o' + fname + ffmt, fname + 'dot')
			call( cmd )

	os.chdir( '..' )


def CreateMainResultsDiagram ( **kwargs ): #results_main

	images_dir         = kwargs.get( 'images_dir' )
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

	os.chdir( 'results' )

	results_dot_fmt = """\
strict digraph model {
	label = "Results for %(period)s"

	rankdir = "LR" ;
	smoothtype = "power_dist" ;
	splines = "%(splinevar)s" ;

	node [ style="filled" ] ;
	edge [ arrowhead="vee" ] ;

	subgraph unused_techs {
		node [
		  color     = "%(unused_color)s",
		  fontcolor = "%(unusedfont_color)s",
		  shape     = "box",
		  fontcolor = "%(font_color)s"
		] ;

		%(dtechs)s
	}

	subgraph unused_energy_carriers {
		node [
		  color     = "%(unused_color)s",
		  fontcolor = "%(unusedfont_color)s",
		  shape     = "circle",
		  fillcolor = "%(fill_color)s"
		] ;

		%(dcarriers)s
	}

	subgraph unused_emissions {
		node [
		  color     = "%(unused_color)s",
		  fontcolor = "%(unusedfont_color)s",
		  shape     = "circle",
		  fillcolor = "%(fill_color)s"
		]

		%(demissions)s
	}

	subgraph in_use_techs {
		node [
		  color     = "%(tech_color)s",
		  fontcolor = "%(usedfont_color)s",
		  shape     = "box"
		  fontcolor = "%(font_color)s"

		] ;

		%(etechs)s
	}

	subgraph in_use_energy_carriers {
		node [
		  color     = "%(commodity_color)s",
		  fontcolor = "%(usedfont_color)s",
		  shape     = "circle",
		  fillcolor = "%(fill_color)s"
		] ;

		%(ecarriers)s
	}

	subgraph in_use_emissions {
		node [
		  color     = "%(commodity_color)s",
		  fontcolor = "%(usedfont_color)s",
		  shape     = "circle",
		  fillcolor = "%(fill_color)s"
		] ;

		%(eemissions)s
	}

	subgraph unused_flows {
		edge [ color="%(unused_color)s" ]

		%(dflows)s
	}

	subgraph in_use_flows {
		subgraph inputs {
			edge [ color="%(arrowheadin_color)s" ] ;

			%(eflowsi)s
		}

		subgraph outputs {
			edge [ color="%(arrowheadout_color)s" ] ;

			%(eflowso)s
		}
	}
	
	{rank = same; %(xnodes)s}
}
"""

	tech_attr_fmt = 'label="%%s\\nCapacity: %%.2f", href="results_%%s_%%s.%s"'
	tech_attr_fmt %= ffmt
	commodity_fmt = 'href="../commodities/rc_%%s_%%s.%s"' % ffmt
	flow_fmt = 'label="%.2f"'

	V_Cap = V_CapacityAvailableByPeriodAndTech
	FI = V_FlowIn
	FO = V_FlowOut
	EI = V_EnergyConsumptionByPeriodInputAndTech    # Energy In
	EO = V_ActivityByPeriodTechAndOutput            # Energy Out
	EmiO = V_EmissionActivityByPeriodAndTech

	epsilon = 0.005  # we only care about last two decimals
	  # but perhaps this should be configurable?  Not until we can do this
	  # both after the fact (i.e. not synchronous with a solve), and via a
	  # configuration file.

	for pp in time_optimize:
		# enabled/disabled   techs/carriers/emissions/flows   in/out
		etechs, dtechs, ecarriers, xnodes = set(), set(), set(), set()
		eemissions = set()
		eflowsi, eflowso, dflows = set(), set(), set()   # edges
		usedc, usede = set(), set()    # used carriers, used emissions

		for tt in tech_all:
			if (pp, tt) not in V_Cap.keys(): continue

			cap = V_Cap[pp, tt]

			if cap:
				etechs.add( (tt, tech_attr_fmt % (tt, cap, tt, pp)) )
			else:
				dtechs.add( (tt, None) )

			for vv in g_processVintages[ pp, tt ]:
				for ii in g_processInputs[ pp, tt, vv ]:
					if (pp,ii,tt) in EI.keys():
						inp = EI[pp, ii, tt]
					else:
						inp =0
					if inp >= epsilon:
						if ii != 'ethos' :
							eflowsi.add( (ii, tt, flow_fmt % inp) )
							ecarriers.add( (ii, commodity_fmt % (ii, pp)) )
							usedc.add( ii )
						else:
							xnodes.add((tt, tech_attr_fmt % (tt, V_Cap[pp, tt], tt, pp)))
					else:
						if ii != 'ethos' :
							dflows.add( (ii, tt, None) )
						else:
							xnodes.add((tt, None))
				for oo in g_processOutputs[ pp, tt, vv ]:
					if(pp, tt, oo) in EO.keys():
						out = EO[pp, tt, oo]
					else:
						out = 0
					if out >= epsilon:
						eflowso.add( (tt, oo, flow_fmt % out) )
						ecarriers.add( (oo, commodity_fmt % (oo, pp)) )
						usedc.add( oo )
					else:
						dflows.add( (tt, oo, None) )

		for ee, ii, tt, vv, oo in EmissionActivity.keys():
			if ( pp, tt, vv ) in g_activeActivity_ptv:
				if (pp, tt) in EmiO.keys():
					amt = EmiO[pp, tt]
				else:
					amt = 0
				if amt < epsilon: continue

				eflowso.add( (tt, ee, flow_fmt % amt) )
				eemissions.add( (ee, None) )
				usede.add( ee )

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

		# link to periods: Do we want to include this in the SVG, or just let the
		# modeler use the standard browser buttons?  I think the latter.
		# for randstr in l_perset:
			# url = 'results%s.%s' % (randstr, ffmt)
			# l_file.write (str(randstr) + '[URL="' + url + '",fontcolor=' + usedfont_color + ', rank="min", style=filled, shape=box, color=' + menu_color + '];\n')
		# l_file.write( images + '[URL="..",shape=house, style=filled, fontcolor=' + usedfont_color + ', color=' + home_color + '];\n')
		# l_file.write ("}\n");
		# l_file.close()

		fname = 'results%s.' % pp
		with open( fname + 'dot', 'w' ) as f:
			f.write( results_dot_fmt % dict(
			  period             = pp,
			  splinevar          = splinevar,
			  arrowheadin_color  = arrowheadin_color,
			  arrowheadout_color = arrowheadout_color,
			  commodity_color    = commodity_color,
			  tech_color         = tech_color,
			  unused_color       = unused_color,
			  unusedfont_color   = unusedfont_color,
			  usedfont_color     = usedfont_color,
			  fill_color		 = fill_color,
			  font_color		 = font_color,
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
	

def quick_run( **kwargs ) : # Call this function if the input file is a database.
	inp_file		   = kwargs.get( 'inp_file' )
	q_flag			   = kwargs.get( 'q_flag' )
	quick_n 		   = kwargs.get( 'quick_n' )
	scenario_name	   = kwargs.get( 'scenario_name' )
	images_dir         = kwargs.get( 'images_dir' )
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
	
	global inp_comm, out_comm
	nodes, tech, ltech, to_tech, from_tech = set(), set(), set(), set(), set()
	if q_flag:
		# Specify the Input and Output Commodities to choose from. Default puts all commodities in the Graph.
		if inp_comm is None and out_comm is None :
			inp_comm = "NOT NULL"
			out_comm = "NOT NULL"
		else :
			if inp_comm is None :
				inp_comm = "NULL"
			else :
				inp_comm = "'"+inp_comm+"'"
			if out_comm is None :
				out_comm = "NULL"
			else :
				out_comm = "'"+out_comm+"'"
		
		#connect to the database
		con = sqlite3.connect(inp_file)
		cur = con.cursor()   # a database cursor is a control structure that enables traversal over the records in a database
		con.text_factory = str #this ensures data is explored with the correct UTF-8 encoding

		print inp_file
		cur.execute("SELECT input_comm, tech, output_comm FROM Efficiency WHERE input_comm is "+inp_comm+" or output_comm is "+out_comm)
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
		if inp_comm is None and out_comm is None :
			inp_comm = "\w+"
			out_comm = "\w+"
		else :
			if inp_comm is None :
				inp_comm = "\W+"
			if out_comm is None :
				out_comm = "\W+"

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
					if not re.search(inp_comm, row[0]) and not re.search(out_comm, row[3]) :
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
	model_dot_fmt = """\
strict digraph model {
	rankdir = "LR" ;

	// Default node and edge attributes
	node [ style="filled" ] ;
	edge [ arrowhead="vee", labelfontcolor="lightgreen" ] ;

	// Define individual nodes
	subgraph techs {
		node [ color="%(tech_color)s", shape="box", fontcolor="%(font_color)s" ] ;

		%(tnodes)s
	}

	subgraph energy_carriers {
		node [ color="%(commodity_color)s", shape="circle", fillcolor="%(fill_color)s" ] ;

		%(enodes)s
	}

	// Define edges and any specific edge attributes
	subgraph inputs {
		edge [ color="%(arrowheadin_color)s" ] ;

		%(iedges)s
	}

	subgraph outputs {
		edge [ color="%(arrowheadout_color)s" ] ;

		%(oedges)s
	}
	
	{rank = same; %(snodes)s}
}
"""

	with open( quick_n + '.dot', 'w' ) as f:
		f.write( model_dot_fmt % dict(
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
	cmd = ('dot', '-T' + ffmt, '-o' + quick_n+'.' + ffmt, quick_n+'.dot')
	call( cmd )



def CreateModelDiagrams ():
	# This function is a "master", calling many other functions based on command
	# line input.  Other than code cleanliness, there is no reason that the
	# logic couldn't be in main()

	# if the user has listed more than one dot_dat, arbitrarily choose the first
	# as the name of this run.
	#datname = os.path.basename( options.dot_dat[0] )[:-4]
	datname = scenario
	
	if not quick_flag:
		images_dir = quick_name + "_" + scenario
		if os.path.exists( images_dir ):
			rmtree( images_dir )
		os.mkdir( images_dir )
		os.chdir( images_dir )
		os.makedirs( 'commodities' )
		os.makedirs( 'processes' )
		os.makedirs( 'results' )
	else:
		images_dir = quick_name
		if os.path.exists( images_dir ):
			rmtree( images_dir )
		os.mkdir( images_dir )
		os.chdir( images_dir )

	##############################################
	#MAIN MODEL AND RESULTS AND EVERYTHING ELSE
	kwargs = dict(
	  inp_file			 = ifile,
	  scenario_name		 = scenario,
	  q_flag			 = True if db_dat_flag else False,
	  quick_n		 	 = quick_name,
	  images_dir         = '%s_%s' % (quick_name, scenario),
	  image_format       = graph_format.lower(),

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

	  #SUBGRAPHS (option 1),
	  sb_incom_color     = 'lightsteelblue' if grey_flag else 'black',
	  sb_outcom_color    = 'lawngreen' if grey_flag else 'black',
	  sb_vpbackg_color   = 'lightgrey',
	  sb_vp_color        = 'white',
	  sb_arrow_color     = 'forestgreen' if grey_flag else 'black',

	  #SUBGRAPH 1 ARROW COLORS
	    # feel free to add more colors here
	  color_list = ('red', 'orange', 'gold', 'green', 'blue', 'purple',
	                'hotpink', 'cyan', 'burlywood', 'coral', 'limegreen',
	                'black', 'brown') if grey_flag else ('black', 'black'),
	)
	####################################

	# Do all necessary work in parallel, taking advantage of whatever cores
	# are available to the computer on which this code is run.  To add a
	# function to the pool, ensure that the function is in the 'gvizFunctions'
	# tuple below, and that the function has all it needs to work passed in
	# via the 'kwargs' dict above.

	gvizFunctions = (
	  CreateCompleteEnergySystemDiagram,
	  CreateCommodityPartialGraphs,
	  CreateProcessPartialGraphs,
	  CreateMainModelDiagram,
	  CreateTechResultsDiagrams,
	  CreateCommodityPartialResults,
	  CreateMainResultsDiagram,
	  CreatePartialSegmentsDiagram,
	) if (quick_flag==False) else (quick_run, )

	for func in gvizFunctions:
			func( **kwargs )

	os.chdir( '..' )

###########Code Starts here#############

def help_user() :
	print '''Use as:
	python Make_Graphviz.py -i (or --input) <input filename>
	| -f (or --format) <Graphviz output format> (Default: svg)
	| -c (or --show_capacity) Choose whether or not the capacity shows up in the
								subgraphs. [Default: not shown]
	| -v (or --splinevar) Choose whether the subgraph edges needs to be straight
							or curved. [Default: use straight lines, not splines]
	| -t (or --graph_type) {explicit_vintages,separate_vintages}
							Choose the type of subgraph depiction desired.
							[Default: separate_vintages]
	| -g (or --gray) if specified, prints graph in grayscale
	| -s (or --scenario) <required scenario name from database>
	| -n (or --name) specify the extension you wish to give your quick run
	| -o (or --output) <Optional output file path(to dump the images folder)>
	| -h  (or --help) print help'''
  
try:
	argv = sys.argv[1:]
	opts, args = getopt.getopt(argv, "hf:cvt:i:s:n:go:", ["help", "format=", "show_capacity", "splinevar", "graph_type=", "input=", "scenario=", "name=", "grey", "output="])
except getopt.GetoptError:          
	help_user()                          
	sys.exit(2) 
	
for opt, arg in opts:
	if opt in ("-h", "--help"):
		help_user()
		sys.exit()
	elif opt in ("-i", "--input"):
		ifile = arg
	elif opt in ("-f", "--format"):
		graph_format = arg
	elif opt in ("-c", "--show_capacity"):
		show_capacity = True
	elif opt in ("-v", "--splinevar") :
		splinevar = True
	elif opt in ("-t", "--graph_type") :
		graph_type = arg
	elif opt in ("-s", "--scenario") :
		scenario = arg
	elif opt in ("-n", "--name") :
		quick_name = arg
	elif opt in ("-o", "--output") :
		res_dir = arg
	elif opt in ("-g", "--grey") :
		grey_flag = False

if ifile is None:
	print "You did not specify one or more of the following required flags: -i(or --input)"
	help_user()
	sys.exit()

file_ty = re.search(r"(\w+)\.(\w+)\b", ifile) # Extract the input filename and extension
if not file_ty :
	print "The file type %s is not recognized." % ifile
	sys.exit(2)
elif file_ty.group(2) in ("db", "sqlite", "sqlite3", "sqlitedb") :
	db_dat_flag = 1
	if scenario is None:
		quick_flag = True
		if quick_name is None:
			quick_name = file_ty.group(1)
		else:
			quick_name = file_ty.group(1) + '_' + quick_name
	else:
		quick_name = file_ty.group(1)
		
elif file_ty.group(2) in ("dat", "txt") :
	quick_flag = True
	db_dat_flag = 0
	if quick_name is None:
		quick_name = file_ty.group(1)
	else:
		quick_name = file_ty.group(1) + '_' + quick_name
else :
	print "The input file type %s is not recognized. Please specify a database or a text file." % ifile
	sys.exit(2)
	
print "Reading File %s ..." %ifile 
if quick_flag :
	ifile = os.path.realpath(ifile)
	if res_dir is None:
		res_dir = "current directory"
	else:
		os.chdir(res_dir)
	CreateModelDiagrams ()
	print "Done. Look for results in %s" %res_dir
else:
	db_file(ifile)
	InitializeProcessParameters ()
	calc_intermediates(ifile)
	print "Creating Diagrams..."
	if res_dir is None:
		res_dir = "current directory"
	else:
		os.chdir(res_dir)
	CreateModelDiagrams ()
	print "Done. Look for results in %s_%s folder in %s" %(quick_name, scenario, res_dir)