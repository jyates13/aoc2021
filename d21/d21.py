from functools import lru_cache
from collections import Counter
import numpy as np


def parse_input(filename):
    lines = open(filename).readlines()

    return (int(lines[0].split("starting position: ")[1]), 
            int(lines[1].split("starting position: ")[1]))


class Die:
    # stupid but simple
    def __init__(self, sides):
        self.d = 1
        self.sides = sides
    
    def __call__(self, *args, **kwargs):
        out = 1 + (self.d - 1) % (self.sides) 
        self.d += 1
        return out


def part1(start):
    score = [0, 0]
    pos = list(start)
    player = 0
    rolls = 0
    die = Die(100)
    while max(score) < 1000:
        roll = die() + die() + die()
        rolls += 3
        pos[player] = 1 + (pos[player] + roll - 1) % 10
        score[player] += pos[player]
        player = 0 if player else 1

    result = min(score) * rolls
    print("Part 1:", start, result)
    return result


# Part 2:
# 7 possible rolls: 3 - 9 inclusive
# Remember to add 3 later! 
rolls = [0] * 7
for i in range(0, 3):
    for j in range(0, 3):
        for k in range(0, 3):
            rolls[i + j + k] += 1


@lru_cache(maxsize=None)
def recursive_solve(ipos, jpos, iscore, jscore):
    wins = [0, 0]

    for roll, count in enumerate(rolls): 
        new_pos = ((roll + 3) + ipos - 1) % 10 + 1
        new_score = iscore + new_pos

        if new_score >= 21:
            wins[0] += count
        else: 
            # flip pos/scores -> flip output
            next_wins = recursive_solve(jpos, new_pos, jscore, new_score)
            wins[0] += count * next_wins[1]
            wins[1] += count * next_wins[0]
    
    return wins


def part2(startPositions):
    # takes on the order of 0.2 seconds
    wins = recursive_solve(startPositions[0], startPositions[1], 0, 0)
    print("Part 2:", startPositions, wins)
    return max(wins)


def part2_slow(startPositions):
    # Method: 
    # i.    take a state from stack (actually a Counter)
    # ii.   run turn from state
    # iii.  add wins from state to win count
    # iv.   add all new states to stack
    # 
    # Takes on the order of a minute
    gameStates = Counter()
    player = 0
    wins = [0, 0]
    gameStates[(player, startPositions[0], startPositions[1], 0, 0)] = 1

    # while there are games not yet won
    while gameStates:
        state, stateCount = list(gameStates.items())[0]
        player, ipos, jpos, iscore, jscore = state

        for roll, count in enumerate(rolls): 
            newPos = ((roll + 3) + ipos - 1) % 10 + 1
            newScore = iscore + newPos

            if newScore >= 21:
                wins[player] += count * stateCount
            else: 
                newState = (0 if player else 1, 
                            jpos, newPos, jscore, newScore)
                gameStates[newState] += count * stateCount

        del gameStates[state]

    print("Part 2:", startPositions, wins)
    return max(wins)


if __name__ == "__main__":
    startPositions = parse_input("sample.txt")
    assert part1(startPositions) == 739785
    assert part2(startPositions) == 444356092776315
    # assert part2_slow(startPositions) == 444356092776315

    startPositions = parse_input("input.txt")
    assert part1(startPositions) == 926610
    assert part2(startPositions) == 146854918035875
    # assert part2_slow(startPositions) == 146854918035875

