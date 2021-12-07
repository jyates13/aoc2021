from statistics import median
import functools


def parse_input(inputFile):
    output = []
    with open(inputFile) as f:
        output = [int(i) for i in f.readline().strip().split(",")]
    
    return output


# could do this more cleverly with a Counter or similar... 
# but this is fine
def part1fuel(offset, values):
    return sum([abs(v - offset) for v in values])


# some sort of binary search would probably get this down to log time
# e.g. direction *= 2 each loop until we pass optimum, then binary search
# but this is fine
def optimise(values, fuelcost=part1fuel):
    med = int(median(values))

    fuel = fuelcost(med, values)
    fuelp = fuelcost(med + 1, values)
    fueln = fuelcost(med - 1, values)

    newfuel = 0
    direction = 0 
    if (fuelp < fuel): 
        direction = 1
        newfuel = fuelp
    elif (fueln < fuel):
        direction = -1
        newfuel = fueln
    else: 
        print(med, fuel)
        return
    
    med = med + direction
    while newfuel < fuel:
        fuel = newfuel
        med += direction
        newfuel = fuelcost(med, values)

    # at this point, we've gone 1 past the optimum
    print(med - direction, fuel)


def part1(values):
    optimise(values, part1fuel)


# actually slower with a cache which is maybe not too surpising
# @functools.lru_cache(maxsize=1000) 
def geosum(n):
    na = abs(n)
    return na*(na+1)//2


def part2fuel(offset, values):
    return sum([geosum(v - offset) for v in values])


def part2(values):
    optimise(values, part2fuel)


if __name__ == "__main__":
    values = parse_input("sample.txt")
    print("Sample:") 
    print(values)
    part1(values)
    part2(values)

    values = parse_input("input.txt")
    print("Input:") 
    part1(values)
    part2(values)
