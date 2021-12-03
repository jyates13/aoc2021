from collections import Counter
from pprint import pprint


# what a mess...


def parse_input(inputFile):
    output = []
    with open(inputFile) as f:
        for line in f: 
            try: 
                if line.strip() != "": 
                    output.append(line.strip())
            except ValueError as e: 
                print(f"Error in '{line}'")
    
    return output


def bint(b):
    return int(b, base=2)


def part1(values: list):
    out = [Counter() for c in values[0]]
    for v in values: 
        for i, char in enumerate(v):
            out[i].update(char)
    
    mc = []
    lc = []
    for o in out:
        if o.most_common()[0][0] == "1":
            mc += ["1"]
            lc += ["0"]
        else: 
            mc += ["0"]
            lc += ["1"]
    
    mc = "".join(mc)
    lc = "".join(lc)

    print(f"Part 1: {bint(mc):8d} x {bint(lc):8d} = {bint(mc) * bint(lc):8d}")


def filterCommon(values: list, mostCondition: callable, tiebreak: callable):
    for i, _ in enumerate(values[0]):
        count = Counter()
        for v in values: 
            lv = [c for c in v]
            count.update(lv[i])

        pos = 0 
        while pos < len(values):
            if len(values) == 1: 
                return values
            lv = [c for c in values[pos]]
            if not mostCondition(lv[i], count.most_common()[0][0]):
                values.pop(pos)
                continue
            elif count["0"] == count["1"]:
                if not tiebreak(lv[i]):
                    values.pop(pos)
                    continue
            pos += 1; 
    
    return values


def part2(values):
    ox, co2 = values.copy(), values.copy() 
    
    ox  = filterCommon(ox,  lambda x, most: x == most, lambda x: x == "1")
    co2 = filterCommon(co2, lambda x, most: x != most, lambda x: x == "0")

    print(f"Part 2: {bint(ox[0]):8d} x {bint(co2[0]):8d} = {bint(ox[0]) * bint(co2[0]):8d}")


if __name__ == "__main__":
    values = parse_input("sample.txt")
    print(values)
    part1(values)
    part2(values)

    values = parse_input("input.txt")
    part1(values)
    part2(values)
