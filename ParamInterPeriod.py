import debug as D

def ParamInterPeriod_Init ( period, model ):
	"Set: Initialize the inter-period years"
	D.write( D.INFO, "InterPeriodSet_Init\n" )
	M = model

	periods = [ p for p in M.period ]
	periods.sort()

	i = periods.index( period )
	length = periods[i +1] - periods[ i ]

	return length

