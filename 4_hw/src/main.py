from GraphMatrixReader import GraphMatrixReader
from SpectralGraphClustering import SpectralGraphClustering

if __name__ == "__main__":
    
    data_path = '../data/example1.dat'

    graph_reader = GraphMatrixReader()
    graph_reader.read_simple_graph(data_path)

    sps_graph_matrix = graph_reader.sps_graph_matrix
    np_graph_matrix = graph_reader.np_graph_matrix

    #print(np_graph_matrix)

    spectral_clustering = SpectralGraphClustering(sps_graph_matrix)
    
    '''
    print("Affinity:", spectral_clustering.compute_affinity())
    print("D matrix:", spectral_clustering.compute_D())
    print("L matrix:", spectral_clustering.compute_L())
    '''

    spectral_clustering.compute_affinity()
    spectral_clustering.compute_D()
    spectral_clustering.compute_L()

    spectral_clustering.compute_X(4)


