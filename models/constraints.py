"""
    TEMOA (Tools for Energy Model Optimization and Analysis)
    Copyright (C) 2010 TEMOA Developer Team

    This file is part of TEMOA.
    TEMOA is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    TEMOA is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with TEMOA.  If not, see <http://www.gnu.org/licenses/>.
"""


import debug as D

def Energy_Demand ( seg, period, model ):
	"""
		Energy Demand Constraint:
		Ensure utility is at least equal to energy demand

		.. math ::
			\sum_{per} \sum_{iper} \sum_{tech\_all} xu(tech,iper,per) * vintage(tech,iper,per) >= energy\_dmd(seg,per)

	"""
	D.write( D.DEBUG, "Energy_Demand: (%s, %d)\n" % (seg, period) )
	M = model
	ans = sum(
	  M.xu[t, i, period] * M.vintage[t, i, period]

	  for t in M.tech_all_by_seg[ seg ]
	  for i in M.invest_period
	)

	return ( ans >= M.energy_dmd[period, seg] )

def Capacity_Req ( seg, period, model ):
	"""
		Capacity requirement

		.. math ::
		   \sum_{per} \sum_{iper} \sum_{tech\_new} xc(tech,iper) * vintage(tech,iper,per) >= power\_dmd(seg,per)

	"""
	D.write( D.DEBUG, "Capacity_Req: (%s, %d)\n" % (seg, period) )
	M = model
	power_production = sum(
	  M.xc[t, i] * M.vintage[t, i, period]

	  for t in M.tech_new_by_seg[ seg ]
	  for i in M.operating_period
	)
	power_production += sum(
		M.t0_capacity[period, t]

		for t in M.tech_existing_by_seg[ seg ]
	)

	return ( power_production >= M.power_dmd[period, seg] )


def Process_Level_Activity ( tech, iper, per, model ):
	"""
		Process Level Activity Constraint

		Utilization < Capacity

	.. math ::
		xu(tech,iper,per) * vintage(tech,iper,per) < xc(tech,iper)

	"""
	D.write( D.DEBUG, "Process_Level_Activity: (%s, %d, %d)\n" % (tech, iper, per) )
	M = model
	utilization = M.xu[tech, iper, per] * M.vintage[tech, iper, per]
	if ( tech in M.tech_new ):
		capacity = M.xc[tech, iper]
	else:
		capacity = M.t0_capacity[per, tech]

	capacity *= M.ratio[ tech ].value * M.cf_max[ tech ]

	return ( utilization < capacity )


def CO2_Emissions_Constraint ( period, model ):
	"""
		CO2 emissions must be less than specified limit.

	.. math ::
		\sum_{tech} \sum_{iper} \sum_{per} xu(tech,iper,per) * vintage(tech,iper,per) * co2\_factors(tech) * 8760 <= co2\_total(per)

	"""
	D.write( D.DEBUG, "CO2_Emissions_Constraint: %d\n" % period )
	M = model
	ans = sum(
	    M.xu[t, i, period]
	  * M.vintage[t, i, period]
	  * M.co2_factors[ t ]
	  * 8760

	  for t in M.tech_all
	  for i in M.operating_period
	)

	return ( ans <= M.co2_tot[period] )


# Constant constraints
def Up_Hydro ( model ):
	"Constraint: Total installed hydro capacity from all periods not to exceed [Doc ref: ?]"
	M = model
	hydro_production = sum(
	  M.xc['hydro_b', i] +
	  M.xc['hydro_s', i] +
	  M.xc['hydro_p', i]

	  for i in M.invest_period
	)

	return ( hydro_production <= M.hydro_max_total )


def Up_Geo ( model ):
	"Constraint: Total installed geothermal capacity from all periods can't exceed 23 GW [Doc ref: ?]"
	M = model
	geo_production = sum( M.xc['geo', i]  for i in M.invest_period )

	return ( geo_production <= M.geo_max_total )


def Up_Winds_Ons ( model ):
	"Constraint: Total installed capacity of on-shore wind power from all periods can't exceed 8 TW [Doc ref: ?]"
	M = model
	wind_onshore_production = sum( M.xc['wind_ons', i]  for i in M.invest_period )

	return ( wind_onshore_production <= M.winds_on_max_total )


def Up_Winds_Offs ( model ):
	"Constraint: Total installed capacity of off-shore wind power from all periods can't exceed 800 GW [Doc ref: ?]"
	M = model
	wind_offshore_production = sum( M.xc['wind_offs', i]  for i in M.invest_period )

	return ( wind_offshore_production <= M.winds_off_max_total )


def Up_Solar_Th ( model ):
	"Constraint: Total installed capacity of thermal solar power from all periods can't exceed 100 GW [Doc ref: ?]"
	M = model
	solar_production = sum( M.xc['solar_th', i]  for i in M.invest_period )

	return ( solar_production <= M.solar_th_max_total )


###############################################################################
#                                 Debugging Constraints                       #
###############################################################################
def Current_Capacity ( seg, per, model ):
	M = model
	power_production = sum(
	  M.xc[t, i]

	  for t in M.tech_new_by_seg[ seg ]
	  for i in M.operating_period
	)
	power_production += sum(
		M.t0_capacity[t, per]

		for t in M.tech_existing_by_seg[ seg ]
	)

	return ( M.curr_capacity[ seg, per ] == power_production )

def Total_Current_Capacity ( per, model ):
	M = model
	total_capacity = sum(
		M.curr_capacity[ s, per ]
		for s in M.segment
	)

	return ( M.total_curr_capacity[ per ] == total_capacity )


def Attach_CO2_seg_per ( seg, per, model ):
	M = model
	co2 = sum(
	    M.xu[t, i, per] * M.vintage[t, i, per]
	  * M.co2_factors[ t ]
	  * 8760

	  for t in M.tech_all_by_seg[ seg ]
	  for i in M.operating_period
	)

	return ( M.CO2_seg_per[seg, per] == co2 )

def Attach_CO2_per ( per, model ):
	M = model
	co2 = sum(
	    M.xu[t, i, per] * M.vintage[t, i, per]
	  * M.co2_factors[ t ]
	  * 8760

	  for t in M.tech_all
	  for i in M.operating_period
	)

	return ( M.CO2_per[ per ] == co2 )
