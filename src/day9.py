import operator
from typing import Tuple, Any

from src.definitions import INPUT_DIR
import logging


class Day9:
    file = None
    pos_head: tuple[int, int] = (0, 0)
    pos_tail: tuple[int, int] = (0, 0)
    multi_tail = [(0, 0)] * 9
    tail_set = {(0, 0)}
    multi_tail_set = {(0, 0)}

    def __init__(self):
        self.file = open(f"{INPUT_DIR}/day9.txt", "r")

    def __del__(self):
        self.file.close()

    def do_the_moves(self, diff):
        self.pos_head = tuple(map(sum, zip(self.pos_head, diff)))
        self.pos_tail = self.follow(self.pos_head, self.pos_tail)
        self.multi_tail_follow()
        self.tail_set.add(self.pos_tail)
        self.multi_tail_set.add(self.multi_tail[-1])
        logging.info(f"head pos: {self.pos_head}")
        logging.info(f"tail pos: {self.pos_tail}")

    def walk(self):
        for line in self.file:
            instruction = line.strip().split()
            logging.info(instruction[0], instruction[1])
            direction = instruction[0]
            count = int(instruction[1])
            if direction == "U":
                for _ in range(count):
                    self.do_the_moves((0, -1))
            elif direction == "D":
                for _ in range(count):
                    self.do_the_moves((0, 1))
            elif direction == "L":
                for _ in range(count):
                    self.do_the_moves((-1, 0))
            elif direction == "R":
                for _ in range(count):
                    self.do_the_moves((1, 0))

    @staticmethod
    def follow(head, tail):
        diff = tuple(map(lambda i, j: i - j, head, tail))
        x = diff[0]
        y = diff[1]
        mov_x, mov_y = 0, 0
        if x > 1 or x < -1 or y > 1 or y < -1:
            if x > 0:
                mov_x = 1
            if x < 0:
                mov_x = -1
            if y > 0:
                mov_y = 1
            if y < 0:
                mov_y = -1
        return tuple(map(sum, zip(tail, (mov_x, mov_y))))

    def multi_tail_follow(self):
        for idx, item in enumerate(self.multi_tail):
            if idx == 0:
                self.multi_tail[idx] = self.follow(self.pos_head, self.multi_tail[idx])
            else:
                self.multi_tail[idx] = self.follow(self.multi_tail[idx - 1], self.multi_tail[idx])

    def solve1(self):
        logging.info("Executing Solve1")
        self.walk()
        return len(self.tail_set)

    def solve2(self):
        logging.info("Executing Solve2")
        return len(self.multi_tail_set)


if __name__ == '__main__':
    d = Day9()
    print(f"ans1: {d.solve1()}")
    print(f"ans2: {d.solve2()}")
