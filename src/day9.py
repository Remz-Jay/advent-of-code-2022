from src.definitions import INPUT_DIR
import logging

HEAD: int = 0


class Day9:

    def __init__(self):
        self.file = open(f"{INPUT_DIR}/day9.txt", "r")
        rope_length: int = 10
        self.rope: list[tuple[int, int]] = [(0, 0)] * rope_length
        self.knot_positions_unique: list[set[tuple[int, int]]] = [{(0, 0)}] * rope_length

    def __del__(self):
        self.file.close()

    def do_the_moves(self, diff: tuple[int, int], count: int):
        for _ in range(count):
            self.rope[HEAD] = tuple[int, int](map(sum, zip(self.rope[HEAD], diff)))
            self.multi_tail_follow()
            for idx in range(0, len(self.rope)):
                foo = set[tuple[int, int]](self.knot_positions_unique[idx])
                foo.add(self.rope[idx])
                self.knot_positions_unique[idx] = foo

    def walk(self):
        for line in self.file:
            instruction = line.strip().split()
            logging.info(instruction[0], instruction[1])
            direction = instruction[0]
            count = int(instruction[1])
            if direction == "U":
                self.do_the_moves((0, -1), count)
            elif direction == "D":
                self.do_the_moves((0, 1), count)
            elif direction == "L":
                self.do_the_moves((-1, 0), count)
            elif direction == "R":
                self.do_the_moves((1, 0), count)

    @staticmethod
    def follow(head, tail):
        diff = tuple[int, int](map(lambda i, j: i - j, head, tail))
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
        return tuple[int, int](map(sum, zip(tail, (mov_x, mov_y))))

    def multi_tail_follow(self):
        for idx in range(1, len(self.rope)):
            self.rope[idx] = self.follow(self.rope[idx - 1], self.rope[idx])

    def solve1(self):
        logging.info("Executing Solve1")
        self.walk()
        return len(self.knot_positions_unique[1])

    def solve2(self):
        logging.info("Executing Solve2")
        return len(self.knot_positions_unique[-1])


if __name__ == '__main__':
    d = Day9()
    print(f"ans1: {d.solve1()}")
    print(f"ans2: {d.solve2()}")
