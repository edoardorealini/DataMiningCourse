import argparse
import time

from graph_reader import GraphReader
from graph.Graph import Graph
from CentralityHyperBall import  CentralityHyperBall

if __name__ == '__main__':

	print("HyperBall algorithm for Mining Data Streams")
	print("Adriano Mundo & Edoardo Realini")
	print("KTH Royal Institute of Technology - 2020\n")

	parser = argparse.ArgumentParser(description='Parameters')
	parser.add_argument('-n', dest='n_nodes', type=int, help='Number of nodes to show', nargs='?', default=10)
	parser.add_argument('-b', dest='n_buckets', type=int, help='Number of buckets', nargs='?', default=32)

	args = parser.parse_args()

	print("Number of nodes: ", args.n_nodes)
	n_nodes = args.n_nodes
	n_buckets = args.n_buckets

	filename = '../data/airport_graph.txt'

	reader = GraphReader(path=filename, is_undirected=True)
	graph = reader.read_graph()

	start = time.time()
	print("\nStart the HyperBall algorithm\n")

	hyperball = CentralityHyperBall(graph=graph, num_buckets=n_buckets)
	hyperball.compute_hyper_balls()

	ids = [el for el in range(n_nodes)]

	for idx in ids:
		node = graph.get_node(id=idx)
		print("Node {} Closeness: ".format(idx), hyperball.calculate_closeness(node))
		print("Node {} Lin: ".format(idx), hyperball.calculate_lin(node))
		print("Node {} Harmonic: ".format(idx), hyperball.calculate_harmonic(node))

	end = time.time()
	print("\nEnd the HyperBall algorithm, time elapsed: ", end - start, " sec.")












