import debug as D

def MarginalCostsParam_Init ( tech, iper, per, model ):
	D.write( D.INFO, "MarginalCostsParam_Init parameter initialization\n" )

	var_o_m = { # $/kWh
	  'coal'        : 0.0459,
	  'gt_b'        : 0.0317,
	  'gt_p'        : 0.0317,
	  'gt_s'        : 0.0317,
	  'gtcc_b'      : 0.0200,
	  'gtcc_p'      : 0.0200,
	  'gtcc_s'      : 0.0200,
	  'gtcc_ccs'    : 0.0294,
	  'hydro_b'     : 0.0243,
	  'hydro_p'     : 0.0243,
	  'hydro_s'     : 0.0243,
	  'igcc'        : 0.0292,
	  'igcc_ccs'    : 0.0444,
	  'nuclear'     : 0.0049,
	  't0_ng_steam' : 0.0074,
	  't0_dt'       : 0.035,
	  't0_gt'       : 0.031,
	  't0_gtcc'     : 0.0052,
	  't0_hydro'    : 0.014,
	  't0_coal'     : 0.0067,
	  't0_nuclear'  : 0.0016,
	}
	fuel_price = { # $/kWh
	  'diesel'  : 0.054,
	  'nat_gas' : 0.0198,
	  'coal'    : 0.00612,
	  'uranium' : 0.0000612,
	}
	therm_eff = {
	  'coal'        : 0.39,
	  'igcc'        : 0.46,
	  'igcc_ccs'    : 0.41,
	  'gtcc_ccs'    : 0.46,
	  'nuclear'     : 0.33,
	  'geo'         : 0.11,
	  'gtcc_b'      : 0.54,
	  'gtcc_s'      : 0.54,
	  'gtcc_p'      : 0.54,
	  'gt_b'        : 0.40,
	  'gt_s'        : 0.40,
	  'gt_p'        : 0.40,
	  'hydro_b'     : 0.00,
	  'hydro_s'     : 0.00,
	  'hydro_p'     : 0.00,
	  'wind_ons'    : 0.34,
	  'wind_offs'   : 0.34,
	  'solar_th'    : 0.34,
	  'solar_pv'    : 0.34,
	  't0_ng_steam' : 0.28,
	  't0_dt'       : 0.22,
	  't0_gt'       : 0.25,
	  't0_gtcc'     : 0.37,
	  't0_hydro'    : 0.00,
	  't0_coal'     : 0.31,
	  't0_nuclear'  : 0.30,
	}
	if   'coal'        == tech: return (var_o_m[tech] * therm_eff[tech] / fuel_price['coal']    * 8760)
	elif 'gt_b'        == tech: return (var_o_m[tech] * therm_eff[tech] / fuel_price['nat_gas'] * 8760)
	elif 'gt_s'        == tech: return (var_o_m[tech] * therm_eff[tech] / fuel_price['nat_gas'] * 8760)
	elif 'gt_p'        == tech: return (var_o_m[tech] * therm_eff[tech] / fuel_price['nat_gas'] * 8760)
	elif 'gtcc_b'      == tech: return (var_o_m[tech] * therm_eff[tech] / fuel_price['nat_gas'] * 8760)
	elif 'gtcc_s'      == tech: return (var_o_m[tech] * therm_eff[tech] / fuel_price['nat_gas'] * 8760)
	elif 'gtcc_p'      == tech: return (var_o_m[tech] * therm_eff[tech] / fuel_price['nat_gas'] * 8760)
	elif 'gtcc_ccs'    == tech: return (var_o_m[tech] * therm_eff[tech] / fuel_price['nat_gas'] * 8760)
	elif 'igcc'        == tech: return (var_o_m[tech] * therm_eff[tech] / fuel_price['nat_gas'] * 8760)
	elif 'igcc_ccs'    == tech: return (var_o_m[tech] * therm_eff[tech] / fuel_price['nat_gas'] * 8760)
	elif 'nuclear'     == tech: return (var_o_m[tech] * therm_eff[tech] / fuel_price['uranium'] * 8760)
	elif 'hydro_b'     == tech: return (var_o_m[tech] * 8760)
	elif 'hydro_s'     == tech: return (var_o_m[tech] * 8760)
	elif 'hydro_p'     == tech: return (var_o_m[tech] * 8760)
	elif 't0_hydro'    == tech: return (var_o_m[tech] * 8760)
	elif 't0_ng_steam' == tech: return (var_o_m[tech] * therm_eff[tech] / fuel_price['nat_gas'] * 8760)
	elif 't0_gt'       == tech: return (var_o_m[tech] * therm_eff[tech] / fuel_price['nat_gas'] * 8760)
	elif 't0_gtcc'     == tech: return (var_o_m[tech] * therm_eff[tech] / fuel_price['nat_gas'] * 8760)
	elif 't0_dt'       == tech: return (var_o_m[tech] * therm_eff[tech] / fuel_price['diesel']  * 8760)
	elif 't0_coal'     == tech: return (var_o_m[tech] * therm_eff[tech] / fuel_price['coal']    * 8760)
	elif 't0_nuclear'  == tech: return (var_o_m[tech] * therm_eff[tech] / fuel_price['uranium'] * 8760)

	D.write( D.INFO, "Technology with no marginal cost: (%s, %d, %d)\n" % (tech, iper, per) )

	return ( 0 )