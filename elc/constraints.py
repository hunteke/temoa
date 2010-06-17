import debug as D

def Energy_Demand ( seg, period, model ):
	"""
		Energy Demand Constraint: 
		Ensure utility is at least equal to energy demand

		.. math ::
			\sum_{per} \sum_{iper} \sum_{tech_all} xu(tech,iper,per) * vintage(tech,iper,per) >= energy_dmd(seg,per)

	"""
	D.write( D.INFO, "Energy_Demand: (%s, %d)\n" % (seg, period) )
	M = model
	ans = sum(
	  M.xu[t, i, period] * M.vintage[t, i, period]

	  for t in M.tech_all_by_seg[seg]
	  for i in M.invest_period
	)

	return ( ans >= M.energy_dmd[seg, period] )

def Capacity_Req ( seg, period, model ):
	"""
		Capacity requirement

		.. math ::
		   \sum_{per} \sum_{iper} \sum_{tech_new} xc(tech,iper) * vintage(tech,iper,per) >= power_dmd(seg,per)

	"""
	D.write( D.INFO, "Capacity_Req: (%s, %d)\n" % (seg, period) )
	M = model
	ans = sum(
	  M.xc[t, i] * M.vintage[t, i, period]

	  for t in M.tech_new_by_seg[seg]
	  for i in M.invest_period
	)
	return ( ans >= M.power_dmd[seg, period] )


def Process_Level_Activity ( tech, iper, per, model ):
	"""
		Process Level Activity Constraint

		Utilization < Capacity

	.. math ::
		xu(tech,iper,per) * vintage(tech,iper,per) < xc(tech,iper)	

	"""
	D.write( D.INFO, "Process_Level_Activity: (%s, %d, %d)\n" % (tech, iper, per) )
	M = model
	utilization = M.xu[tech, iper, per] * M.vintage[tech, iper, per]
	if ( tech in M.tech_new ):
		capacity = M.xc[tech, iper]
	else:
		if   tech == 't0_ng_steam' : capacity = 120
		elif tech == 't0_dt'       : capacity =  25
		elif tech == 't0_gt'       : capacity =  67
		elif tech == 't0_gtcc'     : capacity =  36
		elif tech == 't0_hydro'    : capacity =  78
		elif tech == 't0_coal'     : capacity = 308
		elif tech == 't0_nuclear'  : capacity = 100
		else:
			print "Whoops: unknown tech: ", tech

	capacity *= M.ratio[ tech ].value * M.cf_max[ tech ].value

	return ( utilization < capacity )


def CO2_Emissions_Constraint ( period, model ):
	"""
		CO2 emissions must be less than specified limit.

	.. math ::
		\sum_{tech} \sum_{iper} \sum_{per} xu(tech,iper,per) * vintage(tech,iper,per) * co2\_factors(tech) * 8760 <= co2\_total(per)

	"""
	D.write( D.INFO, "CO2_Emissions_Constraint: %d\n" % period )
	M = model
	ans = sum(
	    M.xu[t, i, period]
	  * M.vintage[t, i, period]
	  * M.co2_factors[ t ]
	  * 8760

	  for t in M.tech_all
	  for i in M.invest_period
	)

	return ( ans <= M.co2_tot[period] )


# Constant constraints
def Up_Hydro ( model ):
	"Constraint: Total installed hydro capacity from all periods not to exceed [Doc ref: ?]"
	M = model
	ans = sum(
	  M.xc['hydro_b', i] +
	  M.xc['hydro_s', i] +
	  M.xc['hydro_p', i]

	  for i in M.invest_period
	)

	return ( 0 <= ans and ans <= M.hydro_max_total )


def Up_Geo ( model ):
	"Constraint: Total installed geothermal capacity from all periods can't exceed 23 GW [Doc ref: ?]"
	M = model
	ans = sum( M.xc['geo', i]  for i in M.invest_period )

	return ( 0 <= ans and ans <= M.geo_max_total )


def Up_Winds_Ons ( model ):
	"Constraint: Total installed capacity of on-shore wind power from all periods can't exceed 8 TW [Doc ref: ?]"
	M = model
	ans = sum( M.xc['wind_ons', i]  for i in M.invest_period )

	return ( 0 <= ans and ans <= M.winds_on_max_total )


def Up_Winds_Offs ( model ):
	"Constraint: Total installed capacity of off-shore wind power from all periods can't exceed 800 GW [Doc ref: ?]"
	M = model
	ans = sum( M.xc['wind_offs', i]  for i in M.invest_period )

	return ( 0 <= ans and ans <= M.winds_off_max_total )


def Up_Solar_Th ( model ):
	"Constraint: Total installed capacity of thermal solar power from all periods can't exceed 100 GW [Doc ref: ?]"
	M = model
	ans = sum( M.xc['solar_th', i]  for i in M.invest_period )

	return ( 0 <= ans and ans <= M.solar_th_max_total )

