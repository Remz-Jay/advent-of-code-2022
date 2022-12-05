from src.definitions import INPUT_DIR
import logging


class Day3:
    file = None
    alfa = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    rdict = dict([(x[1], x[0]) for x in enumerate(alfa)])

    def __init__(self):
        self.file = open(f"{INPUT_DIR}/day3.txt", "r")

    def __del__(self):
        self.file.close()

    def solve1(self):
        score: int = 0
        for line in self.file:
            line = line.strip()
            logging.info(line)
            strlen = len(line)
            assert strlen % 2 == 0
            logging.info(strlen)
            strlen = int(strlen / 2)
            logging.info(strlen)
            logging.info(f"{line[:strlen]},{line[strlen:]}")
            a = list(set(line[:strlen]) & set(line[strlen:]))
            logging.info(f"{a[0]},{self.rdict[a[0]] + 1}")
            score += (self.rdict[a[0]] + 1)
        return score

    def solve2(self):
        score: int = 0
        itt: int = 0
        strs = []
        self.file.seek(0)
        for line in self.file:
            line = line.strip()
            strs.append(line)
            if itt == 2:
                itt = 0
                logging.info(f"{strs}")
                a = list(set(strs[0]) & set(strs[1]) & set(strs[2]))
                assert len(a) == 1
                logging.info(f"{a}")
                score += (self.rdict[a[0]] + 1)
                strs = []
            else:
                itt = itt + 1
        return score


if __name__ == '__main__':
    d = Day3()
    print(f"ans1: {d.solve1()}")
    print(f"ans2: {d.solve2()}")
