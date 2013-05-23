#!/usr/bin/python

import unittest
import spelling_suggestions

class CommonSubsequenceLengthTest(unittest.TestCase):
    def testEmptyStrings(self):
        self.runTestCase(0, "", "")

    def testEqualStrings(self):
        self.runTestCase(3, "abc", "abc")

    def runTestCase(self, expectedLength, s1, s2):
        actualLength = spelling_suggestions.commonSubsequenceLength(s1, s2)
        self.assertEquals(expectedLength, actualLength)

if __name__ == "__main__":
    unittest.main()
