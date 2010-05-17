import debug as D

def InvestmentCostsParam_Init ( tech, iper, per, model ):
	D.write( D.INFO, "InvestmentCosts_Init parameter initialization\n" )

	if   'coal'        == tech: return 2058
	elif 'geo'         == tech: return 1711
	elif 'gt_b'        == tech: return 634
	elif 'gt_s'        == tech: return 634
	elif 'gt_p'        == tech: return 634
	elif 'gtcc_b'      == tech: return 948
	elif 'gtcc_s'      == tech: return 948
	elif 'gtcc_p'      == tech: return 948
	elif 'gtcc_ccs'    == tech: return 1890
	elif 'igcc'        == tech: return 2378
	elif 'igcc_ccs'    == tech: return 3496
	elif 'nuclear'     == tech: return 3318
	elif 'hydro_b'     == tech: return 2242
	elif 'hydro_s'     == tech: return 2242
	elif 'hydro_p'     == tech: return 2242
	elif 'solar_pv'    == tech: return 6038
	elif 'solar_th'    == tech: return 5021
	elif 'wind_offs'   == tech: return 3851
	elif 'wind_ons'    == tech: return 1923

	D.write( D.INFO, "Warning: Technology with no investment cost: (%s, %d, %d)\n" % ( tech, iper, per ) )

