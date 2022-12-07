import unittest
from src.day7 import Day7


class TestDay7(unittest.TestCase):
    obj = None

    @classmethod
    def setUpClass(cls):
        cls.obj = Day7()

    def test_solve1(self):
        ans = self.obj.solve1()
        self.assertEqual(95437, ans)

    def test_solve2(self):
        ans = self.obj.solve2()
        self.assertEqual(24933642, ans)
