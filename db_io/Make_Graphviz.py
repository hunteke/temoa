from subprocess import call
import os
import sys

from GraphVizUtil import *
from DatabaseUtil import *
from GraphVizFormats import *


def CreateMainResultsDiagram ( **kwargs ): #results_main
	folder = 'whole_system'
	ffmt               = kwargs.get( 'image_format' )
	pp				   = kwargs.get( 'period')

	if (not os.path.exists(folder)):
		os.makedirs( folder )
	os.chdir( folder )
	fname = 'results%s.' % pp
	if (kwargs['grey_flag']):
		fname += 'grey.'

	if (os.path.exists(fname + ffmt)):
		return os.path.join(folder, fname + ffmt)

	dbUtil = DatabaseUtil(kwargs.get( 'ifile' ), kwargs.get( 'scenario_name' ))

	time_exist = dbUtil.getTimePeridosForFlags(flags=['e'])
	time_future = dbUtil.getTimePeridosForFlags(flags=['f'])
	time_optimize = set(sorted( time_future)[:-1])
	
	tech_all = dbUtil.getTechnologiesForFlags(flags=['r','p','pb','ps'])
	
	commodity_carrier = dbUtil.getCommoditiesForFlags(flags=['d','p'])
	commodity_emissions = dbUtil.getCommoditiesForFlags(flags=['e'])

	Efficiency_Input = dbUtil.getCommoditiesByTechnology(comm_type='input')
	Efficiency_Output = dbUtil.getCommoditiesByTechnology(comm_type='output')	

	V_Cap2 = dbUtil.getCapacityForTechAndPeriod(period=pp)
	
	EI2 = dbUtil.getOutputFlowForPeriod(period=pp, comm_type='input')
	EO2 = dbUtil.getOutputFlowForPeriod(period=pp, comm_type='output')

	EmiO2 = dbUtil.getEmissionsActivityForPeriod(period=pp)

	dbUtil.close()

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
			eflowsi.add((row['input_comm'], row['tech'], flow_fmt % row['flow']))
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
		eflowso.add((row['tech'], row['output_comm'], flow_fmt % row['flow']))
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

	args = dict(
	dtechs     = create_text_nodes( dtechs,     indent=2 ),
	etechs     = create_text_nodes( etechs,     indent=2 ),
	xnodes	   = create_text_nodes( xnodes,		indent=2 ),
	dcarriers  = create_text_nodes( dcarriers,  indent=2 ),
	ecarriers  = create_text_nodes( ecarriers,  indent=2 ),
	demissions = create_text_nodes( demissions, indent=2 ),
	eemissions = create_text_nodes( eemissions, indent=2 ),
	dflows     = create_text_edges( dflows,     indent=2 ),
	eflowsi    = create_text_edges( eflowsi,    indent=3 ),
	eflowso    = create_text_edges( eflowso,    indent=3 ),)
	args.update(kwargs)
	
	with open( fname + 'dot', 'w' ) as f:
		f.write( results_dot_fmt % args)

	cmd = ('dot', '-T' + ffmt, '-o' + fname + ffmt, fname + 'dot')
	call( cmd )

	os.chdir( '..' )
	return os.path.join(folder, fname + ffmt)

