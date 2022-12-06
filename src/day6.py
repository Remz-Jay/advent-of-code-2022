from src.definitions import INPUT_DIR
import logging


class Day6:
    file = None

    def __init__(self):
        self.file = open(f"{INPUT_DIR}/day6.txt", "r")

    def __del__(self):
        self.file.close()

    def solve(self, qlen):
        self.file.seek(0)
        q1 = []
        ans = []
        for line in self.file:
            line = line.strip()
            for element in range(0, len(line)):
                q1.append(line[element])
                if len(q1) == qlen:
                    logging.info(q1)
                    if len(set(q1)) == len(q1):
                        logging.info(f"all unique at {element}")
                        ans.append(element + 1)
                        q1 = []
                        break
                    else:
                        q1.pop(0)
        return ans

    def solve1(self):
        logging.info("Executing Solve1")
        return self.solve(4)

    def solve2(self):
        logging.info("Executing Solve2")
        return self.solve(14)


if __name__ == '__main__':
    d = Day6()
    print(f"ans1: {d.solve1()}")
    print(f"ans2: {d.solve2()}")
