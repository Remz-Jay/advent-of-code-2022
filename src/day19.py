import math
import re
from dataclasses import dataclass
from src.definitions import INPUT_DIR
import logging

@dataclass
class Blueprint:
    id: int
    ore_cost: int
    clay_cost: int
    obsidian_cost: tuple[int, int]
    geode_cost: tuple[int, int]

    @property
    def obsidian_ore_cost(self) -> int:
        return self.obsidian_cost[0]

    @property
    def obsidian_clay_cost(self) -> int:
        return self.obsidian_cost[1]

    @property
    def geode_ore_cost(self) -> int:
        return self.geode_cost[0]

    @property
    def geode_obsidian_cost(self) -> int:
        return self.geode_cost[1]

    @property
    def highest_ore_cost(self) -> int:
        return max(self.ore_cost, self.clay_cost, self.obsidian_ore_cost, self.geode_ore_cost)

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3

robots = [
    ORE,
    CLAY,
    OBSIDIAN,
    GEODE
]


class Day19:
    file = None
    def __init__(self):
        self.blueprints: list[Blueprint] = []
        self.max_geodes: int = 0
        self.file = open(f"{INPUT_DIR}/day19.txt", "r")
        for line in self.file:
            blueprint, ore, clay, obsidian_ore, obsidian_clay, geode_ore, geode_obsidian = [int(x) for x in re.findall("\d+", line.strip())]
            self.blueprints.append(Blueprint(blueprint, ore, clay, (obsidian_ore, obsidian_clay), (geode_ore, geode_obsidian)))

    def __del__(self):
        self.file.close()

    def run_blueprint(self,
                      blueprint:        Blueprint,
                      time_left:        int,
                      optimize_for:     int,
                      ore:              int = 0,
                      clay:             int = 0,
                      obsidian:         int = 0,
                      geodes:           int = 0,
                      ore_bots:         int = 1,
                      clay_bots:        int = 0,
                      obsidian_bots:    int = 0,
                      geode_bots:       int = 0,
    ) -> None:

        # Bail if we can't make prerequisites yet
        if optimize_for == OBSIDIAN and not clay_bots: return
        if optimize_for == GEODE and not obsidian_bots: return

        # Bail if another bot would overproduce
        if optimize_for == ORE and ore_bots >= blueprint.highest_ore_cost: return
        if optimize_for == CLAY and clay_bots >= blueprint.obsidian_clay_cost: return
        if optimize_for == OBSIDIAN and obsidian_bots >= blueprint.geode_obsidian_cost: return

        for current_time in range(time_left, 0, -1):
            next_time = current_time - 1
            if optimize_for == ORE and ore >= blueprint.ore_cost:
                for optimize_for in robots:
                    self.run_blueprint(blueprint,
                                       next_time,
                                       optimize_for,
                                       ore          + ore_bots      - blueprint.ore_cost,
                                       clay         + clay_bots,
                                       obsidian     + obsidian_bots,
                                       geodes       + geode_bots,
                                       ore_bots + 1,
                                       clay_bots,
                                       obsidian_bots,
                                       geode_bots)
                return
            if optimize_for == CLAY and ore >= blueprint.clay_cost:
                for optimize_for in robots:
                    self.run_blueprint(blueprint,
                                       next_time,
                                       optimize_for,
                                       ore          + ore_bots      - blueprint.clay_cost,
                                       clay         + clay_bots,
                                       obsidian     + obsidian_bots,
                                       geodes       + geode_bots,
                                       ore_bots,
                                       clay_bots + 1,
                                       obsidian_bots,
                                       geode_bots)
                return
            if optimize_for == OBSIDIAN and ore >= blueprint.obsidian_ore_cost and clay >= blueprint.obsidian_clay_cost:
                for optimize_for in robots:
                    self.run_blueprint(blueprint,
                                       next_time,
                                       optimize_for,
                                       ore          + ore_bots      - blueprint.obsidian_ore_cost,
                                       clay         + clay_bots     - blueprint.obsidian_clay_cost,
                                       obsidian     + obsidian_bots,
                                       geodes       + geode_bots,
                                       ore_bots,
                                       clay_bots,
                                       obsidian_bots + 1,
                                       geode_bots)
                return
            if optimize_for == GEODE and ore >= blueprint.geode_ore_cost and obsidian >= blueprint.geode_obsidian_cost:
                for optimize_for in robots:
                    self.run_blueprint(blueprint,
                                       next_time,
                                       optimize_for,
                                       ore          + ore_bots      - blueprint.geode_ore_cost,
                                       clay         + clay_bots,
                                       obsidian     + obsidian_bots - blueprint.geode_obsidian_cost,
                                       geodes       + geode_bots,
                                       ore_bots,
                                       clay_bots,
                                       obsidian_bots,
                                       geode_bots + 1)
                return
            # clean up (bots are 1/tick, so new = old + bots for this tick)
            ore         += ore_bots
            clay        += clay_bots
            obsidian    += obsidian_bots
            geodes      += geode_bots
        if geodes > self.max_geodes:
            self.max_geodes = geodes

    def solve1(self) -> int:
        logging.info("Executing Solve1")
        result = 0
        for bp in self.blueprints:
            self.max_geodes = 0
            for optimize_for in robots:
                self.run_blueprint(bp, 24, optimize_for)
            logging.info(self.max_geodes, bp)
            result += self.max_geodes * bp.id
        return result

    def solve2(self, bp_range:int = 3) -> int:
        logging.info("Executing Solve2")
        result = []
        for bp in self.blueprints[:bp_range:]:
            self.max_geodes = 0
            for optimize_for in robots:
                self.run_blueprint(bp, 32, optimize_for)
            logging.info(self.max_geodes, bp)
            result.append(self.max_geodes)
        return math.prod(result)


if __name__ == '__main__':
    day = Day19()
    print(f"ans1: {day.solve1()}")
    print(f"ans2: {day.solve2()}")