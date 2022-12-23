import unittest
from src.day23 import Day23


class TestDay23(unittest.TestCase):
    obj = None

    @classmethod
    def setUpClass(cls):
        cls.obj = Day23()

    def test_solve1(self):
        ans = self.obj.solve1()
        self.obj.print_grid()
        self.assertEqual(110, ans)

    def test_solve2(self):
        ans = self.obj.solve2()
        self.assertEqual(20, ans)
