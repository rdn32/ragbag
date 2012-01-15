#!/usr/bin/python

import unittest
import number

class BaseTenTestCase(unittest.TestCase):
    def setUp(self):
        number.init(10,
                    ["", "ten", "hundred", "thousand"],
                    ["", "one", "two", "three", "four",
                     "five", "six", "seven", "eight", "nine"])

    def testRepr(self):
        self.assertEquals("", number.repr(0))
        self.assertEquals("eight", number.repr(8))
        self.assertEquals("threetennine", number.repr(39))
        self.assertEquals("fourhundredonetenone", number.repr(411))
        self.assertEquals("fivethousandtwohundredseven", number.repr(5207))

    def _testLengthsImpl(self, first, power):
        num = 10 ** power
        combined = 0
        for n in range(first, first + num):
            combined = combined + len(number.repr(n))
        prefix = len(number.repr(first))
        self.assertEquals((combined, num), number.lengthUnder(power, prefix))

    def testLengths(self):
        self._testLengthsImpl(0, 1)
        self._testLengthsImpl(0, 3)
        self._testLengthsImpl(400, 2)
        self._testLengthsImpl(20, 1)

if __name__ == '__main__':
    unittest.main()