# Needs some small fixing - cases where no input but output is there. # Check sample graphs
def CreateTechResultsDiagrams ( **kwargs ): # tech results
	folder = 'processes'
	ffmt               = kwargs.get( 'image_format' )
	per 			   = kwargs.get( 'period' )
	tech 			   = kwargs.get( 'inp_technology' )
	
	if (not os.path.exists(folder)):
		os.makedirs( folder )
	os.chdir( folder )
	fname = 'results_%s_%s.' % (tech, per)
	if (kwargs['grey_flag']):
		fname += 'grey.'

	if (os.path.exists(fname + ffmt)):
		return os.path.join(folder, fname + ffmt)

	# enode_attr_fmt = 'href="../commodities/rc_%%s_%%s.%s"' % ffmt
	# vnode_attr_fmt = 'href="results_%%s_p%%sv%%s_segments.%s", ' % ffmt
	# vnode_attr_fmt += 'label="%s\\nCap: %.2f"'
	enode_attr_fmt = 'href="#", onclick="loadNextGraphvizGraph(\'results\', \'%s\', \'%s\')"'
	vnode_attr_fmt = 'href="#", onclick="loadNextGraphvizGraph(\'%s\', \'%s\', \'%s\')"'
	vnode_attr_fmt += 'label="%s\\nCap: %.2f"'

	dbUtil = DatabaseUtil(kwargs.get( 'ifile' ), kwargs.get( 'scenario_name' ))
	total_cap = dbUtil.getCapacityForTechAndPeriod(tech, per)
	flows = dbUtil.getCommodityWiseInputAndOutputFlow(tech, per)
	dbUtil.close()

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
		args = dict(
		cluster_vintage_url = cluster_vintage_url,
		total_cap       = total_cap,
		vnodes          = create_text_nodes( vnodes, indent=2 ),
		enodes          = create_text_nodes( enodes, indent=2 ),
		iedges          = create_text_edges( iedges, indent=2 ),
		oedges          = create_text_edges( oedges, indent=2 ),
		)
		args.update(kwargs)

		with open( fname + 'dot', 'w' ) as f:
			f.write( tech_results_dot_fmt % args)
		cmd = ('dot', '-T' + ffmt, '-o' + fname + ffmt, fname + 'dot')
		call( cmd )


	os.chdir( '..' )
	return os.path.join(folder, fname + ffmt)

def CreateCommodityPartialResults ( **kwargs ): 
	print 'Starting commodity partial results'
	folder 		= 'commodities'
	ffmt            = kwargs.get( 'image_format' )
	per 			= kwargs.get( 'period' )
	comm 			= kwargs.get( 'inp_commodity' )
	
	if (not os.path.exists(folder)):
		os.makedirs( folder )
	os.chdir( folder )
	fname = 'rc_%s_%s.' % (comm, per)
	if (kwargs['grey_flag']):
		fname += 'grey.'
	
	print 'checked and Generated folders'
	
	if (os.path.exists(fname + ffmt)):
		return os.path.join(folder, fname + ffmt)

	print 'Starting database queries'
	dbUtil = DatabaseUtil(kwargs.get( 'ifile' ), kwargs.get( 'scenario_name' ))
	input_total = set(dbUtil.getExistingTechnologiesForCommodity(comm, 'output')['tech'])
	output_total = set(dbUtil.getExistingTechnologiesForCommodity(comm, 'input')['tech'])
	
	flow_in = dbUtil.getOutputFlowForPeriod(per, 'input', comm)
	otechs = set(flow_in['tech'])

	flow_out = dbUtil.getOutputFlowForPeriod(per, 'output', comm)
	itechs = set(flow_out['tech'])

	dbUtil.close()
	print 'done with database queries'

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
		t = flow_in.iloc[i]['tech']
		f = flow_in.iloc[i]['flow']
		enodes.add( (t, node_attr_fmt % (t, per)) )
		eedges.add( (comm, t, 'label="%.2f"' % f) )
	for t in output_total - otechs:
		dnodes.add( (t, None) )
		dedges.add( (comm, t, None) )
	for i in range(len(flow_out)):
		t = flow_out.iloc[i]['tech']
		f = flow_out.iloc[i]['flow']
		enodes.add( (t, node_attr_fmt % (t, per)) )
		eedges.add( (t, comm, 'label="%.2f"' % f) )
	for t in input_total - itechs:
		dnodes.add( (t, None) )
		dedges.add( (t, comm, None) )

	print 'Done with nodes and edgs'
	args = dict(
	resource_node = create_text_nodes( rcnode ),
	used_nodes = create_text_nodes( enodes, indent=2 ),
	unused_nodes = create_text_nodes( dnodes, indent=2 ),
	used_edges = create_text_edges( eedges, indent=2 ),
	unused_edges = create_text_edges( dedges, indent=2 ),
	)
	args.update(kwargs)
	
	with open( fname + 'dot' ,'w') as f:
		f.write( commodity_dot_fmt % args)

	cmd = ('dot', '-T' + ffmt, '-o' + fname + ffmt, fname + 'dot')
	call( cmd )

	os.chdir( '..' )
	print 'Finished commodity partial results. returning'
	return os.path.join(folder, fname + ffmt)

