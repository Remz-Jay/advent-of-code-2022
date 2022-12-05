import unittest
from day2 import Day2


class TestDay2(unittest.TestCase):
    obj = None

    @classmethod
    def setUpClass(cls):
        cls.obj = Day2()

    def test_solve1(self):
        ans = self.obj.solve1()
        self.assertEqual(15, ans)

    def test_solve2(self):
        ans = self.obj.solve2()
        self.assertEqual(12, ans)
