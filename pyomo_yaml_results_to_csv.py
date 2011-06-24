#!/usr/bin/env python

from sys import stdin as SI, stdout as SO, stderr as SE
from pprint import pprint

import yaml

if SI.isatty():
	from sys import argv

	msg = """\
The name of this script is originally rather ... verbose.  That should
reinforce that this is a "quick and dirty" script with a very specific purpose:
to convert Pyomo-based YAML results into a CSV for easier working within a
spreadsheet (or other) program.  It should be a bit more robust than my
previous attempts, but there are a number of tidbits yet to be implemented.

To execute it, pipe YAML output into the stdin.  Any of these will work:

$ %(pname)s < results.yml
$ %(pname)s < results.yml | less
$ cat results.yml | %(pname)s

To put the output to a file, invoke like either of these:

$ %(pname)s < results.yml > results.csv
$ cat results.yml | %(pname)s > results.csv
"""

	SE.write( msg % {'pname': argv[0]} )

	raise SystemExit


data = SI.read()
results = yaml.load( data )

pinfo = results['Problem']
psoln = results['Solution'][1]

obj_name = psoln['Objective'].keys()[0]
obj_val  = psoln['Objective'][obj_name]['Value']

print "Objective function value (%s):,%s" % (obj_name, obj_val)
if 'Variable' in psoln:
	print 'Non-zero variable values:'
	Vars = psoln['Variable']
	for ii in sorted( Vars.keys() ):
		print '"%s",%s' % (ii, Vars[ii]['Value'])
	print


if 'Constraint' in psoln:
	print 'Constraint values:'
	Cons = psoln['Constraint']
	for ii in sorted( Cons.keys() ):
		print '"%s",%s' % (ii, Cons[ii]['Value'])
	print
