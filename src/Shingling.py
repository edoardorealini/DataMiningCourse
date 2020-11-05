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
        self.shingles = np.array(0)
        self.hashed_shingles = np.array(0)


    def cleanup_document(self):
        with open(self.document_filename) as file:
            text = file.read()
            new_text = re.sub(r'[^\w\s]','',text)
            self.document = new_text

    def load_raw_document(self):
        with open(self.document_filename) as file:
            self.document = file.read()
            
    
    '''
    def build_shingles(self, k):

        return

    def hash_shingles(self):

        return
    '''

if __name__ == "__main__":
    s = Shingling("../data/1.txt")
    s.cleanup_document()