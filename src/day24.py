import math
from collections import defaultdict, deque
from src.definitions import INPUT_DIR
import logging


class Day24:
    file = None

    def __init__(self):
        self.grid: defaultdict[tuple] = defaultdict(lambda: ".")
        self.blizzards: defaultdict[tuple] = defaultdict(lambda: [])
        self.blizzards_at_step: defaultdict[int] = defaultdict(lambda: None)
        self.file = open(f"{INPUT_DIR}/day24.txt", "r")
        self.min_x = self.max_x = self.min_y = self.max_y = 0
        self.start: tuple[int, int] = 0, 0
        self.goal: tuple[int, int] = 0, 0
        self.shortest_dist = math.inf
        self.queue = deque()
        y = 0
        for line in self.file:
            self.max_x = len(line)
            for x, char in enumerate(line):
                if char in [">", "v", "^", "<"]:
                    self.blizzards[x, y].append(char)
                else:
                    self.grid[x, y] = char
            y += 1
        self.max_y = y
        for idx in range(self.max_x):
            if self.grid[idx, 0] == ".":
                self.start = idx, 0
                self.cur = self.start
                break
        for idx in range(self.max_x):
            if self.grid[idx, self.max_y - 1] == ".":
                self.goal = idx, self.max_y - 1
                break

    def __del__(self):
        self.file.close()

    def print_grid(self, blizzards, current_position):
        for y in range(self.min_y, self.max_y):
            buffer = f"{str(y).zfill(3)} "
            for x in range(self.min_x, self.max_x):
                b = blizzards[x, y]
                if (x, y) == current_position:
                    buffer += "E"
                elif (x, y) == self.goal:
                    buffer += "G"
                elif (x, y) == self.start:
                    buffer += "S"
                elif b:
                    if len(b) == 1:
                        buffer += b[0]
                    else:
                        buffer += str(len(b))
                else:
                    buffer += self.grid[x, y]
            print(buffer)

    def update_blizzards(self, current_blizzards: defaultdict[tuple]):
        new_blizzards: defaultdict[tuple] = defaultdict(lambda: [])
        for pos, blizzards in current_blizzards.items():
            x, y = pos
            for idx in range(len(blizzards)):
                b = blizzards[idx]
                match b:
                    case ">":
                        if self.grid[x + 1, y] == '#':
                            new_blizzards[1, y].append(b)
                        else:
                            new_blizzards[x + 1, y].append(b)
                    case "<":
                        if self.grid[x - 1, y] == '#':
                            new_blizzards[self.max_x - 2, y].append(b)
                        else:
                            new_blizzards[x - 1, y].append(b)
                    case "v":
                        if self.grid[x, y + 1] == '#':
                            new_blizzards[x, 1].append(b)
                        else:
                            new_blizzards[x, y + 1].append(b)
                    case "^":
                        if self.grid[x, y - 1] == '#':
                            new_blizzards[x, self.max_y - 2].append(b)
                        else:
                            new_blizzards[x, y - 1].append(b)
        return new_blizzards

    def move(self, current_position, step: int = 1, gro=False, sr=False):
        # if step >= self.shortest_dist:
        #     return
        # v = visited.copy()
        # if v[current_position] > 50:
        #     return
        # v[current_position] += 1
        # print(self.shortest_dist, step, current_position)
        # print("move", current_blizzards)
        if self.blizzards_at_step[step] is None:
            self.blizzards_at_step[step] = self.update_blizzards(self.blizzards_at_step[step - 1])
        blizzards = self.blizzards_at_step[step]
        # print("move", new_blizzards)
        x, y = current_position
        # right
        if len(blizzards[x + 1, y]) == 0 and self.grid[x + 1, y] != "#" and y + 1 < self.max_y - 1:
            new_position = x + 1, y
            self.queue.append((new_position, step + 1, gro, sr))
        # down
        if len(blizzards[x, y + 1]) == 0 and self.grid[x, y + 1] != "#":
            new_position = x, y + 1
            self.queue.append((new_position, step + 1, gro, sr))
        # up
        if len(blizzards[x, y - 1]) == 0 and self.grid[x, y - 1] != "#" and y - 1 >= 0:
            new_position = x, y - 1
            self.queue.append((new_position, step + 1, gro, sr))
        # left
        if len(blizzards[x - 1, y]) == 0 and self.grid[x - 1, y] != "#":
            new_position = x - 1, y
            self.queue.append((new_position, step + 1, gro, sr))
        if len(blizzards[x, y]) == 0:
            self.queue.append((current_position, step + 1, gro, sr))

    def solve1(self):
        logging.info("Executing Solve1")
        self.queue.append((self.start, 0, False, False))
        self.blizzards_at_step[-1] = self.blizzards
        visited = set()
        while len(self.queue) > 0:
            print(self.shortest_dist, len(self.queue))
            pos, step, _, _ = self.queue.popleft()
            if not (pos, step) in visited:
                visited.add((pos, step))
                if pos == self.goal:
                    self.shortest_dist = min(self.shortest_dist, step)
                elif step < self.shortest_dist:
                    self.move(pos, step)
        # visited: defaultdict[tuple] = defaultdict(lambda: 0)
        # self.print_grid(b, pos)
        # self.move(b, pos, visited)
        return self.shortest_dist

    def solve2(self):
        logging.info("Executing Solve2")
        self.shortest_dist = math.inf
        self.queue.append((self.start, 0, False, False))
        self.blizzards_at_step[-1] = self.blizzards
        md1 = math.inf
        md2 = math.inf
        visited = set()
        while len(self.queue) > 0:
            pos, step, goal_reached_once, start_reached = self.queue.popleft()
            print(self.shortest_dist, md1, md2, len(self.queue), goal_reached_once, start_reached)
            if not (pos, step, goal_reached_once, start_reached) in visited:
                visited.add((pos, step, goal_reached_once, start_reached))
                if not goal_reached_once and pos == self.goal:
                    self.queue.append((self.goal, step, True, False))
                    md1 = min(md1, step)
                elif goal_reached_once and not start_reached and pos == self.start:
                    self.queue.append((self.start, step, True, True))
                    md2 = min(md2, step)
                elif goal_reached_once and start_reached and pos == self.goal:
                    self.shortest_dist = min(self.shortest_dist, step)
                elif not goal_reached_once and step < md1:
                    self.move(pos, step, goal_reached_once, start_reached)
                elif goal_reached_once and not start_reached and step < md2:
                    self.move(pos, step, goal_reached_once, start_reached)
                elif goal_reached_once and start_reached and step < self.shortest_dist:
                    self.move(pos, step, goal_reached_once, start_reached)
        return self.shortest_dist


if __name__ == '__main__':
    d = Day24()
    print(f"ans1: {d.solve1()}")
    print(f"ans2: {d.solve2()}")
