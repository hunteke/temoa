#!/usr/bin/env python

# {Generated_Script_Warning}

import sys

SE = sys.stderr

if sys.version_info < (2, 7):
	msg = 'Temoa requires Python v2.7.'
	msg += '\n\nPress Enter to quit installation.'
	raw_input( msg )
	raise AssertionError( 'Incompatible Python version detected.' )

if not hasattr(sys, 'getwindowsversion'):
	msg = ('This installer for TEMOA is meant for Windows.  Please either '
	   'update your Python installation to at least v2.7, or download the '
	   'appropriate TEMOA installer.\n')
	SE.write( msg )

	raise AssertionError( 'Unable to determine that OS is Windows.' )

import os
from subprocess import check_call
from zlib import decompress as gzdecompress
from bz2  import decompress as bzdecompress
from base64 import decodestring

userdir = os.environ['USERPROFILE']

try:
	from _winreg import ( OpenKey, CloseKey, QueryValueEx, SetValueEx,
	   HKEY_CURRENT_USER, KEY_ALL_ACCESS, REG_EXPAND_SZ )
except ImportError, e:
	msg = ('Unable to import the Windows registry.\n\n'
	   'Unable to set up environment path for Python, Coopr, and GLPK.'
	   '\n\nPress Enter to quit installation script.')
	raw_input( msg )
	raise

def no_uncompress ( data ): return data

uncompress_scheme = dict(
  gz   = gzdecompress,
  bz   = bzdecompress,
  none = no_uncompress,
)

glpk_dll_uncompress = '{glpk_dll_type}'
glpk_dll_name = '{glpk_dll_name}'
glpk_dll_data = '''\\\n{glpk_dll_data}'''

glpk_exe_uncompress = '{glpk_exe_type}'
glpk_exe_data = '''\\\n{glpk_exe_data}'''

temoa_uncompress = '{temoa_type}'
temoa_data = '''\\\n{temoa_data}'''


python_root = os.path.dirname( sys.executable )

# 1. We install GLPK first because it also alerts us to non-administra

user_programs = os.path.join( userdir, 'Programs' )
glpk_dir      = os.path.join( user_programs, 'GLPK' )
glpk_exe_path = os.path.join( glpk_dir, 'glpsol.exe' )
glpk_dll_path = os.path.join( glpk_dir, glpk_dll_name )
temoa_path    = os.path.join( userdir, 'Desktop', 'temoa.py' )


easy_install_executable = os.path.join( python_root, 'Scripts', 'easy_install.exe' )
coopr_python_executable = os.path.join( python_root, 'Scripts', 'coopr_python.exe' )
if not os.path.exists( coopr_python_executable ):
	if not os.path.exists( easy_install_executable ):
		msg = ('\neasy_install not found.  Have you installed SetupTools?\n\n'
		   'SetupTools is a Python module that aids in distribution of various '
		   'Python projects.  This installer uses it to install Coopr.  At this '
		   "time, this installer is not aware of Coopr on your system, so you'll "
		   'either need to manually install Coopr, or install SetupTools and rerun '
		   'this install script.\n\n'
		   ' SetupTools: http://pypi.python.org/pypi/setuptools\n'
		   ' Coopr:      https://software.sandia.gov/coopr/\n')
		SE.write( msg )
	else:
		msg = ('Coopr not found.  Attempting to install with Easy Install\n\n')
		SE.write( msg )

		try:
			check_call( ( easy_install_executable, '-U', 'coopr' ) )
		except Exception, e:
			msg = '\n\nWhoops!  Error while installing Coopr:\n\n'
			msg += e.strerror + '\n\nPress enter to quit installation.'
			raw_input( msg )
			raise

# Installing GLPK second, mainly so the message is visible while the script
# waits for the user to hit Enter.
if not (os.path.exists( glpk_dir ) and os.path.exists( glpk_exe_path ) ):
	try:
		os.makedirs( glpk_dir, 0755 )
	except WindowsError, e:
		# The only error condition that breeds well is if the directory already
		# exists.  If it doesn't, something else has gone wrong so spit it back
		# to the user to solve.
		if not 'exists' in e.strerror:
			msg = "\nWhoops!  Error installing GLPK to '{{}}':\n\n"
			msg += e.strerror + '\n\nPress return to quit installation.\n'
			raw_input( msg.format( glpk_dir ))
			raise


	SE.write( "\n\nInstalling GLPK to '{{}}'.\n\n".format( glpk_dir ) )
	with open( glpk_exe_path, 'wb' ) as f:
		decompress = uncompress_scheme[ glpk_exe_uncompress ]
		f.write( decompress( decodestring( glpk_exe_data )))
	with open( glpk_dll_path, 'wb' ) as f:
		decompress = uncompress_scheme[ glpk_dll_uncompress ]
		f.write( decompress( decodestring( glpk_dll_data )))


with open( temoa_path, 'wb' ) as f:
	decompress = uncompress_scheme[ temoa_uncompress ]
	f.write( decompress( decodestring( temoa_data )))


try:
	WinEnvKey = r'Environment'
	key = OpenKey( HKEY_CURRENT_USER, WinEnvKey, 0, KEY_ALL_ACCESS )
	winpath, reg_type = QueryValueEx( key, 'Path' )
except WindowsError, e:
	if 'cannot find the file specified' not in e.strerror:
		msg = ('Whoops!  Error while modifying the user PATH environment '
			'variable:\n\n')
		msg += e.strerror + '\n\nPress Enter to quit installation.'
		raw_input( msg )
		raise

	winpath = ''

el_to_add = []
if 'glpk' not in winpath.lower():
	el_to_add.append( glpk_dir )

if 'python' not in winpath.lower():
	el_to_add.append( python_root )
	el_to_add.append( os.path.join( python_root, 'Scripts' ))

if el_to_add:
	path_elements = winpath and winpath.split(';') or list()
	path_elements.extend( el_to_add )
	try:
		SetValueEx( key, 'Path', 0, REG_EXPAND_SZ, ';'.join( path_elements ) )
	except Exception, e:
		msg = ('Unknown error while modifying the user PATH environment variable:'
		   '\n\n')
		msg += e.strerr + '\n\nPress Enter to quit installation.'
		raw_input( msg )
		raise

CloseKey(key)

msg = 'Installation complete.  The temoa.py model file is now on your Desktop.'

if el_to_add:
	msg += '''

Your user PATH environment variable has been augmented:

 {{elements}}

To propogate this change, please logoff and then back on.  (Alternatively, you
may restart your computer as well.)
'''.format( elements='\n '.join(el_to_add) )

msg += '\n\nPress enter to close this Window.'
raw_input( msg )