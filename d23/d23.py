import heapq
from functools import cache, lru_cache
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
    # corridor
    c = [s if s is not None else "." for s in state[:7]]
    string = ['#############\n']
    string.append('#{}{}.{}.{}.{}.{}{}#\n'.format(*c))

    # rooms
    rs = [[a if a is not None else "." for a in r] for r in state[7:]]
    string.append('###{}#{}#{}#{}###\n'.format(
                            *[r[0] for r in rs]))

    for i in range(1, len(state[7])):
        string.append('  #{}#{}#{}#{}#\n'.format(
                            *[r[i] for r in rs]))

    string.append("  #########")
    return "".join(string)


def parse_input(filename, part2=False):
    return parse_input_2(open(filename).read(), part2)


def parse_input_2(text, part2=False):
    amphs = re.findall("[.A-Z]", text)
    state = [amphs[0]] + amphs[1:10:2] + [amphs[10]]
    state = [None if s == "." else s for s in state]
    rooms = [[], [], [], []]
    loc = 11
    while loc < len(amphs): 
        rooms[(loc - 11) % 4].append(None if amphs[loc] == "." else amphs[loc])
        loc += 1
    for i in range(len(rooms)):
        if part2:
            rooms[i] = [rooms[i][0]] + part2add[i] + rooms[i][1:]
    state.extend(rooms)
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
part2win = hash_amph(part2winState)


goals = OrderedDict({"A": 0, "B": 1, "C": 2, "D": 3})
costAmph = {"A": 1, "B": 10, "C": 100, "D": 1000}


def win(state):
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

    if isinstance(location, int):
        # we're in a corridor
        if isinstance(to, int):
            # going along corridor
            cost += 2 * abs(to - location)
            if location == 0 or location == 6: 
                cost -= 1
            if to == 0 or to == 6: 
                cost -= 1

        else: 
            # we going into a room
            room, depth = to

            if (location != room + 1) and (location != room + 2):
                # move to entrance
                a = move_cost(location, room + 1)
                b = move_cost(location, room + 2)
                cost += a if a < b else b
                location = room + 1 if a < b else room + 2
            
            # we're at the entrance
            cost += 2 + depth

    else: 
        # we're in a room 
        # just cheat and reverse the call
        room, depth = location
        a = move_cost(room + 1, location) + move_cost(room + 1, to)
        b = move_cost(room + 2, location) + move_cost(room + 2, to)
        cost += a if a < b else b
    
    return cost


def check_move(state, location, to, flip_destination=False):
    # note: we should only use this for corridor to room and vice versa
    # not for corridor to corridor

    if isinstance(location, int):
        # just reverse the call
        return check_move(state, to, location, True)
    else: 
        room, depth = location

        # if destination is not empty don't bother!
        if flip_destination:
            if state[room + 7][depth] is not None: 
                return False
        else:     
            if state[to] is not None: 
                return False
        # the destination is empty

        while depth > 0: 
            depth -= 1
            if state[room + 7][depth] is not None:
                return False
        # the room is clear
        
        entrances = (room + 1, room + 2)

        # which entrance is closer?
        if to > entrances[1]:
            start = entrances[1]
            end = to
        elif to < entrances[0]:
            start = to
            end = entrances[0]
        else: 
            # to is an entrance and we already know it's empty
            start = to
            end = to 

        # check corridor spaces
        for k in range(start, end + 1):
            if k == to:
                continue
            if state[k] is not None: 
                return False

        return True

