import unittest
from src.day10 import Day10


class TestDay10(unittest.TestCase):
    obj = None

    @classmethod
    def setUpClass(cls):
        cls.obj = Day10()

    def test_solve1(self):
        ans = self.obj.solve1()
        self.assertEqual(13140, ans)

    def test_solve2(self):
        ans = self.obj.solve2()
        self.assertEqual("""##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....

""", ans)
