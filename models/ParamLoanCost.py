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

def ParamLoanCost_Init ( tech, model ):
	from coopr.pyomo.base.numvalue import value as V
	D.write( D.DEBUG, "ParamLoanCost_Init parameter initialization: (%s)\n" % tech )

	M = model
	loan_cost = ( V(M.discount_rate[ tech ]) /
	    (1 - (1 + V(M.discount_rate[tech]) )**(-V(M.loan_life[tech]) ) )
	)

	return loan_cost

