import gc
from src.definitions import INPUT_DIR
import logging

EMPTY = '.'
SENSOR = 'S'
BEACON = 'B'
HASH = '#'

class Day15:
    file = None
    grid = {}

    def __init__(self):
        self.file = open(f"{INPUT_DIR}/day15.txt", "r")
        self.sensors = []
        self.beacons = []
        self.refdict = {}
        self.grid_min_x = 0
        self.grid_max_x = 0
        self.grid_min_y = 0
        self.grid_max_y = 0
        self.margin = 20
        self.skiplist = []
        self.parse_input()

    def __del__(self):
        self.file.close()

    def parse_input(self):
        for line in self.file:
            bits = line.strip().split(':')
            sensor_bits = bits[0].split('=')
            beacon_bits = bits[1].split('=')
            self.sensors.append((int(sensor_bits[1].split(',')[0]), int(sensor_bits[2])))
            self.beacons.append((int(beacon_bits[1].split(',')[0]), int(beacon_bits[2])))
            self.refdict[self.sensors[-1]] = self.beacons[-1]
        # print(self.sensors, self.beacons)
        self.find_min_max(self.sensors)
        self.find_min_max(self.beacons)
        self.add_safety_margin(self.margin)
        print('x:', self.grid_min_x, self.grid_max_x)
        print('y:', self.grid_min_y, self.grid_max_y)
        # self.get_max_distance()
        # exit(1)
        # self.make_grid()
        # self.plot_markers(self.beacons, BEACON)
        # self.plot_markers(self.sensors, SENSOR)
        # self.plot_range()
        # self.print_grid(self.grid_min_x, self.grid_max_x, self.grid_min_y, self.grid_max_y, False, False)

    def get_max_distance(self):
        md = 0
        for sensor, beacon in self.refdict.items():
            distance = self.manhattan_distance(sensor, beacon)
            print(sensor, beacon, distance, self.manhattan_distance(sensor, beacon))
            if distance > md:
                md = distance
        print(md)

    def make_grid(self):
        # self.grid = {(i, j): 0 for i in range(self.grid_min_y, self.grid_max_y)
        #              for j in range(self.grid_min_x, self.grid_max_x)}
        self.grid = {i: 0 for i in range(self.grid_min_y, self.grid_max_y)}
        for x in self.grid:
            self.grid[x] = {i: EMPTY for i in range(self.grid_min_x, self.grid_max_x)}
            gc.collect()
        # print(self.grid)

    def add_safety_margin(self, amount):
        self.grid_min_x -= amount
        self.grid_min_y -= amount
        self.grid_max_x += amount
        self.grid_max_y += amount

    def find_min_max(self, input):
        for i in input:
            assert isinstance(i, tuple)
            if i[0] < self.grid_min_x:
                self.grid_min_x = i[0]
            if i[0] > self.grid_max_x:
                self.grid_max_x = i[0]
            if i[1] < self.grid_min_y:
                self.grid_min_y = i[1]
            if i[1] > self.grid_max_y:
                self.grid_max_y = i[1]

    def manhattan_distance(self, left, right):
        return abs(left[1] - right[1]) + abs(left[0] - right[0])

    def plot_range(self):
        for sensor, beacon in self.refdict.items():
            distance = self.manhattan_distance(sensor, beacon)
            print(sensor, beacon, distance, self.manhattan_distance(sensor, beacon))
            for i in range(sensor[0] - distance, sensor[0] + distance):
                if self.grid[sensor[1]][i] == EMPTY:
                    self.grid[sensor[1]][i] = HASH
            for i in range(sensor[1] - distance, sensor[1] + distance):
                for key, value in self.grid[i].items():
                    if self.manhattan_distance(sensor, (key, i)) <= distance and self.grid[i][key] == EMPTY:
                        self.grid[i][key] = HASH

    def plot_markers(self, input: list, marker: int):
        for i in input:
            self.grid[i[1]][i[0]] = marker

    def print_grid(self, left=0, right=1000, top=0, bottom=1000, do_return=False, legend=True):
        buffer = ""
        if legend:
            digits_left = [x for x in str(left)]
            digits_right = [x for x in str(right)]
            for iter, i in enumerate(digits_left):
                padding = (right - left)
                buffer += f"  {i}{' ' * padding}{digits_right[iter]}\n"
        for key, value in self.grid.items():
            if top <= int(key) <= bottom:
                if legend:
                    buffer += f"{iter} "
                for fookey, foovalue in value.items():
                    if left <= int(fookey) <= right:
                        buffer += str(foovalue)
                buffer += "\n"
        if do_return:
            return buffer
        else:
            print(buffer

    def remove_sensor(self, sensor):
        self.sensors.remove(sensor)
        self.skiplist.append(sensor)

    def get_result_for_line(self, line, max_width=0, return_set=False):
        content = set()
        for sensor, beacon in self.refdict.items():
            if sensor in self.skiplist:
                continue
            sensor_range = self.manhattan_distance(sensor, beacon)
            if sensor[1] - sensor_range <= line <= sensor[1] + sensor_range:
                if max_width:
                    if sensor[0] + sensor_range < 0:
                        self.remove_sensor(sensor)
                        continue
                    if sensor[0] - sensor_range > max_width:
                        self.remove_sensor(sensor)
                        continue
                # print(sensor, beacon, sensor_range)
                width_at_sensor = sensor_range * 2 + 1
                distance_from_source = abs(sensor[1] - line)
                width_at_line = abs(width_at_sensor - distance_from_source * 2)
                per_side = int((width_at_line - 1) / 2)
                # print(sensor, beacon, sensor_range, width_at_sensor, distance_from_source, width_at_line, per_side, sensor[0] - per_side)
                for x in range(sensor[0] - per_side, sensor[0] + per_side + 1):
                    if max_width != 0:
                        if 0 <= x <= max_width:
                            content.add(x)
                    else:
                        if(x, line) not in self.beacons and (x, line) not in self.sensors:
                            content.add(x)
            # else:
            #     self.remove_sensor(sensor)
        if return_set:
            return content
        else:
            return len(content)

    def find_tuning_frequency(self, max_coord=20):
        for l in range(max_coord+1):
            print(l, self.skiplist)
            if self.get_result_for_line(l, max_coord) != max_coord + 1:
                myset = self.get_result_for_line(l, max_coord, True)
                output = []
                for i in range(0, max_coord + 1):
                    if i not in myset:
                        output.append(i)
                assert len(output) == 1
                return output[0] * 4000000 + l

    def solve1(self, line_of_interest=2000000):
        logging.info("Executing Solve1")
        print(len("#########################"))
        return self.get_result_for_line(line_of_interest)

    def solve2(self, max_search=4000000):
        logging.info("Executing Solve2")

        return self.find_tuning_frequency(max_search)


if __name__ == '__main__':
    d = Day15()
    # print(f"ans1: {d.solve1()}")
    print(f"ans2: {d.solve2()}")
