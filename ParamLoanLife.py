import debug as D

def LoanLifeParam_Init ( tech, model ):
	D.write( D.INFO, "LoanLifeParam_Init parameter initialization\n" )

	if   'coal'     == tech: return 20
	elif 'nuclear'  == tech: return 40
	elif 'wind_ons' == tech: return 10
	elif 'solar_pv' == tech: return 15

	return 10

