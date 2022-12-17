from src.definitions import INPUT_DIR
import logging
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

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
        logging.info("Executing Solve2")
        self.file.seek(0)
        return False


if __name__ == '__main__':
    d = Day17()
    print(f"ans1: {d.solve1()}")
    print(f"ans2: {d.solve2()}")
