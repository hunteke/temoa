#!/usr/bin/env coopr_python

import os
import sys

from cStringIO import StringIO
from itertools import product
from pprint import pformat
from shutil import copy as copyfile, rmtree
from textwrap import TextWrapper


wrapper = TextWrapper(
  width             = 80,
  subsequent_indent = '  ',
  break_long_words  = False,
  break_on_hyphens  = False,
)
SE = sys.stderr
instance = None

node_count = 0
stringify = lambda x: ', '.join(str(i) for i in x)

class Storage ( ):
	def __str__ ( self ):
		return pformat( self.__dict__, indent=2)
	__repr__ = __str__

class Param ( object ):
	# will be common to all Parameters, so no sense in storing it N times
	stochasticset = None

	def __init__ ( self, **kwargs ):
		from coopr.pyomo.base import _ProductSet, _SetContainer

		# At the point someone is using this class, they probably know what
		# they're doing, so intentionally die at this point if any of these
		# items are not passed.  They're all mandatory.
		name   = kwargs.pop('param')   # parameter in question to modify
		spoint = kwargs.pop('spoint')  # stochastic point at which to do it
		rate   = kwargs.pop('rate')    # how much to vary the parameter

		param = getattr( instance, name ) # intentionally die if not found.
#		print param, kwargs

		indices = tuple()
		pindex = param.index()

		if isinstance( pindex, _ProductSet ):
			getname = lambda x: x.name
			indices = [ getname(i) for i in param._index_set ]
			skeys = lambda: (' '.join(str(i) for i in k) for k in self.model_keys)

			keys = param.keys()
			f = lambda: lambda x: x[pidx] == spoint
			r = lambda: lambda x: tuple(x[0:pidx] + x[pidx+1:])
			    # reduce keys to remove stochastic parameter

		elif isinstance( pindex, _SetContainer):
			indices = (param._index.name,)
			skeys = lambda: (' '.join(str(i) for i in self.model_keys) )

			keys = param.keys()
			f = lambda: lambda x: x == spoint
			r = lambda: lambda x: ()

		if Param.stochasticset not in indices:
			msg = 'Model parameter not indexed by stochastic set and therefore ' \
			      'is not a stochastic parameter as currently defined for this ' \
			      'model.'
			msg = wrapper.fill( msg )
			msg += '\n\tstochastic set: %s\n\tparameter:      %s'
			raise ValueError, msg % (Param.stochasticset, name)

		# take only the keys about which we care; i.e. /this/ spoint
		pidx = indices.index( Param.stochasticset )

		# we filter out the spoint because it's inherently known by TreeNode,
		# which "owns" /this/ Param
		model_keys = filter( f(), keys )
		my_keys    = map( r(), model_keys )

		items = dict()
		for actual, mine in zip(model_keys, my_keys):
			items[ mine ] = Storage()
			items[ mine ].value = param[ actual ].value
			items[ mine ].rate  = rate

		self.items      = items
		self.name       = name
		self.spoint     = spoint
		self.param      = param
		self.my_keys    = my_keys      # these keys are linked -- in the same
		self.model_keys = model_keys   #   order -- for zip()-ability
		self.skeys      = skeys        # for later, string keys


	def __iter__ ( self ):
		return self.items.__iter__()


	def __getitem__ ( self, i ):
		return self.items[ i ]


	def __str__ ( self ):
		x = '; '.join("(%s, %s)" % (self[i].value, self[i].rate) for i in self )
		return 'Param(%s): %s' % (self.name, x)

	__repr__ = __str__


	def as_ampl ( self, comment='' ):
		pindex = self.param.index()
		if comment:
			comment = '# Decision: %s\n\n' % str(comment)

		keys = self.skeys()
		if isinstance( keys, str ):
			keys = [ keys ]

		vals = ( str(self[i].value) for i in self.my_keys )
		data = '\n  '.join( (' '.join(i for i in v) for v in zip(keys, vals)) )
		data = 'param  %s  :=\n  %s\n\t;\n' % (self.name, data)

		return comment + data



