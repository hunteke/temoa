from temoa_model import model
from temoa_lib import temoa_solve, TemoaError

try:
	temoa_solve( model )
except TemoaError, e:
	raise SystemExit( '\n' + str(e) )

