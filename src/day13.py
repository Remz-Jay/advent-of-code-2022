import functools

from src.definitions import INPUT_DIR
import logging


def compare(left, right):
    logging.info(f"- Compare {left} vs {right}")
    for iter, l in enumerate(left):
        if len(right) > iter:
            r = right[iter]
            if isinstance(l, int) and isinstance(r, int):
                logging.info(f"\t- Compare {l} vs {r}")
                if l < r:
                    logging.info(f"\t\t- Left side is smaller, so inputs are *in the right order*")
                    return 1
                elif l > r:
                    logging.info(f"\t\t- Right side is smaller, so inputs are not in the right order")
                    return -1
            elif isinstance(l, list) and isinstance(r, list):
                test = compare(l, r)
                if test != 0:
                    return test
            elif isinstance(l, int) and isinstance(r, list):
                test = compare([l], r)
                if test != 0:
                    return test
            else:
                test = compare(l, [r])
                if test != 0:
                    return test
        else:
            logging.info(f"- Right side ran out of items, so inputs are not in the right order")
            return -1
    if len(right) > len(left):
        logging.info(f"- Left side ran out of items, so inputs are in the right order")
        return 1
    return 0


class Day13:
    file = None
    inputs = []

    def __init__(self):
        self.file = open(f"{INPUT_DIR}/day13.txt", "r")
        for line in self.file:
            if len(line) > 1:
                self.inputs.append(eval(line.strip()))

    def __del__(self):
        self.file.close()

    def solve1(self):
        logging.info("Executing Solve1")
        pair = 0
        score = 0
        for iter, item in enumerate(self.inputs):
            if iter % 2 == 0:
                left = item
                pair += 1
            else:
                right = item
                logging.info(f"== Pair {pair} ==")
                if compare(left, right) == 1:
                    logging.info(f"Adding {pair} to score")
                    score += pair
        return score

    def solve2(self):
        logging.info("Executing Solve2")
        mylist = sorted(self.inputs, key=functools.cmp_to_key(compare), reverse=True)
        left, right = 0, 0
        for iter, i in enumerate(mylist):
            print(i)
            if i == [[2]]:
                left = iter + 1
            if i == [[6]]:
                right = iter + 1
        print(left, right)
        return left * right


if __name__ == '__main__':
    d = Day13()
    print(f"ans1: {d.solve1()}")
    # print(f"ans2: {d.solve2()}")
