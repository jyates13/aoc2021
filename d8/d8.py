from collections import defaultdict
from pprint import pprint 

def parse_input(inputFile):
    with open(inputFile) as f:
        return [[s.split() for s in line.strip().split("|")] for line in f if line.strip() != ""]


def part1(init):
    count = 0 
    for i in init:
        uniq, output = i
        for j in output:
            if (len(j) == 2) or (len(j) == 3) or (len(j) == 4) or (len(j) == 7):
                count += 1
    print(count)






def setsum(sl):
    out = set()
    for s in sl:
        out = out | s
    return frozenset(out)


def part2solver(uniq, output):
    '''Solver for individual line in part2.

Segment counts per number: 
      number:    0 1 2 3 4 5 6 7 8 9
      segments:  6 2 5 5 4 5 6 3 7 6
Inversed:
      2 segments: 1
      3 segments: 7
      4 segments: 4
      5 segments: 2 3 5
      6 segments: 0 6 9
      7 segments: 8

Use sets of segments 
ie. 9 - 4 means set of segments in 9 minus set of segments in 4
Algorithm:
  i.   7 and 1 are known and share cf -> deduce a from 7 - 1
  ii.  9 contains all of 4 and 4 has no a -> deduce g from 9 - 4 - {a}
  iii. deduce e from 8 - 9
  iv.  of 6 seg numbers, 0 contains 1, 6 does not contain 1, 9 is known
       -> deduce c, d
  v.   deduce b, f
Reverse number to set mapping to get set to number mapping.
Solve output number using map.'''

    # accrue sets based on segment counts
    lengths = defaultdict(list)
    for i in uniq:
        l = len(i)
        lengths[l].append(frozenset(i))

    # some numbers are already known
    keys = {
        1: lengths[2][0],
        4: lengths[4][0],
        7: lengths[3][0],
        8: lengths[7][0]
    }

    # map randomised segments labels to true segments
    mapping = {}
    mapping["a"] = keys[7] - keys[1]
    
    for s in lengths[6]:
        if keys[4] < s:
            keys[9] = s
            mapping["e"] = keys[8] - keys[9]
            mapping["g"] = keys[9] - keys[4] - mapping["a"]

    for s in lengths[6]:
        if (s != keys[9]):
            if (not s > keys[1]): 
                keys[6] = s 
            else: 
                keys[0] = s
                mapping["d"] = keys[4] - s 

    mapping["c"] = keys[4] - keys[6]
    mapping["f"] = keys[6] & keys[1]
    mapping["b"] = keys[8] - setsum(mapping.values())

    keys[2] = setsum([mapping[i] for i in "acdeg"])
    keys[3] = setsum([mapping[i] for i in "acdfg"])
    keys[5] = setsum([mapping[i] for i in "abdfg"])

    reverseKeys = {}
    for k, v in keys.items():
        reverseKeys[v] = k

    out = 0
    for i, s in enumerate(output): 
        out += reverseKeys[frozenset(s)] * 10**(len(output) - 1 - i)
    
    return out

def part2(init):
    out = 0
    for i in init:
        out += part2solver(*i)
    print(out)


if __name__=="__main__":
    init = parse_input("sample.txt")
    pprint(init)
    part1(init)
    part2(init)

    init = parse_input("input.txt")
    part1(init)
    part2(init)
