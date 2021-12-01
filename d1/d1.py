#! /usr/bin/env python 

def part1(depths): 
    increases = 0 
    for i in range(1, len(depths)): 
        if depths[i] > depths[i-1]:
            increases += 1

    return increases

def part2(depths, window):
    increases = 0
    for i in range(window, len(depths)):
        # needless repetetion of work... but doesn't really matter for an easy problem
        if sum(depths[i-window+1:i+1]) > sum(depths[i-window:i]):
            increases += 1
    
    return increases


if __name__ == "__main__":
    depths = []
    with open("input.txt") as f:
        for line in f: 
            try: 
                depths.append(int(line.strip()))
            except ValueError as e: 
                # blank line, ignore 
                pass
    
    print(f"{len(depths)}: {depths}") 
    
    print(part1(depths))
    
    assert(part2(depths, 1) == part1(depths))
    print(part2(depths, 3))
