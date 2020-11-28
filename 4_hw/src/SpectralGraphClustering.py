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
        self.clusters = {}


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

        # TODO check if these dot products are fine!
        step_1 = D_powered.dot(self.affinity_matrix)
        L = step_1.dot(D_powered)

        self.L = L

        return self.L

    
    def compute_X(self, top_k_ev):
        eig_values, eig_vectors = np.linalg.eig(self.L)
        eig_tuples = []

        # Problem should be now fixed, the results in eig_tuples after the sortin operation are correct

        for i, eig in enumerate(eig_values):
            eig_tuples.append((eig, eig_vectors[:, i]))

        eig_tuples = sorted(eig_tuples, key = lambda tup: tup[0], reverse=True)

        # Selecting the top k eigenvectors
        eig_tuples = eig_tuples[:top_k_ev]
        #print(eig_tuples)
        vectors = [tup[1] for tup in eig_tuples]
        np_vectors = np.array(vectors)

        # We want the eigenvectors to be on the columns
        np_vectors = np.transpose(np_vectors) 
        
        self.X = np_vectors

        return self.X


    def compute_Y(self):

        # The normalization should be useless, numpy already normalizes the eigenvectors based on their length
        # Normalizing anyway, you never know

        y_rows = []

        for row_id in range(self.matrix_dimension):
            row = self.X[row_id]

            squared = np.square(row)
            row_sum = np.sum(squared)
            unit_factor = np.sqrt(row_sum)

            row = np.divide(row, unit_factor)

            y_rows.append(row)            

        self.Y = np.array(y_rows)

        return self.Y


    def clusterize_Y(self, k_clusters):

        # Searching for K clusters using KMeans from sklearn
        kmeans = KMeans(n_clusters=k_clusters, random_state=0)
        kmeans.fit(self.Y)

        self.labels = kmeans.labels_

        for i in range(k_clusters):
            self.clusters[i] = []

        for i in range(self.matrix_dimension):
            self.clusters[self.labels[i]].append(i + 1) #Here is where we fix the trick

  
        return self.labels, self.clusters


    # Entry point fo the class, this method calls the sequence cof actions and creates a dictionary
    # For each node ID (as key) we map the cluster (as value) in the dictionary

    def clusterize_graph(self, k=10, sigma=1, top_k_ev=10):

        self.compute_affinity(sigma=sigma)
        self.compute_D()
        self.compute_L()

        self.compute_X(top_k_ev=top_k_ev)
        self.compute_Y()

        return self.clusterize_Y(k_clusters=k)

        
