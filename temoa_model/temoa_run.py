"""
Tools for Energy Model Optimization and Analysis (Temoa): 
An open source framework for energy systems optimization modeling

Copyright (C) 2015,  NC State University

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

A complete copy of the GNU General Public License v2 (GPLv2) is available 
in LICENSE.txt.  Users uncompressing this from an archive may not have 
received this license file.  If not, see <http://www.gnu.org/licenses/>.
"""

from os import path, close as os_close
from sys import argv, stderr as SE, stdout as SO
from signal import signal, SIGINT, default_int_handler
from shutil import copyfile, move

from pyomo.opt import SolverFactory as SF
from pyomo.environ import *

from temoa_config import TemoaConfig

import errno, warnings
import re as reg_exp

signal(SIGINT, default_int_handler)


def temoa_create_and_solve ( model, optimizer, options ):
	"""Create and solve an instance of the model.

	Input arguments:
	model -- the model object
	optimizer -- pyomo object used to perform optimization
	options -- objects that contains user-specified run options
	"""

	from time import clock
	import sys, os, gc

	from pyomo.environ import DataPortal

	from pformat_results import pformat_results

	def create_temoa_instance ( model, options ):
		"""Create a single instance of Temoa."""
		
		try:
			txt_file = open(options.path_to_logs+os.sep+"Complete_OutputLog.log", "w")

		except BaseException as io_exc:
			SE.write("Log file cannot be opened. Please check path. Trying to find:\n"+options.path_to_logs+" folder\n")
			txt_file = open("Complete_OutputLog.log", "w")
			txt_file.write("Log file cannot be opened. Please check path. Trying to find:\n"+options.path_to_logs+" folder\n")

		try:
			if options.keepPyomoLP:
				SE.write('\nSolver will write file: {}\n\n'.format( options.scenario + '.lp' ))
				txt_file.write('\nSolver will write file: {}\n\n'.format( options.scenario + '.lp' ))

			SE.write( '[        ] Reading data files.'); SE.flush()
			txt_file.write( 'Reading data files.')
			begin = clock()
			duration = lambda: clock() - begin

			modeldata = DataPortal( model=model )
			# Recreate the pyomo command's ability to specify multiple "dot dat" files
			# on the command lin			
			for fname in options.dot_dat:
				if fname[-4:] != '.dat':
					msg = "\n\nExpecting a dot dat (e.g., data.dat) file, found '{}'\n"
					raise Exception( msg.format( fname ))
				modeldata.load( filename=fname )
			SE.write( '\r[%8.2f]\n' % duration() )
			txt_file.write( '[%8.2f]\n' % duration() )

			SE.write( '[        ] Creating Temoa model instance.'); SE.flush()
			txt_file.write( 'Creating Temoa model instance.')
			
			instance = model.create_instance( modeldata )
			SE.write( '\r[%8.2f\n' % duration() )
			txt_file.write( '[%8.2f]\n' % duration() )

		except BaseException as model_exc:
			SE.write("exception found in create_temoa_instance\n")
			txt_file.write("exception found in create_temoa_instance\n")
			SE.write(str(model_exc))
			txt_file.write(str(model_exc))
			txt_file.close()

		return instance, txt_file	

	def solve_temoa_instance ( instance, optimizer, options, txt_file ):
		'''Solve a Temoa instance.'''	
		
		begin = clock()
		duration = lambda: clock() - begin
		try:
			SE.write( '[        ] Solving.'); SE.flush()
			txt_file.write( 'Solving.')
			if optimizer:	
				result = optimizer.solve( instance, 
								keepfiles=options.keepPyomoLP, 
								symbolic_solver_labels=options.keepPyomoLP )
				SE.write( '\r[%8.2f\n' % duration() )
				txt_file.write( '[%8.2f]\n' % duration() )
				# return signal handlers to defaults, again
				signal(SIGINT, default_int_handler)
			else:
				SE.write( '\r---------- Not solving: no available solver\n' )
				txt_file.write( '\r---------- Not solving: no available solver\n' )
				return
	
			# ... print the easier-to-read/parse format
			msg = '[        ] Calculating reporting variables and formatting results.'
			SE.write( msg ); SE.flush()
			txt_file.write( 'Calculating reporting variables and formatting results.')
			instance.solutions.store_to(result)
			formatted_results = pformat_results( instance, result, options )
			SE.write( '\r[%8.2f\n' % duration() )
			txt_file.write( '[%8.2f]\n' % duration() )
			SO.write( formatted_results.getvalue() )
			txt_file.write( formatted_results.getvalue() )
			txt_file.close()
		
		except BaseException as model_exc:
			SE.write("\nexception found in solve_temoa_instance\n")
			txt_file.write("\nexception found in solve_temoa_instance\n")
			SE.write(str(model_exc))
			txt_file.write(str(model_exc))
			txt_file.close()

		return result

	def handle_files( options, TemoaConfig, log_name):
		"""Handle log and LP file assuming user called with config file or from interface."""
		if isinstance(options, TemoaConfig) and options.saveTEXTFILE:
			for inpu in options.dot_dat:
				file_ty = reg_exp.search(r"\b([\w-]+)\.(\w+)\b", inpu)
			new_dir = options.path_to_db_io+os.sep+file_ty.group(1)+'_'+options.scenario+'_model'
			if path.isfile(options.path_to_logs+os.sep+log_name) and path.exists(new_dir):
				copyfile(options.path_to_logs+os.sep+log_name, new_dir+os.sep+options.scenario+'_OutputLog.log')
										
		if isinstance(options, TemoaConfig) and options.keepPyomoLP:
			for inpu in options.dot_dat:
				file_ty = reg_exp.search(r"\b([\w-]+)\.(\w+)\b", inpu)
		
			new_dir = options.path_to_db_io+os.sep+file_ty.group(1)+'_'+options.scenario+'_model'
		
			for files in os.listdir(options.path_to_lp_files):
				if files.endswith(".lp"):
					lpfile = files
				else:
					if files == "README.txt":
						continue
					os.remove(options.path_to_lp_files+os.sep+files)
		
			if path.exists(new_dir):
				move(options.path_to_lp_files+os.sep+lpfile, new_dir+os.sep+options.scenario+'.lp')


	if hasattr(options, 'mga'):  # check to see if mga attribute specified
		from collections import defaultdict
		from temoa_rules import TotalCost_rule
		from temoa_mga   import ActivityObj_rule, SlackedObjective_rule, PreviousAct_rule

		scenario_names = []
		scenario_names.append( options.scenario )

		# The MGA algorithm uses different objectives per iteration, so the first
		# step is to remove the original objective function
		model.del_component( 'TotalCost' )
		# Create concrete model
		instance_1, txt_file = create_temoa_instance( model, options )
		# Now add back the objective function that we earlier removed; note that name
		# we choose here (FirstObj) will be copied to the output file.
		instance_1.FirstObj = Objective( rule=TotalCost_rule, sense=minimize )
		instance_1.preprocess()

		result_1 = solve_temoa_instance( instance_1, optimizer, options, txt_file )
		handle_files( options, TemoaConfig, log_name='Complete_OutputLog.log' )
		instance_1.solutions.load_from( result_1, delete_symbol_map=False )
		instance_1.solutions.load_from( result_1 )
		# using value() converts the now-loaded results into a single number,
		# which we'll use with our slightly unusual SlackedObjective_rule below
		# (but defined above).
		Perfect_Foresight_Obj = value( instance_1.FirstObj )
			
		# Create a new parameter that stores the MGA objective function weights
		prev_activity_t = defaultdict( int )		
		prev_activity_t = PreviousAct_rule( instance_1, options.mga_weight, prev_activity_t )		
		
		# Perform MGA iterations
		while options.next_mga():
			instance_mga, txt_file = create_temoa_instance( model, options )
			try:
				txt_file_mga = open(options.path_to_logs+os.sep+"Complete_OutputLog.log", "w")
			except BaseException as io_exc:
				SE.write("MGA Log file cannot be opened. Please check path. Trying to find:\n"+options.path_to_logs+" folder\n")
				txt_file_mga = open("OutputLog_MGA_last.log", "w")
			
			# Update second instance with the new MGA-specific objective function
			# and constraint.
			instance_mga.SecondObj = Objective(
			expr=ActivityObj_rule( instance_mga, prev_activity_t ),
			noruleinit=True,
			sense=minimize
			)
			instance_mga.PreviousSlackedObjective = Constraint(
			rule=None,
			expr=SlackedObjective_rule( instance_mga, Perfect_Foresight_Obj, options.mga ),
			noruleinit=True
			)
			instance_mga.preprocess()
			solve_temoa_instance( instance_mga, optimizer, options, txt_file )
			handle_files( options, TemoaConfig, log_name='Complete_OutputLog.log' )

	else:  #  User requested a single run
		instance_1, txt_file = create_temoa_instance( model, options )
		solve_temoa_instance( instance_1, optimizer, options, txt_file )
		handle_files( options, TemoaConfig, log_name='Complete_OutputLog.log')

					
