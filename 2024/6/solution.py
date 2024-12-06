from sys import argv
from typing import List, Optional

DIRECTIONS = [ # y,x unit vectors
    (-1, 0),  # up
    (0, 1),   # right
    (1, 0),   # down
    (0, -1)   # left
]

def walk_map(map: List[List[str]]) -> Optional[int]:
    """
    Find the initial location + direction then walk the map:
     - If we exit the board, return number of distince tiles
     - If cycle detected, return None
    """
    y,x = None, None
    direction = None
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] in ["^", ">", "v", "<"]:
                y,x = i,j
                direction = ["^", ">", "v", "<"].index(map[i][j])

    assert y is not None and x is not None and direction is not None
    
    visited = set()
    while True:

        if (y,x,direction) in visited:
            return None # loop detected!
        
        visited.add((y,x,direction))
        next_y = y + DIRECTIONS[direction][0]
        next_x = x + DIRECTIONS[direction][1]

        if next_y < 0 or next_y >= len(map) or next_x < 0 or next_x >= len(map[0]):
            return len({(v[0], v[1]) for v in visited})
        
        if map[next_y][next_x] == "#":
            direction = (direction + 1) % 4
            continue

        y = next_y
        x = next_x


def part1(map: list):
    return walk_map(map)
                
def part2(lines):
    found = 0
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            if lines[y][x] == ".":
                new_map = [[c for c in row] for row in lines]
                new_map[y][x] = "#"
                if walk_map(new_map) is None:
                    found += 1

    return found

if __name__ == "__main__":

    INPUTFILE = "input.txt"
    if len(argv) > 1:
        if argv[1] in ("--test", "-t"):
            print("----- TEST MODE -----")
            INPUTFILE = "sample_input.txt"

    with open(INPUTFILE) as ifile:
        lines = ifile.read().splitlines()

    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
