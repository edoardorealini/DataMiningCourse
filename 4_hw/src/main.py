import argparse

from GraphMatrixReader import GraphMatrixReader
from SpectralGraphClustering import SpectralGraphClustering


if __name__ == "__main__":

    print("Spectral Clustering on Graphs")
    print("Adriano Mundo & Edoardo Realini")
    print("KTH Royal Institute of Technology - 2020\n")

    parser = argparse.ArgumentParser(description='Parameters')
    parser.add_argument('-k', dest='k_clusters', type=int, help='Number of clusters to find', nargs='?', default=10)
    parser.add_argument('-s', dest='sigma', type=int, help='Sigma paramenter for computation of affinity', nargs='?', default=1)
    parser.add_argument('-k_ev', dest='top_k_ev', type=int, help='Number of top K eigenvectors to keep', nargs='?', default=10)

    args = parser.parse_args()

    k_clusters = args.k_clusters
    sigma = args.sigma
    top_k_ev = args.top_k_ev

    print("Running clustering algorithm with parameters:")
    print("Number of clusters: ", k_clusters)
    print("Sigma: ", sigma)
    print("Number of Top k Eigenvectors: ", top_k_ev)

    data_paths = ['../data/example1.dat', '../data/example2.dat'] 

    for data_path in data_paths:
        print("--------------------------------------------------------------------------")
        print("Computing data from file: ", data_path)

        graph_reader = GraphMatrixReader()
        graph_reader.read_simple_graph(data_path)

        spectral_clustering = SpectralGraphClustering(graph_reader.sps_graph_matrix)
        labels, clusters = spectral_clustering.clusterize_graph()

        print("Labels: ", labels)
        print("Clusters: ", clusters)
    