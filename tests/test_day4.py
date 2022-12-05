import unittest
from day4 import Day4


class TestDay4(unittest.TestCase):
    obj = None

    @classmethod
    def setUpClass(cls):
        cls.obj = Day4()

    def test_solve1(self):
        ans = self.obj.solve1()
        self.assertEqual(2, ans)

    def test_solve2(self):
        ans = self.obj.solve2()
        self.assertEqual(4, ans)
