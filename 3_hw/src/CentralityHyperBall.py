import numpy as np
from counting.HyperLogLog import HyperLogLog


class CentralityHyperBall():
    def __init__(self, graph, num_buckets):

        # Graph object defined in the Graph class
        self.graph = graph

        # A np matrix that store, for each node x and for each radius r, the cardinality of the HyperBall B(x,r)
        # This data structure is the one to be used for the actual computation of the centralities
        self.hyper_ball_cardinalities = np.zeros((self.graph.num_of_nodes, self.graph.num_of_nodes + 1)) 
        for x in range(self.graph.num_of_nodes):
            self.hyper_ball_cardinalities[x][0] = 1 # The cardinality of all the balls of radius 0 is 1 by default

        # The number of buckets to use when computing the HyperLogLog counting
        self.num_buckets = num_buckets

        # Cardinality of a node at instant t
        self.hyperloglog_balls_cumulative = []

        # List of lists of 2 elements [ [count_t, count_t+1]_1,  [count_t, count_t+1]_2, ... [count_t, count_t+1]_num_nodes]
        # Registers the counters of a node at instant t and t+1 respectively in pos 0 and pos 1 in the list
        self.hyperloglog_balls_diff = [None]*self.graph.num_of_nodes

        # Initializing the data structures with empty structures and then with the initial values

        # For each node initializing the cumulative list and the diff list (with an empty list)
        for node in self.graph.nodes:
            self.hyperloglog_balls_cumulative.append(HyperLogLog(num_buckets))
            self.hyperloglog_balls_diff[node.id] = []
            # Append 1 empty counter per every node in list hyperloglog_balls_diff, in position 0 of the list: representing the count at t=1
            self.hyperloglog_balls_diff[node.id].append(HyperLogLog(num_buckets))

        # For each node:
        #   - get the adjecent nodes in transposed mode (as the paper suggests)
        #   - get a list of all the ids of the adjecent nodes
        #   - for each node call the count function of hyperloglog passing the adjacent nodes list
        for node in self.graph.nodes:
            adjacent_nodes = graph.get_adjacent_nodes_transpose(node)
            adjacent_nodes_id = []
            for adjacent_node in adjacent_nodes:
                adjacent_nodes_id.append(adjacent_node.id)
            
            self.hyperloglog_balls_cumulative[node.id].add(adjacent_nodes_id)

            # Fill the cardinality matrix to be used for centrality computation, for every node.
            # Here we fill the cardinality at instant t = 1, in the next method we will start from t = 2
            self.hyper_ball_cardinalities[node.id][1] = self.hyperloglog_balls_cumulative[node.id].calculate_cardinality()
            self.hyperloglog_balls_diff[node.id][0].add(adjacent_nodes_id)
            #print(self.hyper_ball_cardinalities[node.id][0])


    def compute_hyper_balls(self):
        t = 2

        # Iterate until the nodes finish or there is no update in the counters, convergence has been reached
        while t < self.graph.num_of_nodes and not self.has_reached_convergence(t):
            
            for node in self.graph.nodes:
                # Append in position 1 an empty counter for every node list in the list self.hyperloglog_balls_diff
                self.hyperloglog_balls_diff[node.id].append(HyperLogLog(self.num_buckets)) 
            
            for node in self.graph.nodes:
                for neighbor in self.graph.get_adjacent_nodes_transpose(node):
                    self.hyperloglog_balls_diff[node.id][1].union(self.hyperloglog_balls_diff[neighbor.id][0])

                self.hyperloglog_balls_cumulative[node.id].union(self.hyperloglog_balls_diff[node.id][1])

                self.hyper_ball_cardinalities[node.id][t] = self.hyperloglog_balls_cumulative[node.id].calculate_cardinality()
            
            for node in self.graph.nodes:
                self.hyperloglog_balls_diff[node.id].pop(0) # Makes the counter at pos t+1 -> pos t by removing the first element

            t += 1
        print("Reached convergence in " + str(t) + " iterations")


    def has_reached_convergence(self, t):
        for i in range(len(self.hyper_ball_cardinalities)):
            if self.hyper_ball_cardinalities[i][t-1] != self.hyper_ball_cardinalities[i][t-2]:
                return False

        return True
    

    def calculate_closeness(self, node):
        res = 0
        t = 1
        while t <= self.graph.num_of_nodes and self.hyper_ball_cardinalities[node.id][t] > 0:
            res += t*(self.hyper_ball_cardinalities[node.id][t] - self.hyper_ball_cardinalities[node.id][t - 1])
            t = t + 1
        if res == 0:
            res = 1
        return 1/res


    def calculate_lin(self, node):
        res = 0
        cont = 0
        t = 1
        while t <= self.graph.num_of_nodes and self.hyper_ball_cardinalities[node.id][t] > 0:
            cont += self.hyper_ball_cardinalities[node.id][t] - self.hyper_ball_cardinalities[node.id][t - 1]
            res += t * (self.hyper_ball_cardinalities[node.id][t] - self.hyper_ball_cardinalities[node.id][t - 1])
            t = t + 1
        if res == 0:
            res = 1
        return cont **2 / res


    def calculate_harmonic(self, node):
        res = 0
        t = 1
        while t <= self.graph.num_of_nodes and self.hyper_ball_cardinalities[node.id][t] > 0:
            res += (1/t)*(self.hyper_ball_cardinalities[node.id][t] - self.hyper_ball_cardinalities[node.id][t - 1])
            t = t + 1
        return res
