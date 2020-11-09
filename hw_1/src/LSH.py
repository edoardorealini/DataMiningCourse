import hashlib
import itertools
from CompareSignatures import *


class LSH:

    # Expecting shingles_dict a dictionary containing all the documents dignatures
    # The key in the dictionary is the document's code.
    def __init__(self, signatures_dict):
        self.signatures_dict = signatures_dict
        self.signatures_dict_bands = None
        self.all_candidate_pairs = None
        self.final_pairs = None
        self.hashed_bands = None


    # First we have to divide each shingle list into some bands
    def split_bands(self, bands):
        self.signatures_dict_bands = {}

        for signature in self.signatures_dict:
            splitted_list = []
            row_len = len(self.signatures_dict[signature]) / bands
            row_len = int(row_len)

            for i in range(bands):
                splitted_list.append(self.signatures_dict[signature][i * row_len : i * row_len + row_len])

            self.signatures_dict_bands[signature] = splitted_list  

    def my_hash(self, band_value):
        hash = hashlib.sha1(str(band_value).encode("UTF-8")).hexdigest()
        hash = int(hash, 16) % (2**32 - 1)
        return hash

    
    def my_hash_tuples(self, band):
        band_tuple = tuple(band)
        hash_value = hash(band_tuple) % 1039

        return hash_value


    def filter_threshold(self, all_candidate_pairs, similarity_threshold):
        cs = CompareSignatures()
        filtered_pairs = []

        for pair in all_candidate_pairs:
            #print(pair, self.signatures_dict[pair[0]])
            #print(pair, self.signatures_dict[pair[1]])
            print("Similarity of candidates ", pair, cs.compare_signatures(self.signatures_dict[pair[0]], self.signatures_dict[pair[1]]))
            if(cs.compare_signatures(self.signatures_dict[pair[0]], self.signatures_dict[pair[1]])) >= similarity_threshold:
                filtered_pairs.append(pair)

        return filtered_pairs 

    def flat_list(self, input_list):
        # Flattening the list
        flat_list = []
        for sublist in input_list:
            for item in sublist:
                flat_list.append(item)

        # Removing eventual duplicates
        flat_list = list(set(flat_list))

        return flat_list

    # This function generates the list of all candidates pairs.
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
                hashed_band = self.my_hash_tuples(band)

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
                print("Bucket: ", bucket_id, " len: ", len(buckets[bucket_id]))
                if len(buckets[bucket_id]) > 1:
                    candidate_groups.append(buckets[bucket_id]) 
            
            print("Candidate groups: ", candidate_groups)
            # In document_id_groups we have lists of documents that have equal bands
            # From each group we have to generate tuples, and then put them in all_candidate_pairs
            # Creating the lists of candidate pairs
            candidate_pairs = []
            for group in candidate_groups:
                candidate_pairs.append(list(itertools.combinations(group, 2)))
            
            # Removing eventual duplicates and flattening
            flat_candidate_pairs = self.flat_list(candidate_pairs)

            self.all_candidate_pairs.append(flat_candidate_pairs)

            print(buckets)

        self.all_candidate_pairs = self.flat_list(self.all_candidate_pairs)
        
        return self.all_candidate_pairs
    
    def find_pairs_over_th(self, bands, similarity_threshold):
        candidates = self.find_candidates(bands)
        filtered_pairs = self.filter_threshold(candidates, similarity_threshold)

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
                # This assumption is wrong

                #band_value = sum(band)
                #hashed_band = self.my_hash(band_value)

                hashed_band = self.my_hash_tuples(band)
                hashed_bands[band_id].append(hashed_band)

        self.hashed_bands = hashed_bands

        # Now here we have to search for couples inside the hashes_bands dictionary
        # The result of this snippet is creating lists containing the document ids
        # for which the hashed bands are equal
        candidate_groups = []
        for band in hashed_bands:
            document_ids = [(i + 1) for i, el in enumerate(hashed_bands[band]) if hashed_bands[band].count(el) > 1]
            document_ids = list(set(document_ids))
            candidate_groups.append(document_ids)
        
        # Creating the lists of candidate pairs
        candidate_pairs = []
        for group in candidate_groups:
            candidate_pairs.append(list(itertools.combinations(group, 2)))
        #print(candidate_pairs)
        flat_candidate_pairs = []
        for sublist in candidate_pairs:
            for item in sublist:
                flat_candidate_pairs.append(item)
        
        flat_candidate_pairs = list(set(flat_candidate_pairs))
        self.all_candidate_pairs = flat_candidate_pairs

        final_pairs = list(self.filter_threshold(self.all_candidate_pairs, similarity_threshold))        
        self.final_pairs = final_pairs

        return final_pairs

