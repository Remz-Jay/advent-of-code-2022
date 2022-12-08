from src.definitions import INPUT_DIR
import logging
import numpy as np


class Day8:
    file = None
    matrix = None
    num_rows = 0
    num_cols = 0

    def __init__(self):
        self.file = open(f"{INPUT_DIR}/day8.txt", "r")
        self.prepare_matrix()

    def __del__(self):
        self.file.close()

    def prepare_matrix(self):
        buffer = []
        for line in self.file:
            buffer.append([int(x) for x in [*line.strip()]])
        self.matrix = np.array(buffer)
        logging.info(self.matrix)

    def calc_edges(self):
        self.num_rows = len(self.matrix[0])
        self.num_cols = len(self.matrix)
        return (2 * self.num_rows) + (2 * self.num_cols) - 4

    def calc_inner(self):
        total = 0
        for i in range(1, self.num_cols - 1):
            for j in range(1, self.num_rows - 1):
                visible = False
                value = self.matrix[i, j]
                if value > max(self.matrix[i, :j]):
                    visible = True
                if value > max(self.matrix[i, j + 1:]):
                    visible = True
                if value > max(self.matrix[:i, j]):
                    visible = True
                if value > max(self.matrix[i + 1:, j]):
                    visible = True
                if visible:
                    total += 1
        return total

    @staticmethod
    def get_distance(value, view):
        distance = 0
        for x in view:
            distance += 1
            if x >= value:
                break
        return distance

    def calc_max_scenic_value(self):
        values = []
        for i in range(0, self.num_cols):
            for j in range(0, self.num_rows):
                value = self.matrix[i, j]
                distance_left = self.get_distance(value, np.flip(self.matrix[i, :j]))
                distance_right = self.get_distance(value, self.matrix[i, j + 1:])
                distance_up = self.get_distance(value, np.flip(self.matrix[:i, j]))
                distance_down = self.get_distance(value, self.matrix[i + 1:, j])
                values.append(distance_left * distance_right * distance_up * distance_down)
        return max(values)

    def solve1(self):
        logging.info("Executing Solve1")
        ans1 = 0
        ans1 += self.calc_edges()
        ans1 += self.calc_inner()
        return ans1

    def solve2(self):
        logging.info("Executing Solve2")
        return self.calc_max_scenic_value()


if __name__ == '__main__':
    d = Day8()
    print(f"ans1: {d.solve1()}")
    print(f"ans2: {d.solve2()}")
