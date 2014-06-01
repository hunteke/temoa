#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Temoa Output Parser
  A simple parser to convert Temoa's variable-per-line output to CSV format.

Copyright (C) 2014  Kevin Hunter Kesling

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU Affero General Public License for more details.

Developers of this script will check out a complete copy of the GNU Affero
General Public License in the file COPYING.txt.  Users uncompressing this from
an archive may not have received this license file.  If not, see
<http://www.gnu.org/licenses/>.
"""


from collections import defaultdict
from csv import writer as csv_writer
from operator import itemgetter
from sys import stdin as SI, stdout as SO, stderr as SE, argv
import re

termc_red     = '\033[1;31m'    # Terminal color: red
termc_default = '\033[0;39m'    # Terminal color: default

SE.write("""
This script is a simple parsing script for Temoa's default output.  It converts
the line-per-non-zero-variable output to 2d tables in a single CSV sheet.  You
can open this CSV file in most spreadsheet programs (e.g., LibreOffice Calc,
MS Excel, Gnumeric).
""")

if SI.isatty():
	from os import path

	bname = path.basename( argv[0] )
	msg = """
    {}Error!  No input!{}

This script expects input from stdin.  Specifically, this script does not use
any command line arguments.  Examples of use:

    $ python  {}  < your_results.sol > your_results.csv
    $ cat your_results.sol | python {} > your_results.csv

The first form is generally considered the "better" practice, but both are
functionally equivalent.

