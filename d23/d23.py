import heapq
from functools import lru_cache
from pprint import pprint
from collections import OrderedDict
import re


# part two additional lines
#D#C#B#A#
#D#B#A#C#
part2add = [["D", "D"],
            ["C", "B"],
            ["B", "A"],
            ["A", "C"]]


def hash_amph(state):
    return tuple(state[0:7] + list(map(tuple, state[7:])))


def print_state(state):
    c = [s if s is not None else "." for s in state[:7]]
    string = ['#############\n']
    string.append('#{}{}.{}.{}.{}.{}{}#\n'.format(*c))
    rs = [[a if a is not None else "." for a in r] for r in state[7:]]
    string.append('###{}#{}#{}#{}###\n'.format(
            *[r[0] for r in rs]))
    for i in range(1, len(state[7])):
        string.append('  #{}#{}#{}#{}#\n'.format(
            *[r[i] for r in rs]))
    string.append("  #########")
    return "".join(string)



def parse_input(filename, part2=False):
    state = [None] * 7      # corridor
    amphs = re.findall("[A-Z]", open(filename).read())
    for i in range(4):
        # rooms
        if not part2:
            state.append([amphs[i], amphs[4 + i]])
        else: 
            state.append([amphs[i]] + part2add[i] + [amphs[4 + i]])
    print(hash_amph(state))
    return hash_amph(state)


part1winState = [None] * 7 + \
                [["A"] * 2,
                 ["B"] * 2,
                 ["C"] * 2,
                 ["D"] * 2]
part1win = hash_amph(part1winState)
part2winState = [None] * 7 + \
                [["A"] * 4,
                 ["B"] * 4,
                 ["C"] * 4,
                 ["D"] * 4]
part2win = hash_amph(part1winState)


goals = OrderedDict({"A": 0, "B": 1, "C": 2, "D": 3})
costAmph = {"A": 1, "B": 10, "C": 100, "D": 1000}


def win(state, part2=False):
    if state == part1win:
        return True
    else: 
        return state == part2win


def win_generic(state): 
    for i, c in enumerate(state[7:]):
        for a in c: 
            if a != goals.keys()[i]:
                return False
    return True


def move_cost(location, to):
    cost = 0
    while location != to:
        if isinstance(location, int) and location < 7:
            # we're in a corridor
            if isinstance(to, int) and to < 7:
                # going along corridor
                cost += 2 * abs(to - location)
                if location == 0 or location == 6: 
                    cost -= 1
                if to == 0 or to == 6: 
                    cost -= 1
                location = to
            else: 
                # going into a room
                room, depth = to
                if location == room + 1 or location == room + 2:
                    # we're outside
                    cost += 2 + depth
                    location = (room, depth)
                else: 
                    # move to entrance
                    a = move_cost(location, room + 1)
                    b = move_cost(location, room + 2)
                    cost += a if a < b else b
                    location = room + 1 if a < b else room + 2
        else: 
            # we're in a room 
            room, depth = location
            # just cheat and reverse the call
            a = move_cost(room + 1, location) + move_cost(room + 1, to)
            b = move_cost(room + 2, location) + move_cost(room + 2, to)
            cost += a if a < b else b
            location = to
    return cost


def possible_moves(state):
    moves = []

    for i, c in enumerate(state[0:7]): 
        if c is None:
            continue
        else: 
            # move to room?
            goal = goals[c]
            room = state[7 + goal]
            top = 0
            foundTop = False
            for a in room: 
                if a is None and not foundTop: 
                    top += 1
                if a is not None: 
                    foundTop = True
                if not ((a == c) or (a is None)): 
                    break 
            else: 
                # if not foundTop: 
                #     # room is empty
                #     top -= 1
                cost = costAmph[c] * move_cost(i, (goal, top))
                corr = list(state[:7])
                corr[i] = None
                room = list(state[7 + goal])
                room[top - 1] = c
                move = corr
                for j, r in enumerate(state[7:]): 
                    if goal == j: 
                        move.append(tuple(room))
                    else: 
                        move.append(r)
                move = tuple(move)
                print(print_state(state))
                print(c, room, cost, move)
                input()
                moves.append([cost, move])

    for i, r in enumerate(state[7:]): 
        depth = 0 
        for a in r: 
            if a is None:
                depth += 1
                continue
            else: 
                entrances = (i + 1, i + 2) 
                for j in range(7):
                    if state[j] is not None: 
                        continue 

                    if j > entrances[1]:
                        start = entrances[1]
                        end = j
                    elif j < entrances[0]:
                        start = j 
                        end = entrances[0]
                    else: 
                        start = j
                        end = j 

                    fail = False
                    for k in range(start, end):
                        if state[k] is not None: 
                            fail = True
                            break
                    if fail: 
                        continue

                    cost = costAmph[a] * move_cost((i, depth), j)
                    corr = list(state[:7])
                    corr[j] = a
                    room = list(state[7 + i])
                    room[depth] = None
                    move = corr
                    for k, r in enumerate(state[7:]): 
                        if i == k: 
                            move.append(tuple(room))
                        else: 
                            move.append(r)
                    move = tuple(move)
                    moves.append([cost, move])

                break # only first guy can move
    
    return moves


def solve(state, visited=None, part2=False):
    if visited is None: 
        visited = set()
    stack = []

    count = 0
    heapq.heappush(stack, [0, 0, state])


    done = False
    while stack: 
        cost, _, state = heapq.heappop(stack)
        visited.add(state)
        print(print_state(state), "   ", cost)
        if win(state): 
            break 
        for c, m in possible_moves(state):
            if m in visited: 
                continue
            else: 
                count += 1
                heapq.heappush(stack, [c + cost, count, m])

    print("Cost:", cost)

    return cost


if __name__=="__main__":
    state = parse_input("sample.txt")
    print(print_state(state))
    solve(state, part2=False)
    # for c, p in possible_moves(state):
    #     print(c)
    #     print(print_state(p))




# def dijkstra(array, start, destination):
#     costs = {start: 0}
#     parents = {start: start} # not actually needed
#     unvisited = [start]

#     while unvisited:
#         node = unvisited.pop()
#         parent = parents[node]
#         cost = costs[node]

#         if (node == destination):
#             return cost     # return early in this case

#         j, i = node
#         for dy, dx in (1, 0), (0, 1), (-1, 0), (0, -1):
#             neighbour = (j + dy, i + dx)
#             neighbourCost = safe_index(array, *neighbour)
#             if (neighbourCost is None):
#                 continue    # out of bounds

#             neighbourPathCost = cost + neighbourCost
#             if (neighbour not in costs):
#                 costs[neighbour] = neighbourPathCost
#                 parents[neighbour] = node
#                 unvisited.append(neighbour)
#             elif (neighbourPathCost < costs[neighbour]):
#                 costs[neighbour] = neighbourPathCost
#                 parents[neighbour] = node
        
#         # sort nodes by cost (in reverse as we pop from end)
#         unvisited = sorted(unvisited, key=lambda r: costs[r], reverse=True) 