class TreeNode ( object ):
	def __init__ ( self, *args, **kwargs ):
		# At the point someone is using this class, they probably know what
		# they're doing, so intentionally die at this point if any of these
		# items are not passed.  They're all mandatory.
		self.name   = kwargs.pop('name')      # name of /this/ node
		self.spoint = kwargs.pop('spoint')    # stochastic point of node
		self.prob   = kwargs.pop('prob')      # conditional probability of node
		bname       = kwargs.pop('filebase')  # file name minus extension
		params      = kwargs.pop('params')    # parameters to vary
		types       = kwargs.pop('types')     # names of decisions
		rates       = kwargs.pop('rates')     # rates at which to vary

		myparams = dict()
		for pp, nn in zip(params, self.name):
			paramkwargs = {
			  'param'  : pp,
			  'spoint' : self.spoint,
			  'rate'   : 1 # for "Root", default to 1 (do nothing multiplier)
			}
			if isinstance(self.name, tuple):
				# if not head node, then set rate as specified
				paramkwargs.update( rate=rates[pp][types[pp].index(nn)] )

			myparams[pp] = Param( **paramkwargs )

		self.params = myparams
		self.bname = bname
		self.children = []


	def addChild ( self, node ):
		self.children.append( node )


	def __repr__ ( self ):
		x = self.name
		if isinstance(self.name, tuple): x = ', '.join(x)
		return '%s(%s): ' % ( self.spoint, x ) + ', '.join(str(i) for i in self.params.values())

	def __str__ ( self, indent='  ', space='' ):
		x = ''.join( i.__str__(indent, space + indent) for i in self.children )

		return space + repr(self) + '\n' + x


	def write_dat_files ( self ):
		global node_count
		# Step 1: Write my own file.
		params = self.params.values()
		data = params[0].as_ampl( self.name )
		if len( params ) > 1:
			data += '\n' + '\n'.join(p.as_ampl() for p in params[1:])
		f = open( self.bname + '.dat', 'w' )
		f.write( data )
		f.close()

		node_count += 1
		inform( '\b' * (len(str(node_count -1))+1) + str(node_count) + ' ' )

		# Step 2: Tell my children to write their files
		for c in self.children:
			for p in self.params:
				cp = c.params[p]
				for key in self.params[p]:
					cp[key].value = self.params[p][key].value * cp[key].rate
			c.write_dat_files()

	def get_scenario_data ( self ):
		nodes     = [ self.bname ]
		nodestage = [( self.bname, 's' + str(self.spoint) )]
		probability = [( self.bname, self.prob )]
		scenarios = []
		children  = []

		if not self.children:
			scenarios = [ self.bname[2:] ]
		else:
			children = [ (self.bname, [c.bname for c in self.children]) ]

		for child in self.children:
			s, n, ns, c, p = child.get_scenario_data()
			scenarios   += s
			nodes       += n
			nodestage   += ns
			children    += c
			probability += p

		return scenarios, nodes, nodestage, children, probability

