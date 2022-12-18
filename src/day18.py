from src.definitions import INPUT_DIR
import logging


class Cube:
    x: int = None
    y: int = None
    z: int = None

    def __init__(self, *args) -> None:
        if isinstance(args[0], tuple) or isinstance(args[0], list):
            self.x, self.y, self.z = map(int, args[0])
        else:
            self.x = int(args[0])
            self.y = int(args[1])
            self.z = int(args[2])

    def __eq__(self, other):
        if not isinstance(other, Cube):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.x == other.x and self.y == other.y and self.z == other.z

    def as_tuple(self):
        return self.x, self.y, self.z

    def __str__(self) -> str:
        return f"{self.x},{self.y},{self.z}"


class Day18:
    file = None

    def __init__(self):
        self.cubes = []
        self.file = open(f"{INPUT_DIR}/day18.txt", "r")
        for line in self.file:
            c = Cube(line.split(","))
            self.cubes.append(c)

    def __del__(self):
        self.file.close()

    def neighbor_exists(self, x, y, z):
        c = Cube(x, y, z)
        if c in self.cubes:
            return True
        return False

    def solve1(self):
        logging.info("Executing Solve1")
        total: int = 0
        for c in self.cubes:
            sides: int = 0
            if not self.neighbor_exists(c.x + 1, c.y, c.z): sides += 1
            if not self.neighbor_exists(c.x - 1, c.y, c.z): sides += 1
            if not self.neighbor_exists(c.x, c.y + 1, c.z): sides += 1
            if not self.neighbor_exists(c.x, c.y - 1, c.z): sides += 1
            if not self.neighbor_exists(c.x, c.y, c.z + 1): sides += 1
            if not self.neighbor_exists(c.x, c.y, c.z - 1): sides += 1
            total += sides
        return total

    def solve2(self):
        logging.info("Executing Solve2")
        self.file.seek(0)
        return False


if __name__ == '__main__':
    d = Day18()
    print(f"ans1: {d.solve1()}")
    print(f"ans2: {d.solve2()}")
