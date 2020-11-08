# https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csc_matrix.html#scipy.sparse.csc_matrix
import random

class MinHashing:

    def __init__(self):
        self.signature = None

    def hash_function(self, value, a, b):
        return (a*value + b) % (2**32 - 1)
        
    def compute_signature(self, n_hash_functions, shingles_list):
        a = list(range(0, n_hash_functions))
        b = list(range(0, n_hash_functions))
        b.sort(reverse=True)
        
        signature = []

        for i in range(n_hash_functions):
            hashed_values = []
            for shingle in shingles_list:
                hashed_values.append(self.hash_function(shingle, a[i], b[i]))
            signature.append(min(hashed_values))
            hashed_values.clear()

        self.signature = signature

        """
        for shingle in shingles_list:

        
         
        for shingle in shingles_list[:n_hash_functions]:
            hashed_values = []

            for i in range(n_hash_functions):
                hashed_val = self.hash_function(shingle, a[i], b[i])
                hashed_values.append(hashed_val)

            signature.append(min(hashed_values))

        # self.signature = signature 
        
        
        for i in range(n_hash_functions):

            min_hash = 100000000073

            for shingle in shingles_list:
                hashed_val = self.hash_function(shingle, a[i], b[i])
                if hashed_val < min_hash:
                    min_hash = hashed_val

            signature.append(min_hash)
        """