def get_solvers():
	"""Return the solvers avaiable on the system."""
	from logging import getLogger
	
	logger = getLogger('pyomo.solvers')
	logger_status = logger.disabled
	logger.disabled = True  # no need for warnings: it's what we're testing!
	
	available_solvers = set()
	for sname in SF.services():   # list of solver interface names
		# initial underscore ('_'): Pyomo's method to mark non-public plugins
		if '_' == sname[0]: continue

		solver = SF( sname )
		if not solver: continue

		if 'os' == sname: continue     # Workaround current bug in Coopr
		if not solver.available( exception_flag=False ): continue
		available_solvers.add( sname )

	logger.disabled = logger_status  # put back the way it was.

	if available_solvers:
		if 'cplex' in available_solvers:
			default_solver = 'cplex'
		elif 'gurobi' in available_solvers:
			default_solver = 'gurobi'
		elif 'cbc' in available_solvers:
			default_solver = 'cbc'
		elif 'glpk' in available_solvers:
			default_solver = 'glpk'
		else:
			default_solver = iter(available_solvers).next()
	else:
		default_solver = 'NONE'
		SE.write('\nNOTICE: Pyomo did not find any suitable solvers.  Temoa will '
		   'not be able to solve any models.  If you need help, ask on the '
		   'Temoa Project forum: http://temoaproject.org/\n\n' )

	return (available_solvers, default_solver)



