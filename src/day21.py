from src.definitions import INPUT_DIR
import logging


class Day21:
    file = None

    def __init__(self):
        self.monkeys: dict = {}
        self.file = open(f"{INPUT_DIR}/day21.txt", "r")
        for line in self.file:
            line = line.strip().split(": ")
            self.monkeys[line[0]] = line[1]

    def __del__(self):
        self.file.close()

    def cycle(self):
        for key, value in self.monkeys.items():
            if isinstance(value, str) and value.isnumeric():
                value = int(value)
                self.monkeys[key] = value
            elif isinstance(value, str) and len(value) > 4:
                bits = value.split(" ")
                count = 0
                if not bits[0].lstrip("-").isnumeric() and isinstance(self.monkeys[bits[0]], int):
                    bits[0] = self.monkeys[bits[0]]
                    count += 1
                elif bits[0].lstrip("-").isnumeric():
                    count += 1
                if not bits[2].lstrip("-").isnumeric() and isinstance(self.monkeys[bits[2]], int):
                    bits[2] = self.monkeys[bits[2]]
                    count += 1
                elif bits[2].lstrip("-").isnumeric():
                    count += 1
                if count == 2:
                    self.monkeys[key] = int(eval(f"{bits[0]} {bits[1]} {bits[2]}"))
                else:
                    self.monkeys[key] = f"{bits[0]} {bits[1]} {bits[2]}"


    def solve1(self):
        logging.info("Executing Solve1")
        while not isinstance(self.monkeys["root"], int):
            self.cycle()
            print(self.monkeys)
        return self.monkeys["root"]

    def solve2(self, counter = 337827337000, step = 5): # <-- trial & error to narrow the range
        logging.info("Executing Solve2")
        self.__init__()
        self.monkeys["humn"] = counter
        root = self.monkeys["root"].split()
        del self.monkeys["root"]
        # root[0] 221864598376080 <-- goes down if counter goes up
        # root[2] 109255486022220 <-- constant
        diff_old = 0
        while True:
            while not (isinstance(self.monkeys[root[0]], int) and isinstance(self.monkeys[root[2]], int)):
                self.cycle()
            print(diff_old - self.monkeys[root[0]], self.monkeys[root[0]] - self.monkeys[root[2]])
            diff_old = self.monkeys[root[0]]
            if self.monkeys[root[0]] == self.monkeys[root[2]]:
                print(root[0], root[2], self.monkeys[root[0]], self.monkeys[root[2]])
                return self.monkeys["humn"]
            else:
                self.__init__()
                counter += step # <-- see print(diff_old - self.monkeys[root[0]], self.monkeys[root[0]] - self.monkeys[root[2]])
                self.monkeys["humn"] = counter
                if counter % 1000 == 0:
                    print(counter)



if __name__ == '__main__':
    d = Day21()
    print(f"ans1: {d.solve1()}")
    print(f"ans2: {d.solve2()}")