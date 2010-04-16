import debug as D

def TechLifeParam_Init ( tech, model ):
	D.write( D.INFO, "TechLifeParam_Init parameter initialization\n" )

	# return years (10 years = 1 period)
	if   'coal'     == tech: return 30
	elif 'nuclear'  == tech: return 40
	elif 'wind_ons' == tech: return 20
	elif 'solar_pv' == tech: return 30

	return 20

