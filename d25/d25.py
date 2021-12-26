import numpy as np


def parse_input(filename):
    out = []
    for line in open(filename).readlines():
        if line.strip() != "":
            out.append([c for c in line.strip()])
    return np.array(out)


def prints(arr):
    for line in arr:
        print("".join(line))


def step(arr):
    dimsa, dimsb = arr.shape
    out = arr.copy()
    
    for y in range(dimsa):
        for x in range(dimsb):
            if arr[y,x] == ">":
                xn = (x + 1) % dimsb
                if arr[y,xn] == ".":
                    out[y,x]  = "."
                    out[y,xn] = ">"
    arr[:,:] = out[:,:]

    for y in range(dimsa):
        for x in range(dimsb):
            if arr[y,x] == "v":
                yn = (y + 1) % dimsa
                if arr[yn,x] == ".":
                    out[y,x]  = "."
                    out[yn,x] = "v"
    arr[:,:] = out[:,:]

    return arr

def part1(arr):
    steps = 1
    arr_p = arr.copy()
    
    while np.any(step(arr) != arr_p):
        steps += 1
        arr_p[:,:] = arr[:,:]

    print("Steps:", steps)
    return steps


if __name__ == "__main__":
    init = parse_input("sample.txt")
    prints(init)
    assert part1(init) == 58

    init = parse_input("input.txt")
    prints(init)
    assert part1(init) == 432

