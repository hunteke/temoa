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

def AnnualCost ( per, model ):
	D.write( D.INFO, "Annual Cost\n" )
	M = model

	cost = 0.0

	for t in M.tech_new:
		for i in M.invest_period:
			if (t, i, per) in M.investment:
				# If we built it in a recent time period, need to finish
				# paying off that loan;
				cost += ( M.period_spread[ per ] *
				  M.xc[t, i]
				  * ( M.investment_costs[t, i, per]
				    * M.loan_cost[ t ]

				    + M.fixed_costs[t, i, per] )
				)
			else:
				# otherwise, if it's still operational, we just need to pay
				# the operating costs (fixed O&M).
				cost += (
				    M.period_spread[ per ]
				  * M.xc[t, i]
				  * M.fixed_costs[t, i, per]
				)

	# Finally, how much did we use?  Have to pay for that too.
	cost += sum( [
	    M.xu[t, i, per]
	  * M.marg_costs[t, per]
	  * M.period_spread[ per ]

	  for i in M.invest_period
	  for t in M.tech_all
	] )

	return cost

