from pprint import pprint
from typing import OrderedDict
from time import time


def parse_input(filename):
    program = [l.split() for l in open(filename).read().split("\n") if l.strip() != ""]
    return program


def op_inp(var, inputs, vars):
    vars[var] = inputs
def op_add(a, b, vars):
    vars[a] += (vars[b] if b in vars else int(b))
def op_mul(a, b, vars):
    vars[a] *= (vars[b] if b in vars else int(b))
def op_div(a, b, vars):
    vars[a] = vars[a]//(vars[b] if b in vars else int(b))
def op_mod(a, b, vars):
    vars[a] = vars[a] % (vars[b] if b in vars else int(b))
def op_eql(a, b, vars):
    vars[a] = 1 if vars[a] == (vars[b] if b in vars else int(b)) else 0


ops = {"inp": op_inp,
       "add": op_add,
       "mul": op_mul,
       "div": op_div,
       "mod": op_mod,
       "eql": op_eql}


def intify(inputs):
    return int("".join(map(str, inputs)))


def part1(program):
    subprograms = []
    subprogram = []
    for p in program: 
        if p[0] == "inp":
            if subprogram: 
                subprograms.append(subprogram)
            subprogram = []
        subprogram.append(p)
    subprograms.append(subprogram)

    vars = (("w", 0),
            ("x", 0),
            ("y", 0),
            ("z", 0))
    nextStates = {0: ([], vars)}

    t0 = time()
    for s, subprogram in enumerate(subprograms):
        states = nextStates
        t = time()
        print(f"Subprograms: {s:2d}", 
              f"States: {len(states):8d}", 
              f"Time: {t-t0:9.2f}")
        nextStates = {}
        v = dict(vars)
        for z, vals in states.items():
            for i in range(9, 0, -1):
                num, state = vals
                n = num + [i]
                v["w"] = 0 
                v["x"] = 0
                v["y"] = 0
                v["z"] = z

                for p in subprogram:
                    if p[0] == "inp":
                        ops["inp"](p[1], i, v)
                    else:
                        ops[p[0]](*p[1:], v)

                nextStates[v["z"]] = (n, v)
    
    num, state = nextStates[0]
    print(state, intify(num))
    
    return intify(num)


if __name__ == "__main__":
    program = parse_input("input.txt")
    part1(program)