def write_scenario_file ( stochasticset, tree ):
	( scenarios,
	  nodes,
	  nodestage,
	  children,
	  probability,
	) = tree.get_scenario_data()

	child_fmt     = 'set  Children[%s]  :=\n  %s\n\t;\n'
	scenario_fmt  = 'Scenario%(i)s  Rs%(i)s'
	stages_fmt    = 'set  StageVariables[s%s]  :=\n  %s\n\t;'
	stagecost_fmt = 's%s StochasticPointCost[%s]'

	leaves      = '\n  '.join( scenario_fmt % {'i' : i} for i in scenarios )
	nodes       = '\n  '.join( nodes )
	nodestage   = '\n  '.join( ('   '.join(ns) for ns in nodestage) )
	scenarios   = 'Scenario%s' % '\n  Scenario'.join( scenarios )
	stagecost   = '\n  '.join( stagecost_fmt % (s, s) for s in stochasticset )
	stages      = '\n  s'.join( str(se) for se in stochasticset )

	probability = '\n  '.join(
	  ('  '.join(str(i) for i in p) for p in probability)
	)
	children    = '\n'.join(
	  child_fmt % (c[0], '\n  '.join(c[1]) )
	  for c in children
	)

	stage_var_sets = (
	  stages_fmt % (
	    se,
	    '\n  '.join(
	      sorted( 'V_FlowOut[%s,*,*,*,*,%s,*]' %
	         (se, v)
	         for v in stochasticset[:stochasticset.index( se ) +1]
	      ))
	  )

	  for se in stochasticset   # "stochastic element" = se
	)
	stage_var_sets = '\n\n'.join( stage_var_sets )

	structure = '''\
set  Stages  :=
  s%(stages)s
	;

set  Scenarios  :=
  %(scenarios)s
	;

set  Nodes  :=
  %(nodes)s
	;

%(children_sets)s

%(stage_var_sets)s

param  NodeStage  :=
  %(nodestage)s
	;

param  ConditionalProbability  :=
  %(cond_prob)s
	;

param  ScenarioLeafNode  :=
  %(leaves)s
	;

param  StageCostVariable  :=
  %(stagecost)s
	;

param  ScenarioBasedData  :=  False ;
'''

	structure %= dict(
	  stages        = stages,
	  scenarios     = scenarios,
	  nodes         = nodes,
	  children_sets = children,
	  stage_var_sets = stage_var_sets,
	  nodestage     = nodestage,
	  cond_prob     = probability,
	  leaves        = leaves,
	  stagecost     = stagecost
	)

	with open( 'ScenarioStructure.dat', 'w' ) as f:
		f.write( structure )


def _create_tree ( stochasticset, **kwargs ):
	name   = kwargs.get('name')
	types  = kwargs.get('types')
	rates  = kwargs.get('rates')
	bname  = kwargs.get('bname')
	params = kwargs.get('params')
	prob   = kwargs.get('prob')
	decision_list = kwargs.get('decisions')

	spoint = stochasticset.pop() # stochastic point, use of pop implies ordering
	treekwargs = dict(
	  spoint   = spoint,
	  name     = name,
	  types    = types,
	  rates    = rates,
	  filebase = bname,
	  params   = params,
	  prob     = prob,
	)
	node = TreeNode( **treekwargs )
	global node_count
	node_count += 1
	inform( '\b' * (len(str(node_count -1))+1) + str(node_count) + ' ' )

	if stochasticset:
		decisions = enumerate( decision_list )
		prob = 1.0 / len(decision_list)
		bname = '%ss%%d' % bname  # the format for the basename of the file
		for enum, d in decisions:
			kwargs.update(
			  name  = d,
			  bname = bname % enum,
			  prob  = prob,
			)
			node.addChild( _create_tree(stochasticset[:], **kwargs) )

	return node