def createCompleteInputGraph( **kwargs ) : # Call this function if the input file is a database.
	quick_name 		   = kwargs.get( 'quick_name' )
	ffmt               = kwargs.get( 'image_format' )
	
	nodes, tech, ltech, to_tech, from_tech = set(), set(), set(), set(), set()
	dbUtil = DatabaseUtil(kwargs.get( 'ifile' ))

	if kwargs.get( 'q_flag' ):
		res = dbUtil.getCommoditiesAndTech(kwargs.get( 'inp_commodity' ), kwargs.get( 'inp_technology' ))
	else:
		res = dbUtil.readFromDatFile(kwargs.get( 'inp_commodity' ), kwargs.get( 'inp_technology' ))

	dbUtil.close()
		
	for i in range(len(res)):
		row = res.iloc[i]
		if row['input_comm'] != 'ethos':
			nodes.add(row['input_comm'])
		else :
			ltech.add(row['tech'])
		nodes.add(row['output_comm'])
		tech.add(row['tech'])
		# Now populate the dot file with the concerned commodities
		if row['input_comm'] != 'ethos':
			to_tech.add('"%s"' % row['input_comm'] + '\t->\t"%s"' % row['tech']) 
		from_tech.add('"%s"' % row['tech'] + '\t->\t"%s"' % row['output_comm'])

	
	print "Creating Diagrams...\n"

	args = dict(
	enodes      = "".join('"%s";\n\t\t' % x for x in nodes),
	tnodes      = "".join('"%s";\n\t\t' % x for x in tech),
	iedges      = "".join('%s;\n\t\t' % x for x in to_tech),
	oedges      = "".join('%s;\n\t\t' % x for x in from_tech),
	snodes      = ";".join('"%s"' %x for x in ltech),
	)
	args.update(kwargs)

	with open( quick_name + '.dot', 'w' ) as f:
		f.write( quick_run_dot_fmt % args)
	del nodes, tech, to_tech, from_tech
	cmd = ('dot', '-T' + ffmt, '-o' + quick_name+'.' + ffmt, quick_name+'.dot')
	call( cmd )
	return quick_name+'.'+ffmt
	
def createGraphBasedOnInput(inputs):
	kwargs = processInputArgs(inputs)
	os.chdir(kwargs['res_dir'])

	print "Reading File %s ..." %kwargs['ifile'] 
	print "CreateModelDiagrams with quick_flag = ", kwargs['quick_flag']

	# CreateModelDiagrams function stuff
	if not kwargs['quick_flag']:
		images_dir = kwargs['quick_name'] + "_" + kwargs['scenario_name']
	else:
		images_dir = kwargs['quick_name']

	images_dir += '_graphviz'

	if (not os.path.exists(images_dir)):
		os.mkdir( images_dir )
	os.chdir( images_dir )

	print "Created output folders"
	
	output_filename = ""
	if (kwargs['quick_flag'] == True):
		print "Generating createCompleteInputGraph"
		output_filename = createCompleteInputGraph(**kwargs)
	elif (kwargs['inp_technology'] is None and kwargs['inp_commodity'] is None):
		print "Generating CreateMainResultsDiagram"
		output_filename = CreateMainResultsDiagram(**kwargs)
	elif (kwargs['inp_commodity'] is None):
		print "Generating CreateTechResultsDiagrams"
		output_filename = CreateTechResultsDiagrams(**kwargs)
	elif (kwargs['inp_technology'] is None):
		print "Generating CreateCommodityPartialResults"
		output_filename = CreateCommodityPartialResults(**kwargs)

	os.chdir( '..' )
	result = os.path.join(images_dir, output_filename)

	print "Done. Look for results in %s" %kwargs['res_dir']
	return result


if __name__ == "__main__":	
	argv = sys.argv[1:]
	createGraphBasedOnInput(argv)
