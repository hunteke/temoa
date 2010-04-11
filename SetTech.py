def TechSet_Init ( model ):
	ans = []
	ans.extend( [ i for i in model.tech_base ] )
	ans.extend( [ i for i in model.tech_shoulder ] )
	ans.extend( [ i for i in model.tech_peak ] )

	return ans

