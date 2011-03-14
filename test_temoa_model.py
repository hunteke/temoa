#!/usr/bin/env lpython

import argparse
from cStringIO import StringIO
from optparse import OptionParser, OptionGroup
import os
from sys import stderr, argv

from coopr.opt.base import SolverFactory

from model import create_TEMOA_model as create_model

SE = stderr.write
basename = argv[0]

opt = SolverFactory('glpk_experimental')  # created once, for aggregation
opt.keepFiles = False

###############################################################################
# Begin "Was I executed correctly?" check.

if '__main__' != __name__:
	msg = """
This script is a test suite for the TEMOA model implementation.  It looks like
you're attempting to run this through Pyomo.  Please instead use Coopr's Python
to invoke this script:

$ lpython %(base)s
$ lpython %(base)s  individual_test.dat
"""
	SE( msg % { 'base' : basename, } )

	raise SystemExit

# End "Was I executed correctly?" check.
###############################################################################

###############################################################################
# Begin main test function

def runTest ( M, datfile, **kwargs ):
	"""\
Returns 'OK' or 'FAIL' if test output compares equal to a baseline output.

M:               Pyomo optimization model
datfile:         (string)
   path to normal AMPL data file for the Pyomo model M
baseline:        (string) (Default: equal to datfile)
   path to a baseline file for comparison against test output
create_baseline: (string) (Default: None)
   path to new baseline file.  Will blindly overwrite an existing baseline, so
   be careful!
"""
	baseline        = kwargs.pop('baseline', datfile + '.baseline')
	create_baseline = kwargs.pop('create_baseline', None)
	return_data     = kwargs.pop('return_data', False)

	datfile += '.dat'

	red = green = normal = ''
	if stderr.isatty():
		red    = '\x1B[1;31m'
		green  = '\x1B[1;32m'
		normal = '\x1B[0;39m'
		blue   = '\x1B[1;34m'

	msg = ''
	run_output = StringIO()
	failed = True
	try:
		instance = M.create( datfile )
		results = opt.solve( instance )

		soln = results['Solution']
		solv = results['Solver']      # currently unused, but may want it later
		prob = results['Problem']     # currently unused, but may want it later

		obj_value = soln.Objective.obj.Value

		Vars = soln.Variable
		Cons = soln.Constraint

		var_keys = sorted(
		  ii
		  for ii in Vars
		  if abs(Vars[ ii ].value) > 1e-16   # i.e. "if it's non-zero"
		)

		constraint_keys = sorted(
		  ii
		  for ii in Cons
		  if 'c_' == ii[:2]            # all Coopr constraint keys being with c_
		  if abs(Cons[ ii ].value) > 1e-16    # i.e. "if it's non-zero"
		)

		def get_int_padding ( ObjSet ):
			def wrapped ( key ):
				val = ObjSet[ key ].value
				return len(str(int(val)))
			return wrapped
		def get_dec_padding ( ObjSet ):
			def wrapped ( key ):
				val = ObjSet[ key ].value
				return len(str(val - int(val)))
			return wrapped

		run_output.write( "Objective function value: %s\n" % obj_value )
		run_output.write( "Non-zero variable values for '%s'\n" % instance.name )

		# This padding code make the display of the output values line up at
		# the period
		int_padding = max(map( get_int_padding(Vars), var_keys ))
		dec_padding = max(map( get_dec_padding(Vars), var_keys ))
		format = "  %%%dd%%-%ds  %%s\n" % (int_padding, dec_padding)
			# Works out to something like "%8d%-11s  %s"

		for key in var_keys:
			int_part = int(Vars[ key ].value)
			dec_part = str(Vars[ key ].value - int_part)[1:]
			run_output.write( format % (int_part, dec_part, key) )

		run_output.write( "\nBinding constraint values for '%s'\n" % instance.name)

		int_padding = max(map( get_int_padding(Cons), constraint_keys ))
		dec_padding = max(map( get_dec_padding(Cons), constraint_keys ))
		format = "  %%%dd%%-%ds  %%s\n" % (int_padding, dec_padding)
			# Works out to something like "%8d%-11s  %s"

		for key in constraint_keys:
			int_part = int(Cons[ key ].value)
			dec_part = str(Cons[ key ].value - int_part)[1:]
			run_output.write( format % (int_part, dec_part, key[4:-1]) )

		del instance, results, soln, prob, solv
		failed = False
	except Exception, e:
		print e
		msg = "  %sError optimizing test.  Debug with pyomo:  $ lpython %s %s%s"
		msg %= (blue, basename, datfile, normal)
		# don't care how it failed, just that it did.  The how is for further

	msg = '%sFAIL%s   (%s)%s' % (red, normal, datfile, msg)
	test = False
	if not failed:
		if create_baseline:
			with open( baseline, 'w' ) as f:
				f.write(run_output.getvalue())

		with open( baseline, 'r' ) as f:
			baseline_data = f.read()

		if baseline_data == run_output.getvalue():
			test = True
			msg = '%sOK%s' % (green, normal)

		if return_data:
			return (test, msg, run_output.getvalue(), baseline_data)

	return (test, msg)

