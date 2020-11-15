import argparse
import itertools
import time

from Apriori import *

if __name__ == '__main__':

	print("A-propri algorithm for computing Association Rules\n")

	parser = argparse.ArgumentParser(description='Parameters')
	parser.add_argument('-k', dest='k_tuples', type=int, help='Number of k-tuples for frequent items', nargs='?', default=4)
	parser.add_argument('-s', dest='support', type=int, help='Support of itemsets', nargs='?', default=1000)
	parser.add_argument('-c', dest='confidence', type=int, help='Confidence of itemsets', nargs='?', default=0.5)

	args = parser.parse_args()

	print("Number of k-tuples: ", args.k_tuples)
	print("Support: ", args.support)
	print("Confidence: ", args.confidence)

	k_tuples = args.k_tuples
	support = args.support
	confidence = args.confidence

	filename = "../data/T10I4D100K.dat"
	apriori = Apriori(filename, support)
	apriori.load_dataset()
	baskets = apriori.baskets
	times = []

	start = time.time()
	print("\nStart Apriori Pipeline\n")

	for i in range(k_tuples):
		if (i == 0):
			start_stage = time.time()
			
			apriori.generate_candidates_ck(baskets, None, 1)
			apriori.filter_candidates(apriori.candidates[i], support)
			
			end_stage = time.time()
			times.append(end_stage - start_stage)
		
		else:
			start_stage = time.time()
			
			apriori.generate_candidates_ck(baskets, apriori.filtered[i-1], i+1)
			apriori.filter_candidates(apriori.candidates[i], support)
			if (i >= 2):
				print("L" + str(i+1) +": ", apriori.filtered[i])

			end_stage = time.time()
			times.append(end_stage - start_stage)

	end = time.time()
	print("\nEnd Apriori Pipeline, time elapsed: ", end - start)

	apriori.candidates_plot(k_tuples)
	apriori.filtered_plot(k_tuples)
	apriori.timelapsed_plot(times, k_tuples)


	# NAIVE BUT WORKING
	# apriori.generate_candidates_ck(baskets, None, 1)
	# apriori.filter_candidates(apriori.candidates[0], args.support)

	# apriori.generate_candidates_ck(baskets, apriori.filtered[0], 2)
	# apriori.filter_candidates(apriori.candidates[1], args.support)

	# apriori.generate_candidates_ck(baskets, apriori.filtered[1], 3)
	# apriori.filter_candidates(apriori.candidates[2], args.support)






	
