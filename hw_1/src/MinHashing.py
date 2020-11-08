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
            min_hash = (2**32 - 1)

            for shingle in shingles_list:
                hash_value = self.hash_function(shingle, a[i], b[i])
                
                if hash_value < min_hash:
                    min_hash = hash_value

            signature.append(min_hash)
            
        self.signature = signature
        
