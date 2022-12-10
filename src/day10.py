from src.definitions import INPUT_DIR
import logging


class Day10:

    def __init__(self):
        self.file = open(f"{INPUT_DIR}/day10.txt", "r")
        self.register_x = 1
        self.wait = 0
        self.pos = 0
        self.clock_cycles = 0
        self.commands: list[tuple[int, int]] = []
        self.crt_buffer = [[]]
        self.parse_commands()

    def __del__(self):
        self.file.close()

    def parse_commands(self):
        for line in self.file:
            bits = line.strip().split()
            if len(bits) > 1:
                self.commands.append(tuple[int, int]((int(bits[1]), 2)))
            else:
                self.commands.append(tuple[int, int]((0, 1)))

    def sum_cycles(self):
        score = 0
        for y in range(0, 240, 1):
            self.tick()
            if self.clock_cycles + 1 in range(20, 221, 40):
                logging.info(self.clock_cycles, self.register_x)
                score += (self.clock_cycles + 1) * self.register_x
            if self.clock_cycles in range(0, 241, 40):
                self.crt_buffer.append([])
        return score

    def tick(self):
        foo = self.clock_cycles % 40
        if foo == self.register_x - 1 or foo == self.register_x or foo == self.register_x + 1:
            self.crt_buffer[-1].append("#")
        else:
            self.crt_buffer[-1].append(".")
        self.clock_cycles += 1
        command = self.commands[self.pos]
        logging.info(self.clock_cycles, self.register_x, self.pos, self.wait, command[1], command[0])
        if command[1] > 1 and self.wait < command[1] - 1:
            self.wait += 1
        else:
            self.register_x += command[0]
            self.pos += 1
            self.wait = 0

    def solve1(self):
        logging.info("Executing Solve1")
        return self.sum_cycles()

    def solve2(self):
        logging.info("Executing Solve2")
        strbuf = ""
        for x in self.crt_buffer:
            for y in x:
                strbuf += y
            strbuf += "\n"
        return strbuf


if __name__ == '__main__':
    d = Day10()
    print(f"ans1: {d.solve1()}")
    print(f"ans2:\n{d.solve2()}")
