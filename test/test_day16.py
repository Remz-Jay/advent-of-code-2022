import unittest
from src.day16 import Day16


class TestDay16(unittest.TestCase):
    obj = None

    @classmethod
    def setUpClass(cls):
        cls.obj = Day16()

    def test_solve1(self):
        ans = self.obj.solve1()
        self.assertEqual(1651, ans)

    @unittest.skip("Haven't implemented this yet..")
    def test_solve2(self):
        ans = self.obj.solve2()
        self.assertEqual(1707, ans)
