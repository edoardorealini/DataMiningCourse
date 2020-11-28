from GraphMatrixReader import GraphMatrixReader

if __name__ == "__main__":
    
    data_path = '../data/example1.dat'

    graph_reader = GraphMatrixReader()
    graph_reader.read_simple_graph(data_path)

    sps_graph_matrix = graph_reader.sps_graph_matrix

