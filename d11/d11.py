import numpy as np
from pprint import pprint


def parse_input(inputFile):
    with open(inputFile) as f:
        return np.array([[int(s) for s in line.strip()] for line in f if line.strip() != ""])


def safe_index(array, x, y):
    try:
        if (x >= 0) and (y >= 0):
            return array[x,y]
    except IndexError as e:
        pass
    return None


def oct_flash_dfs(octs, i, j, flashed): 
    flashes = 1
    octs[i,j] = 0
    flashed.add((i,j)) 
    for x, y in ((0, 1), (1, 0), (0, -1), (-1, 0), 
                 (1, 1), (1, -1), (-1, 1), (-1, -1)):
        newLoc = (i + x, j + y)
        if not newLoc in flashed: 
            if safe_index(octs, *newLoc) is not None:
                octs[i + x, j + y] += 1
                if octs[newLoc] > 9:
                    flashes += oct_flash_dfs(octs, *newLoc, flashed)

    return flashes


def step(octs):
    flashCount = 0
    flashed = set()
    x, y = octs.shape
    octs += 1

    for j in range(y):
        for i in range(x):
            if octs[i,j] > 9:
                flashCount += oct_flash_dfs(octs, i, j, flashed)

    return flashCount


def part1(octs, steps):
    flashCount = 0
    for _ in range(steps):
        flashCount += step(octs)
    
    print(f"Flashes in {steps:3d} steps:  ", flashCount)
    return flashCount


def part2(octs, start=0):
    steps = start
    while (np.any(octs != np.zeros_like(octs))):
        step(octs)
        steps += 1
    print("Steps until sync:      ", steps)
    return steps 


if __name__=="__main__":
    import matplotlib.pyplot as plt

    init = parse_input("sample.txt")

    flashes = part1(init, 1)
    assert "\n".join("".join(str(i) for i in line) for line in init) == \
'''6594254334
3856965822
6375667284
7252447257
7468496589
5278635756
3287952832
7993992245
5957959665
6394862637'''

    flashes += part1(init, 1)
    assert "\n".join("".join(str(i) for i in line) for line in init) == \
'''8807476555
5089087054
8597889608
8485769600
8700908800
6600088989
6800005943
0000007456
9000000876
8700006848'''

    flashes += part1(init, 98)
    assert flashes                  == 1656
    assert part2(init, 100)         == 195

    # plt.imshow(init)
    # plt.show()

    init = parse_input("input.txt")
    assert part1(init.copy(), 100)  == 1599 
    assert part2(init, 0)           == 418