def create_tree ( stochasticset, opts ):
	types  = opts.types
	rates  = opts.rates
	params = opts.params
	prob   = 1

	if params is None:
		msg = 'Must specify at least one stochastic parameter to vary.'
		raise ValueError, msg

	if None in (types, rates):
		msg = 'Must specify both the stochastic decision names (types=) and '   \
		   'rates (rates=)'
		raise ValueError, msg

	tkeys = sorted( types.keys() )
	rkeys = sorted( rates.keys() )
	if len(tkeys) != len(rkeys):
		msg = 'types and rates keys lengths do not match.  Are you missing a '  \
		   'a type or rate?\n\ttypes: %s\n\trates: %s'
		types = stringify( types )
		rates = stringify( rates )
		raise ValueError, msg % ( types, rates )


	for key, rkey in zip( tkeys, rkeys ):
		if key != rkey:
			msg = 'Missing a parameter rate or type argument.\n'                 \
			      '  type params: %s\n  rate params: %s'
			raise ValueError, msg % ( stringify(tkeys), stringify(rkeys) )

		if len( types[key] ) != len( rates[key] ):
			msg = "Missing a type name or rate value for '%s'.\n"                \
			      '  names: %s\n  rates: %s'
			names  = stringify( types[key] )
			values = stringify( rates[key] )
			raise ValueError, msg % ( key, names, values )

		for i in rates[key]:
			if not isinstance(i, (int, long, float)):
				msg = 'rates argument must be a list of rates (numbers)\n'        \
				      "  Offending item: '%s' (is %s)\n  rates list: %s"
				rates = stringify( rates[r] )
				raise ValueError, msg % ( i, type(i), rates[r] )

	stochasticset.reverse()

	decisions = [ types[i] for i in sorted(types.keys()) ]
	params.sort()
	kwargs = dict(
	  name      = 'Root',
	  bname     = 'R',
	  types     = types,
	  rates     = rates,
	  params    = params,
	  decisions = [ i for i in product( *decisions ) ],
	  prob      = 1,  # conditional probability, but root guaranteed to occur
	)
	return _create_tree( stochasticset, **kwargs )


def inform ( x ):
	global verbose
	if verbose:
		SE.write( x )
		SE.flush()


def setup_directory ( dname, force ):
	if os.path.exists( dname ):
		if os.path.isdir( dname ):
			files = os.listdir( dname )
			if files and not force:
				msg = 'Not empty: %s\n\nIf you want to use this directory anyway,'\
				   ' use the --force flag.'
				raise Warning, msg % dname

			# would be potentially useful to put this into a thread to speed up
			# the process.  like 'mv somedir to_del; rm -rf to_del &'
			rmtree( dname )
			os.mkdir( dname )
		else:
			msg = 'Error - already exists: %s'
			raise NameError, msg % dname
	else:
		os.mkdir( dname )




def test_model_parameters ( M, opts ):
	try:
		getattr(M, opts.stochasticset)
	except:
		msg = ('Whoops!  The stochastic set is not available from the model.  '
		   'Did you perhaps typo the name?\n'
		   '  Model name: %s\n'
		   '  Stochastic name: %s')
		raise ValueError, msg % (M.name, opts.stochasticset)

	try:
		for pname in opts.params:
			param = getattr(M, pname)
	except:
		msg = 'Whoops!  Parameter not available from the model.  Have you '     \
		   'perhaps typoed the name?\n'                                         \
		   '  Model name: %s\n'                                                 \
		   '  Parameter name: %s'
		raise ValueError, msg %(M.name, pname)


