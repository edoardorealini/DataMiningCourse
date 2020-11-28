from graph.Node import Node
from graph.Edge import Edge

class Graph:

    def __init__(self, num_of_nodes):
        self.num_of_nodes = num_of_nodes

        self.nodes = []
        self.edges = []

        for i in range(num_of_nodes):
            self.nodes.append(Node(i))

        self.adjacent_list = [[] for i in range(num_of_nodes)]
        self.adjacent_list_transpose = [[] for i in range(num_of_nodes)]


    def get_node(self, id):
        return self.nodes[id]

    
    def add_edge(self, edge):
        try:
            self.edges.append(edge)
            self.adjacent_list[edge.source.id].append(edge.dest)
            self.adjacent_list_transpose[edge.dest.id].append(edge.source)
        except:
            print('Source id: ', edge.source.id)
            print('Dest id: ', edge.dest.id)

    def get_adjacent_nodes(self, node):
        return self.adjacent_list[node.id]


    def get_adjacent_nodes_transpose(self, node):
        return self.adjacent_list_transpose[node.id]