from pprint import pprint

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y 
    
    def __repr__(self):
        return f"({self.x}, {self.y})"
    
    def __eq__(self, other):
        return (self.x, self.y) == other


def parse_input(filename):
    with open(filename) as f: 
        return f.readline().strip("target area: ").split(",")


def step(pos, vel):
    nextPos = Coord(pos.x + vel.x, pos.y + vel.y)

    if vel.x == 0:
        newX = 0
    elif vel.x > 0:
        newX = vel.x - 1
    elif vel.x < 0:
        newX = vel.x + 1
    nextVel = Coord(newX, vel.y - 1)

    return nextPos, nextVel


def hit_target(pos, target):
    return ((target[0][0] <= pos.x <= target[0][1]) and
            (target[1][0] <= pos.y <= target[1][1]))


def run_vel(pos, vel, target):
    maxY = pos.y

    # while 
    # ((right of target and going left) or (left of target and going right))
    # and (above or going up)
    while (((pos.x >= min(target[0])) and (vel.x <= 0)) or \
           ((pos.x <= max(target[0])) and (vel.x >= 0))) and \
          ((pos.y >= min(target[1])) or (vel.y >= 0)):
        pos, vel = step(pos, vel)
        maxY = max(maxY, pos.y)
        if hit_target(pos, target):
            return maxY

    return None


def solve(init, printAll=False):
    xr = list(map(int, init[0].strip().strip("x=").split("..")))
    yr = list(map(int, init[1].strip().strip("y=").split("..")))

    maxY = -1
    maxYVel = Coord(0, 0)
    allowable = []

    # Very slow, dumb solution but solved it on the train 
    # Smarter solutions exist but this was satisfactory ¯\_(ツ)_/¯
    for x in range(0, xr[1] + 1, 1):
        for y in range(yr[0] - 1, 1000, 1):
            vel = Coord(x, y)
            pos = Coord(0, 0)
            newY = run_vel(pos, vel, [xr, yr])
            if newY is not None:
                # we found a solution
                allowable.append(vel)
                if newY > maxY:
                    maxY = newY
                    maxYVel = vel
                    if printAll: print(f"New max at {vel}: {newY}")

    print(f"Max Y: {maxYVel} achieves {maxY}")
    print(f"Allowed shots: {len(allowable)}")
    if printAll:
        print(allowable) 

    return maxY, allowable


def parse_allowed(filename):
    # Just a check that we find all the same on-target shots 
    ls = open(filename).read().split()
    return [tuple(map(int, token.strip().split(","))) for token in ls if token.strip() != ""]


if __name__=="__main__":
    init = parse_input("sample.txt")
    allowed = parse_allowed("allowed.txt")
    # hacky - sort by x then y 
    allowed = sorted(allowed, key=lambda r: r[0] * 1000 + r[1])
    # print(allowed)

    maxY, foundValid = solve(init, printAll=True)
    assert maxY == 45
    assert foundValid == allowed 

    init = parse_input("input.txt")
    maxY, foundValid = solve(init)
    assert maxY == 17766
    assert len(foundValid) == 1733