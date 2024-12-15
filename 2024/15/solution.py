from sys import argv
from dataclasses import dataclass
from typing import List, Dict, Set, Tuple, Any
import re

@dataclass
class Coord:
    x: int
    y: int

    @property
    def gps(self) -> int:
        return self.x + 100*self.y
    
    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)
    
    def copy(self) -> "Coord":
        return Coord(self.x, self.y)
    
    def __hash__(self):
        return hash((self.x, self.y))

class Warehouse:
    
    # given in x,y deltas
    MOVES = {
        ">": Coord(1,0),
        "v": Coord(0,1),
        "<": Coord(-1,0),
        "^": Coord(0,-1)
    }

    def __init__(self, lines: List[str]):

        self.boxes: Set[Coord] = set()
        self.walls: Set[Coord] = set()
        self.robot: Coord = None

        for y in range(len(lines)):
            for x in range(len(lines[y])):
                if lines[y][x] == "#":
                    self.walls.add(Coord(x,y))
                elif lines[y][x] == "O":
                    self.boxes.add(Coord(x,y))
                elif lines[y][x] == "@":
                    self.robot = Coord(x,y)

    @property
    def checksum(self) -> int:
        return sum([b.gps for b in self.boxes])

    def move(self, cmd: str) -> None:
        d = self.MOVES[cmd]
        cur = self.robot.copy()
       
        # first see if pushing will do anything
        to_move = []
        while True:
            cur += d
            if cur in self.boxes:
                to_move.append(cur)
                continue # keep pushing more boxes
            elif cur in self.walls:
                return # this move doesn't do anything (up against a wall)
            else:
                break # we can actually move
        
        # now push
        if len(to_move) > 0:
            self.boxes.remove(to_move[0])
            self.boxes.add(to_move[-1] + d)
        self.robot += d

class WideWarehouse:
    
    # given in x,y deltas
    MOVES = {
        ">": Coord(1,0),
        "v": Coord(0,1),
        "<": Coord(-1,0),
        "^": Coord(0,-1)
    }

    def __init__(self, lines: List[str]):

        self.lboxes: Set[Coord] = set()
        self.rboxes: Set[Coord] = set()
        self.walls: Set[Coord] = set()
        self.robot: Coord = None

        for y in range(len(lines)):
            for x in range(len(lines[y])):
                if lines[y][x] == "#":
                    self.walls.add(Coord(x*2,y))
                    self.walls.add(Coord(x*2+1,y))
                elif lines[y][x] == "O":
                    self.lboxes.add(Coord(x*2,y))
                    self.rboxes.add(Coord(x*2+1,y))
                elif lines[y][x] == "@":
                    self.robot = Coord(x*2,y)

    @property
    def checksum(self) -> int:
        return sum([b.gps for b in self.lboxes])

    def move(self, cmd: str) -> None:
        d = self.MOVES[cmd]
        cur = self.robot.copy()

        # find the list of boxes which need to be pushed
        # (ordered from furthest to closest)
        # or early-exit if this push eventually runs up against a wall

        to_move = []
        if cmd in {"<", ">"}:
            while True:
                cur += d
                if cur in self.lboxes or cur in self.rboxes:
                    to_move.append(cur)
                    cur += d
                    to_move.append(cur)
                    continue # keep pushing more boxes
                elif cur in self.walls:
                    return # this move doesn't do anything (up against a wall)
                else:
                    break # we can actually move
        
        elif cmd in {"v", "^"}:
            frontier = {cur}
            while True:
                new_frontier: Set[Coord] = set()
                for box in frontier:
                    if box + d in self.walls:
                        return # cannot move due to a wall
                    if box + d in self.lboxes:
                        new_frontier.add(box+d)
                        new_frontier.add(box+d+Coord(1,0))
                    if box + d in self.rboxes:
                        new_frontier.add(box+d)
                        new_frontier.add(box+d+Coord(-1,0))
                if len(new_frontier) == 0: # there is room to push
                    break
                to_move.extend(list(new_frontier))
                frontier = new_frontier
        
        # now push
        for b in to_move[::-1]:
            if b in self.rboxes:
                self.rboxes.remove(b)
                self.rboxes.add(b+d)
            elif b in self.lboxes:
                self.lboxes.remove(b)
                self.lboxes.add(b+d)
            else:
                raise Exception("Did not find expected box")
        
        self.robot += d                   

def parse_input(lines: List[str]) -> Tuple[Warehouse, List[str]]:
    
    warehouse_lines = []
    for i in range(len(lines)):
        if len(lines[i]) == 0:
            break
        warehouse_lines.append(lines[i])
    
    moves = []
    for i in range(i+1, len(lines)):
        moves.extend(list(lines[i]))

    return warehouse_lines, moves

def simulate(warehouse: Warehouse, moves: List[str]):
    for move in moves:
        warehouse.move(move)
    return warehouse.checksum

if __name__ == "__main__":

    INPUTFILE = "input.txt"
    if len(argv) > 1:
        if argv[1] in ("--test", "-t"):
            print("----- TEST MODE -----")
            INPUTFILE = "sample_input.txt"

    with open(INPUTFILE) as ifile:
        lines = ifile.read().splitlines()
    
    warehouse_lines, moves = parse_input(lines)

    print(f"Part 1: {simulate(Warehouse(warehouse_lines), moves)}")
    print(f"Part 2: {simulate(WideWarehouse(warehouse_lines), moves)}")
