from collections import defaultdict

from src.definitions import INPUT_DIR
import logging


class Day25:
    file = None

    def __init__(self):
        self.snafu_input: list[str] = []
        self.file = open(f"{INPUT_DIR}/day25.txt", "r")
        for line in self.file:
            self.snafu_input.append(line.strip())

    def __del__(self):
        self.file.close()

    @staticmethod
    def translate_snafu_to_decimal(snafu) -> int:
        values: list[int] = []
        snafu_rev = snafu[::-1]
        for idx in range(len(snafu_rev)):
            char = snafu_rev[idx]
            if char == "-":
                value = -1
            elif char == "=":
                value = -2
            else:
                value = int(char)
            if idx > 0:
                value = value * (5**idx)
            values.append(value)
            # print(idx, char, value)
        decimal = sum(values)
        return decimal

    @staticmethod
    def translate_decimal_to_snafu(decimal) -> str:
        i = 1
        while decimal // (5 ** i) > 0:
            i += 1
        values: list[int] = [0] * i
        for x in range(i - 1, 0, -1):
            f = decimal // (5 ** x)
            values[x] = f
            decimal -= values[x] * (5 ** x)
        values[0] = decimal
        found = True
        while found:
            found = False
            for k, v in enumerate(values):
                if v >= 3:
                    try:
                        values[k + 1] += 1
                    except IndexError:
                        values.append(1)
                    values[k] = v - 5
                    found = True
        snafu = ""
        for i in range(len(values) - 1, -1, -1):
            if values[i] >= 0:
                snafu += str(values[i])
            elif values[i] == -1:
                snafu += "-"
            elif values[i] == -2:
                snafu += "="
            else:
                assert False, "euhhh.."
        assert isinstance(snafu, str)
        return snafu

    def solve1(self):
        logging.info("Executing Solve1")
        decimals: list[int] = []
        for snafu in self.snafu_input:
            decimal: int = self.translate_snafu_to_decimal(snafu)
            decimals.append(decimal)
        print(decimals, sum(decimals))
        return self.translate_decimal_to_snafu(sum(decimals))

    def solve2(self):
        logging.info("Executing Solve2")
        return False


if __name__ == '__main__':
    d = Day25()
    print(f"ans1: {d.solve1()}")
    print(f"ans2: {d.solve2()}")
