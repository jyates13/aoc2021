from pprint import pprint


def parse_input(filename):
    commands = []
    print(filename)

    for line in open(filename).read().split("\n"):
        if line == "":
            continue

        state, boundsLine = line.strip().split()

        bounds = []
        # increase upper bound by 1 as this 
        # makes intersections easier
        for dimension in boundsLine.split(","):
            pts = dimension.split("=")[1].split("..")
            bounds.append([int(pts[0]), int(pts[1]) + 1])

        commands.append([1 if state == "on" else 0, bounds])

    return commands


def area(a):
    return (a[0][1] - a[0][0]) * \
           (a[1][1] - a[1][0]) * \
           (a[2][1] - a[2][0])


def intersection(a, b):
    '''Intersection of two cuboids (-> another cuboid)'''
    x = [max(a[0][0], b[0][0]), min(a[0][1], b[0][1])]
    if x[1] - x[0] <= 0:
        return None
    y = [max(a[1][0], b[1][0]), min(a[1][1], b[1][1])]
    if y[1] - y[0] <= 0:
        return None
    z = [max(a[2][0], b[2][0]), min(a[2][1], b[2][1])]
    if z[1] - z[0] <= 0:
        return None
    return [x, y, z]


def subtract_inter(state, a, i):
    '''Split a cuboid a into six regions that don't include the intersect i'''
    splits = []

    # Hard to explain these in a comment... 
    # If we had a Rubiks cube and subtracted the core cube, 
    # these regions would be:
    for a in [ # entire front/back sides of 9 cubes 
              [a[0], [a[1][0], i[1][0]], a[2]],
              [a[0], [i[1][1], a[1][1]], a[2]],
               # 3 cubes on top/bottom 
              [a[0], i[1], [a[2][0], i[2][0]]],
              [a[0], i[1], [i[2][1], a[2][1]]],
               # remaining central cube on left/right
              [[a[0][0], i[0][0]], i[1], i[2]],
              [[i[0][1], a[0][1]], i[1], i[2]]]:

        if area(a) > 0:
            splits.append([state, a])

    return splits


def solve(commands, bounds_constraint=None):
    '''Count cubes that are on after series of commands. 
Method: 
    i.    Take the next cuboid from the instructions 
    ii.   Check intersection with each earlier "on" cuboid ("done" pile)
    iii.  If both cuboids are on, subtract intersection from new cuboid
    iv.   If new is off and "done" cuboid is on, subtract intersection 
          from done cuboid
    v.    If new cuboid is on and any segments remain after all 
          subtractions, add them to "done" pile.
    vi.   Count all cubes in cuboids in "done" pile at the end. 

Note we only keep "on" cuboids
'''
    done = []

    for state, boundsOrig in commands: 
        bounds = [b.copy() for b in boundsOrig]
        if bounds_constraint is not None:
            # if outside of the question bounds (part 1), skip, 
            # else set max bounds to question bounds
            invalid = False
            for b in bounds: 
                if (b[1] < -bounds_constraint) or (b[0] > bounds_constraint):
                    invalid = True
                    break
                b[0] = max(b[0],-bounds_constraint)
                b[1] = min(b[1], bounds_constraint + 1)
            if invalid:
                continue

        # Start with plain cuboid.
        toAdd = [[state, bounds]]

        i = 0
        # for each cuboid that is still on
        while i < len(done):
            doneState, doneBounds = done[i]

            j = 0
            # for each cuboid that we want to turn on with this command
            while j < len(toAdd):
                _, addBounds = toAdd[j]

                # check if cuboids under consideration intersect
                inter = intersection(addBounds, doneBounds)
                if inter is None: 
                    j += 1
                    continue

                if state: 
                    # if both "on", remove intersection and keep remainder 
                    # under consideration (to avoid double counting)
                    addSplits = subtract_inter(state, addBounds, inter)
                    del toAdd[j]
                    if addSplits:
                        for s in addSplits:
                            toAdd.insert(j, s)
                            j += 1
                    j -= 1

                else: 
                    # if cuboid under consideration is an "off" cuboid, remove 
                    # the intersection from the cuboid in the current "on" pile
                    # Note if we're doing an "off" cuboid we never split it, only
                    # the "done" cuboids, so j == 0
                    doneSplits = subtract_inter(doneState, doneBounds, inter)
                    del done[i]
                    if doneSplits: 
                        for s in doneSplits:
                            done.insert(i, s)
                            i += 1
                    i -= 1

                j += 1
            i += 1

        if state: 
            # if anything remains to switch on, add it to the "on" pile
            done.extend(toAdd)

    cubes = 0
    for state, bounds in done:
        cubes += area(bounds)

    print("Final cubes:", cubes)
    return cubes


if __name__ == "__main__":
    commands = parse_input("sample_0.txt")
    assert solve(commands, bounds_constraint=50) == 1

    commands = parse_input("sample_1.txt")
    assert solve(commands, bounds_constraint=50) == 39

    commands = parse_input("sample_2.txt")
    assert solve(commands, bounds_constraint=50) == 590784

    commands = parse_input("sample_3.txt")
    assert solve(commands, bounds_constraint=50) == 474140
    assert solve(commands) == 2758514936282235

    commands = parse_input("input.txt")
    assert solve(commands, bounds_constraint=50) == 568000
    assert solve(commands) == 1177411289280259

