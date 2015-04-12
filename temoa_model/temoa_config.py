from temoa_lib import TemoaError
from os.path import abspath, isfile

class TemoaConfigError ( TemoaError ): pass

class TemoaConfig( object ):
	tokens = (
		'dot_dat',
		'output',
		'scenario',
		'fix_variables',
		'how_to_cite',
		'version',
		'solver',
		'generate_solver_lp_file',
		'keep_pyomo_lp_file',
		'eciu',
		'saveEXCEL',
		'mga'
	)
	
	t_ignore  = '[ \t]'
	
	def __init__(self, **kwargs):
		self.file_location    = None
		self.dot_dat          = list() # Use Kevin's name.
		self.output           = None # May update to a list if multiple output is required.
		self.scenario         = None
		self.saveEXCEL        = None
		self.how_to_cite      = None
		self.version          = False
		self.fix_variables    = None
		self.generateSolverLP = False
		self.keepPyomoLP      = False
		self.eciu             = None
		self.mga	      = None

		# To keep consistent with Kevin's argumetn parser, will be removed in the futre.
		self.graph_format     = None
		self.show_capacity    = False
		self.graph_type       = 'separate_vintages'
		self.use_splines      = False
		
		if 'd_solver' in kwargs.keys(): 
			self.solver = kwargs['d_solver']
		else:
			self.solver = None

	def __repr__(self): 
		msg = """
           Config file: {}
            Input file: {}
           Output file: {}
              Scenario: {}
    Spreadsheet output: {}

Citation output status: {}
 Version output status: {}
   Fixed variable file: {}

Selected solver status: {}
Solver LP write status: {}
 Pyomo LP write status: {}

       MGA slack value: {}
 
       Stochastic eciu: {}
		""".format(\
			self.file_location, \
			self.dot_dat, \
			self.output, \
			self.scenario, \
			self.saveEXCEL, \
			self.how_to_cite, \
			self.version, \
			self.fix_variables, \
		  	self.solver, \
			self.generateSolverLP, \
			self.keepPyomoLP, \
			self.mga, \
			self.eciu)
		return msg

	def t_COMMENT(self, t):
		r'\#.*'
		pass
	
	def t_dot_dat(self, t):
		r'--input(\s+|\=)[-\\\/\:\.\~\w]+\.dat\b|--input(\s+|\=)[-\\\/\:\.\~\w]+\.db\b'
		self.dot_dat.append(abspath(t.value.replace('=', ' ').split()[1]))
	
	def t_output(self, t):
		r'--output(\s+|\=)[-\\\/\:\.\~\w]+\.db\b'
		self.output = abspath(t.value.replace('=', ' ').split()[1])
	
	def t_scenario(self, t):
		r'--scenario(\s+|\=)\w+\b'
		self.scenario = t.value.replace('=', ' ').split()[1]
	
	def t_saveEXCEL(self, t):
		r'--saveEXCEL((\s+|\=)[-\\\/\:\.\~\w]+\.xlsx)?\b'
		if ' ' in t.value.replace('=', ' '):
			self.saveEXCEL = t.value.replace('=', ' ').split()[1]
		elif self.scenario:
			self.saveEXCEL = self.scenario + '.xlsx'
	
	def t_how_to_cite(self, t):
		r'--how_to_cite\b'
		self.how_to_cite = True

	def t_version(self, t):
		r'--version\b'
		self.version = True

	def t_fix_variables(self, t):
		r'--fix_variables(\s+|\=)[-\\\/\:\.\~\w]+\b'
		self.fix_variables = abspath(t.value.replace('=', ' ').split()[1])

	def t_solver(self, t):
		r'--solver(\s+|\=)\w+\b'
		self.solver = t.value.replace('=', ' ').split()[1]
	
	def t_generate_solver_lp_file(self, t):
		r'--generate_solver_lp_file\b'
		self.generateSolverLP = True
	
	def t_keep_pyomo_lp_file(self, t):
		r'--keep_pyomo_lp_file\b'
		self.keepPyomoLP = True
		
	def t_eciu(self, t):
		r'--eciu(\s+|\=)[-\\\/\:\.\~\w]+\b'
		self.eciu = abspath(t.value.replace('=', ' ').split()[1])
        
	def t_mga(self, t):
		r'--mga(\s+|\=)[\.\d]+'
		self.mga = float(t.value.replace('=', '').split()[1])
	
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
		
		if not self.dot_dat:
			raise TemoaConfigError('Input file not specified.')
		
		for i in self.dot_dat:
			if not isfile(i):
				raise TemoaConfigError('Cannot locate input file: {}'.format(i))
		
		if self.output is None:
			raise TemoaConfigError('Output file not specified.')
		
		if not isfile(self.output):
			raise TemoaConfigError('Cannot locate output file: {}.'.format(self.output))
		
		if not self.scenario:
			raise TemoaConfigError('Scenario name not specified.')
