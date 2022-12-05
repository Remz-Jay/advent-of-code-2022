import unittest
from day3 import Day3


class TestDay3(unittest.TestCase):
    obj = None

    @classmethod
    def setUpClass(cls):
        cls.obj = Day3()

    def test_solve1(self):
        ans = self.obj.solve1()
        self.assertEqual(157, ans)

    def test_solve2(self):
        ans = self.obj.solve2()
        self.assertEqual(70, ans)
