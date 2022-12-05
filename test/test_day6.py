import unittest
from src.day6 import Day6


class TestDay6(unittest.TestCase):
    obj = None

    @classmethod
    def setUpClass(cls):
        cls.obj = Day6()

    def test_solve1(self):
        ans = self.obj.solve1()
        self.assertEqual(True, ans)

    def test_solve2(self):
        ans = self.obj.solve2()
        self.assertEqual(True, ans)
