import numpy as np
import re
import random
from collections import OrderedDict
import hashlib

class Shingling:    

    def __init__(self, document_filename):
        self.document_filename = document_filename
        self.document_id = None
        self.document = ""
        self.shingles = None
        self.hashed_shingles = None

    def load_clean_document(self):
        with open(self.document_filename) as file:
            self.document_id = self.document_filename[8:10]
            self.document_id = int(self.document_id.replace(".",""))
            text = file.read()
            text = text.lower() # All text to lower cases
            text = text.replace("  ", " ") # Removing useless double spaces
            cleaned_text = re.sub(r'[^\w\s]','', text) # Removing all puncuation
            cleaned_text = cleaned_text.replace('\n', '') # Flattening to 1 line string

            self.document  = cleaned_text

    def load_raw_document(self):
        with open(self.document_filename) as file:
            self.document = file.read()
                
    
    def build_shingles(self, k_length):
        shingles = []

        for i in range(0, len(self.document) - k_length):
            shingles.append((self.document[i : i + k_length]))
   
        self.shingles = list(dict.fromkeys(shingles))
       

    def hash_shingles(self):
        hashed_shingles = []

        for shingle in self.shingles:
            hashed_shingles.append(self.my_hash(shingle))
            
        #self.hashed_shingles = sorted(hashed_shingles)
        self.hashed_shingles = hashed_shingles


    def my_hash(self, shingle):
        hash = hashlib.sha1(shingle.encode("UTF-8")).hexdigest()
        hash = int(hash, 16) % (2**32 - 1)
        return hash
    
    
    """ 
    def hash_ascii(self, shingle):
        a = 50
        b = 25

        sum_ascii = 0

        for char in shingle:
            sum_ascii += ord(char)

        hash_val = (a * sum_ascii + b) % (2**32 - 1)

        return hash_val 
    """    
    