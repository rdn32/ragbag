#!/usr/bin/python

import unittest
import spelling_suggestions

class CommonSubsequenceLengthTest(unittest.TestCase):
    def testEmptyStrings(self):
        self.assertEquals(0, spelling_suggestions.commonSubsequenceLength("", ""))
if __name__ == "__main__":
    unittest.main()
