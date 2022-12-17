import functools

import networkx

from src.definitions import INPUT_DIR
import logging
import networkx as nx
import matplotlib.pyplot as plt

CLOSED = 0
OPEN = 1


class Day16:
    file = None

    def __init__(self):
        self.file = open(f"{INPUT_DIR}/day16.txt", "r")
        self.graph = nx.Graph()
        self.parse_input()

    def parse_input(self):
        for line in self.file:
            # Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
            bits = line.strip().split(' ')
            flow_rate = int(bits[4].split('=')[1].replace(';', ''))
            self.graph.add_node(bits[1], flow_rate=flow_rate, state=CLOSED)
            for i in bits[9:]:
                self.graph.add_edge(bits[1], i.replace(',', ''))
        # nx.draw(self.graph, with_labels=True, font_weight='bold')
        # plt.show()
        # print(self.graph.nodes.data())

    def find_open_valves(self):
        retset: list[tuple] = []
        for node_name in self.graph.nodes:
            if self.graph.nodes[node_name]['state'] == OPEN:
                retset.append((node_name, self.graph.nodes[node_name]['flow_rate']))
        return retset

    @functools.lru_cache(maxsize=None)
    def recurse_graph(self, node: str, time_left: int, opened: tuple = ()):
        if time_left < 2: return 0
        total_score = 0
        for adj in self.graph.adj[node]:
            score_open = 0
            if node not in opened and self.graph.nodes[node]['flow_rate'] > 0:
                score_for_node = self.graph.nodes[node]['flow_rate'] * (time_left - 1)
                score_open = score_for_node + self.recurse_graph(adj, time_left - 2, opened + (node,))
            score_move = self.recurse_graph(adj, time_left - 1, opened)
            total_score = max(total_score, score_open, score_move)
        return total_score

    def run_simulation(self, minutes=30):
        score = 0
        location = 'AA'
        for minute in range(minutes + 1):
            print(f"== Minute {minute} == (At {location})")
            ov = self.find_open_valves()
            ovl = len(ov)
            if ovl < 1:
                print("No valves are open.")
            elif ovl == 1:
                print(f"Valve {ov[0][0]} is open, releasing {ov[0][1]} pressure.")
            else:
                names = []
                pressure = 0
                for v in ov:
                    names.append(v[0])
                    pressure += v[1]
                last = names.pop()
                p1 = ", ".join(names)
                p2 = " and ".join([p1, last])
                print(f"Valves {p2} are open, releasing {pressure} pressure.")

    def __del__(self):
        self.file.close()

    def solve1(self):
        logging.info("Executing Solve1")
        # self.run_simulation()
        return self.recurse_graph("AA", 30)

    def solve2(self):
        logging.info("Executing Solve2")
        self.file.seek(0)
        return False


if __name__ == '__main__':
    d = Day16()
    print(f"ans1: {d.solve1()}")
    print(f"ans2: {d.solve2()}")
