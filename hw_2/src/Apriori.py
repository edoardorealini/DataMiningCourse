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
			if candidates.get(items) is None:
					candidates[items] = 1
			else:
				candidates[items] += 1
	
	#print(len(candidates))

	return candidates

# generate the C2 -> next: to integrate with the previous function
def generate_candidates_2(frequent_items, baskets):

	start = time.time()

	couples = list(itertools.combinations(frequent_items, 2))
	# print("couples: ", couples)

	# TODO contare nei baskets quante volte appare la couple
	C2 = {}
	
	for couple in couples:		
	 	for basket in baskets:
	 		if all(item in basket for item in couple):
	 			if C2.get(couple) == None:
	 				C2[couple] = 1
	 			else: 
	 				C2[couple] += 1


	# for couple in couples:
 # 		count = 0
 # 		for basket in baskets:
 # 			if sublist(couple, basket):
 # 				count+=1
 # 		C2[couple] = count


	print(C2)
	end = time.time()
	print("Time passed:", end - start)

	return C2

def generate_candidates_V2(frequent_items, baskets):

	start = time.time()

	couples = list(itertools.combinations(frequent_items.keys(), 2))
	print("couples: ", len(couples))

	C2 = {}
	
	for couple in couples:		
	 	for basket in baskets:
	 		if all(item in basket for item in couple):
	 			if C2.get(couple) is None:
	 				C2[couple] = 1
	 			else: 
	 				C2[couple] += 1

	print("C2: ", C2)

	items = set(frequent_items.keys())
	
	intersection_el = items.intersection(set(baskets[0]))
	print("int: ", intersection_el)
	new_dict = list(itertools.combinations(sorted(intersection_el),2))
	print("new_dict:" , new_dict)


def generate_candidates_2Trial(frequent_items, baskets):

    start = time.time()

    C2 = {}
    couples = []

    items = set(frequent_items.keys())
    for basket in baskets:
        elements = items.intersection(set(basket))
        sequence = itertools.combinations(sorted(elements), 2)
        for el in sequence:
            couples.append(el)
            if C2.get(el) is None:
                C2[el] = 1
            else: 
                C2[el] += 1

    #print("C2: ", C2)
    end = time.time()
    print("Time passed:", end - start)
    return C2, couples, items



def filter_candidates(candidates, support):

	frequent_items = {}
	for item, occurences in list(candidates.items()):
		if (occurences >= support):
			frequent_items[item] = occurences

	#print(len(frequent_items))
	#print(frequent_items)
	return frequent_items
	

def sublist(lst1, lst2):
    return set(lst1) <= set(lst2)

if __name__ == '__main__':

	filename = '../data/T10I4D100K.dat'
	baskets = load_data(filename)
	C1 = generate_candidates(baskets)
	L1 = filter_candidates(C1, 5000)
	C2 = generate_candidates_V2(L1, baskets)
	#C2 = generate_candidates_2(L1, baskets)
	#L2 = filter_candidates(C2, 1000)
	#print(L2)

