import hashlib
import itertools
from CompareSignatures import *


class LSH:
    
    # Expecting shingles_dict a dictionary containing all the documents dignatures
    # The key in the dictionary is the document's code.
    def __init__(self, signatures_dict):
        self.signatures_dict = signatures_dict
        self.all_candidate_pairs = None
        self.final_pairs = None


    # First we have to divide each shingle list into some bands
    def split_bands(self, bands):
        for signature in self.signatures_dict:
            splitted_list = []
            row_len = len(self.signatures_dict[signature]) / bands
            row_len = int(row_len)

            for i in range(bands):
                splitted_list.append(self.signatures_dict[signature][i * row_len : i * row_len + row_len])

            self.signatures_dict[signature] = splitted_list  

    def my_hash(self, band_value):
        hash = hashlib.sha1(str(band_value).encode("UTF-8")).hexdigest()
        hash = int(hash, 16) % (2**32 - 1)
        return hash


    def filter_threshold(self, all_candidate_pairs, similarity_threshold):
        cs = CompareSignatures()

        filtered_pairs = []

        for pair in all_candidate_pairs:
            if(cs.compare_signatures(self.signatures_dict[pair[0]], self.signatures_dict[pair[1]])) >= similarity_threshold:
                filtered_pairs.append(pair)

        self.final_pairs = filtered_pairs

        return filtered_pairs 


    def find_pairs(self, bands, similarity_threshold):
        self.split_bands(bands)
        # Now the attribute signatures_dict is splittend in bands.
        # We have to keep the hash results for each band. 
        # Dictionary: keys = bands ; values = lists of hash values.
        # The position of the value represents the document from which the band is coming from 

        hashed_bands = {}
        for band_id in range(bands):
            hashed_bands[band_id] = []

        # Iterating over the bands
        for band_id in range(bands):

            for signature in self.signatures_dict:
                band = self.signatures_dict[signature][band_id] # Band is now a list 
                # Here we have to hash the list. 
                # We can do that by summing the elements in the list and hashing them
                band_value = sum(band)
                hashed_band = self.my_hash(band_value)
                hashed_bands[band_id].append(hashed_band)

        # Now here we have to search for couples inside the hashes_bands dictionary
        # The result of this snippet is creating lists containing the document ids
        # for which the hashed bands are equal
        candidate_groups = []
        for band in hashed_bands:
            pairs = [(i + 1) for i, el in enumerate(hashed_bands[band]) if hashed_bands[band].count(el) > 1]
            candidate_groups.append(pairs)
        
        # Creating the lists of candidate pairs
        candidate_pairs = []
        for group in candidate_groups:
            candidate_pairs.append(list(itertools.combinations(group, 2)))
        print(candidate_pairs)
        flat_candidate_pairs = []
        for sublist in candidate_pairs:
            for item in sublist:
                flat_candidate_pairs.append(item)

        self.all_candidate_pairs = flat_candidate_pairs

        return self.filter_threshold(self.all_candidate_pairs, similarity_threshold)

