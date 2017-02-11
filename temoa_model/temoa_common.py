from itertools import product as cross_product, islice, izip

class TemoaError ( Exception ): pass
class TemoaCommandLineArgumentError ( TemoaError ): pass
class TemoaKeyError ( TemoaError ): pass
class TemoaObjectNotFoundError ( TemoaError ): pass
class TemoaFlowError ( TemoaError ): pass
class TemoaValidationError ( TemoaError ): pass
class TemoaNoExecutableError ( TemoaError ): pass
class TemoaInfeasibleError ( TemoaError ): pass

def get_str_padding ( obj ):
	return len(str( obj ))

def iter_in_chunks ( iterable, chunk_size ):
	"""
Group iterable items into chunks.

Given an iterable, e.g. ('a', 1, 'b', 2, 'c', 3), this function converts this
length / chunk_size tuples.  The 'length' in the previous sentence is a
misnomer, however, as this function works with any iterable.

Caveat emptor: with the last example (below), note that incomplete tuples are
   silently discarded.  This function assumes an there are only "complete"
   chunks within the iterable; there are no 'partial chunks'.

For example:

    >>> some_tuple = ('a', 1, 'b', 2, 'c', 3)
    >>> for i in iter_in_chunks( some_tuple, 2 )
    >>>    print i
    ('a', 1)
    ('b', 2)
    ('c', 3)

    >>> for i in iter_in_chunks( some_tuple, 3 )
    >>>    print i
    ('a', 1, 'b')
    (2, 'c', 3)

    >>> for i in iter_in_chunks( some_tuple, 4 )
    >>>    print i
    ('a', 1, 'b', 2)

"""

	return izip( *[islice(iterable, i, None, chunk_size)
	             for i in xrange(chunk_size)] )
