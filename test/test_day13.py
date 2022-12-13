import unittest
from src.day13 import Day13


class TestDay13(unittest.TestCase):
    obj = None

    @classmethod
    def setUpClass(cls):
        cls.obj = Day13()

    def test_solve1(self):
        ans = self.obj.solve1()
        self.assertEqual(13, ans)

    def test_solve2(self):
        self.obj.inputs.append([[2]])
        self.obj.inputs.append([[6]])
        ans = self.obj.solve2()
        self.assertEqual(140, ans)
