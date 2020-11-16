import argparse
import itertools
import time

from Apriori import *
from AssociationRules import *


if __name__ == '__main__':

	print("A-propri algorithm for Association Rule Mining")
	print("Adriano Mundo & Edoardo Realini")
	print("KTH Royal Insitute of Technology - 2020\n")

	parser = argparse.ArgumentParser(description='Parameters')
	parser.add_argument('-k', dest='k_tuples', type=int, help='Number of k-tuples for building frequent itemsets', nargs='?', default=4)
	parser.add_argument('-s', dest='support', type=int, help='Support threshold for filtering itemsets', nargs='?', default=1000)
	parser.add_argument('-c', dest='confidence', type=int, help='Confidence threshold for association rules filtering', nargs='?', default=0.8)
	parser.add_argument('-p', dest='plot', type=bool, help='Set to True to show interesting plots', nargs='?', default=False)

	args = parser.parse_args()

	print("Parameter values:")
	print("Number of k-tuples: ", args.k_tuples)
	print("Support: ", args.support)
	print("Confidence threshold: ", args.confidence)
	print("Plotting: ", args.plot)

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
			if (i >= 1):
				print("L" + str(i+1) +": ", apriori.filtered[i])

			end_stage = time.time()
			times.append(end_stage - start_stage)

	end = time.time()
	print("\nEnd Apriori Pipeline, time elapsed: ", end - start, " sec.")

	#print(apriori.filtered)

	rule_generator = AssociationRules(apriori.filtered)
	start = time.time()
	rules = rule_generator.generate_all_rules(args.confidence)
	end = time.time()
	elapsed_time = end - start

	print("\n\nAssociation rules generation \nConfidence threshold set to: ", args.confidence)
	print("\n\tRule \t\t Confidence\n")
	for rule in rules:
		print(" {} --> {}  \t{}".format(rule[0], rule[1], rule[2]))

	print("\nElapsed time for rule generation: ", elapsed_time, " sec.")

	if args.plot:
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

