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

#from temoa_common import *

from os import path, close as os_close
from sys import argv, stderr as SE, stdout as SO
from signal import signal, SIGINT, default_int_handler
from shutil import copyfile, move

from pyomo.opt import SolverFactory as SF
from temoa_config import TemoaConfig


import errno, warnings
import re as reg_exp

import pyomo.environ
  # workaround for Coopr's brain dead signal handler
signal(SIGINT, default_int_handler)

TEMOA_GIT_VERSION  = 'HEAD'
TEMOA_RELEASE_DATE = 'Today'

###############################################################################
# Miscellaneous routines


def version ( options ):
	from sys import stdout as SO
	from os.path import basename, dirname
	import os

	bname = basename( dirname( __file__ ))

	if 'HEAD' == TEMOA_GIT_VERSION:
		msg = """
{}: Temoa Model, v"Bleeding Edge"

You are using a development version of Temoa.  Use Git to determine the current
branch name and number.  Command line hints:

      # from within the code directory
    $ git branch
    $ git status    # to remind you of any changes you have made
    $ git log -1    # -1 is optional, showing only the most recent commit
"""

		args = (bname,)

	else:
		msg = """
{}: Temoa Model, Release Date: {}
Git Hash: {}

Temoa does not currently have version numbers, but uses the date of release as a
proxy.  The hexadecimal Git Hash number uniquely identifies the exact
branch/commit that created '{}'.
"""

		args = (bname, TEMOA_RELEASE_DATE, TEMOA_GIT_VERSION, bname)

	msg += """
Copyright (C) 2015 NC State University

We provide Temoa -- the model and associated scripts -- "as-is" with no express
or implied warranty for accuracy or accessibility.  Temoa is a research tool,
given in good faith to the community (anyone who uses Temoa for any purpose) as
free software under the terms of the GNU General Public License, version 2.
"""

	try:
		txt_file = open(options.path_to_logs+os.sep+"Complete_OutputLog.log", "w")
	except BaseException as io_exc:
		SE.write("Log file cannot be opened. Please check path. Trying to find:\n"+options.path_to_logs+" folder\n")
		txt_file = open("Complete_OutputLog.log", "w")

	txt_file.write( msg )
	SO.write( msg.format( *args ))
	#raise SystemExit


def bibliographicalInformation ( options ):
	from sys import stdout as SO
	import os

	msg = """
Please cite the following paper if your use of Temoa leads to a publishable
result:

  Title:     Modeling for Insight Using Tools for Energy Model Optimization and Analysis (Temoa)
  Authors:   Kevin Hunter, Sarat Sreepathi, Joseph F. DeCarolis
  Date:      November, 2013
  Publisher: Elsevier
  Journal:   Energy Economics
  Volume:    40
  Pages:     339 - 349
  ISSN:      0140-9883
  DOI:       http://dx.doi.org/10.1016/j.eneco.2013.07.014
  URL:       http://www.sciencedirect.com/science/article/pii/S014098831300159X

For copy and paste or BibTex use:

  Kevin Hunter, Sarat Sreepathi, Joseph F. DeCarolis, Modeling for Insight Using Tools for Energy Model Optimization and Analysis (Temoa), Energy Economics, Volume 40, November 2013, Pages 339-349, ISSN 0140-9883, http://dx.doi.org/10.1016/j.eneco.2013.07.014.

  (BibTeX)
@article{Hunter_etal_2013,
  title   = "Modeling for {I}nsight {U}sing {T}ools for {E}nergy {M}odel {O}ptimization and {A}nalysis ({T}emoa)",
  journal = "Energy Economics",
  volume  = "40",
  pages   = "339 - 349",
  month   = "November",
  year    = "2013",
  issn    = "0140-9883",
  doi     = "http://dx.doi.org/10.1016/j.eneco.2013.07.014",
  url     = "http://www.sciencedirect.com/science/article/pii/S014098831300159X",
  author  = "Kevin Hunter and Sarat Sreepathi and Joseph F. DeCarolis"
}

"""

	try:
		txt_file = open(options.path_to_logs+os.sep+"Complete_OutputLog.log", "w")
	except BaseException as io_exc:
		SE.write("Log file cannot be opened. Please check path. Trying to find:\n"+options.path_to_logs+" folder\n")
		txt_file = open("Complete_OutputLog.log", "w")

	txt_file.write( msg )
	SO.write( msg )
	#raise SystemExit



