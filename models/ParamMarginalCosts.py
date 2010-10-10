import debug as D

def MarginalCostsParam_Init ( tech, per, model ):
	D.write( D.INFO, "MarginalCostsParam_Init parameter initialization\n" )
	M = model
	var_o_m = { # $/kWh
	  'coal'        : 0.0459,
	  'geo'         : 0.0000,
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
	  't0_coal'     : 0.0067,
	  't0_dt'       : 0.0350,
	  't0_gt'       : 0.0310,
	  't0_gtcc'     : 0.0052,
	  't0_hydro'    : 0.0140,
	  't0_ng_steam' : 0.0074,
	  't0_nuclear'  : 0.0016,
	  'solar_pv'    : 0.0000,
	  'solar_th'    : 0.0000,
	  'wind_offs'   : 0.0000,
	  'wind_ons'    : 0.0000,
	}
	
	therm_eff = {
	  'coal'        : 0.39,
	  'gt_b'        : 0.40,
	  'gt_s'        : 0.40,
	  'gt_p'        : 0.40,
	  'gtcc_b'      : 0.54,
	  'gtcc_s'      : 0.54,
	  'gtcc_p'      : 0.54,
	  'gtcc_ccs'    : 0.46,
	  'igcc'        : 0.46,
	  'igcc_ccs'    : 0.41,
	  'nuclear'     : 0.33,
	  't0_coal'     : 0.31,
	  't0_dt'       : 0.22,
	  't0_gt'       : 0.25,
	  't0_gtcc'     : 0.37,
	  't0_hydro'    : 0.00,
	  't0_ng_steam' : 0.28,
	  't0_nuclear'  : 0.30,
	}
	if   'coal'        == tech: return (var_o_m[tech] + M.coal_price[per] / therm_eff[tech] * 8760)()
	elif 'geo'			 == tech: return (var_o_m[tech] * 8760)
	elif 'gt_b'        == tech: return (var_o_m[tech] + M.ng_price[per] / therm_eff[tech] * 8760)()
	elif 'gt_s'        == tech: return (var_o_m[tech] + M.ng_price[per] / therm_eff[tech] * 8760)()
	elif 'gt_p'        == tech: return (var_o_m[tech] + M.ng_price[per] / therm_eff[tech] * 8760)()
	elif 'gtcc_b'      == tech: return (var_o_m[tech] + M.ng_price[per] / therm_eff[tech] * 8760)()
	elif 'gtcc_s'      == tech: return (var_o_m[tech] + M.ng_price[per] / therm_eff[tech] * 8760)()
	elif 'gtcc_p'      == tech: return (var_o_m[tech] + M.ng_price[per] / therm_eff[tech] * 8760)()
	elif 'gtcc_ccs'    == tech: return (var_o_m[tech] + M.ng_price[per] / therm_eff[tech] * 8760)()
	elif 'hydro_b'     == tech: return (var_o_m[tech] * 8760)
	elif 'hydro_s'     == tech: return (var_o_m[tech] * 8760)
	elif 'hydro_p'     == tech: return (var_o_m[tech] * 8760)
	elif 'igcc'        == tech: return (var_o_m[tech] + M.coal_price[per] / therm_eff[tech] * 8760)()
	elif 'igcc_ccs'    == tech: return (var_o_m[tech] + M.coal_price[per] / therm_eff[tech] * 8760)()
	elif 'nuclear'     == tech: return (var_o_m[tech] * 8760)
	elif 't0_coal'     == tech: return (var_o_m[tech] + M.coal_price[per] / therm_eff[tech] * 8760)()
	elif 't0_dt'       == tech: return (var_o_m[tech] + M.diesel_price[per] / therm_eff[tech] * 8760)()
	elif 't0_gt'       == tech: return (var_o_m[tech] + M.ng_price[per] / therm_eff[tech] * 8760)()
	elif 't0_gtcc'     == tech: return (var_o_m[tech] + M.ng_price[per] / therm_eff[tech] * 8760)()
	elif 't0_hydro'    == tech: return (var_o_m[tech] * 8760)
	elif 't0_ng_steam' == tech: return (var_o_m[tech] + M.ng_price[per] / therm_eff[tech] * 8760)()
	elif 't0_nuclear'  == tech: return (var_o_m[tech] + M.urn_price[per] / therm_eff[tech] * 8760)()
	elif 'solar_pv'    == tech: return (var_o_m[tech] * 8760)
	elif 'solar_th'    == tech: return (var_o_m[tech] * 8760)
	elif 'wind_offs'   == tech: return (var_o_m[tech] * 8760)
	elif 'wind_ons'    == tech: return (var_o_m[tech] * 8760)

	D.write( D.INFO, "Technology with no marginal cost: (%s, %d, %d)\n" % (tech, per) )

	return ( 0 )
