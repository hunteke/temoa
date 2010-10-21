#!/usr/bin/env python

#sys.argv = sys.argv[:1]
#import IPython; IPython.Shell.IPShellEmbed()()

from itertools import product
from optparse import OptionParser, OptionGroup
import os
from pprint import pformat
import random
from shutil import copy as copyfile
import sys
from textwrap import TextWrapper

wrapper = TextWrapper(
  width             = 80,
  subsequent_indent = '  ',
  break_long_words  = False,
  break_on_hyphens  = False,
)
SE = sys.stderr.write
instance = None

stringify = lambda x: ', '.join(str(i) for i in x)

class Storage ( ):
	def __str__ ( self ):
		return pformat( self.__dict__, indent=2)
	__repr__ = __str__

class Param ( object ):

	def __init__ ( self, **kwargs ):
		from coopr.pyomo.base import _ProductSet, _SetContainer

		name   = kwargs.pop('param')
		period = kwargs.pop('period')
		rate   = kwargs.pop('rate')

		param = getattr( instance, name ) # intentionally die if not found.

		indices = ()
		pindex = param.index()


		if isinstance( pindex, _ProductSet ):
			getname = lambda x: x.name
			indices = [ getname(i) for i in param._index_set ]
			skeys = lambda: (' '.join(str(i) for i in k) for k in self.model_keys)

			keys = param.keys()
			f = lambda: lambda x: x[pidx] == period
			r = lambda: lambda x: tuple(x[0:pidx] + x[pidx+1:])
			    # reduce keys to remove period

		elif isinstance( pindex, _SetContainer):
			indices = (param._index.name,)
			skeys = lambda: (' '.join(str(i) for i in self.model_keys) )

			keys = param.keys()
			f = lambda: lambda x: x == period
			r = lambda: lambda x: ()

		#if isinstance(param.index(), dict)

		if 'operating_period' not in indices:
			msg = "Model parameter '%s' does not have a period index.  It is"    \
			      ' therefore not a stochastic parameter as currently defined'   \
			      ' for this model.'
			raise KeyError, msg % name

		# take only the keys about which we care; i.e. /this/ period
		pidx = indices.index('operating_period')

		# we filter out the period because it's inherently known by TreeNode,
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
		self.period     = period
		self.param      = param
		self.my_keys    = my_keys      # these keys are linked, in the same
		self.model_keys = model_keys   #   order, so can use zip()
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
		self.name   = kwargs.pop('name')     # intentionally die if not passed
		self.period = kwargs.pop('period')   # intentionally die if not passed
		self.prob   = kwargs.pop('prob')     # intentionally die if not passed
		bname       = kwargs.pop('filebase') # intentionally die if not passed
		params      = kwargs.pop('params')   # intentionally die if not passed
		types       = kwargs.pop('types')    # intentionally die if not passed
		rates       = kwargs.pop('rates')    # intentionally die if not passed

		myparams = dict()
		for p, n in zip(params, self.name):
			paramkwargs = {
			  'param'  : p,
			  'period' : self.period,
			  'rate'   : 1 # for "Root", default to 1 (do nothing multiplier)
			}
			if isinstance(self.name, tuple):
				# if not head node, then set rate as specified
				paramkwargs.update( rate=rates[p][types[p].index(n)] )

			myparams[p] = Param( **paramkwargs )

		self.params = myparams
		self.bname = bname
		self.children = []


	def addChild ( self, node ):
		self.children.append( node )


	def __repr__ ( self ):
		x = self.name
		if isinstance(self.name, tuple): x = ', '.join(x)
		return '%s(%s)' % ( self.period, x ) + ': ' + ', '.join(str(i) for i in self.params.values())

	def __str__ ( self, indent='  ', space='' ):
		x = ''.join( i.__str__(indent, space + indent) for i in self.children )

		return space + repr(self) + '\n' + x


	def write_dat_files ( self ):
		# Step 1: Write my own file.
		params = self.params.values()
		data = params[0].as_ampl( self.name )
		if len( params ) > 1:
			data += '\n' + '\n'.join(p.as_ampl() for p in params[1:])
		f = open( self.bname + '.dat', 'w' )
		f.write( data )
		f.close()
		inform('.')

		# Step 2: Tell my children to write their files
		for c in self.children:
			for p in self.params:
				cp = c.params[p]
				for key in self.params[p]:
					cp[key].value = self.params[p][key].value * cp[key].rate
			c.write_dat_files()

	def get_scenario_data ( self ):
		nodes     = [ self.bname ]
		nodestage = [( self.bname, 'p' + str(self.period) )]
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

