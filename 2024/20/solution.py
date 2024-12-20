from sys import argv
from dataclasses import dataclass
from typing import List, Set, Optional

@dataclass
class Coord:
    x: int
    y: int
    
    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: "Coord") -> "Coord":
        return Coord(self.x - other.x, self.y - other.y)
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def distance(self, other: "Coord") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

c1 = Coord(1,1)
c2 = Coord(2,3)
assert c1 + c2 == Coord(3,4)
assert c1 - c2 == Coord(-1, -2) 
assert c1.distance(c2) == c2.distance(c1) == 3 

class Maze:

    DIRECTIONS: Set[Coord] = {
        Coord(1, 0),  # east
        Coord(0, 1),  # south
        Coord(-1, 0), # west
        Coord(0, -1)  # north
    }

    def __init__(self, lines: List[str]) -> None:
        self.walls: Set[Coord] = set()
        self.size: int = 0 # the max coord in either axis
        self.end: Coord = None
        self.start: Coord = None

        assert len(lines) == len(lines[0]) # double-check that the maze is square
        self.size = len(lines)

        for y in range(len(lines)):
            for x in range(len(lines[y])):
                if lines[y][x] == "#":
                    self.walls.add(Coord(x,y))
                elif lines[y][x] == "S":
                    self.start = Coord(x,y)
                elif lines[y][x] == "E":
                    self.end = Coord(x,y)

        # how far is each tile from the start?
        # this can be used to measure the value of a given shortcut,
        # based on the delta of the distance of the two tiles
        self.distances = {self.start: 0}

    
    def solve(self) -> Optional[int]:
        # use a simple BFS to mark the "cost to finish" from every tile
        t = 1 # current time in picoseconds
        frontier: Set[Coord] = set([self.start])
        while True:

            if self.end in self.distances:
                break

            new_frontier = set()
            for c in frontier:
                for d in self.DIRECTIONS:
                    new_coord = c + d
                    if all([ # bounds checking, etc
                        new_coord.x < self.size,
                        new_coord.x >= 0,
                        new_coord.y < self.size,
                        new_coord.y >= 0,
                        new_coord not in self.walls,
                        new_coord not in self.distances,
                    ]):
                        new_frontier.add(new_coord)
            
            for c in new_frontier:
                self.distances[c] = t

            frontier = new_frontier

            t += 1
                        
def part1(maze: Maze) -> int:
    total = 0
    for c1 in maze.distances:
        for c2 in maze.distances:
            if c1.distance(c2) == 2:
                # how much time did we save by cheating?
                delta = (maze.distances[c1] - maze.distances[c2]) - 2
                if delta >= 100:
                    total += 1

    return total

def part2(maze: Maze) -> int:
    total = 0
    for c1 in maze.distances:
        for c2 in maze.distances:
            if c1.distance(c2) <= 20:
                # how much time did we save by cheating?
                delta = (maze.distances[c1] - maze.distances[c2]) - c1.distance(c2)
                if delta >= 100:
                    total += 1

    return total

if __name__ == "__main__":

    INPUTFILE = "input.txt"
    if len(argv) > 1:
        if argv[1] in ("--test", "-t"):
            print("----- TEST MODE -----")
            INPUTFILE = "sample_input.txt"

    with open(INPUTFILE) as ifile:
        lines = ifile.read().splitlines()

    maze = Maze(lines)
    maze.solve()

    print(f"Part 1: {part1(maze)}")
    print(f"Part 2: {part2(maze)}")
