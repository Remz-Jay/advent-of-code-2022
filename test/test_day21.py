import unittest
from src.day21 import Day21


class TestDay21(unittest.TestCase):
    obj = None

    @classmethod
    def setUpClass(cls):
        cls.obj = Day21()

    def test_solve1(self):
        ans = self.obj.solve1()
        self.assertEqual(152, ans)

    def test_solve2(self):
        ans = self.obj.solve2(0, 1)
        self.assertEqual(301, ans)
