from src.definitions import INPUT_DIR, Graph
import logging

alphabet = "abcdefghijklmnopqrstuvwxyz"
rdict = dict([(x[1], x[0]) for x in enumerate(alphabet)])


class Day12:
    file = None

    def __init__(self):
        self.file = open(f"{INPUT_DIR}/day12.txt", "r")
        self.start = (0, 0)
        self.end = (0, 0)
        self.map = None
        self.graph = None
        self.graph_prepped = False
        self.parse_input()

    def __del__(self):
        self.file.close()

    def parse_input(self):
        pos_y = 0
        buffer = []
        for line in self.file:
            line = line.strip()
            buffer.append([])
            pos_x = 0
            for element in line:
                if element == 'S':
                    self.start = (pos_x, pos_y)
                    buffer[pos_y].append(rdict['a'])
                elif element == 'E':
                    self.end = (pos_x, pos_y)
                    buffer[pos_y].append((rdict['z']))
                else:
                    buffer[pos_y].append(rdict[element])
                pos_x += 1
            pos_y += 1
        self.map = buffer

    def print_map(self, path):
        foo = [['.'] * len(self.map[0]) for i in range(len(self.map))]
        char = 'X'
        for i, v in enumerate(path):
            if i < len(path) - 1:
                next_coord = path[i + 1]
                if next_coord[0] > v[0]:
                    char = ">"
                if next_coord[0] < v[0]:
                    char = "<"
                if next_coord[1] > v[1]:
                    char = "v"
                if next_coord[1] < v[1]:
                    char = "^"
                foo[v[1]][v[0]] = char
        for y in foo:
            buf = ""
            for x in y:
                buf += x
            logging.info(buf)

    def prepare_graph(self):
        g = Graph()
        for iter_y, y in enumerate(self.map):
            for iter_x, x in enumerate(y):
                # print(x, iter_x, iter_y)
                if iter_x > 0:
                    distance = self.map[iter_y][iter_x - 1] - x
                    g.add_edge((iter_x, iter_y), (iter_x - 1, iter_y), distance)
                if iter_y > 0:
                    distance = self.map[iter_y - 1][iter_x] - x
                    g.add_edge((iter_x, iter_y), (iter_x, iter_y - 1), distance)
                if iter_x < len(y) - 1:
                    distance = self.map[iter_y][iter_x + 1] - x
                    g.add_edge((iter_x, iter_y), (iter_x + 1, iter_y), distance)
                if iter_y < len(self.map) - 1:
                    distance = self.map[iter_y + 1][iter_x] - x
                    g.add_edge((iter_x, iter_y), (iter_x, iter_y + 1), distance)
        g.process()
        self.graph = g
        self.graph_prepped = True

    def find_from_start(self):
        if not self.graph_prepped:
            self.prepare_graph()
        return self.graph.shortest_path(self.start, self.end)

    def find_for_value(self, value):
        if not self.graph_prepped:
            self.prepare_graph()
        paths = set()
        for iter_y, y in enumerate(self.map):
            for iter_x, x in enumerate(y):
                if x == value:
                    foo = (iter_x, iter_y)
                    returned_path = self.graph.shortest_path(foo, self.end)
                    if returned_path > 0:
                        paths.add(returned_path)
        return min(paths)

    def solve1(self):
        logging.info("Executing Solve1")
        return self.find_from_start()

    def solve2(self):
        logging.info("Executing Solve2")
        return self.find_for_value(rdict['a'])


if __name__ == '__main__':
    d = Day12()
    print(f"ans1: {d.solve1()}")
    print(f"ans2: {d.solve2()}")
