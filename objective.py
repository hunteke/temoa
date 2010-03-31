import debug as D

def Objective_Rule ( model ):
	D.write( D.INFO, "Objective rule\n" )
	M = model

	cost = []
#	for t in M.tech_new:
#		for p in M.munge_period:
#			discount = sum(
#			  (1 + M.global_discount_rate.value)**(M.munge_period[0] - y - p)
#			  for y in range(0, M.inter_period[p])
#			)
#			for i in M.invest_period:
#				cost.append( discount * (
#				   M.xc[t, i]
#				 * ( M.investment_costs[t, i, p]
#				   * ( M.discount_rate[ t ]
#				     / (1 - (1 + M.discount_rate[t].value)**(-M.loan_life[t].value ) ) )
#				   * M.investment[t, i, p]
#
#				   + M.fixed_costs[t, i, p] )
#
#				 + M.xu[t, i, p]
#				 * M.marg_costs[t, i, p]
#				))
#	return sum(cost)

	cost = []
	for p in M.munge_period:
		period_spread = sum(
		  (1 + M.global_discount_rate.value)**(M.munge_period[0] - y - p)
		  for y in range(0, M.inter_period[p])
		)
		for t in M.tech_new:
			loan_cost = ( M.discount_rate[ t ] /
			    (1 - (1 + M.discount_rate[t].value)**(-M.loan_life[t].value ) ) )
			for i in M.invest_period:
				cost.append( period_spread * (
				   M.xc[t, i]
				 * ( M.investment_costs[t, i, p]
				   * loan_cost
				   * M.investment[t, i, p]

				   + M.fixed_costs[t, i, p] )
				))
		for t in M.tech_all:
			for i in M.invest_period:
				cost.append( period_spread * (
				 + M.xu[t, i, p]
				 * M.marg_costs[t, i, p]
				))

	return sum(cost)
