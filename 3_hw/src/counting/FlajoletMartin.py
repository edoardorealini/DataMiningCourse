import math 
import statistics
import hashlib
import random

class FlajoletMartin:

	def __init__(self, n_elements, l_size_group, k_groups):
		# amount of bits to be used (L)
		self.length = math.ceil(math.log2(n_elements))
		self.l = l_size_group
		self.k = k_groups


	# calc_card with improved accuracy
	# use k*l hash functions splitted into k distinct groups, each of size l
	# for each group median of results -> median of l elements
	# then the mean of the k groups to obtain the final estimate
	def estimate_cardinality(self, multiset_elements):

		averages = [0] * self.k
		for k in range(self.k):

			medians = [0] * self.l
			for l in range(self.l):
				medians[l] = self.calculate_r(multiset_elements)
			averages[k] = statistics.median(medians)

		estimate = int(2**statistics.mean(averages))

		return estimate

	# compute the max r(a) seen, hence the max numbers of 0's in the tail
	def calculate_r(self, elements):

		hashed_idx = []
		for element in elements:
			hashed_idx.append(self.lsb_index(self.hash_element(element)))

		return max(hashed_idx)

	# return the index of the LSB starting from 0 (from right) 
	# it is like finding the number of tails 0's 
	def lsb_index(self, element):
		return (element&-element).bit_length()-1

	# hash element mapping element -> [0, 2ˆL - 1]
	def hash_element(self, element):
		a = random.randint(1, 2**self.length - 1)
		b = random.randint(1, 2**self.length - 1)
		return (a * element + b) % (2**self.length - 1)


	

	
