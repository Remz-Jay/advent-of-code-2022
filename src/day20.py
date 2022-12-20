from src.definitions import INPUT_DIR
import logging

KEY = 811589153

class Day20:
    file = None

    def __init__(self):
        self.input = []
        self.actual = []
        self.decrypted = []
        self.file = open(f"{INPUT_DIR}/day20.txt", "r")
        for line in self.file:
            value = int(line.strip())
            self.input.append(value)
        self.actual = [x for x in range(len(self.input))]
        self.decrypted = [x * KEY for x in self.input]
        logging.info(self.input)
        logging.info(self.actual)
        logging.info(self.decrypted)
    def __del__(self):
        self.file.close()

    def translate(self, input_list: []) -> list:
        output = []
        for i in self.actual:
            output.append(input_list[i])
        return output

    def run_the_numbers(self, input_list: [], rounds=None):
        counter = 0
        assert len(input_list) == len(self.actual)
        for idx, value in enumerate(input_list):
            if rounds is not None:
                if counter == rounds:
                    return
                else:
                    counter += 1
            idx_actual = self.actual.index(idx)
            idx_insert = (idx_actual + value) % (len(input_list) - 1)
            logging.info(f" {idx_insert} = ({idx_actual} + {value} % ({len(input_list)} - 1)")
            if idx_insert == 0 and value < 0:
                logging.info("beep boop")
                idx_insert = len(input_list)
            self.actual.pop(idx_actual)
            self.actual.insert(idx_insert, idx)

    def get_result(self, input_list: list):
        output = self.translate(input_list)
        idx_0 = output.index(0)
        num_1000 = output[(idx_0 + 1000) % len(output)]
        num_2000 = output[(idx_0 + 2000) % len(output)]
        num_3000 = output[(idx_0 + 3000) % len(output)]
        return num_1000 + num_2000 + num_3000

    def solve1(self):
        logging.info("Executing Solve1")
        # the grove coordinates can be found by looking at the 1000th, 2000th, and 3000th numbers after the value 0, wrapping around the list as necessary.
        self.run_the_numbers(self.input)
        return self.get_result(self.input)

    def solve2(self):
        logging.info("Executing Solve2")
        for _ in range(10):
            self.run_the_numbers(self.decrypted)
        return self.get_result(self.decrypted)

if __name__ == '__main__':
    d = Day20()
    print(f"ans1: {d.solve1()}")
    print(f"ans2: {d.solve2()}")

