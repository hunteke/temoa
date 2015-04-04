from IPython import embed as II
from temoa_lib import TemoaError
from os.path import abspath, isfile

class TemoaConfigError ( TemoaError ): pass

class TemoaConfig( object ):
	tokens = (
		'dot_dat',
		'dot_db',
		'fix_variables',
		'how_to_cite',
		'version',
		'solver',
		'generate_solver_lp_file'
		'keep_pyomo_lp_file',
		'graph_format',
		'show_capacity',
		'graph_type',
		'use_splines',
		'eciu',
		'saveEXCEL'
	)
	
	t_ignore  = '[ \t]'
	
	def __init__(self, **kwargs):
		self.file_location = None
		
		self.dot_dat = list() # Return the absolute path
		self.dot_db = list() # Return the absolute path
		self.fix_variables = None
		self.how_to_cite = None
		self.version = False
		
		if 'd_solver' in kwargs.keys(): 
			self.solver = kwargs['d_solver']
		else:
			self.solver = None
		self.generateSolverLP = False
		self.keepPyomoLP = False
		
		self.graph_format = None
		self.show_capacity = False
		self.graph_type = 'separate_vintages'
		self.splinevar = False
		
		self.eciu = None
		
		self.saveEXCEL = None
		
		
	def __repr__(self):
		msg = """
           Config file: {}
            .dat files: {}
             .db files: {}
   Fixed variable file: {}

Citation output status: {}
 Version output status: {}

Selected solver status: {}
Solver LP write status: {}
 Pyomo LP write status: {}
 Graphviz graph format: {}

Graphviz show capacity: {}
   Graphviz graph type: {}
    Graphviz splinevar: {}

       Stochastic eciu: {}
    Spreadsheet output: {}
		""".format(self.file_location, \
				   self.dot_dat, \
				   self.dot_db, \
				   self.fix_variables, \
				   self.how_to_cite, \
				   self.version, \
				   self.solver, \
				   self.generateSolverLP, \
				   self.keepPyomoLP, \
				   self.graph_format, \
				   self.show_capacity, \
				   self.graph_type, \
				   self.splinevar, \
				   self.eciu, \
				   self.saveEXCEL)
		return msg

	def t_COMMENT(self, t):
		r'\#.*'
		pass
	
	def t_dot_dat(self, t):
		r'\S+\.dat\b'  # Conservative expression of file name: r'[\\\/\:\.\w]+\.dat\b'
		self.dot_dat.append(abspath(t.value))
	
	def t_dot_db(self, t):
		r'\S+\.db\b'
		self.dot_db.append(abspath(t.value))
	
	def t_fix_variables(self, t):
		# Should we add something before '--' ?
		r'--fix_variables\=\w+\b|--fix_variables\s+\w+\b'
		self.fix_variables = t.value.replace('=', ' ').split()[1]
	
	def t_how_to_cite(self, t):
		r'[\s\n]?--how_to_cite\b'
		self.how_to_cite = True

	def t_version(self, t):
		r'[\s\n]?--version\b'
		self.version = True

	def t_solver(self, t):
		r'[\s\n]?--solver\=\w+\b|[\s\n]?--solver\s+\w+\b'
		self.solver = t.value.replace('=', ' ').split()[1]
	
	def t_generate_solver_lp_file(self, t):
		r'[\s\n]?--generate_solver_lp_file\b'
		self.generateSolverLP = True
	
	def t_keep_pyomo_lp_file(self, t):
		r'[\s\n]?--keep_pyomo_lp_file\b'
		self.keepPyomoLP = True
	
	def t_graph_format(self, t):
		r'[\s\n]?--graph_format\=\w+\b|[\s\n]?--graph_format\s+\w+\b'
		self.graph_format = t.value.replace('=', ' ').split()[1]
	
	def t_show_capacity(self, t):
		r'[\s\n]?--show_capacity\b'
		self.show_capacity = True
	
	def t_graph_type(self, t):
		r'[\s\n]?--graph_type\=explicit_vintages\b|[\s\n]?--graph_type\=separate_vintages\b|[\s\n]?--graph_type\s+explicit_vintages\b|[\s\n]?--graph_type\s+separate_vintages\b'
		self.graph_type = t.value.replace('=', ' ').split()[1]
	
	def t_use_splines(self, t):
		r'[\s\n]?--use_splines\b'
		self.splinevar = True
	
	def t_eciu(self, t):
		r'[\s\n]?--eciu\=\S+\b|[\s\n]?--eciu\s+\S+\b'
		self.eciu = t.value.replace('=', ' ').split()[1]
	
	def t_saveEXCEL(self, t):
		r'[\s\n]?--saveEXCEL\b'
		self.saveEXCEL = True
	
	def t_newline(self,t):
		r'\n+|(\r\n)+|\r+' # '\n' (In linux) = '\r\n' (In Windows) = '\r' (In Mac OS)
		t.lexer.lineno += len(t.value)
	
	def t_error(self, t):
		print "Illegal character '%s'" % t.value[0]
		t.lexer.skip(1)
	
	def build(self,**kwargs):
		from ply import lex
		if 'config' in kwargs:
			if isfile(kwargs['config']):
				self.file_location= abspath(kwargs.pop('config'))
			else:
				msg = 'No such file exist: {}'.format(kwargs.pop('config'))
				raise TemoaConfigError( msg )

		self.lexer = lex.lex(module=self, **kwargs)
		if self.file_location:
			with open(self.file_location, 'rb') as f:
				self.lexer.input(f.read())
			while True:
				tok = self.lexer.token()
				if not tok: break
	
#########################################################################

def test_TemoaConfig():
	temoa_lexer = TemoaConfig(d_solver='default_solver')
	temoa_lexer.build(config='config.cfg')
	print temoa_lexer
	print temoa_lexer.lexer.lineno

if __name__ == '__main__':
	test_TemoaConfig()