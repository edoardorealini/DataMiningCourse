import argparse
import itertools
import time

from CompareSets import CompareSets
from Shingling import Shingling
from MinHashing import MinHashing
from CompareSignatures import CompareSignatures
from LSH import LSH


if __name__ == "__main__":
    print("Testing and showing the LSH pipeline with parameters")

    parser = argparse.ArgumentParser(description='Parameters')
    parser.add_argument('-ks', dest='k_shingles', type=int, help='Dimension of Shingles',  nargs='?', default=5)
    parser.add_argument('-nhf', dest='n_hash_functions', type=int, help='Number of hash functions to use for MinHashing',  nargs='?', default=100)
    parser.add_argument('-b', dest='bands', type=int, help='Bands for LSH procedure',  nargs='?', default=25)
    parser.add_argument('-st', dest='similarity_threshold', type=float, help='Similarity threshold for LSH procedure',  nargs='?', default=0.1)

    args = parser.parse_args()

    print("Shingle dimension: ", args.k_shingles)
    print("MinHash # functions: ", args.n_hash_functions)
    print("Number of bands: ", args.bands)
    print("Similarity threshold: ", args.similarity_threshold)

    # load file and create Shingling objects
    file_list = []
    shingling_objects = []
    for i in range(1, 11):
        filename = "../data/" + str(i) + ".txt"
        file_list.append(filename)
        shingling_objects.append(Shingling(filename))

    # create shingles and hashed shingles for each document 
    for shingling in shingling_objects:
        #print(shingle.document_filename)
        shingling.load_clean_document()
        shingling.build_shingles(k_length = args.k_shingles)
        shingling.hash_shingles()

    c_set = CompareSets()
    c_sign = CompareSignatures()

    # jaccard all possible pairs 
    pairs = list(itertools.combinations(shingling_objects, 2))

    start_time = time.time()

    jaccard_list = []
    for i in range(len(pairs)): 
        jaccard_list.append(c_set.calculateJaccard(pairs[i][0].hashed_shingles, pairs[i][1].hashed_shingles)) 
        print("Jaccard Similarity between " + str(pairs[i][0].document_id) + " and " + str(pairs[i][1].document_id) + ": " + str(jaccard_list[i]))

    jaccard_filtered = []
    for i in range(len(jaccard_list)):
        if jaccard_list[i] >= args.similarity_threshold:
            jaccard_filtered.append(tuple((pairs[i][0].document_id, pairs[i][1].document_id)))

    print("Filtered couples over Threshold - Jaccard: " , jaccard_filtered)

    end_time = time.time()
    print("Time Elapsed Jaccard: ", end_time - start_time)

    minhashing_objects = []
    for i, shingling in enumerate(shingling_objects):
        minhashing_objects.append(MinHashing())
        minhashing_objects[i].compute_signature(args.n_hash_functions, shingling.hashed_shingles)

    pairs_minh = list(itertools.combinations(minhashing_objects, 2))

    start_time_minh = time.time()

    minhashing_list = []
    for i in range(len(pairs_minh)):
        minhashing_list.append(c_sign.compare_signatures(pairs_minh[i][0].signature, pairs_minh[i][1].signature))
        print("Signature Similarity between " + str(pairs[i][0].document_id) + " and " + str(pairs[i][1].document_id) + ": " + str(minhashing_list[i]))

    minhashing_filtered = []
    for i in range(len(minhashing_list)):
        if minhashing_list[i] >= args.similarity_threshold:
            minhashing_filtered.append(tuple((pairs[i][0].document_id, pairs[i][1].document_id)))

    print("Filtered couples over Threshold - MinHashing: " , minhashing_filtered)

    end_time_minh = time.time()
    print("Time Elapsed MinHashing: ", end_time_minh - start_time_minh)

    signature_dict = {}

    for i, minhashing in enumerate(minhashing_objects):
        signature_dict[i + 1] = minhashing.signature

    lsh = LSH(signature_dict)
    lsh.find_pairs(args.bands, args.similarity_threshold)

    print(signature_dict)

    print("Final Candidates: ", lsh.final_pairs)


    #for pair in pairs:
     #   print("Jaccard similarity: " + str(pair.document_filename) +)

    """
    c_set = CompareSets()
    
    

    
    signatures_dict = {}

    c_sig = CompareSignatures()
    c_set = CompareSets()
    m = MinHashing()

    for i, file in enumerate(file_names):
        s = Shingling(file)
        s.load_clean_document()
        s.build_shingles(k_length=args.k_shingles)
        s.hash_shingles()

        m.compute_signature(n_hash_functions=args.n_hash_functions, shingles_list=s.hashed_shingles)

        signatures_dict[i + 1] = m.signature
    

    lsh = LSH(signatures_dict=signatures_dict)

    #print("Signatures dict before banding: ", lsh.signatures_dict)

    lsh.find_pairs(bands=args.bands, similarity_threshold=args.similarity_threshold)
    """

    """ 
    print("\nAll Candidates: ", lsh.all_candidate_pairs)
    print("\nSignatures dict after banding: ", lsh.signatures_dict)
     
    
    print("\nHashed bands: ", lsh.hashed_bands)
    print("\nAll Candidates: ", lsh.all_candidate_pairs)
    print("\nFinal candidates: ", lsh.final_pairs)
    """

