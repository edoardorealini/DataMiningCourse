from CompareSets import CompareSets
from Shingling import Shingling
from MinHashing import MinHashing
from CompareSignatures import CompareSignatures
from LSH import LSH

import time

if __name__ == "__main__":
    print("Running the full pipeline")

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
        s.build_shingles(k_length=10)
        s.hash_shingles()

        m.compute_signature(n_hash_functions=100, shingles_list=s.hashed_shingles)

        signatures_dict[i + 1] = m.signature
    
    lsh = LSH(signatures_dict=signatures_dict)
    lsh.find_pairs(bands=20, similarity_threshold=0.2)

    print(lsh.final_pairs)

