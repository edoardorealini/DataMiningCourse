import time
import random

from multiset import Multiset 
from FlajoletMartin import *
from HyperLogLog import *

def generate_multiset(multiset_len, n_elements):

		multiset = Multiset()

		fill = multiset_len
		while fill > 0:
			random_el = random.randint(0, n_elements)
			#multiplicity_el = random.randint(1, 1 + int(multiset_len / 1000))
			multiplicity_el = 1
			multiset.add(random_el, multiplicity_el)
			fill -= multiplicity_el

		return multiset


if __name__ == '__main__':
	
	multiset_len = 1000
	n_elements = 2**32 - 1
	multiset = generate_multiset(multiset_len, n_elements)

	k = 50
	l = 20
	fm = FlajoletMartin(n_elements, l, k)

	# start = time.time()
	# print("FlajoletMartin cardinality approx: ", fm.estimate_cardinality(list(multiset)))
	# end = time.time()
	# print("Time elapsed: ", round(end-start,3))

	n_buckets = 32
	hyperloglog = HyperLogLog(n_buckets)

	start = time.time()
	print("HyperLogLog cardinality approx: ", hyperloglog.estimate_cardinality(list(multiset)))
	end = time.time()
	print("Time elapsed: ", round(end-start,3))
