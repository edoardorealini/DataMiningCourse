import pandas as pd
import numpy as np
import scipy.sparse as sps


class GraphMatrixReader:

    def __init__(self):
        self.sps_graph_matrix = None # Sparse matrix representing the graph in CSR format: for fast row entries
        self.dense_graph_matrix = None # Dense version of the matrix
        self.np_graph_matrix = None # np ndarray version of the matrix

        self.number_of_nodes = 0

    # This method reads a graph in the format fo CSV file with 2 columns
    # And converts it into a scipy sparse matrix representation and returns
    # The resulting matrix is the Adjacency matrix of the given graph    
    def read_simple_graph(self, path):

        df = pd.read_csv(path, sep=',')

        # Getting the number of nodes in the dataset
        unique_start = df['start_node'].unique().tolist()
        unique_end = df['end_node'].unique().tolist()

        unique_start.extend(unique_end)
        unique_nodes = unique_start
        unique_nodes = list(set(unique_nodes))

        self.number_of_nodes = len(unique_nodes)

        print("Reading graph from file {} with {} nodes.".format(path, self.number_of_nodes))

        ones = np.ones(df.shape[0])

        col1 = df["start_node"]
        col2 = df["end_node"]

        graph_matrix =  sps.coo_matrix((ones, (col1, col2)), shape=(self.number_of_nodes + 1, self.number_of_nodes + 1))

        self.sps_graph_matrix = graph_matrix.tocsr()
        self.np_graph_matrix = graph_matrix.toarray()
        self.dense_graph_matrix = graph_matrix.todense()

        return self.sps_graph_matrix


    def read_synthetic_graph(self, path):
        
        # TODO implement this method
        # Understand the structure of the file example2.dat and implement a method similar to the existing one

        pass