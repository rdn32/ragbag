#!/usr/bin/python

from contextlib import nested
import re

ASM_SUFFIX = ".asm"
HACK_SUFFIX = ".hack"

class error(Exception): pass

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

def assemble(src_filename):
    if not src_filename.endswith(ASM_SUFFIX):
        raise error, "Illegal file name '%s'" % src_filename
    tgt_filename = src_filename[:-len(ASM_SUFFIX)] + HACK_SUFFIX

    symbols = SymbolTable()

    with nested(open(src_filename, "r"), open(tgt_filename, "w")) as (src, tgt):
        # First pass: get addresses for all labels
        pc = 0
        instrs = getInstructions(src)
        for instr in instrs:
            if instr.type == "L":
                symbols.set(instr.symbol, pc)
            else:
                pc = pc + 1

        # Second pass: generate code
        for instr in instrs:
            out = None
            if instr.type == "A":
                if instr.symbol is None:
                    value = instr.value
                else:
                    value = symbols.getOrGenerate(instr.symbol)
                out = "0" + binary(value, 15)
            elif instr.type == "C":
                out = "111" + compCode[instr.comp] + destCode[instr.dest] + jmpCode[instr.jmp]

            if out:
                tgt.write(out)
                tgt.write("\n")

def getInstructions(src):
    instrs = []
    for line in src:
        line = re.sub(r"//.*", "", line).strip()
        m = Matcher(line)

        if m.match(r"^$"):
            pass
        elif m.match(r"^@(\d+)$"):
            value = int(m.group(1))
            instrs.append(AInstr(int(m.group(1)), None))
        elif m.match(r"^@([^()]+)"):
            instrs.append(AInstr(None, m.group(1)))
        elif m.match(r"^([^=;]+)=([^=;]+)$"):
            instrs.append(CInstr(m.group(1), m.group(2), None))
        elif m.match(r"^([^=;]+);([^=;]+)$"):
            instrs.append(CInstr(None, m.group(1), m.group(2)))
        elif m.match(r"^\(([^()]+)\)"):
            instrs.append(LInstr(m.group(1)))

    return instrs

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

class SymbolTable(object):
    def __init__(self):
        self.symbols = {}
        self.next_var = 0x0010

        self.symbols["SP"] = 0
        self.symbols["LCL"] = 1
        self.symbols["ARG"] = 2
        self.symbols["THIS"] = 3
        self.symbols["THAT"] = 4
        for r in range(16):
            self.symbols["R%d" % r] = r
        self.symbols["SCREEN"] = 0x4000
        self.symbols["KBD"] = 0x6000

    def set(self, symbol, value):
        self.symbols[symbol] = value

    def getOrGenerate(self, symbol):
        if symbol not in self.symbols:
            self.symbols[symbol] = self.next_var
            self.next_var += 1
        return self.symbols[symbol]

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

if __name__ == "__main__":
    import sys
    for arg in sys.argv[1:]:
        assemble(arg)

