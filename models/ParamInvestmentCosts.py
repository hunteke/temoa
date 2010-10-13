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

def InvestmentCostsParam_Init ( tech, iper, per, model ):
	D.write( D.DEBUG, "InvestmentCosts_Init parameter initialization\n" )

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

	D.write( D.WARN, "Warning: Technology with no investment cost: (%s, %d, %d)\n" % ( tech, iper, per ) )

