import unittest
from src.day9 import Day9
from src.definitions import INPUT_DIR


class TestDay9(unittest.TestCase):
    obj = None

    @classmethod
    def setUpClass(cls):
        cls.obj = Day9()

    def test_solve1(self):
        ans = self.obj.solve1()
        self.assertEqual(13, ans)

    def test_solve2(self):
        ans = self.obj.solve2()
        self.assertEqual(1, ans)

    def test_solve2b(self):
        self.obj = Day9()
        self.obj.file = open(f"{INPUT_DIR}/day9b.txt", "r")
        self.obj.walk()
        ans = self.obj.solve2()
        self.assertEqual(36, ans)
