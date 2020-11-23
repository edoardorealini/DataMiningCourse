from graph_reader import GraphReader
from graph.Graph import Graph

airport_data = '../data/airport_graph.txt'
web_google = '../data/web-Google.txt'
web_nd = '../data/web-NotreDame.txt'

reader = GraphReader(path=web_google,is_undirected=True)
graph = reader.read_graph()

for i in range(graph.num_of_nodes):
    print(graph.get_node(i).id)
