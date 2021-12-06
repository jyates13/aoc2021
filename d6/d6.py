from pprint import pprint 

def parse_input(inputFile):
    with open(inputFile) as f:
        return list(map(int, f.readline().strip().split(",")))


class Fish:
    def __init__(self, initialFish, reprod = 7, mature = 2):
        self.reprod = reprod
        self.mature = mature
        self.fish = [0] * (self.reprod + self.mature)
        self.time = 0
        for f in initialFish:
            self.fish[f] += 1
    
    def step(self, printout=False):
        newFish = self.fish[0]
        self.fish[0:-1] = self.fish[1:]
        self.fish[-1] = newFish 
        self.fish[self.reprod - 1] += newFish
        self.time += 1
        if printout: 
            pprint(self.fish)
    
    def stepN(self, n, printout=False):
        for _ in range(n):
            self.step(printout)
    
    def print(self):
        print(f"Fish: time {self.time}, count {sum(self.fish)}")


def part1(initialFish):
    fish = Fish(initialFish)
    fish.stepN(80)
    fish.print()


def part2(initialFish):
    fish = Fish(initialFish)
    fish.stepN(256)
    fish.print()


def verif():
    from collections import Counter
    with open("verif.txt") as f:
        for line in f:
            c = Counter(line.strip().split(","))
            for i in range(9):
                print(c[str(i)], end=" ")
            print("")

if __name__=="__main__":
    init = parse_input("sample.txt")
    verif()
    fish = Fish(init)
    fish.stepN(18, printout=True)
    fish.print()
    fish.stepN(62)
    fish.print()
    fish.stepN(176)
    fish.print()

    init = parse_input("input.txt")
    part1(init)
    part2(init)
