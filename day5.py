import copy
import logging
import re
import sys


def send_message(local_stacks):
    message = ""
    for s in local_stacks:
        if s:
            message += s.pop()
    return message


class Day5:
    file = None
    stacks = [[] for i in range(9)]
    operations = []

    def __init__(self):
        self.file = open("input/day5.txt", "r")
        for line in self.file:
            if "[" in line:
                iterator = re.finditer(r'[A-Z]', line)
                indices = [m.start(0) for m in iterator]
                for i in indices:
                    self.stacks[int(i / 4)].append(line[i])
            elif "move" in line:
                foo = line.split()
                self.operations.append([foo[1], foo[3], foo[5]])

        for i in range(len(self.stacks)):
            self.stacks[i].reverse()
        logging.info(self.stacks)
        logging.info(self.operations)

    def __del__(self):
        self.file.close()

    def solve1(self):
        local_stacks = copy.deepcopy(self.stacks)
        for o in self.operations:
            for i in range(int(o[0])):
                obj = local_stacks[int(o[1]) - 1].pop()
                local_stacks[int(o[2]) - 1].append(obj)
            logging.info(local_stacks)
        return send_message(local_stacks)

    def solve2(self):
        local_stacks = copy.deepcopy(self.stacks)
        for o in self.operations:
            objs = []
            for i in range(int(o[0])):
                objs.append(local_stacks[int(o[1]) - 1].pop())
            objs.reverse()
            local_stacks[int(o[2]) - 1].extend(objs)
            logging.info(local_stacks)
        return send_message(local_stacks)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.ERROR, format='%(levelname)-8s %(message)s')
    d = Day5()
    print(f"ans1: {d.solve1()}")
    print(f"ans2: {d.solve2()}")
