from django.views.decorators.http import require_http_methods

# Django does not define some of these decorators, so if we want them (we do),
# then we must define them for ourselvess.  Thus, per the HTTP/1.1 RFC, section
# 9.8 (http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html#sec9.8)

_mod_vars = globals()
_require_doc = 'Decorator to require that a view only accept the {} method.'
methods = ( 'CONNECT', 'DELETE', 'GET', 'HEAD', 'OPTIONS', 'POST', 'PUT', 'TRACE' )

for m in methods:
	_name = 'require_{}'.format( m )
	_mod_vars[ _name ] = require_http_methods( [m] )
	_mod_vars[ _name ].__doc__ = _require_doc.format( m )
	del _name

del _require_doc, _mod_vars

