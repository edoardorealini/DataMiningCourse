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
        shs[i-1].build_shingles(5)
        shs[i-1].hash_shingles()
        print("----------------------" + str(i) + "---------------------")
        print(len(shs[i-1].hashed_shingles))
        print(len(list(set(shs[i-1].hashed_shingles))))

    print("elapsed time " + str(time.time() - start_time))

    for i in range(0,9):
    	print("jaccard similarity tra " + str(i) + " " + str(i+1))
    	print(cs.calculateJaccard(shs[i].hashed_shingles, shs[i+1].hashed_shingles))
