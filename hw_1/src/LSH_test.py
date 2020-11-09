from LSH import LSH

if __name__ == "__main__":

    signatures = {
        0: [2, 2, 3, 5],
        1: [10, 11, 38, 4],
        2: [2, 2, 0, 5],
        3: [0, 100, 40, 2]
    }


    lsh = LSH(signatures_dict=signatures)

    print("Signatures dict before banding: ", lsh.signatures_dict)

    lsh.find_pairs(bands=2, similarity_threshold=0.1)

    print("All Candidates: ", lsh.all_candidate_pairs)
    print("Signatures dict after banding: ", lsh.signatures_dict)
    print("Hashed bands: ", lsh.hashed_bands)
    print("Final candidates: ", lsh.final_pairs)

