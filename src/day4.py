from src.definitions import INPUT_DIR


def prep_line(line):
    line = line.strip()
    parts = line.split(",")
    parts_a = parts[0].split("-")
    parts_b = parts[1].split("-")
    elf_a = set(range(int(parts_a[0]), int(parts_a[1]) + 1))
    elf_b = set(range(int(parts_b[0]), int(parts_b[1]) + 1))
    return elf_a, elf_b


class Day4:
    file = None

    def __init__(self):
        self.file = open(f"{INPUT_DIR}/day4.txt", "r")

    def __del__(self):
        self.file.close()

    def solve1(self):
        score: int = 0
        for line in self.file:
            elves = prep_line(line)
            if elves[0].issubset(elves[1]) or elves[1].issubset(elves[0]):
                score += 1
        return score

    def solve2(self):
        score: int = 0
        self.file.seek(0)
        for line in self.file:
            elves = prep_line(line)
            set_c = list(elves[0] & elves[1])
            if len(set_c) > 0:
                score += 1
        return score


if __name__ == '__main__':
    d = Day4()
    print(f"ans1: {d.solve1()}")
    print(f"ans2: {d.solve2()}")
