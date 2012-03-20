#!/usr/bin/env python

import platform, os, sys, shutil

from glob import glob
from subprocess import check_call
from tempfile import mkdtemp
from time import sleep

SE = sys.stderr

from IPython import embed as II

if sys.argv[1] != 'WinXP':
	SE.write( "Not WinXP\n" )
	# Seems silly, but a sanity check/reminder to whoever runs this.  For this
	# first cut of this script, the logic is rather specifically geared toward
	# Windows XP.
	raise SystemExit

script_name = 'InstallTemoa_{}.py'.format( sys.argv[1] )

SE.write( 'Incorporating GLPK and TEMOA into script . . .' )
SE.flush()
from zlib import compress as gzcompress
from bz2 import compress as bzcompress
from base64 import encodestring

glpk_dll_name = glob('glpk*.dll')[0]
glpk_dll_data = open( glpk_dll_name, 'rb' ).read()
glpk_exe_data = open( 'glpsol.exe', 'rb' ).read()
temoa_data    = open( 'temoa.py', 'rb' ).read()

def smallest_compression ( data ):
	smallest = encodestring( data )
	current = len( smallest )
	compress_type = 'none'
	for i in xrange( 1, 10 ):
		bz = encodestring( bzcompress( data ))
		gz = encodestring( gzcompress( data ))
		if len( bz ) < current:
			current = len( bz )
			smallest = bz
			compress_type = 'bz'
		if len( gz ) < current:
			current = len( gz )
			smallest = gz
			compress_type = 'gz'
	return smallest, compress_type

glpk_dll_data, glpk_dll_type = smallest_compression( glpk_dll_data )
glpk_exe_data, glpk_exe_type = smallest_compression( glpk_exe_data )
temoa_data, temoa_type = smallest_compression( temoa_data )

SE.write( ' done.\n' )
SE.flush()


install_script = '''\
#!/usr/bin/env python

import sys

SE = sys.stderr

if not hasattr(sys, 'getwindowsversion'):
	msg = ('This installer for TEMOA is meant for Windows.  Please either '
	   'update your Python installation to at least v2.7, or download the '
	   'appropriate TEMOA installer.\\n')
	SE.write( msg )

	raise AssertionError( 'Unable to determine that OS is Windows.' )

import os
from subprocess import check_call
from zlib import decompress as gzdecompress
from bz2  import decompress as bzdecompress
from base64 import decodestring

try:
	from _winreg import ( OpenKey, CloseKey, QueryValueEx, SetValueEx,
	   HKEY_LOCAL_MACHINE, KEY_ALL_ACCESS )
except ImportError:
	msg = ('Unable to import the Windows registry: Unable to set up environment '
	   'path for Python, Coopr, and GLPK\\n')
	SE.write( msg )
	raise

def no_uncompress ( data ): return data

uncompress_scheme = dict(
  gz   = gzdecompress,
  bz   = bzdecompress,
  none = no_uncompress,
)

glpk_dll_uncompress = '{glpk_dll_type}'
glpk_dll_name = '{glpk_dll_name}'
glpk_dll_data = '\''\\\n{glpk_dll_data}'\''

glpk_exe_uncompress = '{glpk_exe_type}'
glpk_exe_data = '\''\\\n{glpk_exe_data}'\''

temoa_uncompress = '{temoa_type}'
temoa_data = '\''\\\n{temoa_data}'\''


python_root = os.path.dirname( sys.executable )

easy_install_executable = os.path.join( python_root, 'Scripts', 'easy_install.exe' )
coopr_python_executable = os.path.join( python_root, 'Scripts', 'coopr_python.exe' )
if not os.path.exists( coopr_python_executable ):
	if not os.path.exists( easy_install_executable ):
		msg = ('\\neasy_install not found.  Have you installed SetupTools?\\n\\n'
		   'SetupTools is a Python module that aids in distribution of various '
		   'Python projects.  This installer uses it to install Coopr.  At this '
		   "time, this installer is not aware of Coopr on your system, so you'll "
		   'either need to manually install Coopr, or install SetupTools and rerun '
		   'this install script.\\n\\n'
		   ' SetupTools: http://pypi.python.org/pypi/setuptools\\n'
		   ' Coopr:      https://software.sandia.gov/coopr/\\n')
		SE.write( msg )
	else:
		msg = ('Coopr not found.  Attempting to install with Easy Install\\n')
		SE.write( msg )

		check_call( ( easy_install_executable, '-U', 'coopr' ) )

progs = os.environ['PROGRAMFILES']
userdir = os.environ['USERPROFILE']
glpk_dir = os.path.join( progs, 'GLPK' )
glpk_exe_path = os.path.join( glpk_dir, 'glpsol.exe' )
glpk_dll_path = os.path.join( glpk_dir, glpk_dll_name )
temoa_path = os.path.join( userdir, 'Desktop', 'temoa.py' )

if not (os.path.exists( glpk_dir ) and os.path.exists( glpk_exe_path ) ):
	try:
		os.mkdir( glpk_dir )
	except WindowsError, e:
		if not 'exists' in e.strerror: raise

	SE.write( 'Installing GLPK\\n' )
	with open( glpk_exe_path, 'wb' ) as f:
		decompress = uncompress_scheme[ glpk_exe_uncompress ]
		f.write( decompress( decodestring( glpk_exe_data )))
	with open( glpk_dll_path, 'wb' ) as f:
		decompress = uncompress_scheme[ glpk_dll_uncompress ]
		f.write( decompress( decodestring( glpk_dll_data )))

with open( temoa_path, 'wb' ) as f:
	decompress = uncompress_scheme[ temoa_uncompress ]
	f.write( decompress( decodestring( temoa_data )))

WinXPEnvKey = r'SYSTEM\ControlSet001\Control\Session Manager\Environment'
key = OpenKey( HKEY_LOCAL_MACHINE, WinXPEnvKey, 0, KEY_ALL_ACCESS )
winpath, reg_type = QueryValueEx( key, 'Path' )

el_to_add = []
if 'glpk' not in winpath.lower():
	el_to_add.append( glpk_dir )

if 'python' not in winpath.lower():
	el_to_add.append( python_root )
	el_to_add.append( os.path.join( python_root, 'Scripts' ))

if el_to_add:
	path_elements = winpath.split(';')
	path_elements.extend( el_to_add )
	SetValueEx( key, 'Path', 0, reg_type, ';'.join( path_elements ) )
CloseKey(key)

msg = 'Installation complete.  The temoa.py model file is now on your Desktop.'

if el_to_add:
	msg += '\''

The system path has additional elements:

 {{elements}}

To propogate this change, please logoff and then back on.  (Alternatively, you
may restart your computer as well.)
'\''.format( elements='\\n '.join(el_to_add) )

msg += '\\n\\nPress enter to close this Window.'
raw_input( msg )
'''.format(
  glpk_dll_type = glpk_dll_type,
  glpk_dll_name = glpk_dll_name,
  glpk_dll_data = glpk_dll_data,
  glpk_exe_type = glpk_exe_type,
  glpk_exe_data = glpk_exe_data,
  temoa_type    = temoa_type,
  temoa_data    = temoa_data
)


with open( script_name, 'w') as f:
	f.write( install_script )

SE.write( 'Install script created: {}\n'.format( script_name ))
