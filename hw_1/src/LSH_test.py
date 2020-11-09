from LSH import LSH
from CompareSignatures import *

if __name__ == "__main__":

    signatures = {
        0: [2, 2, 3, 5],
        1: [10, 11, 38, 4],
        2: [2, 2, 0, 5],
        3: [0, 100, 40, 2]
    }


    lsh = LSH(signatures_dict=signatures)

    print("Signatures dict before banding: ", lsh.signatures_dict)

    lsh.find_pairs_over_th(bands=2, similarity_threshold=0.1)

    print("All Candidates: ", lsh.all_candidate_pairs)
    print("Signatures dict after banding: ", lsh.signatures_dict)
    print("Final candidates: ", lsh.final_pairs)

    cs = CompareSignatures()
    similarity = cs.compare_signatures(signatures[0], signatures[2])
    print("Signature similarity 1-3: ", similarity)

