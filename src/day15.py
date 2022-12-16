from src.definitions import INPUT_DIR
import logging

EMPTY = '.'
SENSOR = 'S'
BEACON = 'B'
HASH = '#'


class Sensor:
    position: tuple
    closest_beacon: tuple
    range: int

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]


class Day15:
    file = None
    grid = {}

    def __init__(self):
        self.file = open(f"{INPUT_DIR}/day15.txt", "r")
        self.sensors: list[Sensor] = []
        self.beacons: list[tuple] = []
        self.parse_input()

    def __del__(self):
        self.file.close()

    def get_sensor_at_position(self, pos: tuple):
        for s in self.sensors:
            if s.position == pos:
                return s
        return False

    def parse_input(self):
        for line in self.file:
            bits = line.strip().split(':')
            sensor_bits = bits[0].split('=')
            beacon_bits = bits[1].split('=')
            s = Sensor()
            s.position = (int(sensor_bits[1].split(',')[0]), int(sensor_bits[2]))
            s.closest_beacon = (int(beacon_bits[1].split(',')[0]), int(beacon_bits[2]))
            s.range = self.manhattan_distance(s.position, s.closest_beacon)
            self.sensors.append(s)
            self.beacons.append(s.closest_beacon)

    def get_max_distance(self):
        md = 0
        for sensor, beacon in self.refdict.items():
            distance = self.manhattan_distance(sensor, beacon)
            print(sensor, beacon, distance, self.manhattan_distance(sensor, beacon))
            if distance > md:
                md = distance
        print(md)

    def make_grid(self):
        self.grid = {i: 0 for i in range(self.grid_min_y, self.grid_max_y)}
        for x in self.grid:
            self.grid[x] = {i: EMPTY for i in range(self.grid_min_x, self.grid_max_x)}

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
            print(buffer)

    def get_result_for_line(self, line):
        content = set()
        for sensor in self.sensors:
            if sensor.y - sensor.range <= line <= sensor.y + sensor.range:
                width_at_sensor = sensor.range * 2 + 1
                distance_from_source = abs(sensor.y - line)
                width_at_line = abs(width_at_sensor - distance_from_source * 2)
                per_side = int((width_at_line - 1) / 2)
                # logging.info(sensor, beacon, sensor_range, width_at_sensor, distance_from_source, width_at_line, per_side, sensor[0] - per_side)
                for x in range(sensor.x - per_side, sensor.x + per_side + 1):
                    if (x, line) not in self.beacons and not self.get_sensor_at_position((x, line)):
                        content.add(x)
        return len(content)

    def find_tuning_frequency(self, max_coord=20, start=0):
        for y in range(start, max_coord + 1):
            ranges = []
            for sensor in self.sensors:
                if sensor.y - sensor.range <= y <= sensor.y + sensor.range:
                    distance_from_source = abs(sensor.y - y)
                    delta = sensor.range - distance_from_source
                    ranges.append((sensor.x - delta, sensor.x + delta))
            x = 0
            while x <= max_coord:
                found = False
                for r in ranges:
                    if r[0] <= x <= r[1]:
                        x = r[1] + 1
                        found = True
                if not found:
                    return x * 4000000 + y

    def solve1(self, line_of_interest=2000000):
        logging.info("Executing Solve1")
        return self.get_result_for_line(line_of_interest)

    def solve2(self, max_search=4000000):
        logging.info("Executing Solve2")
        return self.find_tuning_frequency(max_search, 0)


if __name__ == '__main__':
    d = Day15()
    print(f"ans1: {d.solve1()}")
    print(f"ans2: {d.solve2()}")
