from cStringIO import StringIO

try:
	from coopr.pyomo import *
except:

	import os, sys
	ppath = '/path/to/coopr/bin'
	path = """Option 1:
$ PATH=%(ppath)s:$PATH
$ which python

Option 2:
$ %(ppath)s/python  %(base)s  ...
"""
	if 'win' in sys.platform:
		ppath = 'C:\\path\\to\\coopr\\bin'
		path = """Option 1:
C:\\> set PATH=%(ppath)s:%%PATH%%
C:\\> python  %(base)s  ...

Option 2:
C:\\> %(ppath)s\\python  %(base)s  ...
"""

	base = os.path.basename( sys.argv[0] )
	path %= { 'ppath' : ppath, 'base' : base }
	msg = """\
Unable to find coopr.pyomo on the Python system path.  Are you running Coopr's
version of Python?  Here is one way to check:

  # look for items that have to do with the Coopr project
python -c "import sys, pprint; pprint.pprint(sys.path)"

If you aren't running with Coopr's environment for Python, you'll need to either
update your PATH environment variable to use Coopr's Python setup, or always
explicitly use the Coopr path:

%s
"""

	raise SystemExit, msg % path



def temoa_solve ( model ):
	from sys import argv, stderr, stdout

	from coopr.opt import SolverFactory
	from coopr.pyomo import ModelData

	from pformat_results import pformat_results

	SE, SO = stderr.write, stdout.write

	if len( argv ) < 2:
		SE( "No data file (dot dat) specified.  Exiting.\n" )
		raise SystemExit

	opt = SolverFactory('glpk_experimental')
	opt.keepFiles = False
	# opt.options.wlp = "temoa_model.lp"  # output GLPK LP understanding of model

	# Recreate the pyomo command's ability to specify multiple "dot dat" files
	# on the command line
	mdata = ModelData()
	for f in argv[1:]:
		if f[-4:] != '.dat':
			SE( "Expecting a dot dat (data.dat) file, found %s\n" % f )
			raise SystemExit
		mdata.add( f )
	mdata.read( model )

	# Now do the solve and ...
	instance = model.create( mdata )
	result = opt.solve( instance )

	# ... print the easier-to-read/parse format
	SO( pformat_results( instance, result ) )
