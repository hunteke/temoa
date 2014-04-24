# vim:sw=3:ts=3:fileencoding=utf-8:list:listchars=tab\:»·,trail\:·:noexpandtab:
# :encoding=utf-8:indentSize=3:tabSize=3:noTabs=false:

from django.http import HttpResponse
from django.utils.encoding import iri_to_uri

class _HttpResponseRedirection(HttpResponse):
	def __init__ ( self, redirect_to ):
		HttpResponse.__init__( self )
		self['Location'] = iri_to_uri(redirect_to)

class HttpResponseContinue(HttpResponse):
	status_code = 100

class HttpResponseSwitchingProtocols(HttpResponse):
	status_code = 101

class HttpResponseCreated(HttpResponse):
	status_code = 201

class HttpResponseAccepted(HttpResponse):
	status_code = 202

class HttpResponseNonAuthoritativeInformation(HttpResponse):
	status_code = 203

class HttpResponseNoContent(HttpResponse):
	status_code = 204

class HttpResponseResetContent(HttpResponse):
	status_code = 205

class HttpResponsePartialContent(HttpResponse):
	status_code = 206

class HttpResponseMultipleChoices(HttpResponse):
	status_code = 300

class HttpResponsePermanentRedirect(_HttpResponseRedirection):
	status_code = 301
HttpResponseMovedPermanently = HttpResponsePermanentRedirect

class HttpResponseRedirect(_HttpResponseRedirection):
	status_code = 302
HttpResponseFound = HttpResponseRedirect

class HttpResponseSeeOther(_HttpResponseRedirection):
	status_code = 303

class HttpResponseNotModified(HttpResponse):
	status_code = 304

class HttpResponseUseProxy(_HttpResponseRedirection):
	status_code = 305

class HttpResponseTemporaryRedirect(_HttpResponseRedirection):
	status_code = 307

class HttpResponseBadRequest(HttpResponse):
	status_code = 400

class HttpResponseUnauthorized(HttpResponse):
	status_code = 401

class HttpResponseForbidden(HttpResponse):
	status_code = 403

class HttpResponseNotFound(HttpResponse):
	status_code = 404

class HttpResponseNotAllowed(HttpResponse):
	status_code = 405

	def __init__(self, permitted_methods):
		HttpResponse.__init__(self)
		self['Allow'] = ', '.join(permitted_methods)
HttpResponseMethodNotAllowed = HttpResponseNotAllowed

class HttpResponseProxyAuthenticationRequired(HttpResponse):
	status_code = 407

class HttpResponseRequestTimeout(HttpResponse):
	status_code = 408

class HttpResponseConflict(HttpResponse):
	status_code = 409

class HttpResponseGone(HttpResponse):
	status_code = 410

class HttpResponseLengthRequired(HttpResponse):
	status_code = 411

class HttpResponsePreconditionFailed(HttpResponse):
	status_code = 412

class HttpResponseRequestEntityTooLarge(HttpResponse):
	status_code = 413

class HttpResponseRequestURITooLong(HttpResponse):
	status_code = 414

class HttpResponseUnsupportedMediaType(HttpResponse):
	status_code = 415

class HttpResponseRequestedRangeNotSatisfiable(HttpResponse):
	status_code = 416

class HttpResponseExpectationFailed(HttpResponse):
	status_code = 417

class HttpResponseServerError(HttpResponse):
	status_code = 500
HttpResponseInternalServerError = HttpResponseServerError

class HttpResponseNotImplemented(HttpResponse):
	status_code = 501

class HttpResponseBadGateway(HttpResponse):
	status_code = 502

class HttpResponseServiceUnavailable(HttpResponse):
	status_code = 503

class HttpResponseGatewayTimeout(HttpResponse):
	status_code = 504

class HttpResponseHTTPVersionNotSupported(HttpResponse):
	status_code = 505

