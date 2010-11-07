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

def VintagePeriodParam_Init ( tech, iper, per, model ):
	from coopr.pyomo.base.numvalue import value as V
	D.write( D.DEBUG, "VintagePeriod parameter initialization: (%s, %d, %d)\n" % (tech, iper, per) )

	if tech in model.tech_life:
		# does this get called len(per)*len(iper)*len(M.tech_life) times? (484 currently)
		tech_life_time = V( model.tech_life[ tech ] )
	if tech[0:2] == 't0':
		if iper > 2000: return False

	# returns 1 if the technology is still "alive" in this period
	# given an install period (iper).  0 otherwise.
	# this effectively creates a binary matrix
	return ( iper <= per and per < iper + tech_life_time )

