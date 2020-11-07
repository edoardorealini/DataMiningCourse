'''
Shingling Class Methods:
- Load document
- Clean up of the document from useless characters such as parentheses, commas ...
- Building fo the k-shingles from the document
- Compute the hash values for each shingle and order the set of unique shingles

Shingling Class Attributes:
- Document
- Shingles set
- Hashed shingles set

'''

import numpy as np
import re

class Shingling:    

    def __init__(self, document_filename):
        self.document_filename = document_filename
        self.document = ""
        self.shingles = None
        self.hashed_shingles = None

    def load_clean_document(self):
        with open(self.document_filename) as file:
            text = file.read()
            text = text.lower()
            text = text.replace("  ", " ")
            cleaned_text = re.sub(r'[^\w\s]','', text)
            cleaned_text = cleaned_text.replace('\n', '')

            self.document  = cleaned_text

    def load_raw_document(self):
        with open(self.document_filename) as file:
            self.document = file.read()
                
    
    def build_shingles(self, k_length):
        shingles = []
        for i in range(len(self.document)):
            shingles.append((self.document[i:i+k_length]))

        self.shingles = list(set(shingles))

    def hash_shingles(self):

        hashed_shingles = []
        for el in self.shingles:
            hashed_shingles.append(hash(el) % (10 ** 10))
    
        self.hashed_shingles = sorted(hashed_shingles)

    