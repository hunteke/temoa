import debug as D

def Objective_Rule ( model ):
	D.write( D.INFO, "Objective rule\n" )
	M = model

	# This is another test comment
	# This is another test comment
	# This is another test comment
	cost = 0.0
	for p in M.operating_period:
		for t in M.tech_new:
			for i in M.invest_period:
				if (t, i, p) in M.investment:
					cost += ( M.period_spread[ p ] *
					  M.xc[t, i]
					  * (  M.investment_costs[t, i, p]
					     * M.loan_cost[ t ]

					     + M.fixed_costs[t, i, p] )
					)
				else:
					cost += (
					    M.period_spread[ p ]
					  * M.xc[t, i]
					  * M.fixed_costs[t, i, p]
					)

		cost += sum( [
		    M.xu[t, i, p]
		  * M.marg_costs[t, i, p]
		  * M.period_spread[ p ]

		  for i in M.invest_period
		  for t in M.tech_all
		] )

	return cost

