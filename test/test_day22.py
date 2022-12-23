import unittest
from src.day22 import Day22, Dir


class TestDay22(unittest.TestCase):
    obj = None

    @classmethod
    def setUpClass(cls):
        cls.obj = Day22()

    def test_rotate_left(self):
        self.obj.dir = Dir.RIGHT
        self.obj.rotate_left()
        self.assertEqual(Dir.UP, self.obj.dir)

    def test_rotate_right(self):
        self.obj.dir = Dir.UP
        self.obj.rotate_right()
        self.assertEqual(Dir.RIGHT, self.obj.dir)

    def test_warp_left(self):
        self.obj.dir = Dir.RIGHT
        val = self.obj.warp((12, 4))
        self.assertEqual((0, 4), val)

    def test_warp_right(self):
        self.obj.dir = Dir.LEFT
        val = self.obj.warp((-1, 4))
        self.assertEqual((11, 4), val)

    def test_warp_up(self):
        self.obj.dir = Dir.DOWN
        val = self.obj.warp((0, 8))
        self.assertEqual((0, 4), val)

    def test_warp_down(self):
        self.obj.dir = Dir.UP
        val = self.obj.warp((0, 3))
        self.assertEqual((0, 7), val)

    def test_collision(self):
        self.assertEqual(False, self.obj.check_collision((10, 0)))
        self.assertEqual(True, self.obj.check_collision((11, 0)))

    def test_solve1(self):
        ans = self.obj.solve1()
        self.assertEqual(6032, ans)

    @unittest.skip("Not implemented yet..")
    def test_solve2(self):
        ans = self.obj.solve2()
        self.assertEqual(True, ans)
