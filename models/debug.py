"""
    TEMOA (Tools for Energy Model Optimization and Analysis) 
    Copyright (C) 2010 TEMOA Developer Team 

    This file is part of TEMOA.
    TEMOA is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    TEMOA is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with TEMOA.  If not, see <http://www.gnu.org/licenses/>.
"""


ALL = [ 'debug' ]

i = 1
ERROR   = i; i *= 2
WARNING = i; i *= 2
NORMAL  = i; i *= 2
INFO    = i; i *= 2
DEBUG   = i; i *= 2

LEVEL = NORMAL

del i

class debug:
	pass

def write( level, msg ):
	from sys import stderr
	if ( level <= LEVEL ):
		stderr.write( msg );

debug.write = write

