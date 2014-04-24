# vim:sw=3:ts=3:fileencoding=utf-8:list:listchars=tab\:»·,trail\:·:noexpandtab:
# :encoding=utf-8:indentSize=3:tabSize=3:noTabs=false:

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  # Examples:
  url(r'^', include('process_interface.urls', namespace='process_interface')),
  # url(r'^webui/', include('webui.foo.urls')),

  # url(r'^$', '
  # Uncomment the admin/doc line below to enable admin documentation:
#  url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

  # Uncomment the next line to enable the admin:
  url(r'^admin/', include(admin.site.urls)),

  url(r'^i18n/', include('django.conf.urls.i18n')),
)
