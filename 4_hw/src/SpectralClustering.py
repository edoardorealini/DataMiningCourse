import pandas as pd
import numpy as np


class SpectralClustering:

    def __init__(self, sps_graph_matrix):
        # A scipy.sparse matrix in csr format
        self.sps_graph_matrix = sps_graph_matrix
        self.dense_graph_matrix = sps_graph_matrix.todense()

        self.affinity_matrix = None
        self.D = None
        self.L = None
        self.X = None
        self.Y = None

        self.clusters = {}


    def compute_affinity(self):

        # TODO implement the computation of the affinity matrix using the formula on the paper

        pass


    def compute_D(self):

        # TODO Implement the computation of the D matrix

        pass


    def compute_L(self):

        # TODO implementation of the computation of L matrix accorting to the formula in the paper

        pass

    
    def compute__X(self):

        # TODO compute the X matrix

        pass


    def compute_Y(self):

        # TODO compute the Y matrix

        pass


    def clusterize_Y(self, k):

        # TODO use K means to clusterize as said in the paper

        pass


    def clusterize(self, k):

        # TODO Entry point fo the class, this method calls the sequence cof actions and creates a dictionary
        # For each node ID (as key) we map the cluster (as value) in the dictionary

        pass

