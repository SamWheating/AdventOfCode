# This is the boilerplate I usually start with
from sys import argv
from typing import List
import math

class Coord:
    # helper class for vectors / coords.
    def __init__(self, y: int, x: int):
        self.y = y
        self.x = x

    def __add__(self, other):
        return Coord(self.y + other.y, self.x + other.x)

    def __sub__(self, other):
        return Coord(self.y - other.y, self.x - other.x)
    
    def __repr__(self) -> str:
        return f"({self.y}, {self.x})"
    
    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y
    
    def __mul__(self, scalar: int):
        return Coord(self.y * scalar, self.x * scalar)
    
    def __hash__(self) -> str:
        return hash((self.y, self.x))
    
    def reduced(self) -> 'Coord':
        gcd = math.gcd(self.y, self.x)
        return Coord(self.y // gcd, self.x // gcd)
    
c = Coord(2,3)*2
assert c.y == 4 and c.x == 6
assert c.reduced() == Coord(2,3)

def find_antinode_pairs(nodes: List[Coord], max_y: int, max_x: int) -> List[Coord]:

    antinodes = set()
    for node in nodes:
        for other in nodes:
            if node == other:
                continue
            delta = node - other
            antinodes.add(node + delta)
            antinodes.add(node - delta - delta)

    # filter out out-of-bounds nodes:
    antinodes = {a for a in antinodes if a.y >= 0 and a.y < max_y and a.x >= 0 and a.x < max_x}

    return antinodes

assert find_antinode_pairs([Coord(1,0), Coord(2,0)],4,4) == {Coord(0,0), Coord(3,0)}
assert find_antinode_pairs([Coord(1,1), Coord(2,2)],2,2) == {Coord(0,0),}
assert find_antinode_pairs([Coord(1,1), Coord(2,2), Coord(3,3)],5,5) == {Coord(0,0), Coord(1,1), Coord(3,3), Coord(4,4)}

def find_antinode_lines(nodes: List[Coord], max_y: int, max_x: int) -> List[Coord]:

    antinodes = set()
    for node in nodes:
        for other in nodes:
            if node == other:
                continue
            
            delta = (node - other).reduced()
            for direction in (-1, 1):
                dist = 0
                while True:
                    a = node + delta*direction*dist
                    if a.y < 0 or a.y >= max_y or a.x < 0 or a.x >= max_x:
                        break
                    antinodes.add(a)
                    dist += 1

    return antinodes

assert find_antinode_lines([Coord(0,0), Coord(1,1)],4,4) == {Coord(0,0), Coord(1,1), Coord(2,2), Coord(3,3)}

def total_antinodes(map: List[str], find_antinodes_fn: callable) -> int:

    antinodes = []

    # find the unique "frequencies" of antinodes to inspect
    chars = set("".join(lines))
    chars.remove(".")
    
    for c in chars:
        coords = []
        for y in range(len(lines)):
            for x in range(len(lines[0])):
                if lines[y][x] == c:
                    coords.append(Coord(y,x))

        if len(coords) > 1:
            antinodes.extend(find_antinodes_fn(coords, len(lines), len(lines[0])))

    return len(set(antinodes))

if __name__ == "__main__":

    INPUTFILE = "input.txt"
    if len(argv) > 1:
        if argv[1] in ("--test", "-t"):
            print("----- TEST MODE -----")
            INPUTFILE = "sample_input.txt"

    with open(INPUTFILE) as ifile:
        line = ifile.read()
        lines = line.splitlines()

    print(f"Part 1: {total_antinodes(lines, find_antinode_pairs)}")
    print(f"Part 2: {total_antinodes(lines, find_antinode_lines)}")