# End miscellaneous routines
###############################################################################

###############################################################################
# Direct invocation methods (when modeler runs via "python model.py ..."

def MGA ( model, optimizer, options, epsilon=1e-6 ):
	from collections import defaultdict
	from time import clock
	import sys, os, gc

	from pyomo.environ import DataPortal

	from temoa_rules import TotalCost_rule
	from pformat_results import pformat_results

	opt = optimizer              # for us lazy programmer types
	dot_dats = options.dot_dat

	scenario_names = []
	scenario_names.append(options.scenario)
	
	def ActivityObj_rule ( M, prev_act_t ):
		new_act = 0
		for t in M.V_ActivityByTech:
			if t in prev_act_t:
				new_act += prev_act_t[ t ] * M.V_ActivityByTech[t]
		return new_act

	def SlackedObjective_rule ( M, prev_cost ):
		# It is important that this function name *not* match its constraint name
		# plus '_rule', else Pyomo will attempt to be too smart.  That is, at the
		# first implementation, the associated constraint name is
		# 'PreviousSlackedObjective', for which Pyomo searches the namespace for
		# 'PreviousSlackedObjective_rule'.  We decidedly do not want Pyomo
		# trying to call this function because it is not aware of the second arg.
		slackcost = (1 + options.mga) * prev_cost 
		oldobjective = TotalCost_rule( M )
		expr = ( slackcost >= oldobjective )
		return expr

	def PreviousAct_rule ( instance ):
		#   The version below weights each technology by its previous cumulative
		#   activity. However, different sectors may be tracked in different units and 
		#   have activities of very different magnitudes. Can also modify the code 
		#   changing 'val' to 1 to implement a integer-based weight to address this non-uniform
		#   weighting issue.
		if options.mga_weight == 'integer':
			for t in instance_1.V_ActivityByTech:
				if t in instance.tech_mga:
					val = value( instance.V_ActivityByTech[t] )
					if abs(val) < epsilon: continue
					prev_activity_t[ t ] += 1.0   #val
                	return prev_activity_t
                
		#   The version below calculates activity by sector and normalized technology-
		#   specific activity by the total activity for the sector. Currently accounts
		#   for electric and transport sectors, but others can be added to the block below.
		elif options.mga_weight == 'normalized':
			sectors = set(['electric', 'transport', 'industrial', 'commercial', 'residential'])
			act     = dict()
			techs   = {'electric':    instance.tech_electric,
			           'transport':   instance.tech_transport,
			           'industrial':  instance.tech_industrial,
			           'commercial':  instance.tech_commercial,
			           'residential': instance.tech_residential}
			for s in sectors:
				if len(techs[s]) > 0:
					act[s] = sum(
			  		value( instance.V_ActivityByTech[S_t] )
			  		for S_t in techs[s]
					)
       	
			for t in instance_1.V_ActivityByTech:
				for s in sectors:
					if t in techs[s]:
						val = value( instance.V_ActivityByTech[t] )
						if abs(val) < epsilon: continue
						prev_activity_t[ t ] += val / act[s]
                	return prev_activity_t


	# The MGA algorithm uses different objectives per iteration, so the first
	# step is to remove the original objective function
	model.del_component( 'TotalCost' )

	
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

		mdata = DataPortal( model=model )
		for fname in dot_dats:
			if fname[-4:] != '.dat':
				msg = "\n\nExpecting a dot dat (e.g., data.dat) file, found '{}'\n"
				raise Exception( msg.format( fname ))
			mdata.load( filename=fname )
		SE.write( '\r[%8.2f\n' % duration() )
		txt_file.write( '\r[%8.2f]\n' % duration() )

		SE.write( '[        ] Creating Temoa model instance.'); SE.flush()
		txt_file.write( 'Creating Temoa model instance.')

		# Create concrete model
		instance_1 = model.create_instance( mdata )

		# Now add in and objective function, like we earlier removed; note that name
		# we choose here (FirstObj) will be copied to the output file.
		instance_1.FirstObj = Objective( rule=TotalCost_rule, sense=minimize )
		instance_1.preprocess()

		SE.write( '\r[%8.2f\n' % duration() )
		txt_file.write( '\r[%8.2f]\n' % duration() )

		SE.write( '[        ] Solving first model instance.'); SE.flush()
		txt_file.write( 'Solving first model instance.')

		if opt:
			result_1 = opt.solve( instance_1, 
								  load_solutions=False, 
								  keepfiles=options.keepPyomoLP, 
								  symbolic_solver_labels = options.keepPyomoLP )
			instance_1.solutions.load_from(result_1, delete_symbol_map=False)

			SE.write( '\r[%8.2f\n' % duration() )
			txt_file.write( '\r[%8.2f]\n' % duration() )

			instance_1.solutions.load_from(result_1)
			formatted_results = pformat_results( instance_1, result_1, options )  
			SO.write( formatted_results.getvalue() )
			txt_file.write( formatted_results.getvalue() )
			txt_file.flush()


			# using value() converts the now-load()ed results into a single number,
			# which we'll use with our slightly unusual SlackedObjective_rule below
			# (but defined above).
			Perfect_Foresight_Obj = value( instance_1.FirstObj )
			
			# Create a new parameter that stores the MGA objective function weights
			prev_activity_t = defaultdict( int )		
			prev_activity_t = PreviousAct_rule( instance_1 )		

			if isinstance(options, TemoaConfig) and options.saveTEXTFILE:
				for inpu in options.dot_dat:
					file_ty = reg_exp.search(r"\b([\w-]+)\.(\w+)\b", inpu)
				
				new_dir = options.path_to_db_io+os.sep+file_ty.group(1)+'_'+options.scenario+'_model'
				
				if path.isfile(options.path_to_logs+os.sep+'Complete_OutputLog.log') and path.exists(new_dir):
					copyfile(options.path_to_logs+os.sep+'Complete_OutputLog.log', new_dir+os.sep+options.scenario+'_OutputLog.log')

			
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
			
			
			#Perform 5 MGA iterations
			while options.next_mga():
				instance_mga = model.create_instance( mdata )


				try:
					txt_file_mga = open(options.path_to_logs+os.sep+"OutputLog_MGA_last.log", "w")
				except BaseException as io_exc:
					SE.write("MGA Log file cannot be opened. Please check path. Trying to find:\n"+options.path_to_logs+" folder\n")
					txt_file_mga = open("OutputLog_MGA_last.log", "w")
				
				#scenario_names.append(options.scenario)
				
				# Update second instance with the new MGA-specific objective function
				# and constraint.
				instance_mga.SecondObj = Objective(
				expr=ActivityObj_rule( instance_mga, prev_activity_t ),
				noruleinit=True,
				sense=minimize
				)
				instance_mga.PreviousSlackedObjective = Constraint(
				rule=None,
				expr=SlackedObjective_rule( instance_mga, Perfect_Foresight_Obj ),
				noruleinit=True
				)
				instance_mga.preprocess()

				if options.keepPyomoLP:
					SE.write('\nSolver will write file: {}\n\n'.format( options.scenario + '.lp' ))
					txt_file.write('\nSolver will write file: {}\n\n'.format( options.scenario + '.lp' ))

				SE.write( '[        ] Solving {}.'.format(options.scenario)); SE.flush()
				txt_file.write( 'Solving {}.'.format(options.scenario)); SE.flush()
				txt_file_mga.write( 'Solving {}.'.format(options.scenario)); SE.flush()
				
				result_mga = opt.solve( instance_mga, 
										load_solutions=False, 
										keepfiles=options.keepPyomoLP, 
										symbolic_solver_labels = options.keepPyomoLP )

				SE.write( '\r[%8.2f\n' % duration() )
				txt_file.write( '\r[%8.2f]\n' % duration() )
				txt_file_mga.write( '\r[%8.2f]\n' % duration() )


				instance_mga.solutions.load_from(result_mga, delete_symbol_map=False)
				formatted_results = pformat_results( instance_mga, result_mga, options )
				SO.write( formatted_results.getvalue() )
				txt_file.write( formatted_results.getvalue() )
				txt_file_mga.write( formatted_results.getvalue() )

				txt_file_mga.flush()
				
				#Keep adding activity from latest iteration to MGA Obj function
				prev_activity_t = PreviousAct_rule( instance_mga )

				# return signal handlers to defaults, again
				signal(SIGINT, default_int_handler)
				
				txt_file_mga.close()
			
				if isinstance(options, TemoaConfig) and options.saveTEXTFILE:
					for inpu in options.dot_dat:
						file_ty = reg_exp.search(r"\b([\w-]+)\.(\w+)\b", inpu)
					
					new_dir = options.path_to_db_io+os.sep+file_ty.group(1)+'_'+options.scenario+'_model'
					
					if path.isfile(options.path_to_logs+os.sep+'OutputLog_MGA_last.log') and path.exists(new_dir):
						copyfile(options.path_to_logs+os.sep+'OutputLog_MGA_last.log', new_dir+os.sep+options.scenario+'_OutputLog.log')


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

						
			txt_file.flush()
			txt_file.close()
		else:
			SE.write( '\r---------- Not solving: no available solver\n' )
			txt_file.write( '\r---------- Not solving: no available solver\n' )
			txt_file.close()
			#return
			
	except BaseException as model_exc:
		SE.write("exception found in MGA()\n")
		txt_file.write("exception found in MGA()\n")
		SE.write(str(model_exc))
		txt_file.write(str(model_exc))
		txt_file.close()
		
	if isinstance(options, TemoaConfig) and options.saveTEXTFILE:
		for inpu in options.dot_dat:
			file_ty = reg_exp.search(r"\b([\w-]+)\.(\w+)\b", inpu)
		
		for sc in scenario_names:
			new_dir = options.path_to_db_io+os.sep+file_ty.group(1)+'_'+sc+'_model'
			
			if path.isfile(options.path_to_logs+os.sep+'Complete_OutputLog.log') and path.exists(new_dir):
				copyfile(options.path_to_logs+os.sep+'Complete_OutputLog.log', new_dir+os.sep+'Complete_OutputLog.log')

		
