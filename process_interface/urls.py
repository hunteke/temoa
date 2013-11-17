from django.conf.urls import patterns, include, url
from views import (
  login_view,
  logout_view,
  home,
  tutorial,
  user,
  user_analyses,
  view,
  test_view,
  get_client_template,

  process_list,
  process_new,
  process_update,
  process_remove,

  analysis_list,
  analysis_info,
  analysis_update,
  analysis_create,

  analysis_commodity_list,
  analysis_create_commodity,
  analysis_update_commodity,
  analysis_delete_commodity,

  analysis_create_segfrac,
  analysis_update_segfrac,
  analysis_delete_segfrac,

  technology_list,
  technology_create,
  technology_update,
  technology_remove,

  process_costfixed_new,
  process_costfixed_update,
  process_costfixed_remove,

  process_costvariable_new,
  process_costvariable_update,
  process_costvariable_remove,

  process_efficiency_new,
  process_efficiency_update,
  process_efficiency_remove,

  process_emissionactivity_new,
  process_emissionactivity_update,
  process_emissionactivity_remove,

  analysis_technology_list,
  analysis_technology_info,
  analysis_technology_update,

  analysis_technology_inputsplit_new,
  analysis_technology_inputsplit_update,
  analysis_technology_inputsplit_remove,

  analysis_technology_outputsplit_new,
  analysis_technology_outputsplit_update,
  analysis_technology_outputsplit_remove,
)

