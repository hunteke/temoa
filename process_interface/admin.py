# vim:sw=3:ts=3:fileencoding=utf-8:list:listchars=tab\:»·,trail\:·:noexpandtab:
# :encoding=utf-8:indentSize=3:tabSize=3:noTabs=false:

to_administrate = (
  'Analysis',
  'AnalysisCommodity',
  'Commodity',
  'CommodityType',
  'Param_CapacityFactorProcess',
  'Param_CapacityFactorTech',
  'Param_CostFixed',
  'Param_CostVariable',
  'Param_Demand',
  'Param_DemandSpecificDistribution',
  'Param_Efficiency',
  'Param_EmissionActivity',
  'Param_EmissionLimit',
  'Param_MaxMinCapacity',
  'Param_ResourceBound',
  'Param_SegFrac',
  'Param_TechInputSplit',
  'Param_TechOutputSplit',
  'Process',
  'Technology',
  'Vintage',
)

_temp = __import__(
  'process_interface.models',
  globals(),
  locals(),
  to_administrate,
  0
)

  # the above __import__ replaces this next line.
# from process_interface.models import ( ... )

from django.contrib import admin

register = admin.site.register
for cls in to_administrate:
	register( getattr( _temp, cls ))