def solve_perfect_foresight ( model, optimizer, options ):
	from time import clock
	import sys, os, gc

	from pyomo.core import DataPortal

	from pformat_results import pformat_results
	
	try:
		txt_file = open(options.path_to_logs+os.sep+"Complete_OutputLog.log", "w")
	except BaseException as io_exc:
		SE.write("Log file cannot be opened. Please check path. Trying to find:\n"+options.path_to_logs+" folder\n")
		txt_file = open("Complete_OutputLog.log", "w")
		txt_file.write("Log file cannot be opened. Please check path. Trying to find:\n"+options.path_to_logs+" folder\n")
	
	try:
	
		opt = optimizer              # for us lazy programmer types
		dot_dats = options.dot_dat

		if options.keepPyomoLP:
			SE.write('\nSolver will write file: {}\n\n'.format( options.scenario + '.lp' ))
			txt_file.write('\nSolver will write file: {}\n\n'.format( options.scenario + '.lp' ))

		SE.write( '[        ] Reading data files.'); SE.flush()
		txt_file.write( 'Reading data files.')
		# Recreate the pyomo command's ability to specify multiple "dot dat" files
		# on the command line
		begin = clock()
		duration = lambda: clock() - begin

		modeldata = DataPortal( model=model )
		for fname in dot_dats:
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

		# Now do the solve
		SE.write( '[        ] Solving.'); SE.flush()
		txt_file.write( 'Solving.')
		if opt:
			result = opt.solve( instance , 
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
		SE.write("exception found in solve_perfect_foresight\n")
		txt_file.write("exception found in solve_perfect_foresight\n")
		SE.write(str(model_exc))
		txt_file.write(str(model_exc))
		txt_file.close()

	if isinstance(options, TemoaConfig) and options.saveTEXTFILE:
		for inpu in options.dot_dat:
			file_ty = reg_exp.search(r"\b([\w-]+)\.(\w+)\b", inpu)
		
		new_dir = options.path_to_db_io+os.sep+file_ty.group(1)+'_'+options.scenario+'_model'
		
		if path.isfile(options.path_to_logs+os.sep+'Complete_OutputLog.log') and path.exists(new_dir):
			copyfile(options.path_to_logs+os.sep+'Complete_OutputLog.log', new_dir+os.sep+options.scenario+'_OutputLog.log')

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

def get_solvers():
	
	from logging import getLogger
	
	logger = getLogger('pyomo.solvers')
	logger_status = logger.disabled
	logger.disabled = True  # no need for warnings: it's what we're testing!
	
	available_solvers = set()
	for sname in SF.services():   # list of solver interface names
		# initial underscore ('_'): Coopr's method to mark non-public plugins
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
	
	import argparse, platform, sys
	import os, re
	from os.path import dirname, abspath

	# used for some error messages below.
	red_bold = cyan_bold = reset = ''
	if platform.system() != 'Windows' and SE.isatty():
		red_bold  = '\x1b[1;31m'
		cyan_bold = '\x1b[1;36m'
		reset     = '\x1b[0m'

	

	available_solvers, default_solver = get_solvers()
	
	parser = argparse.ArgumentParser()
	parser.prog = path.basename( argv[0].strip('/') )

	solver      = parser.add_argument_group('Solver Options')
	stochastic  = parser.add_argument_group('Stochastic Options')
	postprocess = parser.add_argument_group('Postprocessing Options')
	mga         = parser.add_argument_group('MGA Options')

	parser.add_argument('dot_dat',
	  type=str,
	  nargs='*',
	  help='AMPL-format data file(s) with which to create a model instance. '
	       'e.g. "data.dat"'
	)

	parser.add_argument( '--how_to_cite',
	  help='Bibliographical information for citation, in the case that Temoa '
	    'contributes to a project that leads to a scientific publication.',
	  action='store_true',
	  dest='how_to_cite',
	  default=False)

	parser.add_argument( '-V', '--version',
	  help='Display the Temoa version information, then exit.',
	  action='store_true',
	  dest='version',
	  default=False
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

	solver.add_argument('--solver',
	  help="Which backend solver to use.  See 'pyomo --help-solvers' for a list "
	       'of solvers with which Coopr can interface.  The list shown here is '
	       'what Coopr can currently find on this system.  [Default: {}]'
	       .format(default_solver),
	  action='store',
	  choices=sorted(available_solvers),
	  dest='solver',
	  default=default_solver)

	solver.add_argument('--keep_pyomo_lp_file',
	  help='Save the LP file as written by Pyomo.  This is distinct from the '
	       "solver's generated LP file, but /should/ represent the same model.  "
	       'Mainly used for debugging purposes.  '
	       '[Default: remove Pyomo LP file]',
	  action='store_true',
	  dest='keepPyomoLP',
	  default=False)

	#An optional argument with the ability to take a flag (--MGA) and a
	#numeric slack value
	mga.add_argument('--mga',
	  help='Include the flag --MGA and supply a slack-value and recieve a '
	    'Modeling to generate alternatives solution',
	  dest='mga',
	  type=float)

	options = parser.parse_args()
	#print options
	#Namespace(config='config_sample', dot_dat=[], generateSolverLP=False, how_to_cite=False, keepPyomoLP=False, mga=None, solver='mpec_nlp', version=False)

	# Use the Temoa configuration file to overwrite Kevin's argument parser
	if options.config:
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

	# First, the options that exit or do not perform any "real" computation
	if options.version:
		version(options)
		# this function exits
		return

	if options.how_to_cite:
		bibliographicalInformation(options)
		# this function exits.
		return
		
	if options.mga:
		msg = 'MGA specified (slack value: {})\n'.format( options.mga )
		SE.write( msg )

	s_choice = str( options.solver ).upper()
	SE.write('Notice: Using the {} solver interface.\n'.format( s_choice ))
	SE.flush()
	
	SE.write("Continue Operation? [Press enter to continue or CTRL+C to abort]\n")
	SE.flush()
	raw_input() # Give the user a chance to confirm input

	return options


def temoa_solve_ui ( model, config_filename ):
	from os import sep
	
	available_solvers, default_solver = get_solvers()

	temoa_config = TemoaConfig(d_solver=default_solver)
	temoa_config.build(config=config_filename)
	options = temoa_config
	
	global temp_lp_dest
	temp_lp_dest = '/srv/thirdparty/temoa/db_io/'

	from pyutilib.services import TempfileManager
	options.path_to_lp_files = options.path_to_logs + sep + "lp_files"
	TempfileManager.tempdir = options.path_to_lp_files	
	
	#FIXME: Put logic from parse_args() here that are not covered in
	#temoa_config.py. Like --how_to_cite & --version options.
	if options.version:
		version(options)
		# this function exits
		return

	if options.how_to_cite:
		bibliographicalInformation(options)
		# this function exits.
		return
	
	if options.abort_temoa:
		return
	
	run_solve(model, options)


def temoa_solve ( model ):
	
	from argparse import Namespace
	from os import sep

	options = parse_args()

	if options is None:
		return
	
	global temp_lp_dest
	temp_lp_dest = ''
	
	from pyutilib.services import TempfileManager
	options.path_to_lp_files = options.path_to_logs + sep + "lp_files"
	TempfileManager.tempdir = options.path_to_lp_files
	
	run_solve(model,options)

	

	

def run_solve(model,options):
	from sys import argv, version_info, exit
	from shutil import rmtree
	import os
	
	if version_info < (2, 7):
		msg = ("Temoa requires Python v2.7 to run.\n\nIf you've "
		  "installed Pyomo with Python 2.6 or less, you'll need to reinstall "
		  'Pyomo, taking care to install with a Python 2.7 (or greater) '
		  'executable.')
		raise SystemExit( msg )


	from pyomo.opt import SolverFactory

	opt = SolverFactory( options.solver )
	if opt:
		pass
		#if options.keepPyomoLP:
		# 	opt.keepfiles = True
		# 	opt.symbolic_solver_labels = True

	elif options.solver != 'NONE':
		SE.write( "\nWarning: Unable to initialize solver interface for '{}'\n\n"
			.format( options.solver ))
		if SE.isatty():
			SE.write( "Please press enter to continue or Ctrl+C to quit." )
			raw_input()
		else:
			SE.write(
			  '\n\n  Not stopping for user input because stderr is not a tty.'
			  '\n  (This suggests that Temoa is currently running as part of a'
			  '\n  a larger script and the user is not able to see this'
			  '\n  message currently.  The user script is responsible for'
			  '\n  handling this situation appropriately.\n\n')

	try:
		if options.dot_dat:
			if options.mga:
				for inpu in options.dot_dat:
					file_ty = reg_exp.search(r"\b([\w-]+)\.(\w+)\b", inpu)
			
				options.path_to_db_io += os.sep+file_ty.group(1)+'_'+options.scenario+'_model'
				
				if os.path.exists( options.path_to_db_io ):
					rmtree( options.path_to_db_io )
				os.mkdir(options.path_to_db_io)
				
				MGA( model, opt, options )
			else:
				solve_perfect_foresight( model, opt, options )

	except IOError as e:
		if e.errno == errno.EPIPE:
			# stdout has been closed, e.g., a user has quit the 'less' pager
			# There is no error on our part, so just quit gracefully
			return
		raise
	except KeyboardInterrupt as e:
		SE.write( '\n\nUser requested quit.  Exiting Temoa ...\n' )
		SE.flush()
	except SystemExit as e:
		SE.write( '\n\nTemoa exit requested.  Exiting ...\n' )
		SE.flush()


# End direct invocation methods
###############################################################################
