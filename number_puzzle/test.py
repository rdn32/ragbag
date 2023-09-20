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
        self.assertEqual("", number.repr(0))
        self.assertEqual("eight", number.repr(8))
        self.assertEqual("threetennine", number.repr(39))
        self.assertEqual("fourhundredonetenone", number.repr(411))
        self.assertEqual("fivethousandtwohundredseven", number.repr(5207))

    def _testLengthsImpl(self, first, power):
        num = 10 ** power
        combined = 0
        for n in range(first, first + num):
            combined = combined + len(number.repr(n))
        prefix = len(number.repr(first))
        self.assertEqual((combined, num), number.lengthUnder(power, prefix))

    def testLengths(self):
        self._testLengthsImpl(35, 0)
        self._testLengthsImpl(0, 1)
        self._testLengthsImpl(0, 3)
        self._testLengthsImpl(400, 2)
        self._testLengthsImpl(20, 1)

    def _testListImpl(self, power):
        num = 10 ** power
        expected = [number.repr(n) for n in range(num)]
        expected.sort()
        listener = number.ListMaker(num)
        number.traverse("", power, listener)
        self.assertEqual(expected, listener.seen)

    def testLists(self):
        self._testListImpl(1)
        self._testListImpl(2)
        self._testListImpl(3)
        self._testListImpl(4)

    def _testFindImpl(self, power, i):
        num = 10 ** power
        all = [number.repr(n) for n in range(num)]
        all.sort()
        expectedChar = ("".join(all))[i]
        count = 0
        for item in all:
            if i - count >= len(item):
                count = count + len(item)
            else:
                expectedWord = item
                self.assertEqual(expectedChar, item[i - count])
                break
        listener = number.IthCharFinder(i)
        number.traverse("", power, listener)
        self.assertEqual(expectedChar, listener.foundChar)
        self.assertEqual(expectedWord, listener.foundWord)

    def testFind(self):
        self._testFindImpl(1, 9)
        self._testFindImpl(2, 345)
        self._testFindImpl(4, 345)

    def testConvenienceFuncs(self):
        expected = [number.repr(n) for n in range(10 ** 4)]
        expected.sort()
        self.assertEqual(expected[:100], number.makeList(100))
        char, word, index = number.findIth(999)
        self.assertEqual("".join(expected)[999], char)


class BaseThousandTestCase(unittest.TestCase):
    def setUp(self):
        number.initBase1000()

    def testRepr(self):
        self.assertEqual("", number.repr(0))
        self.assertEqual("eight", number.repr(8))
        self.assertEqual("thirtynine", number.repr(39))
        self.assertEqual("fourhundredeleven", number.repr(411))
        self.assertEqual("fivethousandtwohundredseven", number.repr(5207))
        self.assertEqual("twohundredfifteenmillionone", number.repr(215000001))
        self.assertEqual("thirteenbilliontwentysix", number.repr(13000000026))

    def _testListImpl(self, power):
        num = 1000 ** power
        limit = min(num, 1000)
        listener = number.ListMaker(limit)
        number.traverse("", power, listener)
        if limit == num:
            expected = [number.repr(n) for n in range(num)]
            expected.sort()
            self.assertEqual(expected, listener.seen)
        else:
            # Just check the number we have are in sequence
            self.assertEqual(limit, len(listener.seen))
            for i in range(1, limit):
                self.assertTrue(listener.seen[i-1] < listener.seen[i])

    def testLists(self):
        self._testListImpl(1)
        self._testListImpl(2)
        self._testListImpl(3)
        self._testListImpl(4)

    def testConvenienceFuncs(self):
        char, word, index = number.findIth(999999)
        numbers = number.makeList(index + 1)
        combined = "".join(numbers)
        self.assertEqual(combined[999999], char)

if __name__ == '__main__':
    unittest.main()
