import debug as D

def Objective_Rule ( model ):
	""" 
	.. math:: 
		\\begin{eqnarray*}
		\\lefteqn{
		\sum_{per} \sum_{tec} \sum_{iper} \sum_{y=0}^{t(per+1) - t(per)} 
		\\Bigg(
		\\left\\{ 
		c_{i}(tec,iper) 
		* \\frac { r_{i}(tec)} {1-(1+ r_{i}(tec))^{-r_{i}(tec)} }
		* imat(tec,iper,per)  
		+ C_{f}(tec,iper,per) 
		\\right\\} 
		}
		\\\\
		& & 
		\\qquad \\qquad \\qquad \\qquad \\qquad \\qquad
		* x\_cap(tec,iper) 
		+ C_{m}(tec,iper,per) * vmat(tec,iper,per) 
		* x\_util(tec,iper,per) 
		\\Bigg)
		\\\\
		& & 
		\\qquad \\qquad \\qquad \\qquad \\qquad
		* \\frac{1} {(1+r_{g}^{t(per)+y-t(per0)})} 
		\\end{eqnarray*}
		:nowrap:

	**Electricity Sector Model Objective Formulation**

	"""

	"""
	Earlier equation format: 

	.. math:: \sum_{per} \sum_{tec} \sum_{iper} \sum_{y=0}^{t(per+1) - t(per)} ( (c_{i}(tec,iper)*(r_{i}(tec)/1-(1+ r_{i}(tec))^{-r_{i}(tec)})*imat(tec,iper,per)+C_{f}(tec,iper,per)   )*x\_cap(tec,iper) + C_{m}(tec,iper,per)*vmat(tec,iper,per)*x\_util(tec,iper,per) ) * 1/(1+r_{g}^{t(per)+y-t(per0)}
	.. math:: \sum_{p \in operating\_period} \sum_{t \in technologies} \sum_{i \in invest\_period} cost += period\_spread[p] * xc[t,i] * fixed\_costs[t,i,p]
	"""
	D.write( D.INFO, "Objective rule\n" )
	M = model

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

