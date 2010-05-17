def SetOperatingPeriod_Init ( model ):
	"""
	Set: The 'munge' set is all the periods the model can *actually*
	optimize.  This basically means, it's all but the "last" item in
	the 'period' set
	"""

	periods = [ p for p in model.period ]
	periods.sort()

	return periods[:-1]

