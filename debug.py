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

