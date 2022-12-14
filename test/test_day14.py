import unittest
from src.day14 import Day14


class TestDay14(unittest.TestCase):
    obj = None

    @classmethod
    def setUpClass(cls):
        cls.obj = Day14()

    def test_grid(self):
        self.obj.__init__()
        self.assertEquals(494, self.obj.min_x)
        self.assertEquals(503, self.obj.max_x)
        output = self.obj.print_grid(self.obj.min_x, self.obj.max_x, 0, self.obj.max_y, self.obj.insert, True, True)
        expected = """  4     5  5
  9     0  0
  4     0  3
0 ......+...
1 ..........
2 ..........
3 ..........
4 ....#...##
5 ....#...#.
6 ..###...#.
7 ........#.
8 ........#.
9 #########.
"""
        self.assertEqual(expected, output)

    def test_floor_grid(self):
        self.obj.__init__()
        expected = """............o............
...........ooo...........
..........ooooo..........
.........ooooooo.........
........oo#ooo##o........
.......ooo#ooo#ooo.......
......oo###ooo#oooo......
.....oooo.oooo#ooooo.....
....oooooooooo#oooooo....
...ooo#########ooooooo...
..ooooo.......ooooooooo..
#########################
"""
        self.obj.insert_floor()
        self.obj.run_simulation()
        output = self.obj.print_grid(self.obj.min_x, self.obj.max_x, 0, self.obj.max_y, self.obj.insert, True, False)
        self.assertEqual(expected, output)

    def test_solve1(self):
        self.obj.__init__()
        ans = self.obj.solve1()
        self.assertEqual(24, ans)

    def test_solve2(self):
        self.obj.__init__()
        ans = self.obj.solve2()
        self.assertEqual(93, ans)
