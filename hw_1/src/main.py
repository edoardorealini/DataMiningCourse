from CompareSets import *
from Shingling import *
from MinHashing import *
from CompareSignatures import *

import time

if __name__ == "__main__":

    
    filename = '../data/1.txt'
    shingling = Shingling(filename)
    shingling.load_clean_document()
    shingling.build_shingles(6)
    shingling.hash_shingles()
    #print(shingling.shingles)

    filename2 = '../data/2.txt'
    shingling2 = Shingling(filename2)
    shingling2.load_clean_document()
    shingling2.build_shingles(6)
    shingling2.hash_shingles()
    #print("start second")
    #print(shingling2.shingles)

    m = MinHashing()
    m.compute_signature(100,shingling.hashed_shingles)
    print(m.signature)

    print("--------------------------------------")

    m2 = MinHashing()
    m2.compute_signature(100,shingling2.hashed_shingles)
    print(m2.signature)   

    cs = CompareSets()
    print("\n\nJaccard Similiarity is: ")
    print(cs.calculateJaccard(shingling.hashed_shingles, shingling2.hashed_shingles))
  
    csign = CompareSignatures()
    print("Signature Similiarity is: ")
    print(csign.compare_signatures(m.signature, m2.signature))

    
    """
    cs = CompareSets()
    shs = []

    start_time = time.time()

    for i in range(1,13):
        filename = '../data/' + str(i) + '.txt'
        shs.append(Shingling(filename))
        shs[i-1].load_clean_document()
        start_shingles = time.time()
        shs[i-1].build_shingles(k_length=5)
        shs[i-1].hash_shingles()        
        print("----------------------" + str(i) + "---------------------")
        print(len(shs[i-1].hashed_shingles))
        print(len(list(set(shs[i-1].hashed_shingles))))
        print("Shingling time elapsed: " + str(time.time() - start_shingles))

    print("Total elapsed time for shingling: " + str(time.time() - start_time) + "\n\n")

    for i in range(0,11):
    	print("\nJaccard similarity between " + str(i+1) + " " + str(i+2))
    	print(cs.calculateJaccard(shs[i].hashed_shingles, shs[i+1].hashed_shingles))
    """
    
    # MinHashing
    #m = MinHashing()
    #m.compute_signature(100, shs[0].hashed_shingles)
    #print(m.signature)

    
    """
    s = Shingling("../data/1.txt")
    s.load_clean_document()
    s.build_shingles(5)
    s.hash_shingles()

        
    sh1 = s.hashed_shingles

    s.build_shingles(10)
    s.hash_shingles()

    sh2 = s.hashed_shingles

    print(sh1 == sh2) 
    

    m = MinHashing()
    print(m.compute_signature(n_hash_functions=100, shingles_list=s.hashed_shingles))
    """