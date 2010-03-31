import debug as D

def FixedCostsParam_Init ( tech, iper, per, model ):
	D.write( D.INFO, "FixedCostsParam_Init parameter initialization\n" )

	if   'coal'        == tech: return 27.5
	elif 'geo'         == tech: return 165
	elif 'gt_b'        == tech: return 10.5
	elif 'gtcc_b'      == tech: return 11.7
	elif 'gtcc_ccs'    == tech: return 19.9
	elif 'hydro_b'     == tech: return 13.6
	elif 'igcc'        == tech: return 38.7
	elif 'igcc_ccs'    == tech: return 46.1
	elif 'nuclear'     == tech: return 90
	elif 'gt_s'        == tech: return 10.5
	elif 'gtcc_s'      == tech: return 11.7
	elif 'hydro_s'     == tech: return 13.6
	elif 'solar_pv'    == tech: return 11.7
	elif 'solar_th'    == tech: return 56.8
	elif 'wind_offs'   == tech: return 89.5
	elif 'wind_ons'    == tech: return 30.3
	elif 'gt_p'        == tech: return 10.5
	elif 'gtcc_p'      == tech: return 11.7
	elif 'hydro_p'     == tech: return 13.6
	elif 't0_ng_steam' == tech: return 14.6
	elif 't0_dt'       == tech: return  3.7
	elif 't0_gt'       == tech: return  3.3
	elif 't0_gtcc'     == tech: return  4.6
	elif 't0_hydro'    == tech: return  9.4
	elif 't0_coal'     == tech: return 20.4
	elif 't0_nuclear'  == tech: return 79.0