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

def LoanLifeParam_Init ( tech, model ):
	D.write( D.DEBUG, "LoanLifeParam_Init parameter initialization\n" )

	if   'coal'     == tech: return 20
	elif 'nuclear'  == tech: return 40
	elif 'wind_ons' == tech: return 10
	elif 'solar_pv' == tech: return 15

	return 10

