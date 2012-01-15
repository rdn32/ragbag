#!/usr/bin/python

import unittest
import number

class BaseTenTestCase(unittest.TestCase):
    def setUp(self):
        number.init(10,
                    ["", "ten", "hundred", "thousand"],
                    ["zero", "one", "two", "three", "four",
                     "five", "six", "seven", "eight", "nine"])

    def testRepr(self):
        self.assertEquals("eight", number.repr(8))
        self.assertEquals("threetennine", number.repr(39))
        self.assertEquals("fourhundredonetenone", number.repr(411))
        self.assertEquals("fivethousandtwohundredseven", number.repr(5207))

if __name__ == '__main__':
    unittest.main()
