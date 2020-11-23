import math 
import random
import statistics
import time
import hashlib
import numpy as np 

from multiset import Multiset



class HyperLogLog:

	def __init__(self, n_buckets):

		# number of bits -> b bits
		self.bits = math.ceil(math.log2(n_buckets))

		# number of registers -> size m of M / p=2^b
		self.num_registers = int(2 ** self.bits)

		# initialization of the counters -> array M
		self.registers = np.zeros(self.num_registers)

		# alpha values from the paper [hyperloog-2007]
		self.alpha = {16: 0.673, 32: 0.697, 64: 0.709}

		# estimated cardinality
		self.E_star = None


	def add(self, elements):

		for element in elements:
			hashed_element = self.hash_element(element)
			index_j = bin(int("0b1", 2) + int(bin(hashed_element)[:self.bits+1], 2))
			index_j = int(index_j, 2)
			# let ρ(s) represent the position of the leftmost 1 (equivalently one plus the length of the initial run of 0’s)
			lsb = bin(hashed_element)[self.bits+1:]
			lsb = int(lsb, 2)
			#self.registers[index_j] = max(self.registers[index_j], 1 + self.lsb_index(int(bin(hashed_element[self.bits+1:])), 2))
			self.registers[index_j] = max(self.registers[index_j], 1 + self.lsb_index(lsb))

	def estimate_cardinality(self):

		# Z = (sum_{j=0}^{p-1} 2^-M[j])^-1 
		Z_estimate = np.sum(np.exp2(-1 * self.registers)) ** -1
		# E = alpha_p * pˆ2
		E_estimate = self.alpha[self.num_registers] * self.num_registers**2 * Z_estimate

		# small range correction case
		if E_estimate <= (5/2) * self.num_registers:
			num_zero_register = self.calculate_zero_registers()
			if (num_zero_register != 0 ):
				E_star = self.small_range_correction(num_zero_register)
			else:
				E_star = E_estimate

		# no correction
		if E_estimate <= (1/30) * 2**32:
			E_star = np.ceil(E_estimate)

		if E_estimate > (1/30) * 2**32: 
			E_star = self.large_range_correction(E_estimate)

		self.E_star = E_star
		return E_star


	# counting zero elements
	def calculate_zero_registers(self):
		non_zeros = np.count_nonzero(self.registers)
		return np.ceil(self.num_registers - non_zeros)

	def small_range_correction(self, num_zero_register):
		return self.num_registers * np.log(self.num_registers/num_zero_register)

	def large_range_correction(self, E_estimate):
		return np.ceil((-2**32) * np.log(1 - (E_estimate/(2*32))))

	# hashing elements D -> {0,1}^32
	def hash_element(self, element):
		return int(hashlib.sha1(str(element).encode('utf-8')).hexdigest(), 16) % (2**32-1)

	def lsb_index(self, element):
		return (element&-element).bit_length()-1

	def prova(self, elements):
		self.add(elements)
		return self.estimate_cardinality()


if __name__ == '__main__':

	start = time.time()

	multiset_len = 5000
	n_elements = 2**32 - 1

	# Multiset generator 
	def generate_multiset(multiset_len, n_elements):

		multiset = Multiset()

		fill = multiset_len
		while fill > 0:
			random_el = random.randint(0, n_elements)
			#multiplicity_el = random.randint(1, 1 + int(multiset_len ** 0.5))
			multiplicity_el = 1
			multiset.add(random_el, multiplicity_el)
			fill -= multiplicity_el

		return multiset

	multiset = generate_multiset(multiset_len, n_elements)

	print("PROVA", len(np.array(list(multiset))))

	hyperloglog = HyperLogLog(32)	
	print("HyperLogLog cardinality approx: ", hyperloglog.prova(np.array(list(multiset))))


	end = time.time()
	print("Time elapsed: ", round(end-start,3))



	

	
