import unittest
from src.day19 import Day19


class TestDay19(unittest.TestCase):
    obj = None

    @classmethod
    def setUpClass(cls):
        cls.obj = Day19()

    def test_solve1(self):
        ans = self.obj.solve1()
        self.assertEqual(33, ans)

    @unittest.skip("This takes forever; let's not waste GitHub Action minutes")
    def test_solve2(self):
        ans = self.obj.solve2(bp_range=2)
        self.assertEqual(56 * 62, ans)
