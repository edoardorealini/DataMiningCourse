import math 
import numpy as np 
import hashlib

class HyperLogLog:

	def __init__(self, n_buckets):

		# number of bits -> b bits
		self.bits = int(np.ceil(np.log2(n_buckets)))

		# number of registers -> size m/p of M = 2^b
		self.num_registers = int(2 ** self.bits)

		# initialization of the counters -> array M
		self.registers = np.zeros(self.num_registers)

		# alpha values from the paper [hyperloog-2007]
		self.alpha = {16: 0.673, 32: 0.697, 64: 0.709}

		# estimated cardinality
		self.E_star = None

	def estimate_cardinality(self, elements):
		self.add(elements)
		return self.calculate_cardinality()
		

	def add(self, elements):

		for element in elements:
			hashed_element = self.hash_element_md5(element)
			j = hashed_element & (2**self.bits - 1)
			w = hashed_element >> self.bits
			# let ρ(s) represent the position of the leftmost 1 (equivalently one plus the length of the initial run of 0’s)
			self.registers[j] = max(self.registers[j], 1+self.lsb_index(w))

	def calculate_cardinality(self):

		# Z = (sum_{j=0}^{p-1} 2^-M[j])^-1 
		Z_estimate = np.sum(np.exp2(self.registers * -1)) ** -1
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
		# large range correction case
		if E_estimate > (1/30) * 2**32: 
			E_star = self.large_range_correction(E_estimate)

		self.E_star = E_star
		return E_star

	def union(self, hyploglog):
		self.registers = np.maximum(self.registers, hyploglog.registers)

	# counting zero elements
	def calculate_zero_registers(self):
		non_zeros = np.count_nonzero(self.registers)
		return np.ceil(self.num_registers - non_zeros)

	def small_range_correction(self, num_zero_register):
		return self.num_registers * np.log(self.num_registers/num_zero_register)

	def large_range_correction(self, E_estimate):
		return np.ceil((-2**32) * np.log(1 - (E_estimate/(2*32))))

	def lsb_index(self, element):
		return (element&-element).bit_length()-1

	# hashing elements D -> {0,1}^32
	def hash_element_md5(self, element):
		return int(hashlib.md5(str(element).encode('utf-8')).hexdigest(), 16) % (2**32)


