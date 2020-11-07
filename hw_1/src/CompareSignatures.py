class CompareSignatures:

    def __init__(self):
        self.sim_probability = 0

    def compare_signatures(self, sig1, sig2):
        length = len(sig1)
        equals = 0

        for i in range(length):
            if sig1[i] == sig2[i]:
                equals += 1

        self.sim_probability = equals/length

        return equals/length

