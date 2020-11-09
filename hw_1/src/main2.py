import argparse

from CompareSets import CompareSets
from Shingling import Shingling
from MinHashing import MinHashing
from CompareSignatures import CompareSignatures
from LSH import LSH

import time

if __name__ == "__main__":
    print("Running the full pipeline")

    parser = argparse.ArgumentParser(description='Parameters')
    parser.add_argument('-ks', dest='k_shingles', type=int, help='Dimension of Shingles',  nargs='?', default=10)
    parser.add_argument('-nhf', dest='n_hash_functions', type=int, help='Number of hash functions to use for MinHashing',  nargs='?', default=100)
    parser.add_argument('-b', dest='bands', type=int, help='Bands for LSH procedure',  nargs='?', default=20)
    parser.add_argument('-st', dest='similarity_threshold', type=float, help='Similarity threshold for LSH procedure',  nargs='?', default=0.5)

    args = parser.parse_args()

    print("With parameters: ")
    print("Shingle dimension: ", args.k_shingles)
    print("MinHash # functions: ", args.n_hash_functions)
    print("Number of bands: ", args.bands)
    print("Similarity threshold: ", args.similarity_threshold)

    file_names = []
    for i in range(1, 13):
        file_name = "../data/" + str(i) + ".txt"
        file_names.append(file_name)
    
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
    print("\nAll Candidates: ", lsh.all_candidate_pairs)
    print("\nSignatures dict after banding: ", lsh.signatures_dict)
     
    """
    print("\nHashed bands: ", lsh.hashed_bands)
    print("\nAll Candidates: ", lsh.all_candidate_pairs)
    print("\nFinal candidates: ", lsh.final_pairs)

