import debug as D

def InvestmentPeriodParam_Init ( tech, iper, per, model ):
	D.write( D.INFO, "InvestmentPeriod parameter initialization\n" )
	loan_life_time = 10
	if tech in model.loan_life:
		loan_life_time = model.loan_life[ tech ].value

	# returns 1 if the loan for the tech is active for the current period, 
	# given an investment period (iper). 0 otherwise
	# this effectively creates a binary matrix
	return ( iper <= per and per < iper + loan_life_time )

