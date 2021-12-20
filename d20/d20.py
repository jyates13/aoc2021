import numpy as np
from pprint import pprint 
import matplotlib.pyplot as plt


def parse_input(filename):
    algo, image = open(filename).read().split("\n\n")
    algo  = [1 if c == "#" else 0 for c in algo]
    image = np.array([[1 if c == "#" else 0 for c in line] \
             for line in image.split("\n") if line.strip() != ""], dtype=int)
    image = pad_array(image)
    image = pad_array(image)
    return algo, image


def get_convolved(array, j, i):
    bits = array[j-1:j+2,i-1:i+2].flatten()
    out = 0
    for b in bits: 
        out = (out << 1) | b
    return out


def pad_array(array, unseen_value=0):
    output = np.full([s + 2 for s in array.shape], unseen_value, dtype=int)
    output[1:-1,1:-1] = array[:,:]
    return output 


def step(algo, image, unseen_value=0, plot=False):
    image = pad_array(image, unseen_value)
    out = image.copy()
    sj, si = image.shape
    for j in range(1, sj - 1):
        for i in range(1, si - 1):
            out[j,i] = algo[get_convolved(image, j, i)]
    
    new_unseen = algo[get_convolved(np.full((3,3), unseen_value), 1, 1)]
    out[0] = new_unseen
    out[-1] = new_unseen
    out[:,0] = new_unseen
    out[:,-1] = new_unseen

    if plot:
        plt.imshow(out)
        plt.show()
    return out, new_unseen


def solve(algo, image, steps, plot=False):
    unseen = 0

    while (steps):
        image, unseen = step(algo, image, unseen_value=unseen, plot=(plot or steps==1))
        steps -= 1
    print("Sum:", np.sum(image))
    
    return np.sum(image)


if __name__=="__main__":
    algo, image = parse_input("sample.txt")
    assert solve(algo, image.copy(), 2) == 35
    assert solve(algo, image.copy(), 50) == 3351

    algo, image = parse_input("input.txt")
    assert solve(algo, image.copy(), 2) == 4928
    assert solve(algo, image.copy(), 50) == 16605

