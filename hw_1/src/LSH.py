import hashlib
import itertools
from CompareSignatures import *


class LSH:

    # Expecting shingles_dict a dictionary containing all the documents signatures
    # The key in the dictionary is the document's code
    # The values are lists representing the signatures
    def __init__(self, signatures_dict):
        # Initializing the attributes

        # signatures_dict: contains the signatures given in input
        self.signatures_dict = signatures_dict

        # signatures_dict_bands will contain the signatures after the split_bands procedure 
        self.signatures_dict_bands = None

        # all_candidate_pairs will contain all the pairs that are found with LSH technique
        self.all_candidate_pairs = None

        # final_pairs will contain the final filtered pairs according to the similarity threshold given as input
        self.final_pairs = None
        

    # Input: number of bands
    # Oputput: fills the attribute signatures_dict_bands with the signatures splitted in sublists
    # each sublist in the signature list is a band.
    # the function also returns the resulting dictionary 
    # Controls: the function checks if the number of requested bands is actually feasible. Otherwise launches an exception.
    def split_bands(self, bands):
        self.signatures_dict_bands = {}

        # Exception if the number of bands is not compatible with the cardinality of the signature 
        if len(self.signatures_dict[1]) % bands != 0:
            raise Exception("\n\nError: number of bands = " + str(bands) + " is not compatible with the cardinality of the signature = " + str(len(self.signatures_dict[1])))

        for signature in self.signatures_dict:
            splitted_list = []
            row_len = len(self.signatures_dict[signature]) / bands
            row_len = int(row_len)

            # Splitting the signature into bands of row_len length
            for i in range(bands):
                splitted_list.append(self.signatures_dict[signature][i * row_len : i * row_len + row_len])

            self.signatures_dict_bands[signature] = splitted_list  
        
        return self.signatures_dict_bands

    # Method specifically defined for the hashing of the band
    # Input: band in form of list of integers, bucket quantity
    # Output: the hased value of the band
    def my_hash(self, band, buckets):
        band_tuple = tuple(band)
        hash_value = hash(band_tuple) % buckets

        return hash_value

    
    # Util method that flattens a list given in input
    def flat_list(self, input_list):
        # Flattening the list
        flat_list = []
        for sublist in input_list:
            for item in sublist:
                flat_list.append(item)

        # Removing eventual duplicates
        flat_list = list(set(flat_list))

        return flat_list


    # This method generates the list of all candidates pairs.
    # In this case we hash the bands and put it into buckets.
    # Buckets: dictionary where the key is the hash and the value is the list of documents that
    # ended in such bucket.
    # From this last dictionary we pick the lists that have length > 2, and generate the pairs as tuples
    # This operations have to be done separately per each band!
    def find_candidates(self, bands):
        self.all_candidate_pairs = []

        # Splitting the original dictionary of signatures into bands.
        self.split_bands(bands)

        # Now for each band in the signatures we have to search for pairs with the hash method
        for band_id in range(bands):
            buckets = {}

            # Now we iterate over the signatures and pick only the band with id = band_id
            for signature_id in self.signatures_dict_bands:
                band = self.signatures_dict_bands[signature_id][band_id]
                hashed_band = self.my_hash(band=band, buckets=1039)

                # Handling the case in which the bucket does not still exists
                if buckets.get(hashed_band) is None:
                    buckets[hashed_band] = []
                    # Appending the value of the document that hashed in the bucket
                    buckets[hashed_band].append(signature_id)
                
                else:
                    buckets[hashed_band].append(signature_id)

            # Here we have to search for pairs
            # We do that by filtering only the lists in bucket dictionary that have length > 2
            candidate_groups = []
            for bucket_id in buckets:
                if len(buckets[bucket_id]) > 1:
                    candidate_groups.append(buckets[bucket_id]) 
            
            # In document_id_groups we have lists of documents that have equal bands
            # From each group we have to generate tuples, and then put them in all_candidate_pairs
            # Creating the lists of candidate pairs
            candidate_pairs = []
            for group in candidate_groups:
                candidate_pairs.append(list(itertools.combinations(group, 2)))
            
            # Removing eventual duplicates and flattening
            flat_candidate_pairs = self.flat_list(candidate_pairs)

            # Adding the candidate pairs to the complete list in attribute all_candidate_pairs
            self.all_candidate_pairs.append(flat_candidate_pairs)

        self.all_candidate_pairs = self.flat_list(self.all_candidate_pairs)
        
        return self.all_candidate_pairs


    # This method filters all the found candidate pairs by means of a given similarity threshold
    # Input: the list of all the candidate pairs found by the function find_candidates,
    # the similarity_threshold value given in input
    # Output: a list of filtered pairs by similarity
    def filter_threshold(self, all_candidate_pairs, similarity_threshold):
        cs = CompareSignatures()
        filtered_pairs = []

        for pair in all_candidate_pairs:
            if(cs.compare_signatures(self.signatures_dict[pair[0]], self.signatures_dict[pair[1]])) >= similarity_threshold:
                filtered_pairs.append(pair)

        return filtered_pairs 

    # Main method of the class.
    # Given the number of bands: bands and the similarity threshold returns the filtered list of pairs
    # These pairs are found with LSH and filtered according to the similarity threshold given as input
    def find_pairs(self, bands, similarity_threshold):
        candidates = self.find_candidates(bands)
        filtered_pairs = self.filter_threshold(candidates, similarity_threshold)

        self.final_pairs = filtered_pairs
        return filtered_pairs

