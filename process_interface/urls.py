from django.conf.urls import patterns, include, url
from views import (
  analysis_info,
  analysis_update,
  analysis_new,
  list_analyses,
  home,
  get_messages,
  process_info,
  process_list,
  tutorial,
  update_process,
  new_efficiency,
  update_efficiency,
  new_emissionactivity,
  update_emissionactivity,
  new_costfixed,
  update_costfixed,
  new_costvariable,
  update_costvariable,
  user,
  user_analyses,
  view,
  test_view,
)

urlpatterns = patterns('',
  url(r'^$',          home,     name='home'),
  url(r'^interact/$', view,     name='view'),
  url(r'^tutorial/$', tutorial, name='tutorial'),
  url(r'^user/list$',      user, name='users'),
  url(r'^user/(?P<username>\w+)/analyses$', user_analyses, name='user_analyses'),

  url(r'^session_messages/$', get_messages, name='session_messages'),

  url(r'^analysis/list$',      list_analyses, name='list_analyses'),
  url(r'^analysis/New$',       analysis_new, name='analysis_new'),
  url(r'^analysis/(?P<analysis_id>\d+)$', analysis_info, name='analysis_info'),
  url(r'^analysis/(?P<analysis_id>\d+)/update$', analysis_update, name='analysis_update'),
  url(r'^analysis/(?P<analysis_id>\d+)/process_list$', process_list, name='process_list'),
  url(r'^analysis/(?P<analysis_id>\d+)/process_info/(?P<process_ids>(?:\d+,?)+)$', process_info, name='process_info' ),
#  url(r'^analysis/(?P<analysis_id>\d+)/technology_info/(?P<process_ids>(?:\d+,?)+)$', technology_info, name='technology_info'),

#  url(r'^analysis/(?P<analysis_id>\d+)/update/technology/(?P<technology_id>\d+)$', update_analysis_technology, name='update_analysis_technology'),
#  url(r'^analysis/(?P<analysis_id>\d+)/update/technology/(?P<technology_id>\d+)/delete/(?P<parameter>\w+)$', remove_analysis_technology_datum, name='remove_analysis_technology_datum'),

  url(r'^analysis/(?P<analysis_id>\d+)/create/process/(?P<process_id>\d+)/Efficiency$', new_efficiency, name='new_efficiency'),
  url(r'^analysis/(?P<analysis_id>\d+)/update/process/(?P<process_id>\d+)/(?P<efficiency_id>\d+)/Efficiency$', update_efficiency, name='update_efficiency'),

  url(r'^analysis/(?P<analysis_id>\d+)/create/process/(?P<process_id>\d+)/EmissionActivity$', new_emissionactivity, name='new_emissionactivity'),
  url(r'^analysis/(?P<analysis_id>\d+)/update/process/(?P<process_id>\d+)/(?P<emissionactivity_id>\d+)/EmissionActivity$', update_emissionactivity, name='update_emissionactivity'),

  url(r'^analysis/(?P<analysis_id>\d+)/create/process/(?P<process_id>\d+)/CostFixed$', new_costfixed, name='new_costfixed'),
  url(r'^analysis/(?P<analysis_id>\d+)/update/process/(?P<process_id>\d+)/(?P<costfixed_id>\d+)/CostFixed$', update_costfixed, name='update_costfixed'),

  url(r'^analysis/(?P<analysis_id>\d+)/create/process/(?P<process_id>\d+)/CostVariable$', new_costvariable, name='new_costvariable'),
  url(r'^analysis/(?P<analysis_id>\d+)/update/process/(?P<process_id>\d+)/(?P<costvariable_id>\d+)/CostVariable$', update_costvariable, name='update_costvariable'),

  url(r'^analysis/(?P<analysis_id>\d+)/update/process/(?P<process_id>\d+)$', update_process, name='update_process'),

#  url(r'^analysis/(?P<analysis_id>\d+)/update/process/(?P<process_id>\d+)$', update_analysis_process, name='update_analysis_process'),
#  url(r'^analysis/(?P<analysis_id>\d+)/update/process/(?P<process_id>\d+)/delete/(?P<parameter>\w+)$', remove_analysis_process_datum, name='remove_analysis_process_datum'),
  url(r'^test$', test_view, name='test'),
)