urlpatterns = patterns('',
  url(r'^$',          home,        name='home'),
  url(r'^login/$',    login_view,  name='login'),
  url(r'^logout/$',   logout_view, name='logout'),
  url(r'^interact/$', view,        name='view'),
  url(r'^tutorial/$', tutorial,    name='tutorial'),
  url(r'^user/list$', user,        name='users'),
  url(r'^user/(?P<username>\w+)/analyses$', user_analyses, name='user_analyses'),
  url(r'^client_template/(?P<template>\w+.ejs)$', get_client_template, name='get_client_template'),

  url(r'^analysis/(?P<analysis_id>\d+)/process/list/json$',   process_list, name='process_list'),

# Analysis
  url(r'^analysis/list$',   analysis_list,   name='analysis_list'),
  url(r'^analysis/create$', analysis_create, name='analysis_create'),
  url(r'^analysis/(?P<analysis_id>\d+)$', analysis_info, name='analysis_info'),
  url(r'^analysis/(?P<analysis_id>\d+)/update$', analysis_update, name='analysis_update'),

# AnalysisSegFrac
  url(r'^analysis/(?P<analysis_id>\d+)/segfrac/create$', analysis_create_segfrac, name='analysis_create_segfrac' ),
  url(r'^analysis/(?P<analysis_id>\d+)/segfrac/update/(?P<segfrac_id>\d+)$', analysis_update_segfrac, name='analysis_update_segfrac' ),
  url(r'^analysis/(?P<analysis_id>\d+)/segfrac/remove/(?P<segfrac_id>\d+)$', analysis_delete_segfrac, name='analysis_delete_segfrac' ),

# Process
  url(r'^analysis/(?P<analysis_id>\d+)/process/list$', process_list, name='process_list'),
#  url(r'^analysis/(?P<analysis_id>\d+)/process/info/(?P<process_ids>(?:\d+,?)+)$', process_info, name='process_info' ),
  url(r'^analysis/(?P<analysis_id>\d+)/process/create$', process_new, name='process_new' ),
  url(r'^analysis/(?P<analysis_id>\d+)/process/remove/(?P<process_id>(?:\d+,?)+)$', process_remove, name='process_remove' ),
  url(r'^analysis/(?P<analysis_id>\d+)/process/update/(?P<process_id>\d+)$', process_update, name='process_update'),

# ProcessCostFixed
  url(r'^analysis/(?P<analysis_id>\d+)/process/(?P<process_id>\d+)/create/CostFixed$', process_costfixed_new, name='process_costfixed_new'),
  url(r'^analysis/(?P<analysis_id>\d+)/process/(?P<process_id>\d+)/update/CostFixed/(?P<costfixed_id>\d+)$', process_costfixed_update, name='process_costfixed_update'),
  url(r'^analysis/(?P<analysis_id>\d+)/process/(?P<process_id>\d+)/remove/CostFixed/(?P<costfixed_id>\d+)$', process_costfixed_remove, name='process_costfixed_remove'),

# ProcessCostVariable
  url(r'^analysis/(?P<analysis_id>\d+)/process/(?P<process_id>\d+)/create/CostVariable$', process_costvariable_new, name='process_costvariable_new'),
  url(r'^analysis/(?P<analysis_id>\d+)/process/(?P<process_id>\d+)/update/CostVariable/(?P<costvariable_id>\d+)$', process_costvariable_update, name='process_costvariable_update'),
  url(r'^analysis/(?P<analysis_id>\d+)/process/(?P<process_id>\d+)/remove/CostVariable/(?P<costvariable_id>\d+)$', process_costvariable_remove, name='process_costvariable_remove'),

# ProcessEfficiency
  url(r'^analysis/(?P<analysis_id>\d+)/process/(?P<process_id>\d+)/create/Efficiency$', process_efficiency_new, name='process_efficiency_new'),
  url(r'^analysis/(?P<analysis_id>\d+)/process/(?P<process_id>\d+)/update/Efficiency/(?P<efficiency_id>\d+)$', process_efficiency_update, name='process_efficiency_update'),
  url(r'^analysis/(?P<analysis_id>\d+)/process/(?P<process_id>\d+)/remove/Efficiency/(?P<efficiency_id>\d+)$', process_efficiency_remove, name='process_efficiency_remove'),

# ProcessEmissionActivity
  url(r'^analysis/(?P<analysis_id>\d+)/process/(?P<process_id>\d+)/create/EmissionActivity$', process_emissionactivity_new, name='process_emissionactivity_new'),
  url(r'^analysis/(?P<analysis_id>\d+)/Efficiency/(?P<efficiency_id>\d+)/update/EmissionActivity/(?P<emissionactivity_id>\d+)$', process_emissionactivity_update, name='process_emissionactivity_update'),
  url(r'^analysis/(?P<analysis_id>\d+)/Efficiency/(?P<efficiency_id>\d+)/remove/EmissionActivity/(?P<emissionactivity_id>\d+)$', process_emissionactivity_remove, name='process_emissionactivity_remove'),

# Technology
  url(r'^technology/list$',   technology_list, name='technology_list'),
  url(r'^technology/create$', technology_create, name='technology_create'),
  url(r'^technology/update/(?P<technology_id>(?:\d+))$', technology_update, name='technology_update'),
  # url(r'^technology/info/(?P<technology_ids>(?:\d+,?)+)$', technology_info, name='technology_info' ),
  url(r'^technology/remove/(?P<technology_id>(?:\d+,?)+)$', technology_remove, name='technology_remove' ),

# AnalysisTechnology
  url(r'^analysis/(?P<analysis_id>\d+)/technology/list$', analysis_technology_list, name='analysis_technology_list'),
  url(r'^analysis/(?P<analysis_id>\d+)/technology/info/(?P<technology_id>\d+)$', analysis_technology_info, name='analysis_technology_info'),
  url(r'^analysis/(?P<analysis_id>\d+)/technology/update/(?P<technology_id>\d+)$', analysis_technology_update, name='analysis_technology_update'),

# AnalysisCommodity
  url(r'^analysis/(?P<analysis_id>\d+)/commodity/list$', analysis_commodity_list, name='analysis_commodity_list' ),
  url(r'^analysis/(?P<analysis_id>\d+)/create/commodity/(?P<ctype>demand|emission|physical)$', analysis_create_commodity, name='analysis_create_commodity' ),
  url(r'^analysis/(?P<analysis_id>\d+)/update/commodity/(?P<commodity_id>\d+)$', analysis_update_commodity, name='analysis_update_commodity' ),
  url(r'^analysis/(?P<analysis_id>\d+)/delete/commodity/(?P<commodity_id>\d+)$', analysis_delete_commodity, name='analysis_delete_commodity' ),

# TechInputSplit
  url(r'^analysis/(?P<analysis_id>\d+)/technology/(?P<technology_id>\d+)/InputSplit/create$', analysis_technology_inputsplit_new, name='analysis_technology_inputsplit_new'),
  url(r'^analysis/(?P<analysis_id>\d+)/technology/(?P<technology_id>\d+)/InputSplit/update/(?P<tis_id>\d+)$', analysis_technology_inputsplit_update, name='analysis_technology_inputsplit_update'),
  url(r'^analysis/(?P<analysis_id>\d+)/technology/(?P<technology_id>\d+)/InputSplit/remove/(?P<tis_id>\d+)$', analysis_technology_inputsplit_remove, name='analysis_technology_inputsplit_remove'),

# TechInputSplit
  url(r'^analysis/(?P<analysis_id>\d+)/technology/(?P<technology_id>\d+)/OutputSplit/create$', analysis_technology_outputsplit_new, name='analysis_technology_outputsplit_new'),
  url(r'^analysis/(?P<analysis_id>\d+)/technology/(?P<technology_id>\d+)/OutputSplit/update/(?P<tos_id>\d+)$', analysis_technology_outputsplit_update, name='analysis_technology_outputsplit_update'),
  url(r'^analysis/(?P<analysis_id>\d+)/technology/(?P<technology_id>\d+)/OutputSplit/remove/(?P<tos_id>\d+)$', analysis_technology_outputsplit_remove, name='analysis_technology_outputsplit_remove'),

)

