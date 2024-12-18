from sys import argv
from dataclasses import dataclass
from typing import List, Dict, Set, Optional

@dataclass
class Coord:
    x: int
    y: int
    
    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: "Coord") -> "Coord":
        return Coord(self.x - other.x, self.y - other.y)
    
    def copy(self) -> "Coord":
        return Coord(self.x, self.y)
    
    def __hash__(self):
        return hash((self.x, self.y))

c1 = Coord(1,1)
c2 = Coord(2,3)
assert c1 + c2 == Coord(3,4)
assert c1 - c2 == Coord(-1, -2) 

class Maze:

    DIRECTIONS: Set[Coord] = {
        Coord(1, 0),  # east
        Coord(0, 1),  # south
        Coord(-1, 0), # west
        Coord(0, -1)  # north
    }

    def __init__(self, size: int) -> None:
        self.walls: Set[Coord] = set()
        self.size = size # the max coord in either axis
        self.end = Coord(size, size)
        self.start = Coord(0,0)
    
    def shortest_path(self) -> Optional[int]:
        # use a simple BFS to find the length of the shortest path
        seen: Dict[Coord, int] = {}
        dist = 1
        frontier: Set[Coord] = set([self.start])
        while True:

            if self.end in seen:
                return seen[self.end]

            new_frontier = set()
            for c in frontier:
                for d in self.DIRECTIONS:
                    new_coord = c + d
                    if all([ # bounds checking, etc
                        new_coord.x <= self.size,
                        new_coord.x >= 0,
                        new_coord.y <= self.size,
                        new_coord.y >= 0,
                        new_coord not in self.walls,
                        new_coord not in seen,
                        new_coord not in frontier,
                    ]):
                        new_frontier.add(new_coord)
            
            for c in new_frontier:
                seen[c] = dist

            if len(new_frontier) == 0:
                return None

            frontier = new_frontier

            dist += 1
                        
def part1(lines: List[str], size: int) -> int:
    m = Maze(size)
    for line in lines[:1024]:
        m.walls.add(Coord(int(line.split(",")[0]), int(line.split(",")[1])))

    return m.shortest_path()

def part2(lines: List[str], size: int):
    # work backwards, since blocked puzzles can be checked much faster.
    for i in range(len(lines),0,-1):
        m = Maze(size)
        for line in lines[:i]:  
            m.walls.add(Coord(int(line.split(",")[0]), int(line.split(",")[1])))

        if m.shortest_path() is not None: # the path is not blocked
            return lines[i]

if __name__ == "__main__":

    INPUTFILE = "input.txt"
    SIZE = 70
    if len(argv) > 1:
        if argv[1] in ("--test", "-t"):
            print("----- TEST MODE -----")
            INPUTFILE = "sample_input.txt"
            SIZE = 6

    with open(INPUTFILE) as ifile:
        lines = ifile.read().splitlines()

    print(f"Part 1: {part1(lines, SIZE)}")
    print(f"Part 2: {part2(lines, SIZE)}")
