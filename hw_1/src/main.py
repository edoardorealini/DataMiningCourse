from CompareSets import *
from Shingling import *

import time

if __name__ == "__main__":

    cs = CompareSets()
    shs = []

    start_time = time.time()

    for i in range(1,11):
        filename = '../data/' + str(i) + '.txt'
        shs.append(Shingling(filename))
        shs[i-1].load_clean_document()
        start_shingles = time.time()
        shs[i-1].build_shingles(5)
        shs[i-1].hash_shingles()        
        print("----------------------" + str(i) + "---------------------")
        print(len(shs[i-1].hashed_shingles))
        print(len(list(set(shs[i-1].hashed_shingles))))
        print("Shingling time elapsed: " + str(time.time() - start_shingles))

    print("Total elapsed time for shingling: " + str(time.time() - start_time) + "\n\n")

    for i in range(0,9):
    	print("\nJaccard similarity between " + str(i) + " " + str(i+1))
    	print(cs.calculateJaccard(shs[i].hashed_shingles, shs[i+1].hashed_shingles))