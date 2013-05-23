#!/usr/bin/python

# Solution to "Spelling Suggestions" puzzle

# Finds the length of the longest common subsequence
# of two strings.
def commonSubsequenceLength(s1, s2):
    # Populate lcs so that lcs[l1,l2] is the length
    # of the longest common subsequence of
    # last l1 characters of s1 and last l2 characters
    # of s2.
    lcs = {}
    for l1 in range(0, 1 + len(s1)):
        for l2 in range(0, 1 + len(s2)):
            if l1 == 0 or l2 == 0:
                result = 0
            elif s1[l1-1] == s2[l2-1]:
                result = 1 + lcs[l1-1, l2-1]
            else:
                result = max(lcs[l1-1, l2],
                             lcs[l1, l2-1])
            lcs[l1,l2] = result
    return lcs[len(s1), len(s2)]

# Given a (possibly) misspelt word, and two
# suggestions as to what it might be, picks
# the more likely.
def pickSuggestion(word, alt1, alt2):
    lcsLength1 = commonSubsequenceLength(word, alt1)
    lcsLength2 = commonSubsequenceLength(word, alt2)
    if lcsLength1 >= lcsLength2:
        return alt1
    else:
        return alt2

# Parses the input, which has the format
# described in README.md, passing each
# set of words and two suggestions to the
# given callback.
def parseInput(input, callback):
    line = input.readline()
    n = int(line.strip())
    for _ in range(n):
        blank = input.readline()
        word = input.readline().strip()
        alt1 = input.readline().strip()
        alt2 = input.readline().strip()
        callback(word, alt1, alt2)

if __name__ == "__main__":
    import sys
    def processCase(word, alt1, alt2):
        print pickSuggestion(word, alt1, alt2)
    parseInput(sys.stdin, processCase)
