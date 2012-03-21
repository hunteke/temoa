#!/usr/bin/env python

import os, sys

from glob import glob

SE = sys.stderr

if sys.argv[1] != 'Windows':
	SE.write( "Not Windows\n" )
	# Seems silly, but a sanity check/reminder to whoever runs this.  For this
	# first cut of this script, the logic is rather specifically geared toward
	# Windows.
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
generated_warning = '''\
Warning/Reminder to the Temoa Project developers: This Python install script
# is generated from another script.  Changes made here will be overwritten by
# the next development iteration.  (If you're an end-user, you're safe!  Change
# away and help us make this installation better by sending back your
# suggestions!)
'''


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


install_script = open( 'WindowsInstallScript.py' ).read().format(
  Generated_Script_Warning = generated_warning,
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
