from sys import stderr as SE
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

	objs = pyomo_instance.objectives()
	if len( objs ) > 1:
		msg = '\nWarning: More than one objective.  Using first objective.\n'
		SE.write( msg )

	# This awkward workaround so as to be generic.  Unfortunately, I don't
	# know how else to automatically discover the objective name
	obj_name = objs.keys()[0]
	obj_value = getattr(soln.Objective, obj_name).Value

	Vars = soln.Variable
	Cons = soln.Constraint

	var_keys = sorted(
	  ii
	  for ii in Vars
	  if abs(Vars[ ii ].value) > 1e-15   # i.e. "if it's non-zero"
	)

	constraint_keys = sorted(
	  ii
	  for ii in Cons
	  if 'c_' == ii[:2]            # all Coopr constraint keys begin with c_
	  if abs(Cons[ ii ].value) > 1e-15    # i.e. "if it's non-zero"
	)

	def get_int_padding ( ObjSet ):
		def wrapped ( key ):
			val = ObjSet[ key ].value
			return len(str(int(val)))
		return wrapped
	def get_dec_padding ( ObjSet ):
		def wrapped ( key ):
			val = abs(ObjSet[ key ].value)
			return len(str(val - int(val)))
		return wrapped

	run_output = StringIO()

	msg = "Objective function value (%s): %s\n"
	run_output.write( msg % (obj_name, obj_value) )
	run_output.write( "Non-zero variable values for '%s'\n" % instance.name )

	if len( var_keys ) > 0:
		# This padding code is what makes the display of the output values
		# line up on the decimal point.
		int_padding = max(map( get_int_padding(Vars), var_keys ))
		dec_padding = max(map( get_dec_padding(Vars), var_keys ))
		format = "  %%%ds%%-%ds  %%s\n" % (int_padding, dec_padding)
			# Works out to something like "%8d%-11s  %s"

		for key in var_keys:
			val = Vars[ key ].value
			int_part = int(abs(val))
			dec_part = str(abs(val) - int_part)[1:]
			if val < 0: int_part = "-%d" % int_part
			run_output.write( format % (int_part, dec_part, key) )

	if 0 == len( constraint_keys ):
		# Since not all Coopr solvers give constraint results, must check
		msg = '\nSelected Coopr solver plugin does not give constraint '        \
		   'information.\n'
		run_output.write( msg )
	else:
		msg = "\nBinding constraint values for '%s'\n"
		run_output.write( msg % instance.name)

		int_padding = max(map( get_int_padding(Cons), constraint_keys ))
		dec_padding = max(map( get_dec_padding(Cons), constraint_keys ))
		format = "  %%%ds%%-%ds  %%s\n" % (int_padding, dec_padding)
			# Works out to something like "%8s%-11s  %s"

		for key in constraint_keys:
			val = Cons[ key ].value
			int_part = int(abs(val))
			dec_part = str(abs(val) - int_part)[1:]
			if val < 0: int_part = "-%d" % int_part
			run_output.write( format % (int_part, dec_part, key[4:-1]) )

	return run_output.getvalue()
