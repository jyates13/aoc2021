from collections import namedtuple
from pprint import pprint
import numpy as np


class BitsCode:
    def __init__(self, line, debug=None):
        self.str_repr = line
        self.code = [int(s, 16) for s in line]
        self.reset()
        self.debug = debug
        self.packetTypeSum = 0
        self.packetVersionSum = 0
        self.callbacks = {
            0: self.sum_cb,
            1: self.product_cb,
            2: self.min_cb,
            3: self.max_cb,
            4: self.literal_cb,
            5: self.gt_cb,
            6: self.lt_cb,
            7: self.eq_cb
        }

    def reset(self):
        self.position = 0
        
    def __repr__(self):
        return f"BitsCode(\"{self.str_repr}\")"

    def take_bits(self, bits=4):
        # This is way overcomplicated but I wanted to use bitwise ops
        # and ints instead of strings.
        #
        # Alternative (simpler) solution to grabbing from self.code
        # might be to store the current char and pull new bits when 
        # it's used up but that's basically the same 
        # 
        # self.position counts in bits but we're accessing a list
        # in chunks of 4
        position = self.position//4
        firstBit = self.position % 4
        
        if len(self.code) < position:
            return IndexError("Not enough bits remaining")

        chunk = 0
        while (bits > 0):
            position = self.position//4
            chunk = chunk << 4
            # Append bits to chunk. If first loop, skip used bits with mask.
            chunk += self.code[position] & (0b1111 >> firstBit)
            # Count bits taken
            move = 4 - firstBit
            bits -= move
            self.position += move
            # From now on we only take full 4 bits
            firstBit = 0

        # If we went too far, lost last bits
        if bits < 0:
            chunk = chunk >> -bits
            self.position += bits

        return chunk
        
    def run(self):
        return self.packet()

    def packet(self):
        pversion = self.take_bits(3)
        ptype    = self.take_bits(3)
        self.packetVersionSum += pversion
        self.packetTypeSum += ptype
        if self.debug: print(f"Packet V{pversion}, T{ptype}")

        if ptype in self.callbacks:
            return self.callbacks[ptype]()
        else: 
            # for part 1 we didn't know the callbacks:
            # return self.operator_cb()
            raise ValueError(f"Unexpected packet type {ptype} at {self.position//4}")

    def literal_cb(self):
        # take 5 bit chunks; while bit 0 is 1, append 4 bit chunks to result
        char = self.take_bits(5)
        number = char & 0b1111
        while (char >> 4):
            number = number << 4
            char = self.take_bits(5)
            number += char & 0b1111
        return number 

    def get_operator_inputs(self):
        # Nothing complicated, just append packet outputs to list of inputs
        lengthType = self.take_bits(1)
        inputs = []

        if lengthType: 
            packets = self.take_bits(11)
            if self.debug: print(f"Running {packets} packets")
            while packets:
                inputs.append(self.packet())
                packets -= 1
        else: 
            bits = self.take_bits(15)
            if self.debug: print(f"Running {bits} bits")
            finalPosition = self.position + bits
            while self.position < finalPosition:
                inputs.append(self.packet())
            assert self.position == finalPosition
        
        return inputs

    def sum_cb(self):
        inputs = self.get_operator_inputs()
        if len(inputs) == 1:
            return inputs[0]
        return np.sum(inputs, dtype=np.int64)
    
    def product_cb(self):
        inputs = self.get_operator_inputs()
        if len(inputs) == 1:
            return inputs[0]
        return np.prod(inputs, dtype=np.int64)
    
    def min_cb(self):
        return np.min(self.get_operator_inputs())
    
    def max_cb(self):
        return np.max(self.get_operator_inputs())

    def gt_cb(self):
        inputs = self.get_operator_inputs()
        return 1 if (inputs[0] > inputs[1]) else 0

    def lt_cb(self):
        inputs = self.get_operator_inputs()
        return 1 if (inputs[0] < inputs[1]) else 0
    
    def eq_cb(self):
        inputs = self.get_operator_inputs()
        return 1 if (inputs[0] == inputs[1]) else 0



        
def parse_input(inputFile, debug=False):
    with open(inputFile) as f:
        return [BitsCode(line.strip(), debug=debug) for line in f if line.strip() != ""]


def run_all(init):
    for b in init:
        b.reset()
        out = b.run()
        print(b)
        print("  Version sum:\t", b.packetVersionSum)
        print("  Type sum:   \t", b.packetTypeSum)
        print("  Output:     \t", out)


# def part2(init):
#     for b in init:
#         b.reset()
#         out = b.run()
#         print(b, "\t\t\t", "Result:", out)
#     return out


if __name__=="__main__":
    # Debugging the take_bits function:
    # 110100101111111000101000
    # VVVTTTAAAAABBBBBCCCCC
    b = BitsCode("D2FE28", debug=True)
    assert b.take_bits(bits=3) == 0b110
    assert b.take_bits(bits=3) == 0b100
    assert b.take_bits(bits=5) == 0b10111
    assert b.take_bits(bits=5) == 0b11110
    assert b.take_bits(bits=5) == 0b00101

    b.reset()
    assert b.run() == 2021

    ''' Sample:
    C200B40A82 finds the sum of 1 and 2, resulting in the value 3.
    04005AC33890 finds the product of 6 and 9, resulting in the value 54.
    880086C3E88112 finds the minimum of 7, 8, and 9, resulting in the value 7.
    CE00C43D881120 finds the maximum of 7, 8, and 9, resulting in the value 9.
    D8005AC2A8F0 produces 1, because 5 is less than 15.
    F600BC2D8F produces 0, because 5 is not greater than 15.
    9C005AC2F8F0 produces 0, because 5 is not equal to 15.
    9C0141080250320F1802104A08 produces 1, because 1 + 3 = 2 * 2.
    '''
    init = parse_input("sample.txt")
    run_all(init)

    init = parse_input("input.txt")
    run_all(init)
