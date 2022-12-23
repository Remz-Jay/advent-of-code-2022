from collections import defaultdict
from itertools import chain

from src.definitions import INPUT_DIR
import logging


class Dir:
    NORTH: int = 0
    SOUTH: int = 1
    WEST: int = 2
    EAST: int = 3


class Day23:
    file = None

    def __init__(self):
        self.grid: defaultdict[tuple] = defaultdict(lambda: ".")
        self.file = open(f"{INPUT_DIR}/day23.txt", "r")
        self.current_dir = Dir.NORTH
        self.min_x = self.max_x = self.min_y = self.max_y = 0
        y = 0
        for line in self.file:
            self.max_x = len(line)
            for x, char in enumerate(line):
                if char == "#":
                    self.grid[x, y] = char
            y += 1
        self.max_y = y

    def __del__(self):
        self.file.close()

    def print_grid(self):
        for y in range(self.min_y, self.max_y):
            buffer = f"{str(y).zfill(3)} "
            for x in range(self.min_x, self.max_x):
                buffer += self.grid[x, y]
            print(buffer)

    def count_grid(self) -> int:
        result = 0
        first_found = False
        for y in range(self.min_y, self.max_y):
            buffer = ""
            for x in range(self.min_x, self.max_x):
                buffer += self.grid[x, y]
            if first_found or "#" in buffer:
                first_found = True
                result += buffer.count(".")
        return result

    def next_direction(self, cur_dir):
        cdir = cur_dir + 1
        if cdir > Dir.EAST:
            cdir = Dir.NORTH
        cur_dir = (cur_dir + 1) % 4
        assert cur_dir == cdir
        return cur_dir

    def adj(self, pos):
        x, y = pos
        for ax in range(x - 1, x + 2):
            for ay in range(y - 1, y + 2):
                if not (ax == x and ay == y):
                    if self.grid[ax, ay] == "#":
                        return True
        return False

    def dir_adj(self, pos: tuple, direction: int) -> bool:
        x, y = pos
        # print(f"Proposing for elf {pos} in direction {direction}")
        match direction:
            case Dir.NORTH:
                # N, NE, or NW
                adj_pos = [(x, y - 1), (x - 1, y - 1), (x + 1, y - 1)]
            case Dir.SOUTH:
                adj_pos = [(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)]
            case Dir.WEST:
                adj_pos = [(x - 1, y), (x - 1, y - 1), (x - 1, y + 1)]
            case Dir.EAST:
                adj_pos = [(x + 1, y), (x + 1, y - 1), (x + 1, y + 1)]
            case _:
                assert False, f"dir_adj {direction}"
        for p in adj_pos:
            if self.grid[p] == "#":
                return True
        return False

    @staticmethod
    def move(pos: tuple, direction: int) -> tuple:
        x, y = pos
        match direction:
            case Dir.NORTH:
                return x, y - 1
            case Dir.SOUTH:
                return x, y + 1
            case Dir.WEST:
                return x - 1, y
            case Dir.EAST:
                return x + 1, y
            case _:
                assert False, f"funky {direction}"

    def run_round(self, counter: int = 0, exit_on_zero_moves: bool = False) -> bool:
        elves = [key for key, value in self.grid.items() if value == "#"]
        # print(elves)
        proposed_moves = {}
        for elf in elves:
            if self.adj(elf):
                for i in range(4):
                    next_dir = (self.current_dir + i) % 4
                    if not self.dir_adj(elf, next_dir):
                        proposed_moves[elf] = self.move(elf, next_dir)
                        break
        logging.info(f"Proposed moves in round {counter}: {proposed_moves}")
        if exit_on_zero_moves and len(proposed_moves) == 0:
            logging.info(f"No more moves in round {counter}")
            return False
        rev_dict = {}
        for key, value in proposed_moves.items():
            rev_dict.setdefault(value, set()).add(key)

        result = set(chain.from_iterable(
            values for key, values in rev_dict.items()
            if len(values) > 1))
        logging.info(result)
        for dup in result:
            del proposed_moves[dup]
        logging.info(f"After removing duplicates: {proposed_moves}")
        for k, v in proposed_moves.items():
            logging.info(f"Moving {k} to {v}")
            vx, vy = v
            self.min_x = min(vx, self.min_x)
            self.min_y = min(vy, self.min_y)
            self.max_x = max(vx + 1, self.max_x)
            self.max_y = max(vy + 1, self.max_y)
            self.grid[v] = "#"
            self.grid[k] = "."
        # self.print_grid()
        self.current_dir = self.next_direction(self.current_dir)
        return True

    def solve1(self):
        logging.info("Executing Solve1")
        # self.print_grid()
        for r in range(1, 11):
            self.run_round(r)
        return self.count_grid()

    def solve2(self):
        logging.info("Executing Solve2")
        # self.print_grid()
        self.__init__()
        r = 1
        while self.run_round(r, True):
            r += 1
        return r


if __name__ == '__main__':
    d = Day23()
    print(f"ans1: {d.solve1()}")
    print(f"ans2: {d.solve2()}")
