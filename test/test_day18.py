import unittest
from src.day18 import Day18


class TestDay18(unittest.TestCase):
    obj = None

    @classmethod
    def setUpClass(cls):
        cls.obj = Day18()

    def test_solve1(self):
        ans = self.obj.solve1()
        self.assertEqual(64, ans)

    def test_solve2(self):
        ans = self.obj.solve2()
        self.assertEqual(True, ans)