def parse_options ( ):
	from optparse import OptionParser, OptionGroup
	from os import path

	parser = OptionParser()
	parser.usage = ('%prog \\\n'
	   '\t--dirname=<run_name> \\\n'
	   '\t--model=<../path/to/model/file> \\\n'
	   '\t--dotdat=<../path/to/dot/dat/file> \\\n'
	   '\t--stochasticset=<model_stochastic_set> \\\n'
	   '\t--params=<parameters_to_vary> \\\n'
	   '\t--stage-types=<stage_types> \\\n'
	   '\t--stage-rates=<stage_varying_rates> \\\n'
	   '\t[options]')

	mopts = OptionGroup( parser, 'Model Arguments')
	opts  = OptionGroup( parser, 'Stochastic Arguments')
	dbg   = OptionGroup( parser, 'Debugging Arguments')
	parser.add_option_group( mopts )
	parser.add_option_group( opts )
	parser.add_option_group( dbg )

	mopts.add_option('-d','--dotdat',
	  help='Path to the AMPL data file to use as a basis for stochastics',
	  action='store',
	  dest='dotdatpath',
	  type='string')
	mopts.add_option('-m','--model',
	  help='Path to the Pyomo model file to use as a basis for stochastics',
	  action='store',
	  dest='modelpath',
	  type='string')
	mopts.add_option('-s','--stochasticset',
	  help='The model stochastic (decision) points set.  In many models, this '
	     'is a set of time periods.',
	  action='store',
	  dest='stochasticset',
	  type='string')

	opts.add_option('-f','--force',
	  help='If a subdirectory conflicts with --name, then this option directs '
	     'the script to remove all files in it and use it anyway.',
	  action='store_true',
	  dest='force',)
	opts.add_option('-n','--dirname',
	  help='Name of a working directory for the output files.  This script '
	     'will create (or use, if empty) a subdirectory by this name.',
	  action='store',
	  dest='dirname',
	  type='string')
	opts.add_option('-p','--params',
	  help='Comma separated list of model parameters to vary at each '
	       'stochastic stage (period).  Example: power_dmd,co2_tot',
	  action='store',
	  dest='params',
	  type='string')
	opts.add_option('-r','--stage-rates',
	  help='Comma separated list of rate values for each stochastic variable '
	       'at each stages (specified with the --stage-types).  A stage rate '
	       'must be specified for each item in --params.  Example: '
	       'power_dmd:0.85,1.00,1.15',
	  action='append',
	  dest='rates',
	  type='string')
	opts.add_option('-t','--stage-types',
	  help='Comma separated list of stochastic stage types (names) for each '
	       'stochastic variable.  These are the "decision" possibilities of '
	       'the scenario tree.  Stage_types need to be specified for each '
	       'item in --params.  Example: power_dmd:Low,Med,High',
	  action='append',
	  dest='types',
	  type='string')

	dbg.add_option('--debug',
	help='Help with debugging of this script.  Generally only the script '
	     'developers will use this option.',
	  action='store_false'
	)
	dbg.add_option('-q','--quiet',
	  help='Turn off informational messages.',
	  action='store_false',
	  dest='verbose',
	  default=True
	)

	popts, args = parser.parse_args( sys.argv[1:] )
	o = {}

	if not popts.modelpath:
		parser.print_usage()
		raise ValueError, 'Required: -m or --model is a required argument'
	elif not os.path.exists( popts.modelpath ):
		raise ValueError, "Error: model not found: %s" % popts.modelpath

	if not popts.dotdatpath:
		parser.print_usage()
		raise ValueError, 'Required: -d or --dotdatpath is a required argument'
	elif not os.path.exists( popts.dotdatpath ):
		raise ValueError, "Error: data file not found: %s" % popts.dotdatpath

	if not popts.stochasticset:
		parser.print_usage()
		raise ValueError, 'Required: -s or --stochasticset is a required argument'

	if not popts.dirname:
		parser.print_usage()
		raise ValueError, 'Required: -n or --dirname is a required argument'

	if not popts.params:
		parser.print_usage()
		raise ValueError, 'Required: -p or --params is a required argument'
	popts.params = [str(i) for i in popts.params.split(',')]

	if None in ( popts.rates, popts.types ) and popts.rates != popts.types:
		msg = 'Required: stage-rates and stage-types are required arguments'
		raise ValueError, msg

	rates = types = ''
	if popts.rates:
		try:
			rates = dict()
			for r in popts.rates:
				i = 'Model Param(%s)' % r # clear i in case the colon split fails
				key, vals = r.split(':')
				rates[ key ] = [ float(i) for i in vals.split(',') ]
			popts.rates = rates
		except ValueError, e:
			msg = ('stage-rates must be a parameter followed by a list of '
			   'numbers.  Did you use a colon to specify the model parameter '
			   '(i.e. param:n1,n2,...)?\n'
			   '  Specified list: %s')
			raise ValueError, msg % r

	if popts.types:
		types = dict()
		try:
			for t in popts.types:
				i = 'Model Param(%s)' % t  # clear i in case the colon split fails
				key, vals = t.split(':')
				types[ key ] = [ str(i) for i in vals.split(',') ]
			popts.types = types
		except ValueError, e:
			msg = ('stage-types must be a list of names.  Did you use a colon '
			   'to specify the model parameter (i.e. param:n1,n2,...)?\n'
			   '  Specified list: %s')
			raise ValueError, msg % t

	if len(popts.types) != len(popts.rates):
			msg = ('The stage-rates and stage-types options need the same number '
			   'of items.\n'
			   '  stage-rates params: (count: %d) %s\n'
			   '  stage-types params: (count: %d) %s')
			data = [ len(popts.rates), stringify( sorted( popts.rates )) ]
			data.extend( [len(popts.types), stringify( sorted( popts.types ))] )
			msg %= tuple(data)
			raise ValueError, msg

	for key in popts.params:
		if len(popts.types[ key ]) != len(popts.rates[ key ]):
			msg = ('Extra or missing values from stage rates and types argument.\n'
				'  type %(name)s: %(t)s\n'
			   '  rate %(name)s: %(r)s')
			data = dict(
			  name=key,
			  t=stringify(popts.types[ key ]),
			  r=stringify(popts.rates[ key ])
			)
			raise ValueError, msg % data

	global verbose
	verbose = popts.verbose

	return popts, args


