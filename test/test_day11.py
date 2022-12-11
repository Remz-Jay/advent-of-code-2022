import unittest
from src.day11 import Day11


class TestDay11(unittest.TestCase):
    obj = None

    @classmethod
    def setUpClass(cls):
        cls.obj = Day11()

    def test_solve1(self):
        ans = self.obj.solve1()
        self.assertEqual(10605, ans)

    def test_solve2(self):
        ans = self.obj.solve2()
        self.assertEqual(2713310158, ans)
