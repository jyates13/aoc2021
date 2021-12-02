#! /usr/bin/env python 

class Submarine:
    def __init__(self):
        self.depth = 0
        self.horizontal = 0 
        self.aim = 0
        self.commands = {
            "up": self.up,
            "down": self.down,
            "forward": self.forward
        }

    def command(self, command, arg):
        return self.commands[command](arg)
    
    def forward(self, arg):
        self.horizontal += int(arg)
        self.depth += self.aim * int(arg)

    def up(self, arg):
        # self.depth -= int(arg)
        self.aim -= int(arg)

    def down(self, arg):
        # self.depth += int(arg)
        self.aim += int(arg)

    def report(self):
        print(f"Sub at d{self.depth}, h{self.horizontal}, aim {self.aim}")

def run(commands): 
    sub = Submarine()
    for c in commands:
        sub.command(*c)
        # sub.report()

    print(f"Sub ends at d{sub.depth}, h{sub.horizontal}")
    print(f"Answer {sub.depth * sub.horizontal}")
    

def part2(commands):
    pass

def parse_input(inputFile):
    commands = []
    with open(inputFile) as f:
        for line in f: 
            try: 
                if line.strip() != "": 
                    commands.append(line.split())
            except ValueError as e: 
                print(f"Error in '{line}'")
    
    return commands


if __name__ == "__main__":
    commands = parse_input("sample.txt")
    run(commands)

    commands = parse_input("input.txt")
    run(commands)
