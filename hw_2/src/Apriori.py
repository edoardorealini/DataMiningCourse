import os
import time
import itertools 


def load_data(filename):

	file = open(filename, 'r')

	# list containing baskets as list of lists [[1st basket],[2nd basket]]
	baskets = []
	for line in file: 
		basket = line.split(' ')
		basket.remove('\n')
		basket = list(map(int, basket))
		baskets.append(basket)

	# trial to print first basket
	# print(baskets)
	# to be sure everything is int 
	# print(type(baskets[0][0]))

	# debugging -> 1010228 elements, 870 unique elements
	# print(len(baskets))
	# prova = []
	# for basket in baskets:
	# 	for el in basket:
	# 		prova.append(el)
	# print(len(list(set(prova))))

	return baskets

# generate the C1 
def generate_candidates(baskets):

	candidates = {}

	for basket in baskets:
		for items in basket:
			if candidates.get(items) == None:
					candidates[items] = 1
			else:
				candidates[items] += 1
	
	#print(len(candidates))

	return candidates

# generate the C2 -> next: to integrate with the previous function
def generate_candidates_2(frequent_items, baskets):


	couples = list(itertools.combinations(frequent_items, 2))
	print("couples: ", couples)

	# TODO contare nei baskets quante volte appare la couple

	C2 = {}
	for couple in couples:		
	 	for basket in baskets:
	 		if (set(couple).issubset(basket)):
	 			if C2.get(couple) == None:
	 				C2[couple] = 1
	 			else: 
	 				C2[couple] += 1

	print(C2)




def filter_candidates(candidates, support):

	frequent_items = {}
	for item, occurences in list(candidates.items()):
		if (occurences >= support):
			frequent_items[item] = occurences

	#print(len(frequent_items))
	#print(frequent_items)
	return frequent_items



if __name__ == '__main__':

	filename = '../data/T10I4D100K.dat'
	baskets = load_data(filename)
	C1 = generate_candidates(baskets)
	L1 = filter_candidates(C1, 5000)
	C2 = generate_candidates_2(L1, baskets)

