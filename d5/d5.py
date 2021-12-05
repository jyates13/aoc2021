import numpy as np


# alternative: use each vent grid position as hash in a dictionary as the grid is probably sparse  
# it's surely less horrid than this 


def parse_input(inputFile):
    vents = []
    dims = [0, 0]
    with open(inputFile) as f:
        for line in f.readlines(): 
            if line.strip() != "": 
                vals = [list(map(int, pair.split(","))) for pair in line.strip().split("->")]
                vents.append(vals)
                dims[0] = max(dims[0], vals[0][0] + 1, vals[1][0] + 1)
                dims[1] = max(dims[1], vals[0][1] + 1, vals[1][1] + 1)
    return dims, vents 


def part1(dims, vents):
    counts = np.zeros(dims)
    crosses = 0
    for start, end in vents:
        if (start[0] == end[0]) or (start[1] == end[1]):
            minx, maxx = (start[0], end[0]) if start[0] < end[0] else (end[0], start[0])
            miny, maxy = (start[1], end[1]) if start[1] < end[1] else (end[1], start[1])
            slice = counts[miny:maxy+1, minx:maxx+1]
            slice += 1
            crosses += np.sum(slice == 2) 
    print(counts)
    return crosses


def part2(dims, vents):
    counts = np.zeros(dims)
    crosses = 0
    for start, end in vents:
        if (start[0] == end[0]) or (start[1] == end[1]):
            minx, maxx = (start[0], end[0]) if start[0] < end[0] else (end[0], start[0])
            miny, maxy = (start[1], end[1]) if start[1] < end[1] else (end[1], start[1])
            slice = counts[miny:maxy+1, minx:maxx+1]
            slice += 1
            crosses += np.sum(slice == 2)
        else:
            xdir = (end[0]-start[0])//abs(end[0]-start[0])
            ydir = (end[1]-start[1])//abs(end[1]-start[1])
            for loc in zip(range(start[1], end[1] + ydir, ydir),
                           range(start[0], end[0] + xdir, xdir)):
                counts[loc] += 1
                if counts[loc] == 2:
                    crosses += 1 
        
    print(counts)
    return crosses


if __name__=="__main__":
    dims, v = parse_input("sample.txt")
    print(dims, v)
    print(part1(dims, v))
    print(part2(dims, v))

    dims, v = parse_input("input.txt")
    print(dims)
    print(part1(dims, v))
    print(part2(dims, v))
