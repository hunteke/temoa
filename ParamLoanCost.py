def ParamLoanCost_Init ( tech, model ):
	M = model
	loan_cost = ( M.discount_rate[ tech ].value /
	    (1 - (1 + M.discount_rate[tech].value)**(-M.loan_life[tech].value ) ) )

	return loan_cost