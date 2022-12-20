import unittest
from src.day20 import Day20


class TestDay20(unittest.TestCase):
    obj = None

    @classmethod
    def setUpClass(cls):
        cls.obj = Day20()

    def test_initial(self):
        self.obj.__init__()
        compare = self.obj.translate(self.obj.input)
        self.assertEqual([1, 2, -3, 3, -2, 0, 4], compare)

    def test_decrypted(self):
        self.obj.__init__()
        compare = self.obj.translate(self.obj.decrypted)
        self.assertEqual([811589153, 1623178306, -2434767459, 2434767459, -1623178306, 0, 3246356612], compare)

    def test_round1(self):
        self.obj.__init__()
        self.obj.run_the_numbers(self.obj.input, 1)
        compare = self.obj.translate(self.obj.input)
        self.assertEqual([2, 1, -3, 3, -2, 0, 4], compare)

    def test_round2(self):
        self.obj.__init__()
        self.obj.run_the_numbers(self.obj.input, 2)
        compare = self.obj.translate(self.obj.input)
        self.assertEqual([1, -3, 2, 3, -2, 0, 4], compare)

    def test_round3(self):
        self.obj.__init__()
        self.obj.run_the_numbers(self.obj.input, 3)
        compare = self.obj.translate(self.obj.input)
        self.assertEqual([1, 2, 3, -2, -3, 0, 4], compare)

    def test_round4(self):
        self.obj.__init__()
        self.obj.run_the_numbers(self.obj.input, 4)
        compare = self.obj.translate(self.obj.input)
        self.assertEqual([1, 2, -2, -3, 0, 3, 4], compare)

    def test_round5(self):
        self.obj.__init__()
        self.obj.run_the_numbers(self.obj.input, 5)
        compare = self.obj.translate(self.obj.input)
        self.assertEqual([1, 2, -3, 0, 3, 4, -2], compare)

    def test_round6(self):
        self.obj.__init__()
        self.obj.run_the_numbers(self.obj.input, 6)
        compare = self.obj.translate(self.obj.input)
        self.assertEqual([1, 2, -3, 0, 3, 4, -2], compare)

    def test_round7(self):
        self.obj.__init__()
        self.obj.run_the_numbers(self.obj.input)  # should work without specifying rounds
        compare = self.obj.translate(self.obj.input)
        self.assertEqual([1, 2, -3, 4, 0, 3, -2], compare)

    def test_multimix_round1(self):
        self.obj.__init__()
        for _ in range(1):
            self.obj.run_the_numbers(self.obj.decrypted)
        compare = self.obj.translate(self.obj.decrypted)
        self.assertEqual([0, -2434767459, 3246356612, -1623178306, 2434767459, 1623178306, 811589153], compare)

    def test_multimix_round5(self):
        self.obj.__init__()
        for _ in range(5):
            self.obj.run_the_numbers(self.obj.decrypted)
        compare = self.obj.translate(self.obj.decrypted)
        self.assertEqual([0, 811589153, -1623178306, 1623178306, -2434767459, 3246356612, 2434767459], compare)

    def test_multimix_round9(self):
        self.obj.__init__()
        for _ in range(9):
            self.obj.run_the_numbers(self.obj.decrypted)
        compare = self.obj.translate(self.obj.decrypted)
        self.assertEqual([0, 811589153, 1623178306, -2434767459, 3246356612, 2434767459, -1623178306], compare)

    def test_solve1(self):
        self.obj.__init__()
        ans = self.obj.solve1()
        self.assertEqual(3, ans)

    def test_solve2(self):
        self.obj.__init__()
        ans = self.obj.solve2()
        self.assertEqual(1623178306, ans)