def parse_args ( ):
	"""Parse arguments specfied from command line or in config file."""
	import argparse, sys
	import os, re
	from os.path import dirname, abspath

	available_solvers, default_solver = get_solvers()
	
	parser = argparse.ArgumentParser()
	parser.prog = path.basename( argv[0].strip('/') )

	parser.add_argument('dot_dat',
	  type=str,
	  nargs='*',
	  help='AMPL-format data file(s) with which to create a model instance. '
	       'e.g. "data.dat"'
	)

	parser.add_argument( '--path_to_logs',
	  help='Path to where debug logs will be generated by default. See folder debug_logs in db_io.',
	  action='store',
	  dest='path_to_logs',
	  default=re.sub('temoa_model$', 'db_io', dirname(abspath(__file__)))+os.sep+"debug_logs"
	)

	parser.add_argument( '--config',
	 help='Path to file containing configuration information.',
	 action='store',
	 dest='config',
	 default=None
	 )

	parser.add_argument('--solver',
	  help="Which backend solver to use.  See 'pyomo --help-solvers' for a list "
	       'of solvers with which Pyomo can interface.  The list shown here is '
	       'what Pyomo can currently find on this system.  [Default: {}]'
	       .format(default_solver),
	  action='store',
	  choices=sorted(available_solvers),
	  dest='solver',
	  default=default_solver)

	options = parser.parse_args()

	# Can't specify keeping the LP file without config file, so set this 
	# attribute to false
	options.keepPyomoLP = False

	# If the user specifies the config flag, then call TemoaConfig and overwrite
	# the argument parser above.
	if options.config:
		config_flag = 1  #flag indicates config file was used.
		try:
			temoa_config = TemoaConfig(d_solver=default_solver)
			temoa_config.build(config=options.config)
			SE.write(repr(temoa_config))
			options = temoa_config
			SE.write('\nPlease press enter to continue or Ctrl+C to quit.\n')
			#raw_input() # Give the user a chance to confirm input
			if options.abort_temoa:
				return
		except KeyboardInterrupt:
			SE.write('\n\nUser requested quit.  Exiting Temoa ...\n')
			raise SystemExit()
	else:
		config_flag = 0	#flag indicates config file was not used.

	s_choice = str( options.solver ).upper()
	SE.write('Notice: Using the {} solver interface.\n'.format( s_choice ))
	SE.flush()
	
	SE.write("Continue Operation? [Press enter to continue or CTRL+C to abort]\n")
	SE.flush()
	raw_input() # Give the user a chance to confirm input

	return options, config_flag


