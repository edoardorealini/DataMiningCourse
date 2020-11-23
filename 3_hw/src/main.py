from graph_reader import GraphReader
from graph.Graph import Graph

from CentralityHyperBall import  CentralityHyperBall

airport_data = '../data/airport_graph.txt'
web_google = '../data/web-Google.txt'
web_nd = '../data/web-NotreDame.txt'

reader = GraphReader(path=airport_data,is_undirected=True)
graph = reader.read_graph()

hyperball = CentralityHyperBall(graph=graph, num_buckets=32)
hyperball.compute_hyper_balls()

ids = [range(10)]

for idx in ids:
    node = graph.get_node(id=idx)
    print("Node {} Closeness: ".format(idx), hyperball.calculate_closeness(node))