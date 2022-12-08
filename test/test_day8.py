import unittest
from src.day8 import Day8


class TestDay8(unittest.TestCase):
    obj = None

    @classmethod
    def setUpClass(cls):
        cls.obj = Day8()

    def test_solve1(self):
        ans = self.obj.solve1()
        self.assertEqual(21, ans)

    def test_solve2(self):
        ans = self.obj.solve2()
        self.assertEqual(8, ans)
