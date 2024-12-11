from sys import argv
from collections import defaultdict
from typing import Dict, List

def parse_map(lines: List[str]) -> Dict[int, Dict[int, int]]:
    # turn a list of strings into a nested dict of values
    map = defaultdict(dict)
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            map[y][x] = int(lines[y][x])
    return dict(map) # since we want keyErrors for missing values

def find_summits(map: Dict[int, Dict[int, int]], y, x) -> int:
    # find the unique summits (height == 9) reachable from point y,x
    # only moving vertically / horizontally to squares 1 unit higher

    height  = map[y][x]
    if height == 9:
        return [(y,x)]
    
    summits = []
    for (dy, dx) in [(1,0), (-1, 0), (0, 1), (0, -1)]:
            
        try:
            next_height = map[y+dy][x+dx]
        except KeyError: # boundary checks lmao
            continue

        if next_height == height + 1:
            summits.extend(find_summits(map, y+dy, x+dx))

    return list(set(summits))

def rate_trailhead(map: Dict[int, Dict[int, int]], y, x) -> int:
    # find the unique trails to any summit (height==9) from y,x
    # only moving vertically / horizontally to squares 1 unit higher
    height  = map[y][x]
    if height == 9:
        return 1
    
    trails = 0
    for (dy, dx) in [(1,0), (-1, 0), (0, 1), (0, -1)]:
            
        try:
            next_height = map[y+dy][x+dx]
        except KeyError:
            continue

        if next_height == height + 1:
            trails += rate_trailhead(map, y+dy, x+dx)

    return trails

map = parse_map([
    "0123456789",
])

assert len(find_summits(map, 0, 0)) == 1

map = parse_map([
    "0123",
    "7654",
    "8900"
])
assert len(find_summits(map, 0, 0)) == 1

def part1(lines):
    score = 0 
    map = parse_map(lines)
    for y in map:
        for x in map[y]:
            if map[y][x] == 0:
                score +=  len(set(find_summits(map, y, x)))
    return score

def part2(lines):
    score = 0 
    map = parse_map(lines)
    for y in map:
        for x in map[y]:
            if map[y][x] == 0:
                score += rate_trailhead(map, y, x)
    return score

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
