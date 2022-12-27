import unittest
from src.day25 import Day25


class TestDay25(unittest.TestCase):
    obj = None

    @classmethod
    def setUpClass(cls):
        cls.obj = Day25()

    def test_decimal_to_SNAFU(self):
        inputs = {
            1: "1",
            2: "2",
            3: "1=",
            4: "1-",
            5: "10",
            6: "11",
            7: "12",
            8: "2=",
            9: "2-",
            10: "20",
            15: "1=0",
            20: "1-0",
            2022: "1=11-2",
            12345: "1-0---0",
            314159265: "1121-1110-1=0"
        }
        for k, v in inputs.items():
            ans = self.obj.translate_decimal_to_snafu(k)
            self.assertEqual(ans, v)

    def test_SNAFU_to_decimal(self):
        inputs = {
            "1=-0-2": 1747,
            "12111": 906,
            "2=0=": 198,
            "21": 11,
            "2=01": 201,
            "111": 31,
            "20012": 1257,
            "112": 32,
            "1=-1=": 353,
            "1-12": 107,
            "12": 7,
            "1=": 3,
            "122": 37,
        }
        for k, v in inputs.items():
            ans = self.obj.translate_snafu_to_decimal(k)
            self.assertEqual(ans, v)

    def test_solve1(self):
        ans = self.obj.solve1()
        # decimal = 4890
        self.assertEqual("2=-1=0", ans)

    @unittest.skip("Not implemented yet..")
    def test_solve2(self):
        ans = self.obj.solve2()
        self.assertEqual(True, ans)
