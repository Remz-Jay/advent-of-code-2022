import unittest
from src.{{id}} import {{id|capitalize}}


class Test{{id|capitalize}}(unittest.TestCase):
    obj = None

    @classmethod
    def setUpClass(cls):
        cls.obj = {{id|capitalize}}()

    def test_solve1(self):
        ans = self.obj.solve1()
        self.assertEqual(True, ans)

    def test_solve2(self):
        ans = self.obj.solve2()
        self.assertEqual(True, ans)

