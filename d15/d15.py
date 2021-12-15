import numpy as np


def parse_input(inputFile):
    with open(inputFile) as f:
        return np.array([[int(s) for s in line.strip()] for line in f if line.strip() != ""])


def safe_index(array, y, x):
    try:
        if (x >= 0) and (y >= 0):
            return array[y, x]
    except IndexError as e:
        pass
    return None


def dijkstra(array, start, destination):
    costs = {start: 0}
    parents = {start: start} # not actually needed
    unvisited = [start]

    while unvisited:
        node = unvisited.pop()
        parent = parents[node]
        cost = costs[node]

        if (node == destination):
            return cost     # return early in this case

        j, i = node
        for dy, dx in (1, 0), (0, 1), (-1, 0), (0, -1):
            neighbour = (j + dy, i + dx)
            neighbourCost = safe_index(array, *neighbour)
            if (neighbourCost is None):
                continue    # out of bounds

            neighbourPathCost = cost + neighbourCost
            if (neighbour not in costs):
                costs[neighbour] = neighbourPathCost
                parents[neighbour] = node
                unvisited.append(neighbour)
            elif (neighbourPathCost < costs[neighbour]):
                costs[neighbour] = neighbourPathCost
                parents[neighbour] = node
        
        # sort nodes by cost (in reverse as we pop from end)
        unvisited = sorted(unvisited, key=lambda r: costs[r], reverse=True) 


def part1(array):
    c = dijkstra(array, (0,0), (array.shape[0] - 1, array.shape[1] - 1))
    print(c)
    return c


def part2(array):
    shapey = array.shape[0]
    shapex = array.shape[1]
    bigArray = np.zeros([shapey*5, shapex*5], dtype=int)
    for j in range(5):
        for i in range(5):
            bigArray[j * shapey:(j + 1) * shapey,
                     i * shapex:(i + 1) * shapex] = array + i + j

    # 9 -> (8 % 9) + 1 = 9; 10 -> (9 % 9) + 1 = 1; etc.
    bigArray = np.mod(bigArray - 1, 9) + 1
    print(bigArray)
    
    c = dijkstra(bigArray, (0,0), (bigArray.shape[0] - 1, bigArray.shape[1] - 1))
    print(c)
    return c

if __name__=="__main__":
    init = parse_input("sample.txt")
    assert part1(init) == 40
    assert part2(init) == 315

    init = parse_input("input.txt")
    assert part1(init) == 462
    assert part2(init) == 2846