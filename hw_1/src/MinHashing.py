# https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csc_matrix.html#scipy.sparse.csc_matrix
import random

class MinHashing:

    def __init__(self):
        self.signature = None

    def hash_function(self, value, a, b):
        return (a*value + b) % 100000049 # Big prime number to avoid collisions

    
    def compute_signature(self, n_hash_functions, shingles_list):
        a = list(range(1, n_hash_functions + 1))
        b = list(range(1, n_hash_functions + 1))
        b.sort(reverse=True)
        
        signature = []
        
        """ 
        for shingle in shingles_list[:n_hash_functions]:
            hashed_values = []

            for i in range(n_hash_functions):
                hashed_val = self.hash_function(shingle, a[i], b[i])
                hashed_values.append(hashed_val)

            signature.append(min(hashed_values))

        self.signature = signature 
        """
        
        for i in range(n_hash_functions):

            min_hash = 100000049

            for shingle in shingles_list:
                hashed_val = self.hash_function(shingle, a[i], b[i])
                if hashed_val < min_hash:
                    min_hash = hashed_val

            signature.append(min_hash)

        return signature   
