import debug as D

def TechLifeParam_Init ( tech, model ):
	D.write( D.INFO, "LoanLifeParam_Init parameter initialization\n" )

	# return years (10 years = 1 period)
	if   'coal'     : return 30
	elif 'nuclear'  : return 40
	elif 'wind_ons' : return 20
	elif 'solar_pv' : return 25

	return 10

