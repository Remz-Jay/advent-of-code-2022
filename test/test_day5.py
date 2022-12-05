import unittest
from src.day5 import Day5


class TestDay5(unittest.TestCase):
    obj = None

    @classmethod
    def setUpClass(cls):
        cls.obj = Day5()

    def test_solve1(self):
        ans = self.obj.solve1()
        self.assertEqual("CMZ", ans)

    def test_solve2(self):
        ans = self.obj.solve2()
        self.assertEqual("MCD", ans)