def main ( ):
	from os import getcwd
	from time import clock

	opts, args = parse_options()

	cwd = getcwd()

	begin = clock()
	duration = lambda: clock() - begin

	inform( '[      ] Setting up working directory (%s)' % opts.dirname )
	setup_directory( opts.dirname, opts.force )
	inform( '\r[%6.2f\n' % duration() )

	inform( '[      ] Import model definition (%s)' % opts.modelpath )
	mp = opts.modelpath
	modelbase = os.path.basename(mp)[:-3]
	modeldir  = os.path.abspath( os.path.dirname( mp ))

	sys.path.insert(0, modeldir)
	_temp = __import__(modelbase, globals(), locals(), ('model',))
	M = _temp.model
	del _temp
	sys.path.pop(0)

	test_model_parameters( M, opts )

	inform( '\r[%6.2f\n' % duration() )

	inform( '[      ] Create concrete instance (%s)' % opts.dotdatpath )
	ins = M.create( opts.dotdatpath )
	inform( '\r[%6.2f\n' % duration() )

	global instance
	instance = ins

	inform( '[      ] Collecting stochastic points from model (%s)' % M.name )
	spoints = sorted( getattr(ins, opts.stochasticset).value )
	inform( '\r[%6.2f\n' % duration() )

	  # used for friendlier error checking
	Param.stochasticset = opts.stochasticset

	os.chdir( opts.dirname )
	inform( '[      ] Building tree:                          ')
	tree = create_tree( spoints[:], opts )  # give an intentional copy
	inform( '\r[%6.2f\n' % duration() )

	global node_count
	node_count = 0

	inform( '[      ] Writing scenario "dot dat" files:       ')
	tree.write_dat_files()
	write_scenario_file( spoints, tree )
	inform( '\r[%6.2f] Writing scenario "dot dat" files\n' % duration() )

	os.chdir( cwd )
	inform( '[      ] Copying ReferenceModel.dat as scenario tree root' )
	copyfile( opts.dotdatpath, '%s/R.dat' % opts.dirname)
	inform( '\r[%6.2f\n' % duration() )


if '__main__' == __name__:
	try:
		if 1 == len(sys.argv):
			sys.argv.append( '--help' )
		main()
	except Exception, e:
		if '--debug' in sys.argv:
			raise

		msg = 'If you need more verbose (potentially helpful) information '   \
		      'about this error, you can run this program again, and add the' \
		      ' "--debug" command line flag.'
		msg = '\n\n' + str(e) + '\n\n' + wrapper.fill(msg) + '\n'
		SE.write(msg)
