import functools
import sys
from collections import deque

import networkx

from src.definitions import INPUT_DIR
import logging
import networkx as nx

CLOSED = 0
OPEN = 1

sys.setrecursionlimit(10000)


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

    def queue_graph(self):
        interesting_nodes = ["AA"]
        paths = {}
        maxflow = 0
        for n in self.graph.nodes:
            if self.graph.nodes[n]["flow_rate"] > 0:
                interesting_nodes.append(n)
                maxflow += self.graph.nodes[n]["flow_rate"]
        for x in interesting_nodes:
            for y in interesting_nodes:
                if not x == y:
                    dist = networkx.shortest_path(self.graph, x, y)
                    print(x, y, len(dist) - 1)
                    paths[(x, y)] = len(dist) - 1
        print(paths)
        best_result = 0
        queue = deque()
        queue.append(("AA", 30, 0, tuple("AA")))
        visited = set()
        while len(queue) > 0:
            qval = queue.pop()
            if qval not in visited:
                visited.add(qval)
                current_node, time_left, score, opened = qval
                if time_left < 2:
                    continue
                if len(opened) == (len(interesting_nodes) - 1):  # since AA is in there
                    continue
                difference = best_result - score
                needed_score_per_turn = difference / time_left
                if needed_score_per_turn > maxflow:
                    continue
                options = []
                for node_set, distance in paths.items():
                    start, end = node_set
                    if start == current_node and end not in opened and time_left - distance >= 2:
                        options.append((end, distance))
                print(best_result, len(queue), current_node, time_left, score, options)
                if current_node not in opened:
                    score_for_node = self.graph.nodes[current_node]['flow_rate'] * (time_left - 1)
                    best_result = max(best_result, score + score_for_node)
                    for endpoint, distance in options:
                        if time_left - (1 + distance) >= 2:
                            queue.append((endpoint, time_left - (1 + distance), score + score_for_node,
                                          opened + (current_node,)))
                for endpoint, distance in options:
                    queue.append((endpoint, time_left - distance, score, opened))
        return best_result

    #noworkey, too naive
    def new_strategy(self):
        interesting_nodes = ["AA"]
        paths = {}
        maxflow = 0
        time_left = 26
        # find all nodes with valves that have any value
        for n in self.graph.nodes:
            if self.graph.nodes[n]["flow_rate"] > 0:
                interesting_nodes.append(n)
                maxflow += self.graph.nodes[n]["flow_rate"]
        # calculate all distances between all interesting nodes (collapse the graph)
        for x in interesting_nodes:
            for y in interesting_nodes:
                if not x == y:
                    dist = networkx.shortest_path(self.graph, x, y)
                    print(x, y, len(dist) - 1)
                    paths[(x, y)] = len(dist) - 1
        print(paths)

        opened = ["AA"]

        path1 = "AA"
        path2 = "AA"

        next1 = "AA"
        next2 = "AA"

        time_left1 = 26
        time_left2 = 26

        score1 = 0
        score2 = 0

        for _ in range(7):
            option = self.find_next(paths, next1, time_left1, opened)
            print(score1, option)
            path1 += f",{option[0]}"
            score1 += option[1]
            time_left1 = option[2]
            next1 = option[0]
            opened.append(option[0])
            print("PATH1: ", path1, score1)
            option = self.find_next(paths, next2, time_left2, opened)
            print(score2, option)
            path2 += f",{option[0]}"
            score2 += option[1]
            time_left2 = option[2]
            next2 = option[0]
            opened.append(option[0])
            print("PATH2: ", path2, score2)
        print(score1 + score2)

    def find_next(self, paths, start_node, time_left, opened):
        best_end = ""
        best_value = 0
        best_time_spent = 0
        for path, distance in paths.items():
            start, end = path
            if start == start_node and end not in opened:
                flow = self.graph.nodes[end]["flow_rate"]
                new_time = time_left - (distance + 1)
                if new_time >= 0:
                    potential_value = flow * new_time
                    if potential_value > best_value:
                        best_value = potential_value
                        best_end = end
                        best_time_spent = new_time
                    print(start, end, distance, flow, potential_value)
        return best_end, best_value, best_time_spent

    def queue_for_two(self):
        interesting_nodes = ["AA"]
        paths = {}
        maxflow = 0
        for n in self.graph.nodes:
            if self.graph.nodes[n]["flow_rate"] > 0:
                interesting_nodes.append(n)
                maxflow += self.graph.nodes[n]["flow_rate"]
        for x in interesting_nodes:
            for y in interesting_nodes:
                if not x == y:
                    dist = networkx.shortest_path(self.graph, x, y)
                    print(x, y, len(dist) - 1)
                    paths[(x, y)] = len(dist) - 1
        print(paths)
        best_result = 0 #2586
        queue = deque()
        queue.append(("AA", "AA", 26, 26, 0, set()))
        count = 0
        pruned = 0
        visited = set()
        while len(queue) > 0:
            count += 1
            # if count > 100000:
            #     gc.collect()
            #     count = 0
            qval = queue.pop()
            my_node, elephant_node, my_time_left, elephant_time_left, score, opened = qval
            uuid = "".join(sorted(
                [my_node, elephant_node, str(my_time_left).zfill(2), str(elephant_time_left).zfill(2), str(score).zfill(4)]
            ))
            if uuid in visited:
                pruned += 1
                continue
            visited.add(uuid)
            # assert not (score > 0 and (my_node == 'AA' or elephant_node == 'AA')), "someone went back to start"
            # if my_time_left < 2 and elephant_time_left < 2:
            #     continue
            # if len(opened) == (len(interesting_nodes) - 1): # since AA is in there
            #     continue
            difference = best_result - score
            needed_score_per_turn = difference / max(my_time_left, elephant_time_left)
            if needed_score_per_turn > maxflow:
                continue
            my_options = []
            elephant_options = []
            for node_set, distance in paths.items():
                start, end = node_set
                if start == my_node and end not in opened and my_time_left - distance >= 2:
                    my_options.append((end, distance))
                if start == elephant_node and end not in opened and elephant_time_left - distance >= 2:
                    elephant_options.append((end, distance))

            score_for_node = 0
            ele_score_for_node = 0
            if my_node not in opened and my_time_left >= 2:
                score_for_node = self.graph.nodes[my_node]['flow_rate'] * (my_time_left - 1)
                my_time_left -= 1
                opened.add(my_node)
            if elephant_node not in opened and elephant_time_left >= 2:
                ele_score_for_node = self.graph.nodes[elephant_node]['flow_rate'] * (elephant_time_left - 1)
                elephant_time_left -= 1
                opened.add(elephant_node)

            best_result = max(best_result, score + score_for_node + ele_score_for_node)
            print(
                f"it:{format(count, ',d')}\tlv:{format(len(visited), ',d')}\tp:{pruned}\tbr:{best_result}\tlq:{format(len(queue), ',d')}\ti:{my_node}\te:{elephant_node}\tti:{my_time_left}\tte:{elephant_time_left}\ts:{score}\tu:{uuid}"
                # f"oi:{my_options}\n"
                # f"oe:{elephant_options}\n"
                # f"op:{opened}"
            )
            if len(my_options) > 0:
                for my_end, my_distance in my_options:
                    if len(elephant_options) > 0:
                        for ele_end, ele_distance in elephant_options:
                            queue.append(
                                (my_end, ele_end,
                                 my_time_left - my_distance, elephant_time_left - ele_distance,
                                 score + score_for_node + ele_score_for_node,
                                 opened.copy()
                                 )
                            )
                        else:
                            queue.append(
                                (my_end, elephant_node,
                                 my_time_left - my_distance, 0,
                                 score + score_for_node + ele_score_for_node,
                                 opened.copy()
                                 )
                            )
            else:
                for ele_end, ele_distance in elephant_options:
                    queue.append(
                        (my_node, ele_end,
                         0, elephant_time_left - ele_distance,
                         score + score_for_node + ele_score_for_node,
                         opened.copy()
                         )
                    )
            # # only elephant opens
            # if elephant_node not in opened:
            #     ele_score_for_node = self.graph.nodes[elephant_node]['flow_rate'] * (elephant_time_left - 1)
            #     best_result = max(best_result, score + ele_score_for_node)
            #     # i don't
            #     for my_end, my_distance in my_options:
            #         for ele_end, ele_distance in elephant_options:
            #             if (my_node == elephant_node and my_end != ele_end) or my_node != elephant_node:
            #                 queue.append(
            #                     (my_end, ele_end, my_time_left - my_distance,  elephant_time_left - (1 + ele_distance),
            #                      score + ele_score_for_node, opened + (elephant_node,)))
            #
            # for my_end, my_distance in my_options:
            #     for ele_end, ele_distance in elephant_options:
            #         if my_end != ele_end:
            #             queue.append((my_end, ele_end, time_left - my_distance, elephant_time_left - ele_distance,
            #                       score, opened))
        print(best_result)
        return best_result

    @functools.lru_cache(maxsize=None)
    def recurse_graph(self, node: str, time_left: int, opened: tuple = (),
                      elephant_node: str = None, elephant_time_left: int = None):
        print(node, time_left, elephant_node, elephant_time_left, opened)
        if elephant_time_left is None:
            if time_left < 2:
                return 0
        else:
            if time_left < 2 or elephant_time_left < 2:
                return 0
        total_score = 0
        for adj in self.graph.adj[node]:
            score_open = 0
            if node not in opened and self.graph.nodes[node]['flow_rate'] > 0:
                score_for_node = self.graph.nodes[node]['flow_rate'] * (time_left - 1)
                score_open = score_for_node + self.recurse_graph(adj, time_left - 2, opened + (node,),
                                                                 elephant_node, elephant_time_left)
            score_move = self.recurse_graph(adj, time_left - 1, opened, elephant_node, elephant_time_left)
            total_score = max(total_score, score_open, score_move)
            if elephant_node is not None and elephant_time_left is not None:
                for elephant_adj in self.graph.adj[elephant_node]:
                    score_open = 0
                    if node not in opened and self.graph.nodes[elephant_node]['flow_rate'] > 0:
                        score_for_node = self.graph.nodes[elephant_node]['flow_rate'] * (elephant_time_left - 1)
                        score_open = score_for_node + self.recurse_graph(node, time_left, opened + (elephant_node,),
                                                                         elephant_adj, elephant_time_left - 2)
                    score_move = self.recurse_graph(node, time_left, opened, elephant_adj, elephant_time_left - 1)
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
        return self.recurse_graph("AA", 30)
        #return self.queue_graph()

    def solve2(self):
        logging.info("Executing Solve2")
        # return self.recurse_graph("AA", 26, (), "AA", 26)
        self.queue_for_two()
        # self.new_strategy()


if __name__ == '__main__':
    d = Day16()
    # print(f"ans1: {d.solve1()}")
    # time.sleep(5)
    print(f"ans2: {d.solve2()}")