Exiting ...
""".format( termc_red, termc_default, bname, bname )

	raise SystemExit( msg )



def default_csv_converter ( var_name, var_dict, ostream=SO ):
	"""
	Converts the 1 variable value per line of the passed variable to a CSV
	version of same.  In other words, we don't know how to group the indices of
	this variable class, so dumbly write them to the output.
	"""
	data = [[ '{} Values'.format( var_name ) ]]
	data.append( ['Unknown variable; default parser utilized.'] )

	var_dict = sorted( var_dict.items() )
	if isinstance(var_dict[0][0], tuple):
		for k, v in var_dict:
			data.append( list( k ) + [ v ] )
	else:
		for k, v in var_dict:
			data.append( [ k, v ] )
	data.append( [] )  # empty row to split data sets

	writer = csv_writer( ostream )
	writer.writerows( data )



def write_CSV_table ( var_dict, data, rows, indexes, ostream=SO ):
	"""
	Given the row headers and indexes of each datum, convert var_dict to a 2-d
	format in data, and write the output in CSV format to ostream

	var_dict
	  Temoa output variables in a dictionary

	data
	  the list of lists to which to copy the elements from var_dict

	rows
	  row headers of eventual CSV output

	indexes
	  ordered list of cell indexes to access; usually a generator
	"""
	for r in rows:
		# .get( index, '') -> use value accessed by index if it exists, otherwise
		# use an empty string.  Either way, the cell needs to exist to ensure
		# proper CSV alignment
		row = list( r )
		row.extend( var_dict.get(i, '') for i in indexes[r] )

		# remove any trailing empty cells; no need for superfluous commas in the
		# output
		for i in xrange(len(row)):
			if row[-1] != '':
				break
			del row[-1]

		data.append( row )
	data.append( [] )  # empty row so as to visually split data sets

	# finally, write the data in CSV format to ostream
	writer = csv_writer( ostream )
	writer.writerows( data )


def Act_2CSV ( var_dict, ostream=SO ):
	"""
	Converts the 1 variable value per line of the Activity variable to a 2d table
	in CSV format with period columns, and the rows organized by technology,
	vintage, and then slice.

	var_dict: dict of Activity variable index-value pairings.
	  The keys are the indexes, and must be tuples.  The values must be floats.

	ostream: any file-like object, but defaults to stdout

	Does not return anything, but writes output to ostream.
	"""
	P, SDTV = set(), set()
	for p, s, d, t, v in var_dict:
		P.add( p )
		SDTV.add( (s, d, t, v) )
	P, SDTV = sorted(P), sorted( SDTV, key=itemgetter(2, 3, 0, 1) )

	# data is a list of lists, representing the cells of the CSV.  Be sure to
	# append lists (list() or []) to it, otherwise you'll have funky output

	# The first item names this block of data for the user to see
	data = [['Activity Values']]

	# The second row in this block is the header information.
	data.append( ['Season', 'Time of Day', 'Technology', 'Vintage'] + P )

	# The row headers for each row.  These should match with the column headers,
	# written to data in the previous statement.  The write_CSV_table function
	# will write each row in the order specified in this generator.  Note that
	# these _must_ be tuples; if there is only a single item, use the tuple
	# syntax.  For example (s,) instead of just s.
	rows = ( (s, d, t, v) for s, d, t, v in SDTV )

	# Dictionary of cell data, indexed by rows.  The keys are the rows (and thus
	# should match the tuples in the rows generator, above), and the values are
	# a list of the keys in var_dict.  The write_CSV_table function will make a
	# CSV row for each row in rows, and will populate each cell per it's column
	# (in this case, the elements of P; note the 'for p in P').
	indexes = { (s, d, t, v): [ (p, s, d, t, v) for p in P ]
	  for s, d, t, v in SDTV }

	# finally, write_CSV_table does the actual manipulation
	write_CSV_table( var_dict, data, rows, indexes, ostream )


def ActPTV_2CSV ( var_dict, ostream=SO ):
	"""
	Read the docstring for Act_2CSV to understand what this function does.
	"""
	P, TV = set(), set()
	for p, t, v in var_dict:
		P.add( p )
		TV.add( (t, v) )
	P, TV = sorted(P), sorted( TV, key=itemgetter(0, 1) )

	data = [['ActivityByPeriodAndProcess Values']]
	data.append( ['Technology', 'Vintage'] + P )
	rows = ( (t, v) for t, v in TV )
	indexes = { (t, v): [ (p, t, v) for p in P ] for t, v in TV }
	write_CSV_table( var_dict, data, rows, indexes, ostream )


def Cap_2CSV ( var_dict, ostream=SO ):
	"""
	Read the docstring for Act_2CSV to understand what this function does.
	"""
	T, V = set(), set()
	for t, v in var_dict:
		T.add( t )
		V.add( v )
	T, V = sorted( T ), sorted( V )

	data = [['Capacity Values']]
	data.append( ['Technology'] + V )
	rows = ( (t,) for t in T )
	indexes = { (t,): [ (t, v) for v in V ] for t in T }
	write_CSV_table( var_dict, data, rows, indexes, ostream )


def CapPT_2CSV ( var_dict, ostream=SO ):
	"""
	Read the docstring for Act_2CSV to understand what this function does.
	"""
	P, T = set(), set()
	for p, t in var_dict:
		P.add( p )
		T.add( t )
	P, T = sorted( P ), sorted( T )

	data = [['CapacityAvailableByPeriodAndTech Values']]
	data.append( ['Technology'] + P )
	rows = ( (t,) for t in T )
	indexes = { (t,): [ (p, t) for p in P ] for t in T }
	write_CSV_table( var_dict, data, rows, indexes, ostream )


def ActIT_2CSV ( var_dict, ostream=SO ):
	"""
	Read the docstring for Act_2CSV to understand what this function does.
	"""
	I, T = set(), set()
	for i, t in var_dict:
		I.add( i )
		T.add( t )
	I, T = sorted( I ), sorted( T )

	data = [['ActivityByInputAndTech Values']]
	data.append( ['Technology'] + I )
	rows = ( (t,) for t in T )
	indexes = { (t,): [ (i, t) for i in I ] for t in T }
	write_CSV_table( var_dict, data, rows, indexes, ostream )


def ActPT_2CSV ( var_dict, ostream=SO ):
	"""
	Read the docstring for Act_2CSV to understand what this function does.
	"""
	P, T = set(), set()
	for p, t in var_dict:
		P.add( p )
		T.add( t )
	P, T = sorted( P ), sorted( T )

	data = [['ActivityByPeriodAndTech Values']]
	data.append( ['Technology'] + P )
	rows = ( (t,) for t in T )
	indexes = { (t,): [ (p, t) for p in P ] for t in T }
	write_CSV_table( var_dict, data, rows, indexes, ostream )


def ActPITV_2CSV ( var_dict, ostream=SO ):
	"""
	Read the docstring for Act_2CSV to understand what this function does.
	"""
	P, ITV = set(), set()
	for p, i, t, v in var_dict:
		P.add( p )
		ITV.add( (i, t, v) )
	P, ITV = sorted( P ), sorted( ITV, key=itemgetter(1, 2, 0) )

	data = [['ActivityByPeriodInputAndProcess Values']]
	data.append( ['Input', 'Technology', 'Vintage'] + P )
	rows = ( (i, t, v) for i, t, v in ITV )
	indexes = { (i, t, v): [ (p, i, t, v) for p in P ] for i, t, v in ITV }
	write_CSV_table( var_dict, data, rows, indexes, ostream )


def ActPIT_2CSV ( var_dict, ostream=SO ):
	"""
	Read the docstring for Act_2CSV to understand what this function does.
	"""
	P, IT = set(), set()
	for p, i, t in var_dict:
		P.add( p )
		IT.add( (i, t) )
	P, IT = sorted( P ), sorted( IT, key=itemgetter(1, 0) )

	data = [['ActivityByPeriodInputAndTech Values']]
	data.append( ['Input', 'Technology'] + P )
	rows = ( (i, t) for i, t in IT )
	indexes = { (i, t): [ (p, i, t) for p in P ] for i, t in IT }
	write_CSV_table( var_dict, data, rows, indexes, ostream )


def ActPTVO_2CSV ( var_dict, ostream=SO ):
	"""
	Read the docstring for Act_2CSV to understand what this function does.
	"""
	P, TVO = set(), set()
	for p, t, v, o in var_dict:
		P.add( p )
		TVO.add( (t, v, o) )
	P, TVO = sorted( P ), sorted( TVO )

	data = [['ActivityByPeriodProcessAndOutput Values']]
	data.append( ['Technology', 'Vintage', 'Output'] + P )
	rows = ( (t, v, o) for t, v, o in TVO )
	indexes = { (t, v, o): [ (p, t, v, o) for p in P ] for t, v, o in TVO }
	write_CSV_table( var_dict, data, rows, indexes, ostream )


def ActPTO_2CSV ( var_dict, ostream=SO ):
	"""
	Read the docstring for Act_2CSV to understand what this function does.
	"""
	P, TO = set(), set()
	for p, t, o in var_dict:
		P.add( p )
		TO.add( (t, o) )
	P, TO = sorted( P ), sorted( TO )

	data = [['ActivityByPeriodProcessAndOutput Values']]
	data.append( ['Technology', 'Output'] + P )
	rows = ( (t, o) for t, o in TO )
	indexes = { (t, o): [ (p, t, o) for p in P ] for t, o in TO }
	write_CSV_table( var_dict, data, rows, indexes, ostream )


def ActTV_2CSV ( var_dict, ostream=SO ):
	"""
	Read the docstring for Act_2CSV to understand what this function does.
	"""
	T, V = set(), set()
	for t, v in var_dict:
		T.add( t )
		V.add( v )
	T, V = sorted( T ), sorted( V )

	data = [['ActivityByProcess Values']]
	data.append( ['Technology'] + V )
	rows = ( (t,) for t in T )
	indexes = { (t,): [ (t, v) for v in V ] for t in T }
	write_CSV_table( var_dict, data, rows, indexes, ostream )


def ActTO_2CSV ( var_dict, ostream=SO ):
	"""
	Read the docstring for Act_2CSV to understand what this function does.
	"""
	T, O = set(), set()
	for t, o in var_dict:
		T.add( t )
		O.add( o )
	T, O = sorted( T ), sorted( O )

	data = [['ActivityByTechAndOutput Values']]
	data.append( ['Technology'] + O )
	rows = ( (t,) for t in T )
	indexes = { (t,): [ (t, o) for o in O ] for t in T }
	write_CSV_table( var_dict, data, rows, indexes, ostream )


def NoOutput ( *args, **kwargs ):
	"""
	This function ignores the input, and produces no output.  Use it in the
	'known_variables' dictionary (below) for variables that you do not want in
	your output.
	"""
	pass


# This dictionary acts as a 'switch' that points to the appropriate processing
# function for variable classes, once the logic below decides all indexes per
# class has been collected from the input.  As you write the logic to handle
# each class, you can uncomment each line so that the try-except blocks below
# don't fall back to the 'default_csv_converter' function.
known_variables = {
  'Activity'                         : Act_2CSV,
  'ActivityByInputAndTech'           : ActIT_2CSV,
  'ActivityByPeriodAndProcess'       : ActPTV_2CSV,
  'ActivityByPeriodAndTech'          : ActPT_2CSV,
  'ActivityByPeriodInputAndProcess'  : ActPITV_2CSV,
  'ActivityByPeriodInputAndTech'     : ActPIT_2CSV,
  'ActivityByPeriodProcessAndOutput' : ActPTVO_2CSV,
  'ActivityByPeriodTechAndOutput'    : ActPTO_2CSV,
  'ActivityByProcess'                : ActTV_2CSV,
  'ActivityByTechAndOutput'          : ActTO_2CSV,

  'Capacity'                         : Cap_2CSV,
  'CapacityAvailableByPeriodAndTech' : CapPT_2CSV,

  'FlowIn'  : NoOutput,
  'FlowOut' : NoOutput,

  'DiscountedFixedCostsByPeriod'     : NoOutput,
  'DiscountedFixedCostsByPeriodAndProcess' : NoOutput,
  'DiscountedFixedCostsByProcess'    : NoOutput,
  'DiscountedFixedCostsByTech'       : NoOutput,
  'DiscountedFixedCostsByVintage'    : NoOutput,
  'DiscountedInvestmentByPeriod'     : NoOutput,
  'DiscountedInvestmentByProcess'    : NoOutput,
  'DiscountedInvestmentByTech'       : NoOutput,
  'DiscountedPeriodCost'             : NoOutput,
  'DiscountedVariableCostsByPeriod'  : NoOutput,
  'DiscountedVariableCostsByProcess' : NoOutput,
  'DiscountedVariableCostsByTech'    : NoOutput,
  'DiscountedVariableCostsByVintage' : NoOutput,

  'UndiscountedFixedCostsByPeriod'     : NoOutput,
  'UndiscountedFixedCostsByPeriodAndProcess' : NoOutput,
  'UndiscountedFixedCostsByProcess'    : NoOutput,
  'UndiscountedFixedCostsByTech'       : NoOutput,
  'UndiscountedFixedCostsByVintage'    : NoOutput,
  'UndiscountedInvestmentByPeriod'     : NoOutput,
  'UndiscountedInvestmentByProcess'    : NoOutput,
  'UndiscountedInvestmentByTech'       : NoOutput,
  'UndiscountedPeriodCost'             : NoOutput,
  'UndiscountedVariableCostsByPeriod'  : NoOutput,
  'UndiscountedVariableCostsByPeriodAndProcess' : NoOutput,
  'UndiscountedVariableCostsByProcess' : NoOutput,
  'UndiscountedVariableCostsByTech'    : NoOutput,
  'UndiscountedVariableCostsByVintage' : NoOutput,
}

# This regex is the crux of the parser:
#   It matches whitespace followed by a number, followed by more whitespace,
#   followed by 'V_' and then the variable name, finishing with the index
var_re = re.compile( r'^ +(\d+(?:\.\d+)?) +V_(\w+)\[(\S+)\]$' )

# when the previous variable class does not match the current line's class, we
# know we're done collecting the prev group.
prev = None

SE.write('\nReading data from stdin ...\n')

for line in SI:
	# run through each line in the input
	match = var_re.match( line )
	if match:
		# it matched!  it's a variable line!
		val, var, index = match.groups()
		val = float( val )
		index = tuple( index.split(',') )

		if var != prev:
			# given that the Temoa default output groups variable classes together,
			# if this line is not the same class as the previous line, then we've
			# collected all of the indexes in the class.  Proceed with processing.
			if prev:
				try:
					handler = known_variables[ prev ]
				except KeyError as e:
					# There is no special handling for this var; use the default
					# handler, which basically repeats the variable-per-line output
					default_csv_converter( var, values )
				else:
					handler( values )

				del values
				SE.write( 'done.\n' )

			SE.write( 'Processing: {} ... '.format( var ))
			SE.flush()

			values = { index : val }

		prev = var
		values[ index ] = val

if values:
	try:
		handler = known_variables[ prev ]
	except KeyError as e:
		default_csv_converter( var, values )
	else:
		handler( values )

	del values
	SE.write( 'done.\n' )

# Since this script is expected to complete extremely quickly, we inform the
# user at the end of execution that their command line arguments were ignored.
# Otherwise, the message might get lost in the output.
if len(argv) > 1:
	SE.write('\n{}Warning{}: all command line arguments are ignored: {}\n\n'
	  .format( termc_red, termc_default, str(argv[1:])[1:-1] ))

if SO.isatty():
	SE.write("""
{}Notice{}: to save this output, consider redirecting to a file.  Run this
script with no arguments or input for an example usage of the greater-than (>)
operator.\n""".format( termc_red, termc_default ))

cite_msg = """

If you use these results for a published article, please run Temoa with the
'--how_to_cite' command line argument for citation information.
"""

if SO.isatty():
	SO.write( cite_msg )
else:
	SE.write( cite_msg )

