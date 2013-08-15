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
