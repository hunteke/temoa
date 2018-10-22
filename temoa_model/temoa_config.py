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
from os.path import abspath, isfile, splitext, dirname
from os import sep

import re

def db_2_dat(ifile, ofile, options):
	# Adapted from DB_to_DAT.py
	import sqlite3
	import sys
	import re
	import getopt
	
	def write_tech_mga(f):
		cur.execute("SELECT tech FROM technologies")
		f.write("set tech_mga :=\n")
		for row in cur:
			f.write(row[0] + '\n')
		f.write(';\n\n')
	
	def write_tech_sector(f):
		sectors = set()
		cur.execute("SELECT sector FROM technologies")
		for row in cur:
			sectors.add(row[0])
		for s in sectors:
			cur.execute("SELECT tech FROM technologies WHERE sector == '" + s + "'")
			f.write("set tech_" + s + " :=\n")
			for row in cur:
				f.write(row[0] + '\n')
			f.write(';\n\n')

	def query_table (t_properties, f):
		t_type = t_properties[0]   #table type (set or param)
		t_name = t_properties[1]   #table name
		t_dtname = t_properties[2] #DAT table name when DB table must be subdivided
		t_flag = t_properties[3]   #table flag, if any
		t_index = t_properties[4]  #table column index after which '#' should be specified
		if type(t_flag) is list:   #tech production table has a list for flags; this is currently hard-wired
			db_query = "SELECT * FROM " + t_name + " WHERE flag=='p' OR flag=='pb' OR flag=='ps'"
			cur.execute(db_query)
			if cur.fetchone() is None:
				return
			if t_type == "set":
				f.write("set " + t_dtname + " := \n")
			else:
				f.write("param " + t_dtname + " := \n")
		elif t_flag != '':    #check to see if flag is empty, if not use it to make table
			db_query = "SELECT * FROM " + t_name + " WHERE flag=='" + t_flag + "'"
			cur.execute(db_query)
			if cur.fetchone() is None:
				return
			if t_type == "set":
				f.write("set " + t_dtname + " := \n")
			else:
				f.write("param " + t_dtname + " := \n")
	 	else:    #Only other possible case is empty flag, then 1-to-1 correspodence between DB and DAT table names
			db_query = "SELECT * FROM " + t_name
			cur.execute(db_query)
			if cur.fetchone() is None:
				return
			if t_type == "set":
				f.write("set " + t_name + " := \n")
			else:
				f.write("param " + t_name + " := \n")
		cur.execute(db_query)
		if t_index == 0:    #make sure that units and descriptions are commented out in DAT file
			for line in cur:
				str_row = str(line[0]) + "\n"
				f.write(str_row)
				print str_row
		else:
			for line in cur:
				before_comments = line[:t_index+1]    
				before_comments = re.sub('[(]', '', str(before_comments))
				before_comments = re.sub('[\',)]', '    ', str(before_comments))
				after_comments = line[t_index+2:]
				after_comments = re.sub('[(]', '', str(after_comments))
				after_comments = re.sub('[\',)]', '    ', str(after_comments)) 
				search_afcom = re.search(r'^\W+$', str(after_comments))		#Search if after_comments is empty.
				if not search_afcom :
					str_row = before_comments + "# " + after_comments + "\n"
				else :
						str_row = before_comments + "\n"
				f.write(str_row)
				print str_row
		f.write(';\n\n')

	#[set or param, table_name, DAT fieldname, flag (if any), index (where to insert '#')
	table_list = [
		['set',  'time_periods',              'time_exist',          'e',            0],
		['set',  'time_periods',              'time_future',         'f',            0],
		['set',  'time_season',               '',                    '',             0],
		['set',  'time_of_day',               '',                    '',             0],
		['set',  'Zones',        	          '',                    '',             0],
		['set',  'technologies',              'tech_resource',       'r',            0],
		['set',  'technologies',              'tech_production',    ['p','pb','ps'], 0],
		['set',  'technologies',              'tech_baseload',       'pb',           0],
		['set',  'technologies',              'tech_storage',        'ps',           0],
		['set',  'tech_ramping',              '',                    '',             0],
		['set',  'commodities',               'commodity_physical',  'p',            0],
		['set',  'commodities',               'commodity_emissions', 'e',            0],
		['set',  'commodities',               'commodity_demand',    'd',            0],
		['param','MinGenGroupOfTechnologies_Data', '',                    '',             2], \
		['param','SegFrac',                   '',                    '',             2],
		['param','DemandSpecificDistribution','',                    '',             3],
		['param','CapacityToActivity',        '',                    '',             1],
		['param','PlanningReserveMargin',     '',                    '',             1],
		['param','GlobalDiscountRate',        '',                    '',             0],
		['param','DiscountRate',              '',                    '',             2],
		['param','EmissionActivity',          '',                    '',             5],
		['param','EmissionLimit',             '',                    '',             2],
		['param','Demand',                    '',                    '',             2],
		['param','TechOutputSplit',           '',                    '',             3],
		['param','TechInputSplit',            '',                    '',             3],
		['param','MinCapacity',               '',                    '',             2],
		['param','MaxCapacity',               '',                    '',             2],
		['param','MaxActivity',               '',                    '',             2],
		['param','MinActivity',               '',                    '',             2],
		['param','GrowthRateMax',             '',                    '',             1],
		['param','GrowthRateSeed',            '',                    '',             1],
		['param','LifetimeTech',              '',                    '',             1],
		['param','LifetimeProcess',           '',                    '',             2],
		['param','LifetimeLoanTech',          '',                    '',             1],
		['param','CapacityFactorTech',        '',                    '',             3],
		['param','CapacityFactorProcess',     '',                    '',             4],
		['param','Efficiency',                '',                    '',             4],
		['param','ExistingCapacity',          '',                    '',             2],
		['param','CostInvest',                '',                    '',             2],
		['param','CostFixed',                 '',                    '',             3],
		['param','CostVariable',              '',                    '',             3],
		['param','CapacityCredit',            '',                    '',             1],
		['param','RampUp',                    '',                    '',             1],
		['param','RampDown',                  '',                    '',             1]
	]

	with open(ofile, 'w') as f:
		f.write('data ;\n\n')
		#connect to the database
		con = sqlite3.connect(ifile)
		cur = con.cursor()   # a database cursor is a control structure that enables traversal over the records in a database
		con.text_factory = str #this ensures data is explored with the correct UTF-8 encoding
	
		# Return the full list of existing tables.
		table_exist = cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
		table_exist = [i[0] for i in table_exist]
	
		for table in table_list:
			if table[1] in table_exist:
				query_table(table, f)
		if options.mga_weight == 'integer':
			write_tech_mga(f)
		if options.mga_weight == 'normalized':
			write_tech_sector(f)
			
		# Added by Hadi, The following 3 bloack, append the techs groups to the .dat file. 


		if "MinGenGroupOfTechnologies" in table_exist:
			cur.execute("SELECT * FROM MinGenGroupOfTechnologies")
			A=cur.fetchall()
			if len(A)!=0:
				f.write("set " +"GroupOfTechnologies" + " := \n")
				for row in A:
					f.write(row[0]+"   "+row[1]+"   "+str(row[2])+" \n")
				f.write(";\n\n")
		


		if "ReserveMargin" in table_exist:
			cur.execute("SELECT * FROM ReserveMargin")
			A=cur.fetchall()
			if len(A)!=0:
				f.write("set " +"ReserveMargin" + " := \n")
				for row in A:
					f.write(row[0]+"   "+row[1]+" \n")
				f.write(";\n\n")

		

		cur.close()
		con.close()

