'''
Class CompareSets 
- computes the jaccard similarity between two sets of hashed shingles [integer type]
'''
class CompareSets: 

	# not necessary, I think
	def __init__(self):
		self.set_one = {}
		self.set_two = {}

	def calculateJaccard(self, set_one, set_two):

		set_one = set(set_one)
		set_two = set(set_two)

		intersection_cardinality = len(set_one.intersection(set_two))
		#print(intersection_cardinality)
		union_cardinality = len(set_one.union(set_two))
		#print(union_cardinality)

		jaccard_similarity = round(intersection_cardinality / union_cardinality, 3)

		return jaccard_similarity
