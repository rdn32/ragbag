#!/usr/bin/python

import unittest
import spelling_suggestions

class CommonSubsequenceLengthTest(unittest.TestCase):
    def testEmptyStrings(self):
        self.runTestCase(0, "", "")

    def testEqualStrings(self):
        self.runTestCase(3, "abc", "abc")

    def testDisjointStrings(self):
        self.runTestCase(0, "abc", "def")

    def testSimilarStrings(self):
        self.runTestCase(3, "abXXXbXXcXXX", "YaYYYYYYbc")

    def runTestCase(self, expectedLength, s1, s2):
        actualLength = spelling_suggestions.commonSubsequenceLength(s1, s2)
        self.assertEquals(expectedLength, actualLength)

class SuggestionPickerTest(unittest.TestCase):
    def testSampleExample1(self):
        word = "remimance"
        alt1 = "remembrance"
        alt2 = "reminiscence"
        self.runTestCase(alt1, word, alt1, alt2)

    def testSampleExample2(self):
        word = "inndietlly"
        alt1 = "immediately"
        alt2 = "incidentally"
        self.runTestCase(alt2, word, alt1, alt2)

    def runTestCase(self, expectedAlt, word, alt1, alt2):
        actualAlt = spelling_suggestions.pickSuggestion(word, alt1, alt2)
        self.assertEquals(expectedAlt, actualAlt)

if __name__ == "__main__":
    unittest.main()
