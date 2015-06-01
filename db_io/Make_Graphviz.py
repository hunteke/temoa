from subprocess import call
import sqlite3
import sys
import getopt
import re
	
nodes = set()
ltech = set()
tech = set()
to_tech = set()
from_tech = set()
ifile = None  #Input File
fname = None  #Output Graphviz Filename
ffmt = 'svg'  #Default Format
set_color = 0 #Default Colored Outputs
inp_comm = None
out_comm = None

def help_user() :
	print '''Use as:
	python task1.py -d (or --datafile) <input filename>
	| -f (or --format) <Graphviz output format> (Optional: defaults to svg)
	| -i (or --input) <input commodity name> (Optional)
	| -o (or --output) <output commodity name> (Optional)
	| -n (or --name) <name of output Graphviz file> (Optional: defaults to datafile name)
	| -g (or --gray) if specified, prints graph in grayscale
	| -h  (or --help) print help'''

try:
	argv = sys.argv[1:]
	opts, args = getopt.getopt(argv, "hgd:f:i:o:n:", ["help", "gray", "datafile=", "format=", "input=", "output=", "name="])
except getopt.GetoptError:          
	help_user()                          
	sys.exit(2) 
	
for opt, arg in opts:
	if opt in ("-f", "--format"):
		ffmt = arg
	elif opt in ("-i", "--input"):
		inp_comm = arg
	elif opt in ("-o", "--output"):
		out_comm = arg
	elif opt in ("-n", "--name"):
		fname = arg
	elif opt in ("-d", "--datafile") :
		ifile = arg
	elif opt in ("-g", "--gray") :
		set_color = '1'
	elif opt in ("-h", "--help") :
		help_user()
		sys.exit()


def db_file(ifile) : # Call this function if the input file is a database.
	global inp_comm, out_comm
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
	con = sqlite3.connect(ifile)
	cur = con.cursor()   # a database cursor is a control structure that enables traversal over the records in a database
	con.text_factory = str #this ensures data is explored with the correct UTF-8 encoding

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

def txt_file(ifile) : # Call this function if the input file is in Text Format
	global inp_comm, out_comm
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
				nodes.add(row[3])
				tech.add(row[1])
				# Now populate the dot file with the concerned commodities
				if row[0] != 'ethos':
					to_tech.add('"%s"' % row[0] + '\t->\t"%s"' % row[1])
				from_tech.add('"%s"' % row[1] + '\t->\t"%s"' % row[3])
						
	if eff_flag is False :	
		print ("Error: The Efficiency Parameters cannot be found in the specified file - "+ifile)
		sys.exit(2)

			
if ifile is None :
	print "You did not specify the input file, remember to use '-d' option"
	help_user()
	sys.exit(2)
else :
	file_type = re.search(r"(\w+)\.(\w+)\b", ifile) # Extract the input filename and extension
	if not file_type :
		print "The file type %s is not recognized." % ifile
		sys.exit(2)
	elif file_type.group(2) in ("db", "sqlite", "sqlite3", "sqlitedb") :
		db_file(ifile)
	elif file_type.group(2) in ("dat", "txt") :
		txt_file(ifile)
	else :
		print "The input file type %s is not recognized. Please specify a database or a text file." % ifile
		sys.exit(2)
		
	if fname is None :
		fname = file_type.group(1)

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
if set_color == '1' :
	arrowheadin_col  = "black"
	arrowheadout_col = "black"
	commodity_col    = "black"
	tech_col         = "black"
	font_col         = "white"
	fill_col         = "white"
else :
	arrowheadin_col  = "firebrick"
	arrowheadout_col = "forestgreen"
	commodity_col    = "lightsteelblue"
	tech_col         = "darkseagreen"
	font_col         = "black"
	fill_col         = "lightsteelblue"

with open( fname + '.dot', 'w' ) as f:
		f.write( model_dot_fmt % dict(
		  arrowheadin_color  = arrowheadin_col,
		  arrowheadout_color = arrowheadout_col,
		  commodity_color    = commodity_col,
		  tech_color         = tech_col,
		  font_color         = font_col,
		  fill_color         = fill_col,
		  enodes             = "".join('"%s";\n\t\t' % x for x in nodes),
		  tnodes             = "".join('"%s";\n\t\t' % x for x in tech),
		  iedges             = "".join('%s;\n\t\t' % x for x in to_tech),
		  oedges             = "".join('%s;\n\t\t' % x for x in from_tech),
		  snodes             = ";".join('"%s"' %x for x in ltech),
		))
del nodes, tech, to_tech, from_tech

cmd = ('dot', '-T' + ffmt, '-o' + fname+ '.' + ffmt, fname + '.dot')
call( cmd )