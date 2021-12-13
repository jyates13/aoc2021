import numpy as np
from pprint import pprint


class Points:
    def __init__(self, lines):
        x, y = 0, 0
        points = []
        while lines:
            line = lines.pop()
            if line == "":
                continue
            cx, cy = line.strip().split(",")
            x = max(x, int(cx) + 1)
            y = max(y, int(cy) + 1)
            points.append((int(cy), int(cx)))

        self.points = np.zeros((y, x))
        for p in points:
            self.points[p] = 1

    def __repr__(self):
        return "\n".join(["".join(
                            ["#" if p > 0 else "." for p in l]) 
                        for l in self.points])

def parse_input(inputFile):
    with open(inputFile) as f:
        folds = []
        pointLines, foldLines = f.read().split("\n\n")
        points = Points(pointLines.split("\n"))

        foldLines = foldLines.split("\n")
        while foldLines:
            l = foldLines.pop(0).strip()
            if l != "":
                folds.append(l.strip("fold along "))
    
    return points, folds


def fold(p: Points, fold) -> Points:
    axis, loc = fold.split("=")
    loc = int(loc)
    shapey, shapex = p.points.shape
    if axis == "y":
        foldy, foldx = p.points[:loc:-1].shape
        p.points[loc - foldy:loc] += p.points[:loc:-1]
        p.points = p.points[0:loc]

    elif axis == "x":
        foldy, foldx = p.points[:,:loc:-1].shape
        p.points[:,loc - foldx:loc] += p.points[:,:loc:-1]
        p.points = p.points[:,0:loc]
        

    return p


def part1(points: Points, folds) -> (Points, int):
    f = folds.pop(0)
    points = fold(points, f)
    pointCount = np.sum(p.points > 0)
    print("Part 1 point count:", pointCount)
    return points, pointCount


def part2(points: Points, folds) -> Points:
    for f in folds:
        points = fold(points, f)
    
    return points



if __name__ == "__main__":
    p, folds = parse_input("sample.txt")
    print("== Sample ==")
    print("Points: ")
    print(p)
    assert p.__repr__() == \
'''...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
...........
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........'''
    print("Folds: ", end="")
    pprint(folds)

    p, pointCount = part1(p, folds)
    print("After fold: ")
    print(p)
    assert p.__repr__() == \
'''#.##..#..#.
#...#......
......#...#
#...#......
.#.#..#.###
...........
...........'''
    assert pointCount == 17

    print("== Input ==")
    p, folds = parse_input("input.txt")
    p, pointCount = part1(p, folds)
    assert pointCount == 763
    p = part2(p, folds)
    print("Part 2:")
    print(p)
