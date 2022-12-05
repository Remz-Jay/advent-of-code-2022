import logging
import sys


class {{id|capitalize}}:
    file = None

    def __init__(self):
        self.file = open("input/{{id}}.txt", "r")

    def __del__(self):
        self.file.close()

    def solve1(self):
        logging.info("Executing Solve1")
        return False

    def solve2(self):
        logging.info("Executing Solve2")
        self.file.seek(0)
        return False


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(levelname)-8s %(message)s')
    d = {{id|capitalize}}()
    print(f"ans1: {d.solve1()}")
    print(f"ans2: {d.solve2()}")
