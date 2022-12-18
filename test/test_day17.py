import unittest
from src.day17 import Day17


class TestDay17(unittest.TestCase):
    obj = None

    @classmethod
    def setUpClass(cls):
        cls.obj = Day17()

    def test_step1(self):
        self.obj.__init__()
        self.obj.run(10)
        output = "\n".join(self.obj.print_grid(True, False, False))
        expected = """|....#..|
|....#..|
|....##.|
|##..##.|
|######.|
|.###...|
|..#....|
|.####..|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+"""
        self.assertEqual(expected, output)

    def test_solve1(self):
        self.obj.__init__()
        ans = self.obj.solve1(2022, False)
        self.assertEqual(3068, ans)

    def test_solve2(self):
        self.obj.__init__()
        ans = self.obj.solve2()
        self.assertEqual(1514285714288, ans)