# End test function
##############################################################################

##############################################################################
# Begin command line parsing

# At the moment, this command line parsing code is rather organic; this was
# just a first cut at the system, so bear with me.  There are currently only
# three ways to run this script:
#
#    Run entire suite of tests:
# $ lpython  test_temoa_model.py
#
#    Run only a single test
# $ lpython  test_temoa_model.py  single_test.dat
#
#    Create the baseline against which to compare a test
# $ lpython  test_temoa_model.py  single_test.dat  --create

parser = argparse.ArgumentParser(
  description='TEMOA Test Suite Options',
  epilog="Usually run as '$ %s' or '$ lpython %s'" % (basename, basename) )

parser.add_argument( '--create', action='store_true', required=False,
  help='Use this run to create the baseline test output against which to '
       'compare future test runs.  (Only allowed when specifying ')
# parser.add_argument( '--show', action='store_true', required=False,
  # help='Show the output of a single test.  This can only be specified with a '
       # 'single test')
parser.add_argument( 'datfile', type=str, nargs='?', default=None,
  help='A single_file.dat to test.  Do not specify to run the whole suite.')


options = parser.parse_args( argv[1:] )

if options.datfile:
	datfile = options.datfile

	if not os.path.exists( datfile ):
		msg = "Error: No such file:  '%s'\n\nSpecified dot dat file does not " \
		      "exist.  Did you typo the file name?\n"
		SE( msg % datfile )
		raise SystemExit

	create_baseline = options.create

	M = create_model()
	name = 'Command line specified test'
	test, msg, data, baseline = runTest(
	  M,
	  options.datfile[:-4],
	  create_baseline=options.create,
	  return_data=True
	)

	print "Result:\n%s\n\nData:\n%s\n" % (msg, data)
	if not test:
		import difflib
		print "Differences:"
		for line in difflib.unified_diff(baseline.split('\n'), data.split('\n')):
			print line

	raise SystemExit

elif options.create:
	msg = "Warning: ignoring --create option.  It can only be used with a " \
	      "single test file\n"
	SE( msg )


# No command line arguments passed, so run entire suite of tests.
tests_to_run = (
  ( 'One period, oil+coal only, use electric heater',
       'test_dot_dats/oil-coal_one_period_pick_electric' ),
  ( 'One period, oil only, use diesel',
       'test_dot_dats/only_oil_one_period_pick_diesel' ),
  ( 'One period, oil only, use gasoline',
       'test_dot_dats/only_oil_one_period_pick_gasoline' ),
)

from os import fork, wait
M = create_model()

for name, datfile in tests_to_run:
	pid = fork()
	if pid:
		# pid > 0, i.e. this is the parent process.
		# Turns out to be necessary to use a fresh version of the model for each
		# test.  It seems that successive runs alter the model, despite
		# "instantiation".  So this forking from a fresh version of the model is
		# necessary.  Sigh.

		wait()
		continue  # as parent, skip actually doing anything with the model.

	# Only children processes execute the last part of this loop.
	test, msg = runTest(M, datfile)
	print  "%s   %s" % (msg, name)
	break
