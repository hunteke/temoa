from cStringIO import StringIO

def pformat_results ( pyomo_instance, pyomo_result ):
	instance = pyomo_instance
	result = pyomo_result

	soln = result['Solution']
	solv = result['Solver']      # currently unused, but may want it later
	prob = result['Problem']     # currently unused, but may want it later

	optimal_solutions = (
	  'feasible', 'globallyOptimal', 'locallyOptimal', 'optimal'
	)
	if str(soln.Status) not in optimal_solutions:
		return "No solution found."

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

	run_output = StringIO()

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

	return run_output.getvalue()
