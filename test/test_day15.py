import unittest
from src.day15 import Day15


class TestDay15(unittest.TestCase):
    obj = None

    @classmethod
    def setUpClass(cls):
        cls.obj = Day15()

    def test_solve1(self):
        ans = self.obj.solve1(9)
        self.assertEqual(25, ans)
        ans = self.obj.solve1(10)
        self.assertEqual(26, ans)
        ans = self.obj.solve1(11)
        self.assertEqual(27, ans)

    def test_solve2(self):
        ans = self.obj.solve2(20)
        self.assertEqual(56000011, ans)
