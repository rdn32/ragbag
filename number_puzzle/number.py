base = None
columns = None
digits = None
max_power = None
lengths_under = None

def init(base_, columns_, digits_):
    global base, columns, digits
    global max_power, lengths_under
    assert base_ > 1
    assert len(digits_) == base_
    assert len(columns_) > 0
    assert columns_[0] == ""
    assert digits_[0] == ""
    base = base_
    columns = columns_
    digits = digits_
    max_power = len(columns_)
    lengths_under = {}

def initBase1000():
    units = ["",      "one",   "two",     "three",  "four",
             "five",  "six",   "seven",   "eight",  "nine"]
    tens  = ["",      "ten",   "twenty",  "thirty", "forty",
             "fifty", "sixty", "seventy", "eighty", "ninety"]

    upTo100 = []
    for t in tens:
        for u in units:
            upTo100.append("%s%s" % (t, u))
    upTo100[11] = "eleven"
    upTo100[12] = "twelve"
    upTo100[13] = "thirteen"
    upTo100[14] = "fourteen"
    upTo100[15] = "fifteen"
    upTo100[16] = "sixteen"
    upTo100[17] = "seventeen"
    upTo100[18] = "eighteen"
    upTo100[19] = "nineteen"

    all = []
    for d in units:
        if not d:
            prefix = ""
        else:
            prefix = "%shundred" % d
        all.extend(prefix + elt for elt in upTo100)

    init(1000, ["", "thousand", "million", "billion"], all)

# Other than for testing, use base 1000
initBase1000()

def repr(n):
    remaining = n
    result = []
    for p in range(max_power):
        d = remaining % base
        remaining = remaining // base
        result.append(columnEntry(d, p))
    if remaining != 0:
        raise ArithmeticError("Overflow")
    result.reverse()
    return "".join(result)

def columnEntry(d, p):
        if d == 0:
            return ""
        else:
            return "%s%s" % (digits[d], columns[p])

def lengthUnder(power, lenPrefix):
    if power == 0:
        return (lenPrefix, 1)

    if power in lengths_under:
        length, count = lengths_under[power]
    else:
        length = 0
        count = 0
        for d in range(base):
            entry = columnEntry(d, power-1)
            subLength, subCount = lengthUnder(power-1, len(entry))
            count = count + subCount
            length = length + subLength
        lengths_under[power] = length, count
        
    return (length + lenPrefix * count, count)

def traverse(prefix, power, listener):
    items = []
    for d in range(base):
        items.append((columnEntry(d, 0), 0))
    for p in range(1, power):
        for d in range(1, base):
            items.append((columnEntry(d, p), p))
    items.sort()
    for entry, p in items:
        listener.visit(prefix + entry, p)

class ListMaker:
    def __init__(self, limit):
        self.seen = []
        self.limit = limit
    def visit(self, prefix, power):
        if len(self.seen) == self.limit:
            pass
        elif power == 0:
            self.seen.append(prefix)
        else:
            traverse(prefix, power, self)

class IthCharFinder:
    def __init__(self, i):
        self.i = i
        self.foundChar = None
        self.foundWord = None
        self.wordIndex = 0
    def visit(self, prefix, power):
        if self.foundChar is None:
            length, count = lengthUnder(power, len(prefix))
            if self.i >= length:
                self.i = self.i - length
                self.wordIndex = self.wordIndex + count
            elif power > 0:
                traverse(prefix, power, self)
            else:
                self.foundWord = prefix
                self.foundChar = prefix[self.i]

def makeList(limit):
    maker = ListMaker(limit)
    traverse("", max_power, maker)
    return maker.seen

def findIth(i):
    finder = IthCharFinder(i)
    traverse("", max_power, finder)
    if finder.foundChar is None:
        raise IndexError("index out of range of number sequence")
    return finder.foundChar, finder.foundWord, finder.wordIndex

if __name__ == "__main__":
    which = 1000000
    char, _, _ = findIth(which - 1)
    print("""\
Take numbers up to %d
Convert to words, sort alphabetically, then concatenate
The %dth character is '%s'\
""" % (base ** max_power, which, char))
