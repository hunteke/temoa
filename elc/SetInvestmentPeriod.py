import debug as D

def SetInvestmentPeriod_Init ( model ):
	D.write( D.INFO, "InvestmentPeriod set initialization\n" )

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

