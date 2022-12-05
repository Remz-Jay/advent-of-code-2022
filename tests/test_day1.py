import unittest
from day1 import Day1


class TestDay1(unittest.TestCase):
    obj = None

    @classmethod
    def setUpClass(cls):
        cls.obj = Day1()

    def test_solve1(self):
        ans = self.obj.solve1()
        self.assertEqual(24000, ans)

    def test_solve2(self):
        ans = self.obj.solve2()
        self.assertEqual(45000, ans)

