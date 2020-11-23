import math 
import random
import statistics
import time

from multiset import Multiset


class FlajoletMartin:

	def __init__(self, n_elements, l_size_group, k_groups):

		# amount of bits to be used (L)
		self.length = math.ceil(math.log2(n_elements))

		self.l = l_size_group
		self.k = k_groups

	# return the index of the LSB starting from 0 (from right) 
	# it is like finding the number of tails 0's 
	def lsb_index(self, element):

		return (element&-element).bit_length()-1


	# hash element mapping element -> [0, 2ˆL - 1]
	def hash_element(self, element):

		a = random.randint(1, 2**self.length - 1)
		b = random.randint(1, 2**self.length - 1)
		return (a * element + b) % (2**self.length - 1)

	# compute the max r(a) seen, hence the max numbers of 0's in the tail
	def calculate_r(self, elements):

		hashed_idx = []
		for element in elements:
			hashed_idx.append(self.lsb_index(self.hash_element(element)))

		return max(hashed_idx)

	# calc_card with improved accuracy
	# use k*l hash functions splitted into k distinct groups, each of size l
	# for each group median of results -> median of l elements
	# then the mean of the k groups to obtain the final estimate
	def calculate_cardinality(self, multiset_elements):

		averages = [0] * self.k
		for k in range(self.k):

			medians = [0] * self.l
			for l in range(self.l):
				medians[l] = self.calculate_r(multiset_elements)
			averages[k] = statistics.median(medians)

		estimate = int(2**statistics.mean(averages))

		return estimate


if __name__ == '__main__':

	start = time.time()

	multiset_len = 1000
	n_elements = 2**32 - 1

	# Multiset generator 
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

	multiset = generate_multiset(multiset_len, n_elements)

	#print("True cardinality: ", len(multiset.keys()))

	fm = FlajoletMartin(n_elements, 50, 20)

	print("FlajoletMartin cardinality approx: ", fm.calculate_cardinality(list(multiset)))

	end = time.time()

	print("Time elapsed: ", round(end-start,3))



	

	
