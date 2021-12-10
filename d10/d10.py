from collections import namedtuple
from pprint import pprint


'''
Why on Earth did I do it like this, you ask? Might be a bit premature but this seems like Intcode (Bracket Edition)
so anticipating (re-)using it a lot for more complicated stuff later. 
'''


class BracketCodeStatus:
    def __init__(self):
        self.error = False      # is there an error? 
        self.callstack = []     # what were we doing? 
        self.output = None      # what is the output? 

    def __repr__(self):
        return f"BracketCodeStatus(error={self.error}, callstack=\"{self.callstack}\", output=\"{self.output}\")"


class BracketCode:
    def __init__(self, line):
        self.code = [s for s in line]
        self.reset()
        self.callbacks = {}

        # add callbacks
        self.matchFunctionFactory("(", ")")
        self.matchFunctionFactory("[", "]")
        self.matchFunctionFactory("{", "}")
        self.matchFunctionFactory("<", ">")

    def reset(self):
        self.position = 0
        self.status = BracketCodeStatus()

    def current(self):
        return self.code[self.position]

    def run(self):
        while (not self.status.error) and (self.current() != "\n"):
            self.next()         # runs one chunk to completion (or error)
            self.position += 1  # so we need to move to next character when complete
        return self.status

    def next(self):
        c = self.current()
        if c in self.callbacks.keys():
            self.callbacks[c]() # call the function associated with character
        else:
            # unexpected character
            self.status.error = True
            self.status.output = c
        return self.status

    def matchFunctionFactory(self, begin, end):
        def matchFunction():
            self.status.callstack.append(begin)
            while True:
                self.position += 1

                if self.current() == end:
                    # if we find match, return 
                    self.status.error = False
                    self.status.callstack.pop()
                    # presumably we'll add some output at a later stage...
                    self.status.output = None
                    return self.status
                else:
                    # else recurse on the next function call
                    self.next()
                    if self.status.error:
                        return self.status 

        # put it in the callback dictionary
        self.callbacks[begin] = matchFunction

    def __repr__(self):
        return f"BracketCode(\"{''.join(self.code).strip()}\")"


def parse_input(inputFile):
    with open(inputFile) as f:
        return [BracketCode(line) for line in f if line.strip() != ""]


part1scores = {")": 3, "]": 57, "}": 1197, ">": 25137}


def part1(init):
    errors = 0
    for program in init:
        status = program.run() 
        if (status.error) and (status.output != "\n"):
            errors += part1scores[status.output]
    print(errors)
    return errors


pairs       = {"(": ")", "[": "]", "{": "}", "<": ">"}
part2scores = {"(": 1,   "[": 2,   "{": 3,   "<": 4}


def part2(init):
    fixScores = []
    for i, program in enumerate(init):
        score = 0
        program.reset()
        status = program.run()

        # if it terminates early on a newline.. 
        if (status.error) and (status.output == "\n"):
            # take the call stack and put each matching character on the end 
            while status.callstack:
                c = status.callstack.pop()
                program.code.insert(len(program.code) - 2, pairs[c])
                score = score * 5 + part2scores[c]

            fixScores.append(score)

    output = sorted(fixScores)[len(fixScores)//2]
    print(output)
    return output


if __name__=="__main__":
    init = parse_input("sample.txt")
    assert part1(init) == 26397
    assert part2(init) == 288957

    init = parse_input("input.txt")
    assert part1(init) == 323613
    assert part2(init) == 3103006161