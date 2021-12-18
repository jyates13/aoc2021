from pprint import pprint


class SnailInt:
    # Silly custom int class that just defines explode/split/magnitude/etc. 
    # operations so that we can call them recursively in the Snail number class.
    def __init__(self, num):
        self.num = num
    
    def explode(self, depth=0):
        # Can't explode an int
        return False, None, None

    def split(self):
        # If we split, we return a new Snail number class and flag the change.
        if self.num >= 10:
            return True, Snail(self.num//2, self.num//2 + self.num % 2)
        return False, None

    def magnitude(self):
        return self.num

    def add_to_right(self, other):
        self.num += other.num

    def add_to_left(self, other):
        self.num += other.num
    
    def __repr__(self):
        return f"{self.num}"

    def copy(self):
        return SnailInt(self.num)


class Snail:
    def __init__(self, left, right, debug=False):
        # Could do this with indexing to save a bit of duplication
        # but left/right is more readable 
        if type(left) is int:
            self.left = SnailInt(left)
        else:
            self.left = left

        if type(right) is int:
            self.right = SnailInt(right)
        else:
            self.right = right
        
        self.debug = debug
        if self.debug:
            self.printer = print

    def copy(self):
        return Snail(self.left.copy(), self.right.copy(), self.debug)

    def printer(self, *args, **kwargs):
        pass

    def magnitude(self):
        # Goes down the tree 'til we find int bedrock. 
        return 3*self.left.magnitude() + 2*self.right.magnitude()

    def reduce(self):
        done = False
        steps = 0
        while not done: 
            self.printer("Steps", steps)
            self.printer(self)
            steps += 1

            # Must do all explodes before splits
            # If an l/r remains at this level, it is just discarded
            changed, l, r = self.explode() 
            if changed: 
                continue

            changed, _ = self.left.split()
            if changed:
                continue

            changed, _ = self.right.split()
            if changed:
                continue

            done = True

    def explode(self, depth=0):
        # Method: track if a snail sub-number explodes
        # If we explode, we pass left/right back up
        # the call chain until we find somewhere to
        # add them, or they are discarded (in self.reduce)

        if depth == 4: # wasn't specified if depth can go above 4...
            self.printer("Explode", self)
            return True, self.left, self.right

        changed, l, r = self.left.explode(depth + 1)
        if changed: 
            if l is not None and r is not None:
                # This is the lowest level; we can guarantee that we use 
                # up the right int if a left Snail explodes (& vice versa) 
                # so if both not None we replace with 0.
                self.left = SnailInt(0)
            if r is not None:
                # If left explodes, we know there is somewhere on the right
                # to add the right component of exploded number 
                # If right is a Snail, we need to add number to its *left*
                self.right.add_to_left(r)
                # r is now used up.
            return True, l, None
    
        changed, l, r = self.right.explode(depth + 1)
        if changed: 
            if l is not None and r is not None: 
                self.right = SnailInt(0)
            if l is not None:
                self.left.add_to_right(l)
            return True, None, r

        return False, None, None

    def add_to_right(self, number):
        # Keep going down until we get to an int.
        self.right.add_to_right(number)

    def add_to_left(self, number):
        self.left.add_to_left(number)

    def split(self):
        changed, sl = self.left.split()
        if changed: 
            if sl is not None:
                # It was an int that just split, so set our new left
                self.printer("Split", self)
                self.left = sl
            return True, None

        changed, sr = self.right.split()
        if changed:
            if sr is not None:
                self.printer("Split", self)
                self.right = sr
            return True, None
        
        return False, None

    def __repr__(self):
        return f"[{self.left}, {self.right}]"


def list_to_snail(l, debug=False):
    # pretty stupid
    if type(l[0]) is int:
        left = SnailInt(l[0])
    else: 
        left = list_to_snail(l[0])
    
    if type(l[1]) is int:
        right = SnailInt(l[1])
    else: 
        right = list_to_snail(l[1])
    
    return Snail(left, right, debug)


def parse_input(filename, debug=False):
    # Uses the dreaded eval
    # Don't run on unknown input!!!
    numbers = []
    for line in open(filename):
        if line.strip() == "":
            continue
        else: 
            numbers.append(list_to_snail(eval(line), debug))

    return numbers


def part1(init, debug=False):
    current = init[0].copy()
    for num in init[1:]:
        current = Snail(current, num.copy(), debug)
        current.reduce()

    print("Sum of inputs:", current)
    mag = current.magnitude()
    print("Magnitude of inputs:", mag)
    return mag


def part2(init, debug=False):
    # simple/stupid
    maxMag = 0

    for i in init:
        for j in init:
            if i == j:
                continue
            current = Snail(i.copy(), j.copy(), debug)
            current.reduce()
            mag = current.magnitude()
            maxMag = max(maxMag, mag)
            best = (i, j)

    print("Max magnitude:", maxMag)
    print("Best:", best[0], "  +  ", best[1])
    return maxMag

if __name__ == "__main__":
    init = parse_input("sample.txt")
    # pprint(init)
    assert part1(init) == 4140
    assert part2(init) == 3993

    init = parse_input("input.txt")
    # pprint(init)
    assert part1(init) == 4235
    assert part2(init) == 4659