def temoa_setup ( model, config_filename ):
	"""This function prepares the model to be solved. 

	Inputs:
	model -- the model object
	config_filename -- config filename, non-blank if called from the UI
	There are three possible ways to call the model:
	1. python temoa_model/ /path/to/data_files
	2. python temoa_model/ --config=/path/to/config/file
	3. function call from the UI
	This function discerns which way the model was called and process the 
	inputs accordingly.
	"""

	from argparse import Namespace
	from os import sep
	
	if config_filename == '':  # Called from the command line
		options, config_flag = parse_args()
		if config_flag == 1:   # Option 2 (using config file)
			from pyutilib.services import TempfileManager
			options.path_to_lp_files = options.path_to_logs + sep + "lp_files"
			TempfileManager.tempdir = options.path_to_lp_files	
		else:  # Must be Option 1 (no config file)
			pass	

	else:   # Config file already specified, so must be an interface call
		available_solvers, default_solver = get_solvers()
		temoa_config = TemoaConfig(d_solver=default_solver)
		temoa_config.build(config=config_filename)
		options = temoa_config
	
		global temp_lp_dest
		temp_lp_dest = '/srv/thirdparty/temoa/db_io/'

		from pyutilib.services import TempfileManager
		options.path_to_lp_files = options.path_to_logs + sep + "lp_files"
		TempfileManager.tempdir = options.path_to_lp_files	
	
	opt = temoa_checks( options )
	
	# Now let's try to solve the model
	try:
		temoa_create_and_solve( model, opt, options )
	except KeyboardInterrupt as e:
		SE.write( '\n\nUser requested quit.  Exiting Temoa ...\n' )
		SE.flush()
	except SystemExit as e:
		SE.write( '\n\nTemoa exit requested.  Exiting ...\n' )
		SE.flush()	


def temoa_checks( options ):
	"""Make sure Python 2.7 is used and that a suitable solver is available."""

	from sys import version_info, exit
	
	if version_info < (2, 7):
		msg = ("Temoa requires Python v2.7 to run.\n\n The model may not solve"
			"properly with another version.")
		raise SystemExit( msg )

	from pyomo.opt import SolverFactory
	opt = SolverFactory( options.solver )
	if opt:
		pass
	elif options.solver != 'NONE':
		SE.write( "\nWarning: Unable to initialize solver interface for '{}'\n\n"
			.format( options.solver ))
		if SE.isatty():
			SE.write( "Please press enter to continue or Ctrl+C to quit." )
			raw_input()
	return opt

