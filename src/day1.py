from src.definitions import INPUT_DIR
import logging


class Day1:
    elves = []
    file = None

    def __init__(self):
        self.file = open(f"{INPUT_DIR}/day1.txt", "r")

    def __del__(self):
        self.file.close()

    def solve1(self):
        calories = 0
        for line in self.file:
            if line.strip():
                calories = calories + int(line)
            else:
                self.elves.append(calories)
                calories = 0
        if calories != 0:
            self.elves.append(calories)
        return max(self.elves)

    def solve2(self):
        self.elves.sort(reverse=True)
        logging.info(self.elves)
        return sum(self.elves[0:3])


if __name__ == '__main__':
    d = Day1()
    print(f"ans1: {d.solve1()}")
    print(f"ans2: {d.solve2()}")
