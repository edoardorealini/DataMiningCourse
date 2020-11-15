import argparse
import itertools
import time

import numpy as np 
import matplotlib.pyplot as plt 

from Apriori import Apriori

if __name__ == '__main__':

	print("A-propri algorithm for computing Association Rules")

	parser = argparse.ArgumentParser(description='Parameters')
	parser.add_argument('-k', dest='k_tuple', type=int, help='Number of k-tuples for frequent items', nargs='?', default=3)
	parser.add_argument('-s', dest='support', type=int, help='Support of itemsets', nargs='?', default=1000)
	parser.add_argument('-c', dest='confidence', type=int, help='Confidence of itemsets', nargs='?', default=0.5)

	args = parser.parse_args()

	print("Number of k-tuples: ", args.k_tuple)
	print("Support: ", args.support)
	print("Confidence: ", args.confidence)
	print("\n")

	filename = "../data/T10I4D100K.dat"
	apriori = Apriori(filename, args.support)
	apriori.load_dataset()
	baskets = apriori.baskets

	apriori.generate_candidates_ck(baskets, None, 1)
	apriori.filter_candidates(apriori.candidates[0], args.support)

	apriori.generate_candidates_ck(baskets, apriori.filtered[0], 2)
	apriori.filter_candidates(apriori.candidates[1], args.support)

	apriori.generate_candidates_ck(baskets, apriori.filtered[1], 3)
	apriori.filter_candidates(apriori.candidates[2], args.support)

	# for el in apriori.candidates:
	# 	print(el)





	
