def SliceSet_Init ( model ):
	ans = []
	ans.extend( [ i for i in model.b_slice ] ) # base
	ans.extend( [ i for i in model.s_slice ] ) # shoulder
	ans.extend( [ i for i in model.p_slice ] ) # peak

	return ans