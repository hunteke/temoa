import sys
import getopt
import re

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
	| -g (or --grey) if specified, prints graph in grayscale
	| -s (or --scenario) <required scenario name from database>
	| -n (or --name) specify the extension you wish to give your quick run
	| -o (or --output) <Optional output file path(to dump the images folder)>
	| -b (or --technology) <Cannot be used with '-a'> Commodity to render diagram around
	| -a (or --commodity) <Cannot be used with '-b'> Technology to render diagram around
	| -y (or --year) the period for which the graph is to be generated (valid only in case of output graph)
	| -h  (or --help) print help'''	

def processInputArgs(inputs):
	output = dict(
		ifile = None,
		graph_format = 'svg',
		show_capacity = False,
		graph_type = 'separate_vintages',
		splinevar = False,
		quick_flag = False,
		quick_name = None,
		grey_flag = True,
		scenario = None,
		res_dir = None,
		inp_comm = None,
		inp_tech = None,
		inp_year = None,
		db_dat_flag = None,
	)

	if inputs is None:
		raise "no arguments found"
	
	for opt, arg in inputs.iteritems():
		print "%s == %s" %(opt, arg)
		
		if opt in ("-h", "--help"):
			help_user()
			sys.exit()
		if opt in ("-i", "--input"):
			output['ifile'] = arg
		elif opt in ("-f", "--format"):
			output['graph_format'] = arg
		elif opt in ("-c", "--show_capacity"):
			output['show_capacity'] = True
		elif opt in ("-v", "--splinevar") :
			output['splinevar'] = True
		elif opt in ("-t", "--graph_type") :
			output['graph_type'] = arg
		elif opt in ("-s", "--scenario") :
			output['scenario'] = arg
		elif opt in ("-y", "--year") :
			output['inp_year'] = int(arg)
		elif opt in ("-n", "--name") :
			output['quick_name'] = arg
		elif opt in ("-o", "--output") :
			output['res_dir'] = arg
		elif opt in ("-g", "--grey") :
			output['grey_flag'] = False
		elif opt in ("-a", "--comm") :
			output['inp_comm'] = arg
		elif opt in ("-b", "--tech") :
			output['inp_tech'] = arg

	if output['ifile'] is None:
			print "You did not specify one or more of the following required flags: -i(or --input)"
			raise "Input file is missing"

	file_ty = re.search(r"([\w-]+)\.(\w+)\b", output['ifile']) # Extract the input filename and extension
	
	if not file_ty :
		raise "The file type %s is not recognized." % output['ifile']
		
	elif file_ty.group(2) in ("db", "sqlite", "sqlite3", "sqlitedb") :
		output['db_dat_flag'] = 1
		
		if output['scenario'] is None:
			output['quick_flag'] = True
			if output['quick_name'] is None:
				output['quick_name'] = file_ty.group(1)
			else:
				output['quick_name'] = file_ty.group(1) + '_' + output['quick_name']
		
		else:
			output['quick_name'] = file_ty.group(1)
			
	elif file_ty.group(2) in ("dat", "txt") :
		output['quick_flag'] = True
		output['db_dat_flag'] = 0
	
		if output['quick_name'] is None:
			output['quick_name'] = file_ty.group(1)
		else:
			output['quick_name'] = file_ty.group(1) + '_' + output['quick_name']
	
	else :
		print "The input file type %s is not recognized. Please specify a database or a text file." % output['ifile']
		sys.exit(2)
	return output

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