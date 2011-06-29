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

	objs = instance.objectives()
	if len( objs ) > 1:
		msg = '\nWarning: More than one objective.  Using first objective.\n'
		SE.write( msg )

	# This awkward workaround so as to be generic.  Unfortunately, I don't
	# know how else to automatically discover the objective name
	obj_name = objs.keys()[0]
	obj_value = getattr(soln.Objective, obj_name).Value

	Vars = soln.Variable
	Cons = soln.Constraint

	try:
		# This /should/ work with Coopr v3.0

		# Sanitize name mapping so we have a consistent interface later
		tmpv, tmpc = instance._label_var_map, instance._label_constraint_map
		var_map = dict({ key : tmpv[ key ].name for key in tmpv })
		con_map = dict({ key : tmpc[ key ].name for key in tmpc })

		var_keys = sorted(
		  (ii.split('(')[0], ii, Vars[ ii ]['Value'])

		  for ii in Vars
		  if abs(Vars[ ii ]['Value']) > 1e-15   # i.e. "if it's non-zero"
		)

	except AttributeError:
		# We are using Coopr prior v3.0

		# Sanitize name mapping so we have a consistent interface later
		var_map = dict({ key : key for key in instance.variables().keys() })
		con_map = dict({ key : key for key in instance.constraints().keys() })

		var_keys = sorted(
		  (ii.split('[')[0], ii, Vars[ ii ]['Value'])

		  for ii in Vars
		  if abs(Vars[ ii ]['Value']) > 1e-15   # i.e. "if it's non-zero"
		)

	con_keys = sorted(
	  (ii.split('[')[0][4:], ii[4:-1], Cons[ ii ]['Value'])
	    # [4:-1] removes the c_[uel]_ part of name

	  for ii in Cons
	  if 'c_' == ii[:2]            # all Coopr constraint keys begin with c_
	  if abs(Cons[ ii ].value) > 1e-15    # i.e. "if it's non-zero"
	)

	# remove the no-longer-necessary sorting key.
	var_info = [ (var_map[ var ], val) for key, var, val in var_keys ]
	con_info = [ (con_map[ con ], val) for key, con, val in con_keys ]

	def get_int_padding ( obj ):
		val = obj[ 1 ]         # obj is 2-tuple, defined within var_info
		return len(str(int(val)))
	def get_dec_padding ( obj ):
		val = abs(obj[ 1 ])    # obj is 2-tuple defined within con_info
		return len(str(val - int(val)))

	run_output = StringIO()

	msg = 'Model name: %s\n'                                                   \
	   'Objective function value (%s): %s\n'                                   \
	   'Non-zero variable values:\n'
	run_output.write( msg % (instance.name, obj_name, obj_value) )

	if len( var_keys ) > 0:
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

	data = run_output.getvalue()

	  # remove the new 3.0 format's superfluous apostrophes
	return data.replace("'",'')
