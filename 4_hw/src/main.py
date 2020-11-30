import argparse
import networkx as nx
import networkx.drawing.nx_pylab as nx_drawing # Docs:  https://networkx.org/documentation/stable/reference/generated/networkx.drawing.nx_pylab.draw_networkx.html
import matplotlib.pyplot as plt
import time

from GraphMatrixReader import GraphMatrixReader
from SpectralGraphClustering import SpectralGraphClustering


if __name__ == "__main__":

    print("Spectral Clustering on Graphs")
    print("Adriano Mundo & Edoardo Realini")
    print("KTH Royal Institute of Technology - 2020\n")

    parser = argparse.ArgumentParser(description='Parameters')
    parser.add_argument('-k', dest='k_clusters', type=int, help='Number of clusters to find', nargs='?', default=4)
    parser.add_argument('-s', dest='sigma', type=float, help='Sigma paramenter for computation of affinity', nargs='?', default=5.0)
    parser.add_argument('-k_ev', dest='top_k_ev', type=int, help='Number of top K eigenvectors to keep', nargs='?', default=4)
    parser.add_argument('-f', dest='filename', type=str, help='Filename of graph in data project folder', nargs='?', default='example1.dat')

    args = parser.parse_args()

    k_clusters = args.k_clusters
    sigma = args.sigma
    top_k_ev = args.top_k_ev
    filename = args.filename

    print("Running clustering algorithm with parameters:")
    print("Number of clusters: ", k_clusters)
    print("Sigma for affinity computation: ", sigma)
    print("Number of Top k Eigenvectors: ", top_k_ev)

    base_path = '../data/'
    data_path = base_path + filename

    timestamp = str(time.time())

    print("\n---------------------------------------------------------------------------------------------")
    print("Computing data from file: ", data_path)

    graph_reader = GraphMatrixReader()
    graph_reader.read_simple_graph(data_path)

    matrix = graph_reader.graph_matrix

    spectral_clustering = SpectralGraphClustering(graph_reader.graph_matrix)
    labels, clusters = spectral_clustering.clusterize_graph(k=k_clusters, sigma=sigma, top_k_ev=top_k_ev)

    print("\nLabels: ", labels)
    print("\nClusters: ", clusters)

    # Saving images of graphs for this run
    nx_drawing.draw_networkx(graph_reader.nx_graph, node_size=graph_reader.number_of_nodes, node_color=labels, with_labels=False, alpha=0.5, edge_color="gray", linewidths = 0.01)
    limits = plt.axis("off")

    filename = data_path.replace('../data/', '')
    filename = filename.replace('.dat', '')

    plt.savefig('../img/' + filename + '-' + timestamp + '.png')
    plt.show()

    