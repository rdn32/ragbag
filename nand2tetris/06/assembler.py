#!/usr/bin/python

from contextlib import nested
import re

ASM_SUFFIX = ".asm"
HACK_SUFFIX = ".hack"

class error(Exception): pass

class Matcher:
    def __init__(self, s):
        self.s = s
        self.m = None

    def match(self, pattern):
        self.m = re.match(pattern, self.s)
        return self.m

    def group(self, n):
        return self.m.group(n)

def binary(n, num_digits):
    result = ""
    for _ in range(num_digits):
        result = str(n & 1) + result
        n = n >> 1
    return result

compCode = {
        "0"   : "0101010",
        "1"   : "0111111",
        "-1"  : "0111010",
        "D"   : "0001100",
        "A"   : "0110000",
        "!D"  : "0001101",
        "!A"  : "0110001",
        "D+1" : "0011111",
        "A+1" : "0110111",
        "D-1" : "0001110",
        "A-1" : "0110010",
        "D+A" : "0000010",
        "D-A" : "0000111",
        "D&A" : "0000000",
        "D|A" : "0010101",
        "M"   : "1110000"
        # TBC
}

destCode = {
        None  : "000",
        "M"   : "001",
        "D"   : "010",
        "MD"  : "011",
        "A"   : "100",
        "AM"  : "101",
        "AD"  : "110",
        "AMD" : "111"
}


def assemble(src_filename):
    if not src_filename.endswith(ASM_SUFFIX):
        raise error, "Illegal file name '%s'" % src_filename
    tgt_filename = src_filename[:-len(ASM_SUFFIX)] + HACK_SUFFIX

    with nested(open(src_filename, "r"), open(tgt_filename, "w")) as (src, tgt):
        for line in src:
            line = re.sub(r"//.*", "", line).strip()
            m = Matcher(line)

            instr = None
            if m.match(r"^$"):
                pass
            elif m.match(r"^@(\d+)$"):
                val = int(m.group(1))
                instr = "0" + binary(val, 15)
            elif m.match(r"([^=]+)=([^=]+)"):
                dest = m.group(1)
                comp = m.group(2)
                instr = "111" + compCode[comp] + destCode[dest] + "000"

            if instr:
                tgt.write(instr)
                tgt.write("\n")

if __name__ == "__main__":
    import sys
    for arg in sys.argv[1:]:
        assemble(arg)

