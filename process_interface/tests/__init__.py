"""
These tests may be run through Django's standard testing interface:

    $ python manage.py test
"""

def suite():
	import unittest
	from os.path import dirname, basename

	appname  = basename(dirname(dirname( __file__ )))
	mod = appname + '.tests'

	return unittest.TestLoader().discover( mod, pattern="*.py")