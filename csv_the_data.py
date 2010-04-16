#!/usr/bin/env python

import re
import sys

# This is crap code.  It is not documented because it's only in the
# repository as a temporary measure, and I do *not* want to encourage
# anyone to rely on this code for anything even remotely mission critical.

def parse_input ( data ):
	from operator import itemgetter
	try:
		import yaml
	except ImportError, err:
		msg  = "  ImportError: %s\n" % str(err)
		msg += "\nThis script relies on an external code base.  You'll need to\n"
		msg += "install the YAML library for Python.  e.g.\n"
		msg += "\nsudo apt-get install python-yaml\n"
		sys.stderr.write( msg )

		return

	data = yaml.load( data )
	variables = data['Solution'][1]['Variable']

	xu_regex = re.compile( '^xu\[(\w+),(\d+),(\d+)\]$' )
	xc_regex = re.compile( '^xc\[(\w+),(\d+)\]$' )

	xc = list()
	xu = list()

	for k in variables.keys():
		reg = xc_regex.match( k )
		if ( reg is not None ):
			line = [
			  'xc',
			  reg.group(1),
			  int(reg.group(2)),
			  variables[k]['Value'],
			]
			xc.append( line )
			continue

		reg = xu_regex.match( k )
		if ( reg is not None ):
			line = [
			  'xu',
			  reg.group(1),
			  int( reg.group(2) ),
			  int( reg.group(3) ),
			  variables[k]['Value'],
			]
			xu.append( line )
			continue

	xc_sorted_by_tech  = sorted(xc, key=itemgetter(1))
	xc_sorted_by_year  = sorted(xc, key=itemgetter(2))
	xc_sorted_by_value = sorted(xc, key=itemgetter(3))

	xu_sorted_by_value  = sorted(xu, key=itemgetter(4))
	xu_sorted_by_invest = sorted(xu_sorted_by_value,  key=itemgetter(2))
	xu_sorted_by_year   = sorted(xu_sorted_by_invest, key=itemgetter(3))
	xu_sorted_by_tech   = sorted(xu_sorted_by_year, key=itemgetter(1))

	xu_summed_invest = dict()
	for i in xu_sorted_by_tech:
		tech = i[1]
		year = i[3]
		if ( tech not in xu_summed_invest ):
			xu_summed_invest.update( { tech : dict() } )
		if ( year not in xu_summed_invest[tech] ):
			xu_summed_invest[tech].update( { year : 0 } )
		xu_summed_invest[tech][year] += i[4]

	years = sorted( set( [year
		for year in xu_summed_invest[tech]
		for tech in xu_summed_invest]) )

	# Done with xu_summed_invest, repurpose it
	xu_summed = ['Technology']
	xu_summed.extend(years)
	xu_summed = [xu_summed]

	for tech in xu_summed_invest:
		row = [
		  xu_summed_invest[tech][y] if y in xu_summed_invest[tech] else 0
		  for y in years ]
		row.insert(0, tech)
		xu_summed.append( row )
	xu_summed = sorted( xu_summed )

	import csv, cStringIO
	xc_by_tech  = cStringIO.StringIO()
	xc_by_year  = cStringIO.StringIO()
	xc_by_value = cStringIO.StringIO()
	xu_summed_f = cStringIO.StringIO()

	writer = csv.writer( xc_by_tech );  writer.writerows( xc_sorted_by_tech )
	writer = csv.writer( xc_by_year );  writer.writerows( xc_sorted_by_year )
	writer = csv.writer( xc_by_value ); writer.writerows( xc_sorted_by_value )
	writer = csv.writer( xu_summed_f );   writer.writerows( xu_summed )
	xc_by_tech.reset()
	xc_by_year.reset()
	xc_by_value.reset()
	xu_summed_f.reset()

	output  = '"XC, sorted by technology:"\n'
	output += xc_by_tech.read()
	output += '\n"XC, sorted by year:"\n'
	output += xc_by_year.read()
	output += '\n"XC, sorted by value:"\n'
	output += xc_by_value.read()
	output += '\n"XU, summed across investment period"\n'
	output += xu_summed_f.read()

	return output

def open_handle ( path, mode, fallback ):
	if '-' == path:
		source = fallback
	else:
		source = open( path, mode )

	return ( source )


def main ( **kwargs ):
	ifile = kwargs.pop( 'ifile', '-' )
	ofile = kwargs.pop( 'ofile', '-' )

	ifile = open_handle( ifile, 'r', sys.stdin )
	csv = parse_input( ifile )
	ifile.close()

	ofile = open_handle( ofile, 'w', sys.stdout )
	ofile.write( csv )
	ofile.close()


def usage ( ):
	import sys, os

	basename = os.path.basename( sys.argv[0] )
	
	print """ usage: %(BNAME)s [-i <path>] [-o <path>]

   -i <path>   input filename  (ex: '%(IFILE)s', '-')
   -o <path>   output filename (ex: '%(OFILE)s', '-')

 If no arguments are passed, this script assumes you want to use stdin and
 stdout.  Example usages:

   # Ex: read from stdin and write to stdout:
 %(BNAME)s < %(IFILE)s > %(OFILE)s
 %(BNAME)s -i - < %(IFILE)s > %(OFILE)s      # equivalent to above
 %(BNAME)s -i - -o - < %(IFILE)s > %(OFILE)s # equivalent to above

 cat %(IFILE)s | %(BNAME)s > %(OFILE)s   # functionally equivalent

   Ex: read from file, write to stdout:
 %(BNAME)s -i %(IFILE)s | less

   Ex: read from file, write to file:
 cat %(IFILE)s | %(BNAME)s | less

   Ex: Use Pyomo output directly:
 pyomo model.py model.dat | %(BNAME)s > %(OFILE)s
""" % {
	  'BNAME': basename,
	  'IFILE': '/tmp/aFile',
	  'OFILE':'/tmp/aFile.csv'
	}

	sys.exit(2)

def get_opts ( args ):
	try:
		import getopt

		sopts = 'hi:o:'                         # Short Options
		lopts = [ 'help', 'input=', 'output=' ] # Long options
		optlist, args = getopt.getopt(args, sopts, lopts)
		if args: raise getopt.GetoptError("unrecognized arguments: %s" % args )

		options = {
		  '-i': 'ifile', '--input'  : 'ifile', # input file
		  '-o': 'ofile', '--output' : 'ofile', # output file
		  '-h': 'help',  '--help'   : 'help',
		}

		args = {}
		for i in optlist:
			args.update({ options[i[0]] : i[1] } )

	except ImportError, err:
		msg  = "Unable to import python's getopt library.  Falling back to stdout"
		msg += "\nand stdin.  Run with --help for other examples.\n"
		sys.stderr.write(msg)

		return {'ifile': '-', 'ofile': '-'}

	except getopt.GetoptError, err:
		print str(err)
		usage()

	return args

if '__main__' == __name__:
	import sys
	args = ['-i', '-', '-o', '-']

	if len(sys.argv) > 1:
		args = sys.argv[1:]

	kwargs = get_opts( args )
	if ( 'help' in kwargs ): usage()

	main(**kwargs)
