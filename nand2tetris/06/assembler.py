#!/usr/bin/python

from contextlib import nested
import re

ASM_SUFFIX = ".asm"
HACK_SUFFIX = ".hack"

class error(Exception): pass

class Matcher(object):
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
        "M"   : "1110000",
        "!M"  : "1110001",
        "-M"  : "1110011",
        "M+1" : "1110111",
        "M-1" : "1110010",
        "D+M" : "1000010",
        "D-M" : "1010011",
        "M-D" : "1000111",
        "D&M" : "1000000",
        "D|M" : "1010101"
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

jmpCode = {
        None  : "000",
        "JGT" : "001",
        "JEQ" : "010",
        "JGE" : "011",
        "JLT" : "100",
        "JNE" : "101",
        "JLE" : "110",
        "JMP" : "111"
}

class AInstr(object):
    def __init__(self, value, symbol):
        self.value = value
        self.symbol = symbol
        self.type = "A"

class CInstr(object):
    def __init__(self, dest, comp, jmp):
        self.dest = dest
        self.comp = comp
        self.jmp = jmp
        self.type = "C"

class LInstr(object):
    def __init__(self, symbol):
        self.symbol = symbol
        self.type = "L"

def doPass(src):
    for line in src:
        line = re.sub(r"//.*", "", line).strip()
        m = Matcher(line)

        if m.match(r"^$"):
            pass
        elif m.match(r"^@(\d+)$"):
            value = int(m.group(1))
            yield AInstr(int(m.group(1)), None)
        elif m.match(r"^@([^()]+)"):
            yield AInstr(None, m.group(1))
        elif m.match(r"^([^=;]+)=([^=;]+)$"):
            yield CInstr(m.group(1), m.group(2), None)
        elif m.match(r"^([^=;]+);([^=;]+)$"):
            yield CInstr(None, m.group(1), m.group(2))
        elif m.match(r"^\(([^()]+)\)"):
            yield LInstr(m.group(1))

def assemble(src_filename):
    if not src_filename.endswith(ASM_SUFFIX):
        raise error, "Illegal file name '%s'" % src_filename
    tgt_filename = src_filename[:-len(ASM_SUFFIX)] + HACK_SUFFIX

    symbols = {}
    symbols["SP"] = 0
    symbols["LCL"] = 1
    symbols["ARG"] = 2
    symbols["THIS"] = 3
    symbols["THAT"] = 4
    for r in range(16):
        symbols["R%d" % r] = r
    symbols["SCREEN"] = 0x4000
    symbols["KBD"] = 0x6000

    with nested(open(src_filename, "r"), open(tgt_filename, "w")) as (src, tgt):
        pc = 0
        for instr in doPass(src):
            if instr.type == "L":
                symbols[instr.symbol] = pc
            else:
                pc = pc + 1

        src.seek(0)
        next_var = 0x0010

        for instr in doPass(src):
            out = None
            if instr.type == "A":
                if instr.symbol is None:
                    value = instr.value
                else:
                    if not instr.symbol in symbols:
                        symbols[instr.symbol] = next_var
                        next_var += 1
                    value = symbols[instr.symbol]
                out = "0" + binary(value, 15)
            elif instr.type == "C":
                out = "111" + compCode[instr.comp] + destCode[instr.dest] + jmpCode[instr.jmp]

            if out:
                tgt.write(out)
                tgt.write("\n")

if __name__ == "__main__":
    import sys
    for arg in sys.argv[1:]:
        assemble(arg)

