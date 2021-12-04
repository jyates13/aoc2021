import numpy as np
from pprint import pprint 


class BingoCard: 
    def __init__(self, body):
        self.dims = int(len(body)**0.5)
        self.marked = np.full((self.dims, self.dims), False)
        self.hashes = {}
        self.hashes_done = {}
        for pos, d in enumerate(body):
            row = (pos) % self.dims
            col = pos // self.dims
            self.hashes[d] = (col, row)
        
    def mark_and_check(self, number):
        if number in self.hashes.keys():
            col, row = self.hashes[number]
            self.mark(col, row)
            self.hashes_done[number] = self.hashes[number]
            del self.hashes[number]
            if self.check(col, row):
                return True
        return False

    def mark(self, col, row):
        self.marked[col, row] = True
    
    def check(self, col, row):
        if np.all(self.marked[col,:]):
            return True
        elif np.all(self.marked[:,row]):
            return True
        return False    
    
    def remaining_sum(self):
        return sum(map(int, self.hashes.keys()))

    def __repr__(self):
        return f"BingoCard\n{self.hashes}\n{self.marked}"


def parse_input(inputFile):
    cards = []
    calls = []
    with open(inputFile) as f:
        calls = f.readline().rstrip().split(",")
        card = []
        for line in f.readlines(): 
            try: 
                if line.strip() == "": 
                    if len(card) == 0:
                        continue 
                    # print(card)
                    cards.append(BingoCard(card))
                    card = []
                else:
                    card += line.rstrip().split()
            except ValueError as e: 
                print(f"Error in '{line}'")
        if len(card) > 0:
            cards.append(BingoCard(card))

    return calls, cards


def part1(calls, cards):
    for c in calls:
        print(c)
        for card in cards:
            if card.mark_and_check(c):
                return c, card.remaining_sum()


def part2(calls, cards):
    lastCall, lastCard = 0, 0 
    for c in calls:
        i = 0
        while i < len(cards):
            card = cards[i]
            if card.mark_and_check(c):
                lastCall = c
                lastCard = card.remaining_sum()
                cards.pop(i)
            else:
                i += 1
    
    return lastCall, lastCard


if __name__=="__main__":
    calls, cards = parse_input("sample.txt")
    winning, card = part1(calls, cards)
    print(winning, card)
    calls, cards = parse_input("sample.txt")
    winning, card = part2(calls, cards)
    print(winning, card)

    calls, cards = parse_input("input.txt")
    winning, card = part1(calls, cards)
    print(winning, card)
    calls, cards = parse_input("input.txt")
    winning, card = part2(calls, cards)
    print(winning, card)