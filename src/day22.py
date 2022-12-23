from itertools import groupby
from collections import defaultdict
from dataclasses import dataclass
from typing import Tuple

from src.definitions import INPUT_DIR
import logging


@dataclass
class Dir:
    # cardinal directions in order, so we can rotate with +/- 1
    RIGHT: int = 0
    DOWN: int = 1
    LEFT: int = 2
    UP: int = 3

    @staticmethod
    def str(indicator: int) -> str:
        match indicator:
            case Dir.RIGHT:
                return "RIGHT"
            case Dir.DOWN:
                return "DOWN"
            case Dir.LEFT:
                return "LEFT"
            case Dir.UP:
                return "UP"
            case _:
                assert False, "is this even possible?"

    @staticmethod
    def sign(indicator: int) -> str:
        match indicator:
            case Dir.RIGHT:
                return "→"
            case Dir.DOWN:
                return "↓"
            case Dir.LEFT:
                return "←"
            case Dir.UP:
                return "↑"
            case _:
                assert False, "is this even possible?"

    @staticmethod
    def xy_for_dir(direction: int) -> tuple[int, int]:
        match direction:
            case Dir.RIGHT:
                x = 1
                y = 0
            case Dir.DOWN:
                x = 0
                y = 1
            case Dir.LEFT:
                x = -1
                y = 0
            case Dir.UP:
                x = 0
                y = -1
            case _:
                assert False, "should not reach"
        return x, y

    def get_dir(self, indicator: str) -> int:
        assert len(indicator) == 1
        if indicator == "L": return self.LEFT
        if indicator == "R": return self.RIGHT
        if indicator == "U": return self.UP
        if indicator == "D": return self.DOWN


class Day22:
    file = None

    def __init__(self):
        # https://docs.python.org/3/library/collections.html#collections.defaultdict
        self.grid = defaultdict(lambda: " ")
        self.dir = Dir.RIGHT
        self.pos = (0, 0)
        self.maxx = 0
        self.file = open(f"{INPUT_DIR}/day22.txt", "r")
        foo = self.file.read()
        gridbit, insbit = foo.split("\n\n")
        y = 0
        for line in gridbit.split("\n"):
            self.maxx = max(self.maxx, len(line))
            for x, char in enumerate(line):
                if char != "":
                    self.grid[x, y] = char
            y += 1
        self.maxy = y
        self.instructions: list[str] = []
        # https://docs.python.org/3/library/itertools.html#itertools.groupby
        for _, g in groupby(insbit, str.isdigit):
            self.instructions.append("".join(g))

    def __del__(self):
        self.file.close()

    def rotate_left(self):
        newdir = self.dir - 1
        if newdir < 0:
            newdir += 4
        self.dir = newdir

    def rotate_right(self):
        newdir = self.dir + 1
        if newdir > 3:
            newdir -= 4
        self.dir = newdir

    def walk(self, count):
        x, y = Dir.xy_for_dir(self.dir)
        for i in range(count):
            tem_pos = (self.pos[0] + x, self.pos[1] + y)
            if not self.check_collision(tem_pos):
                tem_pos = self.warp(tem_pos)
                if not self.check_collision(tem_pos):
                    self.pos = tem_pos
                else:
                    print("Skipping step, colliding with # AFTER warp")
                    break
            else:
                print("Skipping step, colliding with #")
                break
            print(self.pos, self.grid[self.pos])
            self.draw_pos()
        print(f"EOW: at {self.pos} on a {self.grid[self.pos]}")

    def cube_walk(self, count: int):
        x, y = Dir.xy_for_dir(self.dir)
        for i in range(count):
            # dunno
            pass
        self.draw_pos()

    def check_collision(self, pos):
        return True if self.grid[pos] == "#" else False

    def draw_pos(self):
        self.grid[self.pos] = Dir.sign(self.dir)

    def warp(self, pos):
        if self.grid[pos] == " ":
            match self.dir:
                case Dir.RIGHT:
                    # move to left of the current line
                    i = 0
                    while self.grid[i, pos[1]] == " ":
                        i += 1
                    print("WARP LEFT")
                    return i, pos[1]
                case Dir.LEFT:
                    # move to the far right of the current line
                    i = self.maxx
                    while self.grid[i, pos[1]] == " ":
                        i -= 1
                    print("WARP RIGHT")
                    return i, pos[1]
                case Dir.DOWN:
                    # move to the first line and go from there
                    i = 0
                    while self.grid[pos[0], i] == " ":
                        i += 1
                    print("WARP UP")
                    return pos[0], i
                case Dir.UP:
                    # move to the last line and go from there
                    i = self.maxy
                    while self.grid[pos[0], i] == " ":
                        i -= 1
                    print("WARP DOWN")
                    return pos[0], i
        else:
            return pos

    def find_start(self):
        i = 0
        while self.grid[i, 0] != ".":
            i += 1
        self.pos = (i, 0)
        print(self.pos)

    def print_grid(self):
        for y in range(self.maxy):
            buffer = ""
            for x in range(self.maxx):
                buffer += self.grid[x, y]
            print(buffer)

    def solve1(self, width: int = 4):
        logging.info("Executing Solve1")
        self.find_start()
        for i in self.instructions:
            print(f"Doing instruction {i}")
            match i[0]:
                case "L":
                    old = self.dir
                    self.rotate_left()
                    self.draw_pos()
                    print(f"Rotated from {Dir.str(old)} to {Dir.str(self.dir)}")
                case "R":
                    old = self.dir
                    self.rotate_right()
                    self.draw_pos()
                    print(f"Rotated from {Dir.str(old)} to {Dir.str(self.dir)}")
                case _:
                    assert i[0].isdigit(), "only numbers should be left"
                    print(f"Walking {i} steps to {Dir.str(self.dir)}")
                    self.walk(int(i))
            print(f"End of step {i}, current Direction, at:", Dir.str(self.dir), self.pos)
        self.print_grid()
        return 1000 * (self.pos[1] + 1) + 4 * (self.pos[0] + 1) + self.dir

    def solve2(self):
        logging.info("Executing Solve2")
        self.__init__()
        self.find_start()
        for i in self.instructions:
            print(f"Doing instruction {i}")
            match i[0]:
                case "L":
                    old = self.dir
                    self.rotate_left()
                    self.draw_pos()
                    print(f"Rotated from {Dir.str(old)} to {Dir.str(self.dir)}")
                case "R":
                    old = self.dir
                    self.rotate_right()
                    self.draw_pos()
                    print(f"Rotated from {Dir.str(old)} to {Dir.str(self.dir)}")
                case _:
                    assert i[0].isdigit(), "only numbers should be left"
                    print(f"Walking {i} steps to {Dir.str(self.dir)}")
                    self.cube_walk(int(i))
            print(f"End of step {i}, current Direction, at:", Dir.str(self.dir), self.pos)
        self.print_grid()
        return 1000 * (self.pos[1] + 1) + 4 * (self.pos[0] + 1) + self.dir


if __name__ == '__main__':
    d = Day22()
    # yeah, let's not mess up the initial logic
    ans1 = d.solve1()
    print(f"ans1: {ans1}")
    assert(ans1 == 27436 or ans1 == 6032)
    print(f"ans2: {d.solve2()}")