def write_scenario_file ( periods, tree ):
	( scenarios,
	  nodes,
	  nodestage,
	  children,
	  probability,
	) = tree.get_scenario_data()

	x = 'set  Stages  :=  p%s ;\n' % ' p'.join( str(i) for i in periods )
	print x

	x = '\n  Scenario'.join( scenarios )
	x = 'set  Scenarios  :=\n  Scenario%s\n\t;\n' % x
	print x

	x = '\n  '.join( nodes )
	x = 'set  Nodes  :=\n  %s\n\t;\n' % x
	print x

	x = '\n  '.join( ('   '.join(ns) for ns in nodestage) )
	x = 'param  NodeStage  :=\n  %s\n\t;\n' % x
	print x

	x = '\n  '.join( ('  '.join(str(i) for i in p) for p in probability) )
	x = 'param  ConditionalProbability  :=\n  %s\n\t;\n' % x
	print x

	for c in children:
		x = '\n  '.join( c[1] )
		x = 'set  Children[%s]  :=\n  %s\n\t;\n' % (c[0], x )
		print x

	x = '\n  '.join( 'Scenario%(i)s  Rs%(i)s' % {'i':i} for i in scenarios )
	x = 'param  ScenarioLeafNode  :=\n  %s\n\t;\n' % x
	print x

	x = '\n  '.join( 'p%s PeriodCost[%s]' % (p, p) for p in periods )
	x = 'param  StageCostVariable  :=\n  %s\n\t;\n' % x
	print x

	for p in periods:
		x = ' '.join('xu[*,%s,%s]' %(v, p) for v in periods[:periods.index(p)+1])
		x = 'xc[*,%s] %s' % (p, x)
		x = 'set  StageVariables[p%s]  :=  %s ;' % (p, x)
		print wrapper.fill(x)

	print '\nparam ScenarioBasedData := False ;'

def _create_tree ( periods, **kwargs ):
	name   = kwargs.get('name')
	types  = kwargs.get('types')
	rates  = kwargs.get('rates')
	bname  = kwargs.get('bname')
	params = kwargs.get('params')
	prob   = kwargs.get('prob')
	decision_list = kwargs.get('decisions')

	p = periods.pop()

	treekwargs = {
	  'period'   : p,
	  'name'     : name,
	  'types'    : types,
	  'rates'    : rates,
	  'filebase' : bname,
	  'params'   : params,
	  'prob'     : prob,
	}
	node = TreeNode( **treekwargs )
	inform('.')

	if periods:
		decisions = enumerate( decision_list )
		prob = 1.0 / len(decision_list)
		bname = '%ss%%d' % bname  # the format for the basename of the file
		for enum, d in decisions:
			kwargs.update(
			  name  = d,
			  bname = bname % enum,
			  prob  = prob,
			)
			node.addChild( _create_tree(periods[:], **kwargs) )

	return node


def create_tree ( periods, **kwargs ):
	name   = kwargs.pop('name', 'Root')
	bname  = kwargs.pop('bname', 'R')
	types  = kwargs.pop('types', None )
	rates  = kwargs.pop('rates', None )
	params = kwargs.pop('params', None)
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
		msg = 'types and rates keys iterable lengths do not match.\n'           \
		      '  types: %s\n  rates: %s'
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

	periods.sort()
	periods.reverse()

	decisions = [ types[i] for i in sorted(types.keys()) ]
	params.sort()
	kwargs.update(
	  name      = name,
	  bname     = bname,
	  types     = types,
	  rates     = rates,
	  params    = params,
	  decisions = [ i for i in product( *decisions ) ],
	  prob      = 1,  # conditional probability, but root guaranteed to occur
	)
	return _create_tree( periods, **kwargs )


def inform ( x='done.\n' ):
	global verbose
	if verbose:
		SE( x )


def main ( ):
	options, args = parse_options()

	inform('Import model definition from ReferenceModel: ')
	sys.path.insert(0, '../models')
	from ReferenceModel import model as M
	sys.path.remove('../models')
	inform()

	inform('Create concrete instance from ReferenceModel.dat: ')
	ins = M.create('ReferenceModel.dat')
	inform()

	global instance
	instance = ins

	inform('Collecting stochastic points (periods) from the model: ')
	periods = list( ins.operating_period.value )
	inform()

	inform('Building tree: ')
	tree = create_tree( periods[:], **options )
	inform()

	inform('Writing scenario "dot dat" files: ')
	tree.write_dat_files()
	write_scenario_file( periods, tree )
	inform()

	inform('Copying ReferenceModel.dat to R.dat (the scenario tree root): ')
	copyfile('ReferenceModel.dat', 'R.dat')
	inform()


