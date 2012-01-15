base = None
columns = None
digits = None
max_power = None

def init(base_, columns_, digits_):
    global base, columns, digits, max_power
    assert base_ > 1
    assert len(digits_) == base_
    assert len(columns_) > 0
    assert columns_[0] == ""
    base = base_
    columns = columns_
    digits = digits_
    max_power = len(columns_)

def repr(n):
    remaining = n
    result = []
    for p in range(max_power):
        d = remaining % base
        remaining = remaining // base
        if d == 0:
            result.append("")
        else:
            result.append("%s%s" % (digits[d], columns[p]))
    result.reverse()
    return "".join(result)
