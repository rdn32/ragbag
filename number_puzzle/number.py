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

def repr(n):
    remaining = n
    result = []
    for p in range(max_power):
        d = remaining % base
        remaining = remaining // base
        result.append(columnEntry(d, p))
    result.reverse()
    return "".join(result)

def columnEntry(d, p):
        if d == 0:
            return ""
        else:
            return "%s%s" % (digits[d], columns[p])

def lengthUnder(power, prefix):
    if power == 0:
        return (prefix, 1)

    if lengths_under.has_key(power):
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
        
    return (length + prefix*count, count)

def traverse(prefix, power, listener):
    items = []
    for d in range(base):
        items.append((columnEntry(d, 0), 0))
    for p in range(1, power):
        for d in range(1, base):
            items.append((columnEntry(d, p), p))
    items.sort()
    for entry, p in items:
        if listener.shouldStop(prefix, entry, p):
            return True
        elif p == 0:
            listener.visit(prefix, entry)
        elif listener.shouldTraverse(prefix, entry, p):
            stopped = traverse(prefix + entry, p, listener)
            if stopped:
                return True
    return False

class ListMaker:
    def __init__(self):
        self.seen = []
    def shouldStop(self, prefix, entry, power):
        return False
    def shouldTraverse(self, prefix, entry, power):
        return True
    def visit(self, prefix, entry):
        self.seen.append(prefix + entry)