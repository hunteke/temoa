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

def SetInvestmentPeriod_Init ( model ):
	D.write( D.DEBUG, "InvestmentPeriod set initialization\n" )

	# Creates a list of tuples.  A tuple only goes in the list if the cell
	# it "referenced" in the binary matrix would be 1.  This is implemented
	# this not-immediately-intuitive way for efficiency in the objective
	# function creation, but amounts to the same thing.  See documentation.
	# [Doc ref: ?] XXX TODO

	return [
	  (tech, iper, per)
	  for tech in model.tech_new
	  for iper in model.invest_period
	  for per in model.period
	  if ( iper <= per and per < iper + model.loan_life[tech].value )
	]

