import math

from src.definitions import INPUT_DIR
import logging


def get_remainder(num, divisor):
    return num - divisor * (num // divisor)


class Day11:
    file = None

    def __init__(self):
        self.file = open(f"{INPUT_DIR}/day11.txt", "r")
        self.rounds = 0
        self.activity = []
        self.monkeys = []
        self.gcd = 1
        self.no_worries = True
        self.parse_input()

    def __del__(self):
        self.file.close()

    def parse_input(self):
        current_monkey = 0
        items = []
        op = ""
        test = []
        for line in self.file:
            line = line.strip()
            if line.startswith("Monkey"):
                current_monkey = int(line.split()[1].split(":")[0])
            if line.startswith("Starting items"):
                items = list(map(int, line.split(": ")[1].split(",")))
            if line.startswith("Operation"):
                op = line.split(": ")[1].strip()
            if line.startswith("Test"):
                v = int(line.split()[-1])
                test.append(v)
                self.gcd *= v
            if line.startswith("If true"):
                test.append(int(line.split()[-1]))
            if line.startswith("If false:"):
                test.append(int(line.split()[-1]))
                monkey = {
                    "id": current_monkey,
                    "items": items,
                    "operation": op,
                    "test": test
                }
                print(monkey)
                self.monkeys.append(monkey)
                test = []
        self.activity = [0] * len(self.monkeys)

    def run_rounds(self, num_rounds):
        for current_round in range(0, num_rounds):
            self.rounds = current_round
            for monkey in self.monkeys:
                self.process_monkey(monkey)
        logging.info(f"After round {current_round}, the monkeys are holding items with these worry levels:")
        for monkey in self.monkeys:
            logging.info(f"Monkey {monkey['id']}: {monkey['items']}")

    def process_monkey(self, monkey):
        logging.info(f"Monkey {monkey['id']}:")
        for item in monkey["items"]:
            self.activity[monkey['id']] += 1
            exp_as_func = eval('lambda old: ' + monkey["operation"].split('=')[1])
            item = exp_as_func(item)
            logging.info(f"\tMonkey inspects an item with a worry level of {item}.")
            logging.info(f"\t\tWorry level is now {item}.")
            if self.no_worries:
                item = math.floor(item / 3)
            else:
                item = item % self.gcd
            logging.info(f"\t\tMonkey gets bored with item. Worry level is divided by 3 to {item}.")
            div = (item % monkey['test'][0] == 0)
            logging.info(f"\t\tCurrent worry level is {div} divisible by {monkey['test'][0]}.")
            if div:
                logging.info(f"\t\tItem with worry level {item} is thrown to monkey {monkey['test'][1]}.")
                self.monkeys[monkey['test'][1]]["items"].append(item)
            else:
                logging.info(f"\t\tItem with worry level {item} is thrown to monkey {monkey['test'][2]}.")
                self.monkeys[monkey['test'][2]]["items"].append(item)
        monkey["items"] = []

    def get_result(self):
        logging.info(f"== After round {self.rounds + 1} ==")
        for monkey in self.monkeys:
            logging.info(f"Monkey {monkey['id']} inspected items {self.activity[monkey['id']]} times.")
        self.activity.sort(reverse=True)
        return self.activity[0] * self.activity[1]

    def solve1(self):
        logging.info("Executing Solve1")
        self.run_rounds(20)
        return self.get_result()

    def solve2(self):
        logging.info("Executing Solve2")
        self.__init__()
        self.no_worries = False
        self.run_rounds(10000)
        return self.get_result()


if __name__ == '__main__':
    d = Day11()
    print(f"ans1: {d.solve1()}")
    print(f"ans2: {d.solve2()}")
