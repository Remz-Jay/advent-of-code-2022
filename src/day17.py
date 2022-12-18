from collections import Counter
from math import floor
from src.definitions import INPUT_DIR
import logging
from colorama import init as colorama_init
from colorama import Fore

colorama_init()


class Day17:
    file = None

    def __init__(self):
        self.file = open(f"{INPUT_DIR}/day17.txt", "r")
        self.moves = list(self.file.readline().strip())
        self.active_block_x = 0
        self.active_block_y = 0
        self.active_block: list = None
        self.move_counter = 0
        self.piece_counter = 0
        self.block_counter = 0
        self.grid = [[0] * 7]
        self.move_down = False
        self.pieces = [
            [
                [1, 1, 1, 1]
            ],
            [
                [0, 2, 0],
                [2, 2, 2],
                [0, 2, 0]
            ],
            [
                [3, 3, 3],
                [0, 0, 3],
                [0, 0, 3]
            ],
            [
                [4],
                [4],
                [4],
                [4]
            ],
            [
                [5, 5],
                [5, 5]
            ]
        ]

    def __del__(self):
        self.file.close()

    def generate_grid_string(self, line, colored=True):
        if colored:
            output = f"{Fore.BLUE}|{Fore.RESET}"
        else:
            output = "|"
        if line != 0:
            for i in self.grid[line]:
                if i == 0:
                    if colored:
                        output += " "
                    else:
                        output += "."
                elif i > 1:
                    if colored:
                        if i == 2:
                            output += f"{Fore.RED}█{Fore.RESET}"
                        elif i == 3:
                            output += f"{Fore.CYAN}█{Fore.RESET}"
                        elif i == 4:
                            output += f"{Fore.GREEN}█{Fore.RESET}"
                        elif i == 5:
                            output += f"{Fore.MAGENTA}█{Fore.RESET}"
                        elif i == 6:
                            output += f"{Fore.YELLOW}█{Fore.RESET}"
                    else:
                        output += "#"
                else:
                    output += "@"
        else:
            if colored:
                return f"{Fore.BLUE}+-------+{Fore.RESET}"
            else:
                return f"+-------+"
        if colored:
            output += f"{Fore.BLUE}|{Fore.RESET}"
        else:
            output += "|"
        return output

    def print_grid(self, returns=False, numbers=True, colored=True):
        output = []
        for i in range(len(self.grid) - 1, -1, -1):
            if numbers:
                output.append(f"{str(i).rjust(4, '0')}\t{self.generate_grid_string(i, colored)}")
            else:
                output.append(f"{self.generate_grid_string(i, colored)}")
        if returns:
            return output
        else:
            print("\n".join(output))

    def get_next_block(self):
        block = self.pieces[self.piece_counter]
        self.piece_counter += 1
        if self.piece_counter >= len(self.pieces): self.piece_counter = 0
        return block

    def get_next_move(self):
        move = self.moves[self.move_counter]
        self.move_counter += 1
        if self.move_counter >= len(self.moves): self.move_counter = 0
        return move

    def add_lines_to_grid(self, count):
        for i in range(count):
            self.grid.append([0] * 7)

    def drop_new_block(self):
        self.active_block = self.get_next_block()
        self.active_block_x = 2
        self.active_block_y = 0 + len(self.active_block) - 1
        self.add_lines_to_grid(len(self.active_block) + 3)
        self.move_down = False

    def join_matrices(self, mat1, mat2, mat2_off, replace=False):
        # print(mat1, mat2, mat2_off)
        off_x, off_y = mat2_off
        for cy, row in enumerate(mat2):
            for cx, val in enumerate(row):
                if replace and val > 0:
                    val += 1
                if not (mat1[cy - off_y - 1][cx + off_x] > 0 and val == 0):
                    mat1[cy - off_y - 1][cx + off_x] = val
        return mat1

    def check_collision(self, board, shape, offset):
        off_x, off_y = offset
        if off_x < 0:
            logging.info("Colliding (Left)")
            return True
        for cy, row in enumerate(shape):
            for cx, cell in enumerate(row):
                # if cx + off_x < 0:
                #     logging.info("Colliding (Left)")
                #     return True
                try:
                    line = (len(board) - 1) - (off_y - cy)
                    if self.block_counter == 0:
                        print(cx, cy, off_x, off_y, line, cx + off_x, cell, board[line][cx + off_x])
                    if line == 0:
                        logging.info("Colliding (Bottom Line)")
                        return True
                    if cell and board[line][cx + off_x]:
                        logging.info("Colliding (Collision)")
                        return True
                except IndexError:
                    logging.info("Colliding (Index Error)")
                    return True
        return False

    def resolve_block(self):
        if self.active_block is None:
            logging.info("Dropping new Block")
            self.drop_new_block()
            self.block_counter += 1
        while self.active_block is not None:
            self.move_block()

    def move_block(self):
        if self.move_down:
            logging.info("Moving Down")
            self.move_block_vertically()
        else:
            self.move_block_horizontally()
        self.move_down = not self.move_down
        self.remove_empty_lines()

    def remove_empty_lines(self):
        counter = 0
        if self.active_block:
            top = (len(self.grid) - 1) - (self.active_block_y - (len(self.active_block) - 1))
        else:
            top = 0
        for line in range(len(self.grid) - 1, 0, -1):
            logging.info(f"scanning line {line}, active top at {top}")
            if line <= top:
                break
            if self.grid[line].count(0) == 7:
                counter += 1
        for i in range(counter):
            logging.info("Removing line")
            self.grid.pop()
            self.active_block_y -= 1

    def move_block_horizontally(self):
        move = self.get_next_move()
        assert move in "><"
        if move == ">":
            logging.info("Moving Right")
            if not self.check_collision(self.grid, self.active_block, (self.active_block_x + 1, self.active_block_y)):
                self.active_block_x += 1
        else:
            logging.info("Moving Left")
            if not self.check_collision(self.grid, self.active_block, (self.active_block_x - 1, self.active_block_y)):
                self.active_block_x -= 1

    def move_block_vertically(self):
        if not self.check_collision(self.grid, self.active_block, (self.active_block_x, self.active_block_y + 1)):
            self.active_block_y += 1
        else:
            self.join_matrices(self.grid, self.active_block, (self.active_block_x, self.active_block_y), True)
            self.active_block = None

    def check_for_collision(self):
        pass

    def run(self, rounds=2022):
        for i in range(rounds):
            self.resolve_block()
        if self.active_block is not None:
            self.join_matrices(self.grid, self.active_block, (self.active_block_x, self.active_block_y))

    def repeat_moves(self, count):
        for i in range(count):
            self.move_block()

    def solve1(self, count: int = 2022, print: bool = True):
        logging.info("Executing Solve1")
        self.run(count)
        if print:
            self.print_grid(False, True, True)
        return len(self.grid) - 1

    def solve2(self):
        self.__init__()
        total = 0
        lead_in = 0
        history = []
        best = 0
        streak = 0
        stint = 0
        idx_start = 0
        idx_now = 0
        pos_start = 0
        for i in range(1, 10000):
            self.resolve_block()
            new = len(self.grid) - 1
            added = new - total
            total = new
            history.append(added)
            if idx_start == 0:
                try:
                    idx_start = idx_now = history.index(added, 0, -1)
                    pos_start = i
                    streak = 0
                    stint = 0
                except ValueError:
                    continue
            else:
                if streak > 1 and idx_now + 1 + lead_in == pos_start:
                    start = 1000000000000
                    remaining_blocks = start - lead_in
                    cycles = floor(remaining_blocks / streak)
                    lead_in_height = total - (stint * 2)
                    togo = remaining_blocks - (cycles * streak)
                    logging.info(
                        f"Done at block {i}. Streak length is {streak} with height {stint}, started at {pos_start}, with {lead_in} lead in.")
                    logging.info(f"Total height is {total}, lead in should be {lead_in_height}")
                    logging.info(f"Start with {start}. Deduct lead in, makes {remaining_blocks}")
                    logging.info(f"That fits {cycles} cycles")
                    logging.info(f"{togo} iterations to go")
                    result = lead_in_height + (stint * cycles)
                    self.__init__()
                    self.run(lead_in + streak + togo)
                    remainder_total = len(self.grid) - 1
                    diff = remainder_total - stint - lead_in_height
                    logging.info(f"Running remainder yielded {diff} blocks")
                    result += diff
                    return result
                if history[idx_now + 1] == added:
                    streak += 1
                    idx_now += 1
                    stint += added
                else:
                    best = max(best, streak)
                    for _ in range(streak):
                        history.pop(0)
                        lead_in += 1
                    streak = idx_start = idx_now = pos_start = stint = 0
        exit(0)

        """
        So.. yeah, this was quite the process.
        The solve2 solution above isn't what I used to complete the 2nd star. No, I did that "manually".
        It was over 24 hours later that I realized I could count the numbers of grid lines added per block to find
        the pattern, as implemented above.
        Had a different strategy at first: Count the times each unique horizontal "bar" combination (2^7 possibilities)
        appeared in the output, and the most common found value would be the number of times the pattern had repeated.
        Which turned out to be true, but the amount of outliers was so high during iteration, that it was impossible
        for me to reliably detect the start/end of the pattern. So, instead of improving the algo, I just did it by hand.

        Visually compared mountains of output to eventually find a pattern like:

        5876 [(3, 6), (20, 5), (7, 5), (4, 4), (11, 3)]
        5877 [(3, 6), (20, 5), (7, 5), (4, 4), (11, 3)]
        5878 [(3, 6), (20, 5), (7, 5), (4, 4), (11, 3)]
        5879 [(3, 6), (20, 5), (7, 5), (4, 4), (11, 3)]
        5880 [(4, 5), (20, 5), (7, 5), (3, 5), (11, 3)]
        5881 [(4, 6), (20, 5), (7, 5), (3, 4), (11, 3)]
        5882 [(4, 6), (20, 5), (7, 5), (3, 4), (11, 3)]
        5883 [(4, 6), (20, 5), (7, 5), (3, 4), (11, 3)]
        1720
        7596 [(4, 6), (26, 5), (9, 5), (5, 4), (14, 3)]
        7597 [(4, 6), (26, 5), (9, 5), (5, 4), (14, 3)]
        7598 [(4, 6), (26, 5), (9, 5), (5, 4), (14, 3)]
        7599 [(4, 6), (26, 5), (9, 5), (5, 4), (14, 3)]
        7600 [(5, 5), (26, 5), (9, 5), (4, 5), (14, 3)]
        7601 [(5, 6), (26, 5), (9, 5), (4, 4), (14, 3)]
        7602 [(5, 6), (26, 5), (9, 5), (4, 4), (14, 3)]
        7603 [(5, 6), (26, 5), (9, 5), (4, 4), (14, 3)]
        1720
        9316 [(5, 6), (32, 5), (11, 5), (6, 4), (17, 3)]
        9317 [(5, 6), (32, 5), (11, 5), (6, 4), (17, 3)]
        9318 [(5, 6), (32, 5), (11, 5), (6, 4), (17, 3)]
        9319 [(5, 6), (32, 5), (11, 5), (6, 4), (17, 3)]
        9320 [(6, 5), (32, 5), (11, 5), (5, 5), (17, 3)]
        9321 [(6, 6), (32, 5), (11, 5), (5, 4), (17, 3)]
        9322 [(6, 6), (32, 5), (11, 5), (5, 4), (17, 3)]
        9323 [(6, 6), (32, 5), (11, 5), (5, 4), (17, 3)]
        9324 [(6, 6), (32, 5), (11, 5), (5, 4), (17, 3)]

        From there, I did the rest of the calculations by hand, as apparent from the war zone below.
        I'll just leave this heap of garbage in the source, for the viewer to enjoy, and as a testament to the
        pain I endured trying to solve this puzzle :) -- enjoy!
        """

        lead_in = 720
        cycle = 1720
        cycle_height = 2704
        lead_in_height = 1126
        # lead_in = 134
        # cycle = 35
        # cycle_height = 53
        # lead_in_height = 210
        start = 1000000000000
        # exp = 1514285714288
        # foo = 28571428567
        # self.__init__()
        self.run(lead_in + cycle + 720)
        c9 = len(self.grid) - 1
        # print(c9 - cycle_height - lead_in_height)
        # assert 27 + (foo * cycle_height) + lead_in_height == exp
        print(1149 + (581395348 * cycle_height) + lead_in_height)
        # print(1000000000000 - ((foo * cycle) + lead_in))
        # print(start/cycle)
        # print(floor((start-lead_in)/cycle))
        # print(floor((start-lead_in)/cycle) * cycle_height)
        # print(1514285714288 - floor((start-lead_in)/cycle) * cycle_height)
        # print((start-lead_in) % cycle)
        # logging.info("Executing Solve2")
        # self.__init__()
        # self.run(lead_in)
        # c1 = len(self.grid) -1
        # self.__init__()
        # self.run(lead_in + cycle)
        # c2 = len(self.grid) -1
        # self.__init__()
        # self.run(lead_in + (cycle*2))
        # c3 = len(self.grid) - 1
        # self.__init__()
        # self.run(lead_in + (cycle*3))
        # c4 = len(self.grid) - 1
        # print(c1, c2, c3, c4, c2-c1, c3-c1, c4-c1)

        exit(0)
        # find pattern
        for i in range(1, 10000):
            self.resolve_block()
            output = self.print_grid(True, False, False)
            output.pop(-1)
            uniq = set(output)
            counts = {}
            for item in uniq:
                counts[item] = output.count(item)
            counter = Counter(counts.values())
            # for x in range(20):
            #     del counter[x]
            print(i + 1, counter.most_common(5))
            # print(output, len(output))
            # if len(output) % 2 == 0:
            #     half = int(len(output) / 2)
            #     first = output[:half]
            #     first.pop(-1)
            # second = output[half:]
            # second.pop(-1)
            # print(first, second)
            # assert first != second
            # if check:
            #     print(f"repeat found!!! {i}")
            #     break
        return False


if __name__ == '__main__':
    d = Day17()
    print(f"ans1: {d.solve1()}")
    print(f"ans2: {d.solve2()}")
