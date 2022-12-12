import unittest
from src.day12 import Day12


class TestDay12(unittest.TestCase):
    obj = None

    @classmethod
    def setUpClass(cls):
        cls.obj = Day12()

    def test_solve1(self):
        ans = self.obj.solve1()
        self.assertEqual(31, ans)

    def test_solve2(self):
        ans = self.obj.solve2()
        self.assertEqual(29, ans)
