# from collections import defaultdict
from pprint import pprint 
import numpy as np


def parse_input(inputFile):
    with open(inputFile) as f:
        return np.array([[int(s) for s in line.strip()] for line in f if line.strip() != ""])


def get_height_safe(heights, x, y):
    try:
        if (x >= 0) and (y >= 0):
            return heights[x,y]
    except IndexError as e:
        pass
    return None


def part1(heights):
    mins = {}
    x, y = heights.shape

    for j in range(y):
        for i in range(x):
            h = get_height_safe(heights, i, j)
            fail = False

            for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                neighbour = get_height_safe(heights, i + dx, j + dy)
                if (neighbour is not None) and (neighbour <= h): 
                    fail = True 
                    break

            if not fail: 
                # i,j is lower than all its neighbours
                # print(f"low point at {i} {j}: {h}")
                mins[(i,j)] = h 

    risk = sum(mins.values()) + len(mins.values())
    print("Risk factor:   ", risk)
    return risk, mins


def basin_size_dfs(heights, i, j, visited):
    subTreeSize = 1 
    visited.add((i,j)) 
    for x, y in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        newLoc = (i + x, j + y)
        if not newLoc in visited: 
            newH = get_height_safe(heights, *newLoc)
            if (newH is not None) and (newH != 9):
                subTreeSize += basin_size_dfs(heights, *newLoc, visited)
    return subTreeSize


def part2(heights, minima):
    basins = {}
    visited = set()
    for m in minima: 
        basins[m] = basin_size_dfs(heights, *m, visited)
    
    top = sorted(basins.values(), reverse=True)
    out = np.product(top[0:3])
    print("Largest basins:", top[0:3], out)
    return out

if __name__=="__main__":
    import matplotlib.pyplot as plt

    init = parse_input("sample.txt")
    risk, mins = part1(init)
    assert risk == 15
    assert part2(init, mins) == 1134

    # plt.imshow(init)
    # plt.scatter([j for _, j in mins.keys()], [i for i, _ in mins.keys()], c="black")
    # plt.show()

    init = parse_input("input.txt")
    risk, mins = part1(init)
    assert risk == 514
    assert part2(init, mins) == 1103130
    
    plt.imshow(init)
    plt.scatter([j for _, j in mins.keys()], 
                [i for i, _ in mins.keys()], 
                c="white", marker="x", s=10)
    plt.show()

