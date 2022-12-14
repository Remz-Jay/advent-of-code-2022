from subprocess import call

from src.definitions import INPUT_DIR
import logging


class Day14:
    file = None

    def __init__(self):
        self.file = open(f"{INPUT_DIR}/day14.txt", "r")
        self.min_x = 10000
        self.min_y = 10000
        self.max_x = 0
        self.max_y = 0
        self.insert = 500
        self.grid = [['.'] * 1000 for i in range(1000)]
        self.grid[0][self.insert] = "+"
        self.parse_input()

    def __del__(self):
        self.file.close()

    def print_grid(self, left=0, right=1000, top=0, bottom=1000, insert=500, do_return=False, legend=True):
        buffer = ""
        if legend:
            digits_left = [int(x) for x in str(left)]
            digits_right = [int(x) for x in str(right)]
            digits_insert = [int(x) for x in str(insert)]
            for iter, i in enumerate(digits_left):
                padding_l = (insert - left) - 1
                padding_r = (right - insert) - 1
                buffer += f"  {i}{' ' * padding_l}{digits_insert[iter]}{' ' * padding_r}{digits_right[iter]}\n"
        for iter, l in enumerate(self.grid):
            if top <= iter <= bottom:
                if legend:
                    buffer += f"{iter} "
                for i, j in enumerate(l):
                    if left <= i <= right:
                        buffer += j
                buffer += "\n"
        if do_return:
            return buffer
        else:
            logging.info(buffer)

    def parse_input(self):
        for line in self.file:
            parts = line.strip().split(" -> ")
            for iter, item in enumerate(parts):
                if iter < len(parts) - 1:
                    self.draw_line(item, parts[iter + 1])

    def draw_line(self, start, end):
        start_bits = start.split(',')
        start_x = int(start_bits[0])
        start_y = int(start_bits[1])
        end_bits = end.split(',')
        end_x = int(end_bits[0])
        end_y = int(end_bits[1])
        assert start_x == end_x or start_y == end_y
        if start_x == end_x:
            if start_y > end_y:
                temp = end_y
                end_y = start_y
                start_y = temp
            self.draw_the_actual_line(start_y, end_y, start_x)
        else:
            if start_x > end_x:
                temp = end_x
                end_x = start_x
                start_x = temp
            self.draw_the_actual_line(start_x, end_x, start_y)

    def draw_the_actual_line(self, start, end, reference):
        if start > 200:  # = x
            for i in range(start, end + 1):
                self.grid[reference][i] = '#'
            if start < self.min_x:
                self.min_x = start
            if end > self.max_x:
                self.max_x = end
        else:
            for i in range(start, end + 1):
                self.grid[i][reference] = '#'
            if start < self.min_y:
                self.min_y = start
            if end > self.max_y:
                self.max_y = end

    def run_simulation(self):
        score = 0
        while True:
            if not self.insert_new_sand():
                self.print_grid(self.min_x, self.max_x, 0, self.max_y, self.insert, False, False)
                return score
            else:
                score += 1

    def insert_new_sand(self):
        sand = (self.insert, 0)
        stop = False
        while not stop:
            if sand[1] == len(self.grid) - 1 or self.grid[sand[1]][sand[0]] == "o":
                return False
            tile_below = self.grid[sand[1] + 1][sand[0]]
            if tile_below == ".":
                if self.grid[sand[1]][sand[0]] != "+":
                    self.grid[sand[1]][sand[0]] = "."
                sand = (sand[0], sand[1] + 1)
                self.grid[sand[1]][sand[0]] = "~"
            else:
                # bottom left
                tile_below = self.grid[sand[1] + 1][sand[0] - 1]
                if tile_below == ".":
                    if self.grid[sand[1]][sand[0]] != "+":
                        self.grid[sand[1]][sand[0]] = "."
                    sand = (sand[0] - 1, sand[1] + 1)
                    self.grid[sand[1]][sand[0]] = "~"
                else:
                    # bottom right
                    tile_below = self.grid[sand[1] + 1][sand[0] + 1]
                    if tile_below == ".":
                        if self.grid[sand[1]][sand[0]] != "+":
                            self.grid[sand[1]][sand[0]] = "."
                        sand = (sand[0] + 1, sand[1] + 1)
                        self.grid[sand[1]][sand[0]] = "~"
                    else:
                        # settle
                        self.grid[sand[1]][sand[0]] = "o"
                        self.min_x = sand[0] - 2 if sand[0] < self.min_x else self.min_x
                        self.max_x = sand[0] + 2 if sand[0] > self.max_x else self.max_x
                        stop = True
        return True

    def insert_floor(self):
        floor_line = self.grid[self.max_y + 2]
        for i in range(len(floor_line)):
            self.grid[self.max_y + 2][i] = "#"
        self.max_y += 2

    def solve1(self):
        logging.info("Executing Solve1")
        return self.run_simulation()

    def solve2(self):
        logging.info("Executing Solve2")
        self.__init__()
        self.insert_floor()
        return self.run_simulation()


if __name__ == '__main__':
    d = Day14()
    print(f"ans1: {d.solve1()}")
    print(f"ans2: {d.solve2()}")
