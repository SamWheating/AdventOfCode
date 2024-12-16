from sys import argv
from dataclasses import dataclass
from typing import List, Dict, Set, Tuple

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

    DIRECTIONS = {
        0: Coord(1, 0), # east
        1: Coord(0, 1), # south
        2: Coord(-1, 0), # west
        3: Coord(0, -1) # north
    }

    def __init__(self, lines: List[str]) -> None:

        self.costs: Dict[Coord: Dict[int, int]] = {}
        self.walls: Set[Coord] = set()
        self.end: Coord = None

        for y in range(len(lines)):
            for x in range(len(lines[y])):
                if lines[y][x] == "#":
                    self.walls.add(Coord(x,y))
                elif lines[y][x] in {".", "S", "E"}: # start, end
                    self.costs[Coord(x,y)] = {d: 10**10 for d in self.DIRECTIONS}
                if lines[y][x] == "S":
                    self.costs[Coord(x,y)][0] = 0 # starting on start facing east
                if lines[y][x] == "E":
                    self.end = Coord(x,y)
                if lines[y][x] == "S":
                    self.start = Coord(x,y)

    def step(self):
        # update every coord + direction combo with the lowest cost of getting there
        # for each tile+direction combination there are 3 ways to get there:
        # 1) walk from adjacent tile travelling in the same direction
        # 2) turn counterclockwise
        # 3) turn clockwise
        #
        # for each tile + direction, we can evaluate all 3 options and see if any is
        # less expensive than the currently lowest known cost.
        # if so, replace the cost with the new lowest cost.
        for c in self.costs:
            for d in self.DIRECTIONS:
                options = [self.costs[c][d],]
                
                if c - self.DIRECTIONS[d] in self.costs:
                    options.append(self.costs[c - self.DIRECTIONS[d]][d] + 1)
                
                options.append(self.costs[c][(d+1)%4] + 1000) # turn CW
                options.append(self.costs[c][(d-1)%4] + 1000) # turn CCW
                
                self.costs[c][d] = min(options)

    def solve(self) -> None:
        # repeatedly optimize the maze until the lowest cost has been found
        # for all combinations of tile + direction
        seen: Set[int] = set()
        while True:
            self.step()
            step_hash = hash(str(self.costs))
            if step_hash in seen: # the system has stabilized
                return
            seen.add(step_hash)

    @property
    def best_paths(self) -> set[Coord]:
        best_paths: Set[Coord] = set([self.end],)
        end_dir = min(self.costs[self.end].keys(), key=lambda d: self.costs[self.end][d])
        frontier: Set[Tuple[Coord, int]] = {(self.end, end_dir)}
        while True:
            new_frontier: Set[Tuple[Coord, int]] = set()
            for c, dir in frontier:
                cost = self.costs[c][dir] # how did we get to this state/cost?
                if self.costs[c][(dir+1)%4] == cost-1000:
                    new_frontier.add((c,(dir+1)%4))
                if self.costs[c][(dir-1)%4] == cost-1000:
                    new_frontier.add((c,(dir-1)%4))
                if c - self.DIRECTIONS[dir] in self.costs:
                    if self.costs[c - self.DIRECTIONS[dir]][dir] == cost - 1:
                        new_frontier.add((c - self.DIRECTIONS[dir], dir))
            
            if len(new_frontier) == 0:
                break

            for c, _ in new_frontier:
                best_paths.add(c)
            
            frontier = new_frontier    

        return best_paths


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
    print(f"Part 1: {min(maze.costs[maze.end].values())}")
    print(f"Part 2: {len(maze.best_paths)}")