def parse_options ( ):
	parser = OptionParser()
	parser.usage = '%prog --params=<stochastic_parameters> [options]'

	opts = OptionGroup( parser, 'Stochastic Options')
	dbg  = OptionGroup( parser, 'Debugging Options')
	parser.add_option_group( opts )
	parser.add_option_group( dbg )

	opts.add_option('--params',
	  help='Comma separated list of model parameters to vary at each '         \
	       'stochastic stage (period).  Example: power_dmd,co2_tot',
	  action='store',
	  dest='params',
	  type='string')
	opts.add_option('--stage-rates',
	  help='Comma separated list of rate values for each stochastic variable ' \
	       'at each stages (specified with the --stage-types).  A stage rate ' \
	       'must be specified for each item in --params.  Example: '           \
	       'power_dmd:0.85,1.00,1.15',
	  action='append',
	  dest='rates',
	  type='string')
	opts.add_option('--stage-types',
	  help='Comma separated list of stochastic stage types (names) for each '  \
	       'stochastic variable.  These are the "decision" possibilities of '  \
	       'the scenario tree.  Stage_types need to be specified for each '    \
	       'item in --params.  Example: power_dmd:Low,Med,High',
	  action='append',
	  dest='types',
	  type='string')

	dbg.add_option('--debug',
	help='Help with debugging of this script.  Generally only the script '     \
	     'developrs will use this option.',
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

	if popts.params:
		o.update( params=[str(i) for i in popts.params.split(',')] )
	else:
		parser.print_usage()
		raise ValueError, 'params is a required parameter'

	if None in ( popts.rates, popts.types ) and popts.rates != popts.types:
		msg = 'stage-rates and stage-types are required parameters'
		raise ValueError, msg

	rates = types = ''
	if popts.rates:
		try:
			rates = dict()
			for r in popts.rates:
				i = 'Model Param(%s)' % r # clear i in case the colon split fails
				key, vals = r.split(':')
				rates[ key ] = [ float(i) for i in vals.split(',') ]
			o.update( rates=rates )
		except ValueError, e:
			msg = 'stage-rates must be a list of numbers.  Did you use a colon\n'\
			      'to specify the model parameter (i.e. param:n1,n2,...)?\n'     \
			      '  Offending item: %s\n  Specified list: %s'
			msg %= ( i, r )
			raise ValueError, msg

	if popts.types:
		types = dict()
		try:
			for t in popts.types:
				i = 'Model Param(%s)' % t  # clear i in case the colon split fails
				key, vals = t.split(':')
				types[ key ] = [ str(i) for i in vals.split(',') ]
			o.update( types=types )
		except ValueError, e:
			msg = 'stage-types must be a list of names.  Did you use a colon\n'  \
			      'to specify the model parameter (i.e. param:n1,n2,...)?\n'     \
			      '  Offending item: %s\n  Specified list: %s'
			msg %= ( i, t )
			raise ValueError, msg

	if len(types) != len(rates):
			msg = 'The stage-rates and stage-types options need the same number' \
			      ' of items\n' \
			      '  stage-rates: (count: %d) %s\n  stage-types: (count: %d) %s'
			data = [ len(rates), stringify( rates ) ]
			data.extend( [len(types), stringify( types )] )
			msg %= tuple(data)
			raise ValueError, msg

	global verbose
	verbose = popts.verbose

	return o, args


if '__main__' == __name__:
	try:
		# Needed to make the #! line (first line) portable.

		# test if coopr is on path (or otherwise importable) by importing a
		# small item from a known location.  Probably not the best, but I don't
		# know of a better way to test.
		from coopr.pyomo.io.cpxlp import convert_name
	except:
		msg = """\
Unable to find coopr.pyomo on the Python system path.  Are you running Coopr's
version of Python?  Here are two ways to check:

  # should return the python binary located inside the Coopr directory
$ which python

  # look for items that have to do with the Coopr project
$ python -c "import sys; from pprint import pprint as P; P(sys.path)"

If you aren't running with Coopr's environment for Python, you'll need to either
update your PATH environment variable use Coopr's Python setup, or always
explicitly use the path:

Option 1:
$ PATH=/path/to/coopr/bin:$PATH
$ which python

Option 2:
$ /path/to/coopr/bin/python  %s  ...
""" % os.path.basename( sys.argv[0] )

		raise SystemExit, msg

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
		SE(msg)
