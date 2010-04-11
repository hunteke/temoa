def SegmentSet_Init ( model ):
	ans = [
	  '%s %02d:00' % (i, hour)
	  for i in ( 'Spring', 'Summer', 'Fall', 'Winter' )
	  for hour in range(0, 24, 4)
	  #for half in range(0, 60, 30)
	]

	ans = ['Year Round']

	return ans

