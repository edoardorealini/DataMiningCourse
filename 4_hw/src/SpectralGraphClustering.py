import pandas as pd
import numpy as np
import scipy.linalg as la

#https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
from sklearn.cluster import KMeans


class SpectralGraphClustering:


    def __init__(self, sps_graph_matrix):
        # A scipy.sparse matrix in csr format
        self.sps_graph_matrix = sps_graph_matrix
        self.dense_graph_matrix = sps_graph_matrix.todense()
        self.np_graph_matrix = sps_graph_matrix.toarray()
        self.matrix_dimension = self.np_graph_matrix.shape[0]

        self.affinity_matrix = np.zeros((self.matrix_dimension, self.matrix_dimension))
        self.D = np.zeros((self.matrix_dimension, self.matrix_dimension))
        self.L = None
        self.X = None
        self.Y = None

        self.labels = None


    # Computes the affinity between two rows of the matrix that represents the graph
    def two_rows_affinity(self, row1, row2, sigma=1):

        distance_squared = np.square(np.linalg.norm(row1 - row2))
        neg_distance_squared = np.negative(distance_squared)
        affinity = np.exp(neg_distance_squared / (2*np.square(sigma)))

        return affinity


    # Computes the whole affinity matrix as a np ndarray
    def compute_affinity(self, sigma=1):

        matrix = self.np_graph_matrix

        for row_id_1 in range(self.matrix_dimension):
            row1 = matrix[row_id_1]

            for row_id_2 in range(self.matrix_dimension):
                row2 = matrix[row_id_2]
                affinity = self.two_rows_affinity(row1, row2, sigma)

                self.affinity_matrix[row_id_1][row_id_2] = affinity
        
        np.fill_diagonal(self.affinity_matrix, 0)

        return self.affinity_matrix


    # Degree matrix computation
    # This matrix contains per each possition in the main diagonal, the sum of the values of the 
    # corresponding row in the affinity matrix
    def compute_D(self):

        matrix = self.affinity_matrix
        row_sums = []

        for row_id in range(self.matrix_dimension):
            row_sum = np.sum(matrix[row_id])
            row_sums.append(row_sum)

        np.fill_diagonal(self.D, row_sums)

        return self.D


    # Laplacian matrix computation
    def compute_L(self):
        D_powered = self.D.copy()
        la.fractional_matrix_power(D_powered, -1/2)

        step_1 = D_powered.dot(self.affinity_matrix)
        L = step_1.dot(D_powered)

        self.L = L

        return self.L

    
    def compute_X(self, k):
        eig_values, eig_vectors = np.linalg.eig(self.L)

        eig_tuples = list(zip(eig_values, eig_vectors))
        # TODO there is a problem with this following sorting, the eigenvalues that
        # Come after this are not coherent, FIX
        sorted(eig_tuples, key = lambda tup: tup[0])

        # Selecting the top k eigenvectors
        eig_tuples = eig_tuples[:k]
        vectors = [tup[1] for tup in eig_tuples]
        np_vectors = np.array(vectors)

        # We want the eigenvectors to be on the columns
        np.transpose(np_vectors) 
        
        self.X = np_vectors

        return self.X


    def compute_Y(self):

        # The normalization should be useless, numpy already normalizes the eigenvectors based on their length
        self.Y = self.X

        return self.Y


    def clusterize_Y(self, k):

        # Searching for K clusters using KMeans from sklearn
        kmeans = KMeans(n_clusters=k, random_state=0)
        kmeans.fit(self.Y)

        self.labels = kmeans.labels_

        # TODO Here with the labels we have to divide the entry points (the nodes) into their specific clusters
        # Basically each row of the Y matrix represents a node (the node name is the id of the row ??)
        # we can build a dictionary that assiciates per each cluster ID the list of nodes that are predicted to be in it

    def clusterize(self, k):

        # TODO Entry point fo the class, this method calls the sequence cof actions and creates a dictionary
        # For each node ID (as key) we map the cluster (as value) in the dictionary

        pass
