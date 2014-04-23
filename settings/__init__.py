# Django settings for TemoaDB project.

import getpass, os, socket, sys
from os.path import abspath, dirname, join as pjoin, isfile

# Step 1: Import host-specific settings.
hostname = socket.gethostname().lower().split('.')[0].replace('-','')
user     = getpass.getuser()

fname = '{}_{}'.format( user, hostname )

  # First, play nice with new setups.  Inform the user if it's not there.
curdir = dirname( abspath( __file__ ))
if not isfile( pjoin( curdir, fname + '.py' )):
	# Note that isfile is not perfect -- but we're not trying to be!  The
	# following import will fail if, for example, the permissions are wrong.
	missing = pjoin( curdir, fname )
	msg = ("\n\n  Unable to access this host's settings file '{}.py'.  Do you "
	  "need to create it?  There are examples in the settings directory '{}'.")
	raise IOError( msg.format( missing, curdir ))


exec('from .{} import *'.format( fname ) )

# Step 2: Import the non-Git settings (e.g., secret, etc.)
  # First, since local_settings is necessarily not kept in the RCS, play nice
  # with new users and remind them to create it.
curdir = dirname( abspath( __file__ ))
if not isfile( pjoin( curdir, 'local_settings.py' )):
	missing = pjoin( curdir, 'local_settings.py' )
	example = pjoin( curdir, 'local_settings.example.py' )
	msg = ("\n\n  Unable to access '{}' file.  Do you need to create it, "
	  "based on '{}'?")
	raise IOError( msg.format( missing, example ))

  # Now, since it's there, import it without a try block, to let Python/Django
  # do their standard error handling.
from .local_settings import *

