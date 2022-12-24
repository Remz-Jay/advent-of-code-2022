import unittest
from src.day24 import Day24


class TestDay24(unittest.TestCase):
    obj = None

    @classmethod
    def setUpClass(cls):
        cls.obj = Day24()

    def test_solve1(self):
        ans = self.obj.solve1()
        self.assertEqual(18, ans)

    def test_solve2(self):
        ans = self.obj.solve2()
        self.assertEqual(54, ans)
