from collections import Counter
from pprint import pprint


def parse_input(inputFile):
    with open(inputFile) as f:
        polymer, insertions = f.read().split("\n\n")
        polymer = [c for c in polymer.strip()]

        insertions = dict(tuple(i.split(" -> ")) for i in insertions.split("\n") if i.strip() != "")

    return polymer, insertions


def polymerise(polymer, insertions, passes=40):
    '''
We have two counters, one for characters and one for pairs. 
Process for (e.g.) "NN -> C"
    i.   define x: number of occurences of phrase "NN"
    ii.  increment "NC" occurences by x
    iii. increment "CN" occurences by x
    iv.  decrement "NN" occurences by x
    v.   increment "C" count by x

Note: important to use a copy of counter instead of original as we don't 
want to work on (e.g.) new "NC"/"CN" occurences until next round. 
'''
    charCounts = Counter(polymer)
    pairCounts = Counter()

    position = 0 
    while position < len(polymer) - 1:
        pairCounts["".join(polymer[position:position + 2])] += 1
        position += 1

    for _ in range(passes):
        countCopy = pairCounts.copy()
                                                # Example: 
        for key in pairCounts.keys():           # for key NN
            n = pairCounts[key]                 # number of occurences
            if n > 0:
                v = insertions[key]             # insert: C
                ks = [k for k in key]           # [N, N]
                countCopy[ks[0] + v] += n       # count[NC] += count[NN]
                countCopy[v + ks[1]] += n       # count[CN] += count[NN]
                countCopy[key] -= n             # count[NN] -= count[NN]
                # note: don't set to zero - we could have NN -> N
                charCounts[v] += n              # count[C]  += count[NN]

        pairCounts = countCopy

    print(f"Most common - least common after {passes} passes:", charCounts.most_common()[0][1] - charCounts.most_common()[-1][1])
    return charCounts.most_common()[0][1] - charCounts.most_common()[-1][1]


if __name__ == "__main__":
    print("== Sample ==")
    polymer, insertions = parse_input("sample.txt")
    assert polymerise(polymer, insertions, 10) == 1588
    assert polymerise(polymer, insertions, 40) == 2188189693529

    print("== Input ==")
    polymer, insertions = parse_input("input.txt")
    assert polymerise(polymer, insertions, 10) == 4244
    assert polymerise(polymer, insertions, 40) == 4807056953866

