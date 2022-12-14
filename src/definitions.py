import logging
import os
import sys

logging.basicConfig(stream=sys.stdout, level=logging.ERROR, format='%(levelname)-8s %(message)s')

INFINITY = float("inf")
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if 'unittest' in sys.modules.keys():
    INPUT_DIR = os.path.join(ROOT_DIR, '../test/input')
else:
    INPUT_DIR = os.path.join(ROOT_DIR, 'input')


# Modified from: https://github.com/dmahugh/dijkstra-algorithm/blob/master/dijkstra_algorithm.py
class Graph:
    def __init__(self):
        self.graph_edges = []
        self.nodes = set()
        self.adjacency_list = None

    def add_edge(self, edge_from, edge_to, cost):
        self.graph_edges.append((edge_from, edge_to, float(cost)))

    def process(self):
        for edge in self.graph_edges:
            self.nodes.update([edge[0], edge[1]])

        self.adjacency_list = {node: set() for node in self.nodes}
        for edge in self.graph_edges:
            self.adjacency_list[edge[0]].add((edge[1], edge[2]))

    def shortest_path(self, start_node, end_node):
        unvisited_nodes = self.nodes.copy()
        distance_from_start = {
            node: (0 if node == start_node else INFINITY) for node in self.nodes
        }
        previous_node = {node: None for node in self.nodes}
        while unvisited_nodes:
            current_node = min(
                unvisited_nodes, key=lambda node: distance_from_start[node]
            )
            unvisited_nodes.remove(current_node)
            if distance_from_start[current_node] == INFINITY:
                break
            for neighbor, distance in self.adjacency_list[current_node]:
                if distance < 2:
                    if distance < 1:
                        distance = 2
                    new_path = distance_from_start[current_node] + distance
                    if new_path < distance_from_start[neighbor]:
                        distance_from_start[neighbor] = new_path
                        previous_node[neighbor] = current_node
            if current_node == end_node:
                break
        path_length = 0
        current_node = end_node
        while previous_node[current_node] is not None:
            path_length += 1
            current_node = previous_node[current_node]
        return path_length
