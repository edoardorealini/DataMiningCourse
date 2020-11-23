from graph_reader import GraphReader
from graph.Graph import Graph

from CentralityHyperBall import  CentralityHyperBall

airport_data = '../data/airport_graph.txt'

reader = GraphReader(path=airport_data,is_undirected=True)
graph = reader.read_graph()

hyperball = CentralityHyperBall(graph=graph, num_buckets=32)
hyperball.compute_hyper_balls()

ids = [el for el in range(10)]

for idx in ids:
    node = graph.get_node(id=idx)
    print("Node {} Closeness: ".format(idx), hyperball.calculate_closeness(node))
    print("Node {} Lin: ".format(idx), hyperball.calculate_lin(node))
    print("Node {} Harmonic: ".format(idx), hyperball.calculate_harmonic(node))

