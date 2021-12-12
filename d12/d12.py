from pprint import pprint
from collections import namedtuple


class Node:
    def __init__(self, name, revisitable):
        self.name = name
        self.revisitable = revisitable
        self.connections = []

    def add_edge(self, destination):
        self.connections.append(destination)
        destination.connections.append(self)

    def __repr__(self):
        return f"Node({self.name}, {[c.name for c in self.connections]})"


def parse_input(filename):
    nodes = {}
    with open(filename) as f: 
        for line in f:
            first, second = line.strip().split("-")
            if not first in nodes:
                nodes[first] = Node(first, first.isupper())
            if not second in nodes:
                nodes[second] = Node(second, second.isupper())
            nodes[first].add_edge(nodes[second])
    return nodes


def part1(graph):
    completePaths = []
    currentNode = nodes["start"]
    path = [currentNode]
    stack = [path]

    while stack:
        path = stack.pop()
        currentNode = path[-1]
        if currentNode.name == "end":
            completePaths.append(path)
            continue
        for node in currentNode.connections:
            if (not node in path) or (node.revisitable):
                stack.append(path + [node])
    
    print("Part 1 paths: ", len(completePaths))
    return len(completePaths), completePaths


part2tuple = namedtuple("part2", ["path", "visitedTwice"])


def part2(graph):
    completePaths = []
    currentNode = nodes["start"]
    path = [currentNode]
    stack = [part2tuple(path, False)]

    while stack:
        path, visitedTwice = stack.pop()
        currentNode = path[-1]
        if currentNode.name == "end":
            completePaths.append(path)
            continue
        for node in currentNode.connections:
            if (node.revisitable) or (not node in path):
                stack.append(part2tuple(path + [node], visitedTwice))
            elif ((node in path) and (not visitedTwice) and (node.name != "start")):
                stack.append(part2tuple(path + [node], True))
    
    print("Part 2 paths: ", len(completePaths))
    return len(completePaths), completePaths


if __name__ == "__main__":
    nodes = parse_input("sample1.txt")
    pprint(nodes)
    count, paths = part1(nodes)
    pprint([[n.name for n in path] for path in paths])
    assert count == 10
    count, paths = part2(nodes)
    pprint([[n.name for n in path] for path in paths])
    assert count == 36

    nodes = parse_input("sample2.txt")
    count, paths = part1(nodes)
    assert count == 19
    count, paths = part2(nodes)
    assert count == 103

    nodes = parse_input("sample3.txt")
    count, paths = part1(nodes)
    assert count == 226
    count, paths = part2(nodes)
    assert count == 3509

    nodes = parse_input("input.txt")
    count, paths = part1(nodes)
    assert count == 4707
    count, paths = part2(nodes)
    assert count == 130493

