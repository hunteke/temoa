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
