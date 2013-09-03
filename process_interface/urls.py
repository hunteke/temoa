from django.conf.urls import patterns, include, url
from views import (
  analyses,
  analysis_info,
  home,
  get_messages,
  process_info,
  process_list,
  tutorial,
  update_process,
  new_efficiency,
  update_efficiency,
  user,
  view,
  test_view,
)

def Unimplemented ( msg ):
	def view ( *args, **kwargs ):
		# TODO: make this an actual view that does not rely on DEBUG = True
		raise NotImplementedError( msg )
	return view


urlpatterns = patterns('',
  url(r'^$',          home,     name='home'),
  url(r'^interact/$', view,     name='view'),
  url(r'^tutorial/$', tutorial, name='tutorial'),
  url(r'^nojs/$',     Unimplemented('The no-javascript version of TemoaDB is not yet implemented.' ),  name='nojs'),
  url(r'^user/list$',      user, name='users'),
  url(r'^user/(?P<username>\w+)/analyses$', analyses, name='analyses'),

  url(r'^session_messages/$', get_messages, name='session_messages'),

  url(r'^analysis/(?P<analysis_id>\d+)$', analysis_info, name='analysis_info'),
  url(r'^analysis/(?P<analysis_id>\d+)/process_list$', process_list, name='process_list'),
  url(r'^analysis/(?P<analysis_id>\d+)/process_info/(?P<process_ids>(?:\d+,?)+)$', process_info, name='process_info' ),
#  url(r'^analysis/(?P<analysis_id>\d+)/technology_info/(?P<process_ids>(?:\d+,?)+)$', technology_info, name='technology_info'),

#  url(r'^analysis/(?P<analysis_id>\d+)/update/technology/(?P<technology_id>\d+)$', update_analysis_technology, name='update_analysis_technology'),
#  url(r'^analysis/(?P<analysis_id>\d+)/update/technology/(?P<technology_id>\d+)/delete/(?P<parameter>\w+)$', remove_analysis_technology_datum, name='remove_analysis_technology_datum'),

  url(r'^analysis/(?P<analysis_id>\d+)/create/process/(?P<process_id>\d+)/Efficiency$', new_efficiency, name='new_efficiency'),

  url(r'^analysis/(?P<analysis_id>\d+)/update/process/(?P<process_id>\d+)$', update_process, name='update_process'),

#  url(r'^analysis/(?P<analysis_id>\d+)/update/process/(?P<process_id>\d+)$', update_analysis_process, name='update_analysis_process'),
  url(r'^analysis/(?P<analysis_id>\d+)/update/process/(?P<process_id>\d+)/(?P<efficiency_id>\d+)/Efficiency$', update_efficiency, name='update_efficiency'),
#  url(r'^analysis/(?P<analysis_id>\d+)/update/process/(?P<process_id>\d+)/delete/(?P<parameter>\w+)$', remove_analysis_process_datum, name='remove_analysis_process_datum'),
  url(r'^test$', test_view, name='test'),
)

