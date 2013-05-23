#!/usr/bin/python

# Solution to "Spelling Suggestions" puzzle
def commonSubsequenceLength(s1, s2):
    memos = {}
    def lcs(s1, s2):
        if (s1,s2) not in memos:
            if s1 == "" or s2 == "":
                result = 0
            elif s1[0] == s2[0]:
                result = 1 + lcs(s1[1:], s2[1:])
            else:
                result = max(lcs(s1[1:], s2),
                             lcs(s1, s2[1:]))
            memos[s1,s2] = result
        return memos[s1,s2]
    return lcs(s1, s2)
