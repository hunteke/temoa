import debug as D

def LoanLifeParam_Init ( tech, model ):
	D.write( D.INFO, "LoanLifeParam_Init parameter initialization\n" )

	if   'coal'     : return 20
	elif 'nuclear'  : return 40
	elif 'wind_ons' : return 10
	elif 'solar_pv' : return 15

	return 10