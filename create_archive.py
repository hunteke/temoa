#!/usr/bin/env python

"""
Temoa - Tools for Energy Model Optimization and Analysis
  linear optimization; least cost; dynamic system visualization

Copyright (C) 2011-2014  Kevin Hunter, Joseph DeCarolis

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU Affero General Public License for more details.

Developers of this script will check out a complete copy of the GNU Affero
General Public License in the file COPYING.txt.  Users uncompressing this from
an archive may not have received this license file.  If not, see
<http://www.gnu.org/licenses/>.
"""

# This script creates the 'temoa.py' zip archive/executable using Python's
# PyZipFile interface.  It accepts no arguments.

import os

from cStringIO import StringIO
from zipfile import PyZipFile, ZIP_DEFLATED

temoa_pkg = StringIO()
temoa_pkg.write( '#!/usr/bin/env python\n' )
with PyZipFile( temoa_pkg, mode='w', compression=ZIP_DEFLATED ) as zf:
	zf.debug = 3
	zf.writepy( './temoa_model/' )

fname = 'temoa.py'
with open( fname, 'wb' ) as f:
	f.write( temoa_pkg.getvalue() )

os.chmod( fname, 0755 )