class TemoaConfig( object ):
	states = (
	('mga', 'exclusive'),
	)
	
	tokens = (
		'dot_dat',
		'output',
		'scenario',
		'how_to_cite',
		'version',
		'solver',
		'keep_pyomo_lp_file',
		'saveEXCEL',
		'saveTEXTFILE',
		'mgaslack',
		'mgaiter',
		'path_to_db_io',
		'path_to_logs',
		'mgaweight'
	)
	
	t_ANY_ignore  = '[ \t]'
	
	def __init__(self, **kwargs):
		from Queue import Queue
		
		self.__error          = list()
		self.__mga_todo       = Queue()
		self.__mga_done       = Queue()
		
		self.file_location    = None
		self.dot_dat          = list() # Use Kevin's name.
		self.output           = None # May update to a list if multiple output is required.
		self.scenario         = None
		self.saveEXCEL        = False
		self.saveTEXTFILE     = False
		self.how_to_cite      = None
		self.version          = False
		self.generateSolverLP = False
		self.keepPyomoLP      = False
		self.mga              = None # mga slack value
		self.mga_iter         = None
		self.mga_weight       = None

		# To keep consistent with Kevin's argumetn parser, will be removed in the future.
		self.graph_format     = None
		self.show_capacity    = False
		self.graph_type       = 'separate_vintages'
		self.use_splines      = False

		#Introduced during UI Development
		self.path_to_db_io    = re.sub('temoa_model$', 'data_files', dirname(abspath(__file__)))# Path to where automated excel and text log folder will be save as output.
		self.path_to_logs     = self.path_to_db_io+sep+"debug_logs" #Path to where debug logs will be generated for each run. By default in debug_logs folder in db_io.
		self.path_to_lp_files = None 
		self.abort_temoa	  = False
		
		if 'd_solver' in kwargs.keys(): 
			self.solver = kwargs['d_solver']
		else:
			self.solver = None

	def __repr__(self): 
		width = 25
		spacer = '\n' + '-'*width + '\n'
		msg = spacer
		msg += '{:>{}s}: {}\n'.format('Config file', width, self.file_location)
		for i in self.dot_dat:
			if self.dot_dat.index(i) == 0:
				msg += '{:>{}s}: {}\n'.format('Input file', width, i)
			else:
				msg += '{:>25s}  {}\n'.format(' ', i)
		msg += '{:>{}s}: {}\n'.format('Output file', width, self.output)
		msg += '{:>{}s}: {}\n'.format('Scenario', width, self.scenario)	
		msg += '{:>{}s}: {}\n'.format('Spreadsheet output', width, self.saveEXCEL)
		msg += spacer
		msg += '{:>{}s}: {}\n'.format('Citation output status', width, self.how_to_cite)
		msg += '{:>{}s}: {}\n'.format('Version output status', width, self.version)
		msg += spacer
		msg += '{:>{}s}: {}\n'.format('Selected solver status', width, self.solver)
		msg += '{:>{}s}: {}\n'.format('Solver LP write status', width, self.generateSolverLP)
		msg += '{:>{}s}: {}\n'.format('Pyomo LP write status', width, self.keepPyomoLP)
		msg += spacer
		msg += '{:>{}s}: {}\n'.format('MGA slack value', width, self.mga)
		msg += '{:>{}s}: {}\n'.format('MGA # of iterations', width, self.mga_iter)
		msg += '{:>{}s}: {}\n'.format('MGA weighting method', width, self.mga_weight)
		msg += '**NOTE: If you are performing MGA runs, navigate to the DAT file and make any modifications to the MGA sets before proceeding.'
		return msg

	def t_ANY_COMMENT(self, t):
		r'\#.*'
		pass
	
	def t_dot_dat(self, t):
		r'--input[\s\=]+[-\\\/\:\.\~\w]+(\.dat|\.db|\.sqlite)\b'
		self.dot_dat.append(abspath(t.value.replace('=', ' ').split()[1]))
	
	def t_output(self, t):
		r'--output[\s\=]+[-\\\/\:\.\~\w]+(\.db|\.sqlite)\b'
		self.output = abspath(t.value.replace('=', ' ').split()[1])
	
	def t_scenario(self, t):
		r'--scenario[\s\=]+\w+\b'
		self.scenario = t.value.replace('=', ' ').split()[1]
	
	def t_saveEXCEL(self, t):
		r'--saveEXCEL\b'
		self.saveEXCEL = True
	
	def t_saveTEXTFILE(self, t):
		r'--saveTEXTFILE\b'
		self.saveTEXTFILE = True
		
	def t_path_to_db_io(self, t):
		r'--path_to_db_io[\s\=]+[-\\\/\:\.\~\w\ ]+\b'
		self.path_to_db_io = abspath(t.value.replace('=', ',').split(",")[1])
		
	def t_path_to_logs(self, t):
		r'--path_to_logs[\s\=]+[-\\\/\:\.\~\w\ ]+\b'
		self.path_to_logs = abspath(t.value.replace('=', ',').split(",")[1])
	
	def t_how_to_cite(self, t):
		r'--how_to_cite\b'
		self.how_to_cite = True

	def t_version(self, t):
		r'--version\b'
		self.version = True

	def t_solver(self, t):
		r'--solver[\s\=]+\w+\b'
		self.solver = t.value.replace('=', ' ').split()[1]
	
	def t_keep_pyomo_lp_file(self, t):
		r'--keep_pyomo_lp_file\b'
		self.keepPyomoLP = True
		
	def t_begin_mga(self, t):
		r'--mga[\s\=]+\{'
		t.lexer.push_state('mga')
		t.lexer.level = 1
	
	def t_mga_mgaslack(self, t):
		r'slack[\s\=]+[\.\d]+'
		self.mga = float(t.value.replace('=', ' ').split()[1])
		
	def t_mga_mgaiter(self, t):
		r'iteration[\s\=]+[\d]+'
		self.mga_iter = int(t.value.replace('=', ' ').split()[1])
	
	def t_mga_mgaweight(self, t):
		r'weight[\s\=]+(integer|normalized)\b'
		self.mga_weight = t.value.replace('=', ' ').split()[1]
		
	def t_mga_end(self, t):
		r'\}'
		t.lexer.pop_state()
		t.lexer.level -= 1
	
	def t_ANY_newline(self,t):
		r'\n+|(\r\n)+|\r+' # '\n' (In linux) = '\r\n' (In Windows) = '\r' (In Mac OS)
		t.lexer.lineno += len(t.value)
	
	def t_ANY_error(self, t):
		if not self.__error:
			self.__error.append({'line': [t.lineno, t.lineno], 'index': [t.lexpos, t.lexpos], 'value': t.value[0]})
		elif t.lexpos - self.__error[-1]['index'][-1] == 1:
			self.__error[-1]['line' ][-1] = t.lineno
			self.__error[-1]['index'][-1] = t.lexpos
			self.__error[-1]['value'] += t.value[0]
		else:
			self.__error.append({'line': [t.lineno, t.lineno], 'index': [t.lexpos, t.lexpos], 'value': t.value[0]})
		t.lexer.skip(1)

	def next_mga(self):
		if not self.__mga_todo.empty():
			self.__mga_done.put(self.scenario)
			self.scenario = self.__mga_todo.get()
			return True
		else:
			return False
	
	def build(self,**kwargs):
		import ply.lex as lex, os, sys
		
		db_or_dat = True # True means input file is a db file. False means input is a dat file.
		
		if 'config' in kwargs:
			if isfile(kwargs['config']):
				self.file_location= abspath(kwargs.pop('config'))
			else:
				msg = 'No such file exists: {}'.format(kwargs.pop('config'))
				raise Exception( msg )

		self.lexer = lex.lex(module=self, **kwargs)
		if self.file_location:
			with open(self.file_location, 'rb') as f:
				self.lexer.input(f.read())
			while True:
				tok = self.lexer.token()
				if not tok: break
		
		if self.__error:
			width = 25
			msg = '\nIllegal character(s) in config file:\n'
			msg += '-'*width + '\n'
			for e in self.__error:
				msg += "Line {} to {}: '{}'\n".format(e['line'][0], e['line'][1], e['value'])
			msg += '-'*width + '\n'
			sys.stderr.write(msg)
		
			try:
				txt_file = open(self.path_to_logs+os.sep+"Complete_OutputLog.log", "w")
			except BaseException as io_exc:
				sys.stderr.write("Log file cannot be opened. Please check path. Trying to find:\n"+self.path_to_logs+" folder\n")
				txt_file = open("OutputLog.log", "w")

			txt_file.write( msg )
			txt_file.close()
			self.abort_temoa = True
		
		
		if not self.dot_dat:
			raise Exception('Input file not specified.')
		
		for i in self.dot_dat:
			if not isfile(i):
				raise Exception('Cannot locate input file: {}'.format(i))
			i_name, i_ext = splitext(i)
			if (i_ext == '.dat') or (i_ext == '.txt'):
				db_or_dat = False
			elif (i_ext == '.db') or (i_ext == '.sqlite') or (i_ext == '.sqlite3') or (i_ext == 'sqlitedb'):
				db_or_dat = True
			
		if not self.output and db_or_dat:
			raise Exception('Output file not specified.')
		
		if db_or_dat and not isfile(self.output):
			raise Exception('Cannot locate output file: {}.'.format(self.output))
		
		if not self.scenario and db_or_dat:
			raise Exception('Scenario name not specified.')
		
		if self.mga_iter:
			for i in range(self.mga_iter):
				self.__mga_todo.put(self.scenario + '_mga_' + str(i))

		f = open(os.devnull, 'w'); 
		sys.stdout = f # Suppress the original DB_to_DAT.py output
		
		counter = 0
		
		for ifile in self.dot_dat:
			i_name, i_ext = splitext(ifile)
			if i_ext != '.dat':
				ofile = i_name + '.dat'
				db_2_dat(ifile, ofile, self)
				self.dot_dat[self.dot_dat.index(ifile)] = ofile
				counter += 1
		f.close()
		sys.stdout = sys.__stdout__
		if counter > 0:
			sys.stderr.write("\n{} .db DD file(s) converted\n".format(counter))