def possible_moves(state):
    moves = []

    for i, c in enumerate(state[0:7]): 
        if c is None:
            continue
        else: 
            # we've found a guy in the corridor - move to room?
            goal = goals[c]
            room = state[7 + goal]
            top = 0
            found = False
            for a in room: 
                # how full is the room?
                if a is None and not found: 
                    top += 1
                if a is not None: 
                    found = True
                if not ((a == c) or (a is None)):
                    # if there's a non-matching guy in there, don't block him in 
                    break 
            else: 
                # we can try to move into the room 
                top -= 1
                if not check_move(state, i, (goal, top)):
                    # path is blocked
                    continue

                # set up new state
                cost = costAmph[c] * move_cost(i, (goal, top))
                corr = list(state[:7])
                corr[i] = None
                room = list(state[7 + goal])
                room[top] = c
                move = corr
                for j, r in enumerate(state[7:]): 
                    if goal == j: 
                        move.append(tuple(room))
                    else: 
                        move.append(r)
                move = tuple(move)
                moves.append([cost, move])

    for i, r in enumerate(state[7:]): 
        depth = 0 
        # find the top guy in the room
        for j, a in enumerate(r): 
            if a is None:
                depth += 1
                continue
            else: 
                skip = True
                # if the room is already good, don't move anyone out
                correct = list(goals.keys())[i]
                for k in range(j, len(r)):
                    if r[k] != correct:
                        # there's (e.g.) a B in an A room so we need to move top guy 
                        skip = False
                        break
                if skip: 
                    break
 
                # check all corridor spots
                for k in range(7):
                    if not check_move(state, (i, depth), k):
                        # path is blocked
                        continue

                    # set up new state
                    cost = costAmph[a] * move_cost((i, depth), k)
                    corr = list(state[:7])
                    corr[k] = a
                    room = list(state[7 + i])
                    room[depth] = None
                    move = corr
                    for l, r in enumerate(state[7:]): 
                        if i == l: 
                            move.append(tuple(room))
                        else: 
                            move.append(r)
                    move = tuple(move)
                    moves.append([cost, move])
                
                # only first guy in the room can move so break
                break 
    
    return moves


def astar_heuristic(state):
    cost = 0
    for i, c in enumerate(state[0:7]): 
        # for each corridor guy, cost to get to room
        if c is not None:
            cost += costAmph[c] * move_cost(i, (goals[c], 0))
    
    for i, r in enumerate(state[7:]): 
        for j, a in enumerate(r): 
            # for each room guy, cost to get to right room
            if a is not None: 
                if i == goals[a]:
                    # already in the right place
                    continue
                cost += costAmph[a] * move_cost((i, j), (goals[a], 0))

    return cost


def solve_astar(state):
    visited = set()
    stack = []

    count = 0
    heapq.heappush(stack, [0, 0, 0, state])

    done = False
    while stack: 
        _, cost, _, state = heapq.heappop(stack)
        visited.add(state)

        if not count % 10000: 
            print(f"Checking move {count:8d}, cost {cost:5d}...")

        if win(state): 
            break

        for mc, m in possible_moves(state):
            if m in visited: 
                continue
            else: 
                count += 1
                c = mc + cost
                h = c + astar_heuristic(m)
                heapq.heappush(stack, [h, c, count, m])

    print("Cost:", cost)

    return cost


@cache
def solve(state, p=False):
    if p:
        print(print_state(state))

    cost = None
    if win(state): 
        return 0
    
    for c, m in possible_moves(state):
        x = solve(m)
        if x is None: 
            continue
        endcost = c + x
        if (cost is None) or (endcost < cost):
            cost = endcost 
    return cost


if __name__=="__main__":
    state = parse_input("sample.txt")
    print(print_state(state))
    # cost = solve(state)
    cost = solve_astar(state)
    assert cost == 12521
    print(cost)
    

    state = parse_input("sample.txt", part2=True)
    print(print_state(state))
    cost = solve(state)
    assert cost == 44169
    print(cost)


    state = parse_input("input.txt")
    print(print_state(state))
    # cost = solve(state)
    cost = solve_astar(state)
    assert cost == 19167
    print(cost)

    state = parse_input("input.txt", part2=True)
    print(print_state(state))
    cost = solve(state)
    assert cost == 47665
    print(cost)

