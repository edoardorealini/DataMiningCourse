import hashlib

# hash element mapping element -> [0, 2ˆL - 1]
def hash_element(self, element, length):
	a = random.randint(1, 2**length - 1)
	b = random.randint(1, 2**length - 1)
	return (a * element + b) % (2**length - 1)

# hashing elements D -> {0,1}^32
def hash_element_md5(self, element):
	return int(hashlib.md5(str(element).encode('utf-8')).hexdigest(), 16) % (2**32)