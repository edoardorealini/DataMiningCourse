import pandas as pd
import numpy as np
import scipy.sparse as sps
import networkx as nx


class GraphMatrixReader:

    def __init__(self):
        self.graph_matrix = None # np ndarray version of the matrix
        self.number_of_nodes = 0
        self.nx_graph = nx.Graph()
        self.start_nodes = None
        self.end_nodes = None

    
    def gen_matrix(self, row_indices, column_indices, shape):

        matrix = np.zeros(shape)

        for row, column in zip(row_indices, column_indices):
            matrix[row][column] = 1

        return matrix

    
    def gen_nx_graph(self):
        self.nx_graph.add_nodes_from(range(self.number_of_nodes))

        for i in range(self.start_nodes.shape[0]):
            self.nx_graph.add_edge(self.start_nodes[i], self.end_nodes[i])
    
    
    # This method reads a graph in the format fo CSV file with 2 columns
    # And converts it into a scipy sparse matrix representation and returns
    # The resulting matrix is the Adjacency matrix of the given graph    
    def read_simple_graph(self, path):

        df = pd.read_csv(path, sep=',', names=['start_node', 'end_node'])

        # Getting the number of nodes in the dataset
        unique_start = df['start_node'].unique().tolist()
        unique_end = df['end_node'].unique().tolist()

        unique_start.extend(unique_end)
        unique_nodes = unique_start
        unique_nodes = list(set(unique_nodes))

        self.number_of_nodes = len(unique_nodes)

        print("Reading graph from file {} with {} nodes.".format(path, self.number_of_nodes))

        ones = np.ones(df.shape[0])

        start_nodes = df["start_node"].values
        end_nodes = df["end_node"].values

        #print(start_nodes)

        col_ones = np.ones(start_nodes.shape[0])

        # Little trick, now rememeber that the node_ids are all -1 invalue wrt the originals
        start_nodes = np.subtract(start_nodes, col_ones)
        end_nodes = np.subtract(end_nodes, col_ones)

        start_nodes = start_nodes.astype(np.int32)
        end_nodes = end_nodes.astype(np.int32)
        #print(start_nodes, "\n", end_nodes)

        graph_matrix = self.gen_matrix(row_indices=start_nodes, column_indices=end_nodes, shape=(self.number_of_nodes, self.number_of_nodes))

        self.graph_matrix = graph_matrix
        self.start_nodes = start_nodes
        self.end_nodes = end_nodes

        # Here generate the nx graph, we have all the information!
        self.gen_nx_graph()


        return self.graph_matrix
        


    def read_synthetic_graph(self, path):
        
        # TODO implement this method
        # Understand the structure of the file example2.dat and implement a method similar to the existing one

        pass

