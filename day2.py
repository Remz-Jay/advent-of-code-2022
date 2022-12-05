import logging
import sys
from enum import IntEnum


class Action(IntEnum):
    Rock = 1
    Paper = 2
    Scissors = 3


class Day2:
    file = None
    amap = {
        'X': 1,
        'Y': 2,
        'Z': 3,
        'A': 1,
        'B': 2,
        'C': 3,
    }

    victories = {
        Action.Rock: [Action.Scissors],  # Rock beats scissors
        Action.Paper: [Action.Rock],  # Paper beats rock
        Action.Scissors: [Action.Paper]  # Scissors beats paper
    }

    losses = {
        Action.Rock: [Action.Paper],  # Rock beats scissors
        Action.Paper: [Action.Scissors],  # Paper beats rock
        Action.Scissors: [Action.Rock]  # Scissors beats paper
    }

    def __init__(self):
        self.file = open("input/day2.txt", "r")

    def __del__(self):
        self.file.close()

    def solve1(self):
        score: int = 0
        for line in self.file:
            tokens = line.split()
            action_elf = Action(self.amap[tokens[0]])
            action_me = Action(self.amap[tokens[1]])
            logging.info(f"elf: {action_elf}")
            logging.info(f"me: {action_me}")
            score += action_me

            defeats = self.victories[action_me]
            if action_me == action_elf:
                logging.info(f"Both players selected {action_me.name}. It's a tie!")
                score += 3
            elif action_elf in defeats:
                logging.info(f"{action_me.name} beats {action_elf.name}! You win!")
                score += 6
            else:
                logging.info(f"{action_elf.name} beats {action_me.name}! You lose.")
        return score

    def solve2(self):
        score: int = 0
        self.file.seek(0)
        for line in self.file:
            tokens = line.split()
            action_elf = Action(self.amap[tokens[0]])
            if tokens[1] == 'X':
                logging.info('you need to lose')
                score += self.victories[action_elf][0]
            elif tokens[1] == 'Y':
                logging.info('you need to draw')
                score += 3 + action_elf
            else:
                logging.info('you need to win')
                score += 6 + self.losses[action_elf][0]
        return score


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.ERROR, format='%(levelname)-8s %(message)s')
    d = Day2()
    print(f"ans1: {d.solve1()}")
    print(f"ans2: {d.solve2()}")
