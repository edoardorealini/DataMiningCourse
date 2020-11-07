from CompareSets import *
from Shingling import *
from MinHashing import *
from CompareSignatures import *

import time

if __name__ == "__main__":

    """ 
    cs = CompareSets()
    shs = []

    start_time = time.time()

    for i in range(1,11):
        filename = '../data/' + str(i) + '.txt'
        shs.append(Shingling(filename))
        shs[i-1].load_clean_document()
        start_shingles = time.time()
        shs[i-1].build_shingles(k_length=10)
        shs[i-1].hash_shingles()        
        print("----------------------" + str(i) + "---------------------")
        print(len(shs[i-1].hashed_shingles))
        print(len(list(set(shs[i-1].hashed_shingles))))
        print("Shingling time elapsed: " + str(time.time() - start_shingles))

    print("Total elapsed time for shingling: " + str(time.time() - start_time) + "\n\n")

    for i in range(0,9):
    	print("\nJaccard similarity between " + str(i) + " " + str(i+1))
    	print(cs.calculateJaccard(shs[i].hashed_shingles, shs[i+1].hashed_shingles))

    # MinHashing
    m = MinHashing()
    print(m.compute_signature(100, shs[0].hashed_shingles))

    print(shs[0].build_shingles) 

    """

    s = Shingling("../data/1.txt")
    s.load_clean_document()
    s.build_shingles(5)
    s.hash_shingles()

    s2 = Shingling("../data/2.txt")
    s2.load_clean_document()
    s2.build_shingles(5)
    s2.hash_shingles()

    """     
    sh1 = s.hashed_shingles

    s.build_shingles(10)
    s.hash_shingles()

    sh2 = s.hashed_shingles

    print(sh1 == sh2) 
    """

    m = MinHashing()
    signature_1 = m.compute_signature(n_hash_functions=100, shingles_list=s.hashed_shingles)
    signature2 = m.compute_signature(n_hash_functions=100, shingles_list=s2.hashed_shingles)

    compare_sig = CompareSignatures()
    compare_sets = CompareSets()

    j_sim = compare_sets.calculateJaccard(s.hashed_shingles, s2.hashed_shingles)
    prob_sim = compare_sig.compare_signatures(sig1=signature_1, sig2=signature2)

    # print(s.hashed_shingles)

    print("Jaccard between 1 and 2: {}".format(j_sim))
    print("Probability of similarity between 1 and 2: {}".format(prob_sim))
