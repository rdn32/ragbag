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
