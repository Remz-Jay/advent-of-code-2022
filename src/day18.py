import functools
import math
import sys

from src.definitions import INPUT_DIR
import logging

sys.setrecursionlimit(10000)


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
    min_x = min_y = min_z = math.inf
    max_x = max_y = max_z = -math.inf

    def __init__(self):
        self.cubes = []
        self.ok = []
        self.nok = []
        self.cur = []
        self.file = open(f"{INPUT_DIR}/day18.txt", "r")
        for line in self.file:
            c = Cube(line.split(","))
            self.cubes.append(c)
            self.min_x = min(self.min_x, c.x)
            self.min_y = min(self.min_y, c.y)
            self.min_z = min(self.min_z, c.z)
            self.max_x = max(self.max_x, c.x)
            self.max_y = max(self.max_y, c.y)
            self.max_z = max(self.max_z, c.z)
        self.min_x -= 1
        self.min_y -= 1
        self.min_z -= 1
        self.max_x += 1
        self.max_y += 1
        self.max_z += 1

    def __del__(self):
        self.file.close()

    def neighbor_exists(self, x, y, z):
        c = Cube(x, y, z)
        if c in self.cubes:
            return True
        return False

    @functools.lru_cache(maxsize=None)
    def can_see_open_air(self, x, y, z):
        c = Cube(x, y, z)
        if c in self.cur: return False
        if c in self.ok: return True
        if c in self.nok: return False
        if not self.min_x <= x <= self.max_x:
            self.ok.append(c)
            return True
        if not self.min_y <= y <= self.max_y:
            self.ok.append(c)
            return True
        if not self.min_z <= z <= self.max_z:
            self.ok.append(c)
            return True
        if c in self.cubes:
            self.nok.append(c)
            return False
        self.cur.append(c)
        if self.can_see_open_air(c.x + 1, c.y, c.z):
            self.ok.append(c)
            self.cur.remove(c)
            return True
        if self.can_see_open_air(c.x - 1, c.y, c.z):
            self.ok.append(c)
            self.cur.remove(c)
            return True
        if self.can_see_open_air(c.x, c.y + 1, c.z):
            self.ok.append(c)
            self.cur.remove(c)
            return True
        if self.can_see_open_air(c.x, c.y - 1, c.z):
            self.ok.append(c)
            self.cur.remove(c)
            return True
        if self.can_see_open_air(c.x, c.y, c.z + 1):
            self.ok.append(c)
            self.cur.remove(c)
            return True
        if self.can_see_open_air(c.x, c.y, c.z - 1):
            self.ok.append(c)
            self.cur.remove(c)
            return True
        self.nok.append(c)
        self.cur.remove(c)
        return False

    def neighbor_exists_or_is_a_bubble(self, x, y, z):
        c = Cube(x, y, z)
        if not self.min_x <= x <= self.max_x:
            return False
        if not self.min_y <= y <= self.max_y:
            return False
        if not self.min_z <= z <= self.max_z:
            return False
        if c in self.cubes:
            return True
        else:
            sides = 0
            if self.neighbor_exists(c.x + 1, c.y, c.z): sides += 1
            if self.neighbor_exists(c.x - 1, c.y, c.z): sides += 1
            if self.neighbor_exists(c.x, c.y + 1, c.z): sides += 1
            if self.neighbor_exists(c.x, c.y - 1, c.z): sides += 1
            if self.neighbor_exists(c.x, c.y, c.z + 1): sides += 1
            if self.neighbor_exists(c.x, c.y, c.z - 1): sides += 1
            return True if sides == 6 else False

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
        total: int = 0
        for c in self.cubes:
            sides: int = 0
            if self.can_see_open_air(c.x + 1, c.y, c.z): sides += 1
            if self.can_see_open_air(c.x - 1, c.y, c.z): sides += 1
            if self.can_see_open_air(c.x, c.y + 1, c.z): sides += 1
            if self.can_see_open_air(c.x, c.y - 1, c.z): sides += 1
            if self.can_see_open_air(c.x, c.y, c.z + 1): sides += 1
            if self.can_see_open_air(c.x, c.y, c.z - 1): sides += 1
            total += sides
        return total


if __name__ == '__main__':
    d = Day18()
    print(f"ans1: {d.solve1()}")
    print(f"ans2: {d.solve2()}")
