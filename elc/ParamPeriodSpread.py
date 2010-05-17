def ParamPeriodSpread_Init ( period, model ):
	M = model
	spread = sum( [
	  (1 + M.global_discount_rate.value)**(M.operating_period.first() - y - period)

	  for y in range(0, M.inter_period[period])
	])

	return spread

