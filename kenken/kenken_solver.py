#!/usr/bin/python

from collections import defaultdict

rows = cols = range(6)
coords = [(r,c) for r in rows for c in cols]
digits = [n+1 for n in range(6)]

class State(object):
    def __init__(self):
        self.squares = dict((coord, None) for coord in coords)
        self.row_unused = [set(digits) for r in rows]
        self.col_unused = [set(digits) for c in cols]

    def getValue(self, coord):
        return self.squares[coord]

    def canPlace(self, coord, d):
        (r,c) = coord
        return (self.squares[coord] is None
                and d in self.row_unused[r]
                and d in self.col_unused[c])

    def place(self, coord, d):
        assert self.canPlace(coord, d)
        (r,c) = coord
        self.squares[coord] = d
        self.row_unused[r].remove(d)
        self.col_unused[c].remove(d)

    def clear(self, coord):
        d = self.squares[coord]
        assert d is not None
        (r,c) = coord
        self.squares[coord] = None
        self.row_unused[r].add(d)
        self.col_unused[c].add(d)

    def __str__(self):
        chars = {}
        for coord in self.squares:
            if self.squares[coord] is None:
                chars[coord] = ' '
            else:
                chars[coord] = '%d' % self.squares[coord]

        lines = ["".join(chars[r,c] for c in cols) for r in rows]
        return "".join(line + "\n" for line in lines)

class Constraint(object):
    def __init__(self, target, coords):
        self.target = target
        self.coords = coords

    def _getValues(self, state):
        return [state.getValue(coord) for coord in self.coords]

    def hasConflict(self, state):
        pass

class AddConstraint(Constraint):
    def hasConflict(self, state):
        result = 0
        for value in self._getValues(state):
            if value is None:
                return False
            result += value
        return result != self.target

class MulConstraint(Constraint):
    def hasConflict(self, state):
        result = 1
        for value in self._getValues(state):
            if value is None:
                return False
            result *= value
        return result != self.target

class SubConstraint(Constraint):
    def hasConflict(self, state):
        values = self._getValues(state)
        assert len(values) == 2
        if None in values:
            return False
        return self.target + min(values) != max(values)

class DivConstraint(Constraint):
    def hasConflict(self, state):
        values = self._getValues(state)
        assert len(values) == 2
        if None in values:
            return False
        a, b = min(values), max(values)
        return self.target * min(values) != max(values)

constraint_classes = {
    '+' : AddConstraint,
    '*' : MulConstraint,
    '-' : SubConstraint,
    '/' : DivConstraint
}

def parse(input):
    lines = [line.strip() for line in input]
    lines = [line for line in lines if len(line)]

    coords_by_name = defaultdict(list)
    for i, name in enumerate("".join(lines[:6])):
        coord = divmod(i, 6)
        coords_by_name[name].append(coord)

    constraint_map = {}

    for line in lines[6:]:
        parts = line.split(" ")
        coords_for_constraint = coords_by_name[parts[0]]
        target = int(parts[1])
        if len(parts) < 3:
            constraint_class = AddConstraint
            assert len(coords_for_constraint) == 1
        else:
            constraint_class = constraint_classes[parts[2]]

        constraint = constraint_class(target, coords_for_constraint)
        for coord in coords_for_constraint:
            constraint_map[coord] = constraint

    assert set(constraint_map.keys()) == set(coords)

    return constraint_map

def solve(constraint_map, state=None, i=0):
    if state == None: state = State()

    if i == len(coords):
        yield str(state)
    else:
        coord = coords[i]
        constraint = constraint_map[coord]
        for d in digits:
            if state.canPlace(coord, d):
                state.place(coord, d)
                if not constraint.hasConflict(state):
                    for result in solve(constraint_map, state, i+1):
                        yield result
                state.clear(coord)

if __name__ == "__main__":
    import sys
    print("\n".join(soln for soln in solve(parse(sys.stdin))), end='')
