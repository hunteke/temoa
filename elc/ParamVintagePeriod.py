import debug as D

def VintagePeriodParam_Init ( tech, iper, per, model ):
	D.write( D.INFO, "VintagePeriod parameter initialization: (%s, %d, %d)\n" % (tech, iper, per) )

	if tech in model.tech_life:
		# does this get called len(per)*len(iper)*len(M.tech_life) times? (484 currently)
		tech_life_time = model.tech_life[ tech ].value
	if tech[0:2] == 't0':
		if iper > 2000: return False

	# returns 1 if the technology is still "alive" in this period
	# given an install period (iper).  0 otherwise.
	# this effectively creates a binary matrix
	return ( iper <= per and per < iper + tech_life_time )

