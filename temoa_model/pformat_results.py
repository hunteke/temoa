from sys import stderr as SE
from cStringIO import StringIO

def pformat_results ( pyomo_instance, pyomo_result ):
	from coopr.pyomo import Objective

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

	objs = instance.active_components( Objective )
	if len( objs ) > 1:
		msg = '\nWarning: More than one objective.  Using first objective.\n'
		SE.write( msg )

	# This awkward workaround so as to be generic.  Unfortunately, I don't
	# know how else to automatically discover the objective name
	obj_name = objs.keys()[0]
	obj_value = getattr(soln.Objective, obj_name).Value

	Vars = soln.Variable
	Cons = soln.Constraint

	var_info = sorted(
	  (ii.split('(')[0],
	   ii.replace('_,', ',')
	     .replace(',_', ',')
	     .replace('(_', '(')
	     .replace('_)', ')'),
	   Vars[ ii ]['Value']
	  )

	  for ii in Vars
	  if abs(Vars[ ii ]['Value']) > 1e-15
	)

	con_info = sorted(
	  (ii.split('[')[0][4:],
	   ii[4:-1]     # [4:-1] removes the c_[uel]_ part of name
	     .replace('_,', ',')
	     .replace(',_', ',')
	     .replace('(_', '(')
	     .replace('_)', ')'),
	   Cons[ ii ]['Value']
	  )

	  for ii in Cons
	  if 'c_' == ii[:2]            # all Coopr constraint keys begin with c_
	  if abs(Cons[ ii ].value) > 1e-15    # i.e. "if it's non-zero"
	)

	# remove the no-longer-necessary sorting key.
	con_info = [ (con, val) for sortkey, con, val in con_info ]
	var_info = [ (var, val) for sortkey, var, val in var_info ]

	def get_int_padding ( obj ):
		val = obj[ 1 ]         # obj is 2-tuple, defined within var_info
		return len(str(int(val)))
	def get_dec_padding ( obj ):
		val = abs(obj[ 1 ])    # obj is 2-tuple defined within con_info
		return len(str(val - int(val)))

	run_output = StringIO()

	msg = ( 'Model name: %s\n'
	   'Objective function value (%s): %s\n'
	   'Non-zero variable values:\n'
	)
	run_output.write( msg % (instance.name, obj_name, obj_value) )

	if len( var_info ) > 0:
		# This padding code is what makes the display of the output values
		# line up on the decimal point.
		int_padding = max(map( get_int_padding, var_info ))
		dec_padding = max(map( get_dec_padding, var_info ))
		format = "  %%%ds%%-%ds  %%s\n" % (int_padding, dec_padding)
			# Works out to something like "%8d%-11s  %s"

		for key, val in var_info:
			int_part = int(abs(val))
			dec_part = str(abs(val) - int_part)[1:]  # remove (negative and) 0
			if val < 0: int_part = "-%d" % int_part
			run_output.write( format % (int_part, dec_part, key) )

	else:
		run_output.write( '\nAll variables have a zero (0) value.\n' )

	if 0 == len( con_info ):
		# Since not all Coopr solvers give constraint results, must check
		msg = '\nSelected Coopr solver plugin does not give constraint data.\n'
		run_output.write( msg )
	else:
		msg = '\nBinding constraint values:\n'
		run_output.write( msg )

		int_padding = max(map( get_int_padding, con_info ))
		dec_padding = max(map( get_dec_padding, con_info ))
		format = "  %%%ds%%-%ds  %%s\n" % (int_padding, dec_padding)
			# Works out to something like "%8s%-11s  %s"

		for key, val in con_info:
			int_part = int(abs(val))
			dec_part = str(abs(val) - int_part)[1:]
			if val < 0: int_part = "-%d" % int_part
			run_output.write( format % (int_part, dec_part, key) )

	return run_output.getvalue()
