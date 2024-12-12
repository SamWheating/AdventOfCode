from sys import argv
from typing import List, Dict, Tuple, Set

from dataclasses import dataclass

def perimiter(points: Set[Tuple[int, int]]) -> int:

    p = 0
    deltas = [(0,1), (0,-1), (1,0), (-1,0)]
    for pt in points:
        for dy,dx in deltas:
            if (pt[0] + dy, pt[1] + dx) not in points:
                p += 1
    return p

assert perimiter([(0,0)]) == 4
assert perimiter([(0,0), (0,1)]) == 6

def num_sides(points: Set[Tuple[int, int]]) -> List[Set[Tuple[int,int]]]:
    # given a shape defined by a set 1x1 tiles, find the number of edges in its perimiter

    sides: List[Set[Tuple[int,int]]] = []

    # tangent is a length-1 vector perpendicular to an edge
    # if point is in group but point+tangent is not, then its an edge
    #
    # plane is in-line with an edge. If point+plane or point-plane is in an existing group,
    # then point is also a part of the same edge
    for tangent, plane in [
        ((1,0), (0,1)),
        ((-1,0), (0,1)),
        ((0,1), (1,0)),
        ((0,-1), (1,0)),
    ]:

        subset: List[Set[Tuple[int,int]]] = []
        # first find all edges facing in the given direction (length 1)
        for p in points:
            if (p[0]+tangent[0], p[1]+tangent[1]) not in points:
                subset.append({p})

        # now merge adjacent edges until we can't merge any more
        while True:
            merged = False
            for g1 in subset:
                for g2 in subset:
                    if g1 == g2:
                        continue
                    for p in g1:
                        a = (p[0]+plane[0], p[1]+plane[1])
                        b = (p[0]-plane[0], p[1]-plane[1])
                        if a in g2 or b in g2:
                            # merge these groups since they're adjacent:
                            merged = True
                            subset = [s for s in subset if s != g1 and s != g2]
                            subset.append(g1 | g2)
                            break
                    if merged:
                        break
                if merged:
                    break

            if not merged:
                sides.extend(subset)
                break

    return len(sides)

assert num_sides({(0,0), (0,1)}) == 4
assert num_sides({(0,0), (0,1), (0,2)}) == 4
assert num_sides({(0,0), (0,1), (1,1)}) == 6

def find_groups(lines: List[List]) -> List[Set[Tuple[int,int]]]:

    deltas = [(0,1), (0,-1), (1,0), (-1,0)]
    groups = []
    # find the first non-counted set
    while True:
        group = set()
        crop = None
        for y in range(len(lines)):
            for x in range(len(lines[y])):
                if lines[y][x] is not None:
                    group.add((y,x))
                    crop = lines[y][x]
                    break
            if crop is not None:
                break

        if crop is None:
            return groups
        
        # now expand the set until we can't find any more adjacent tiles of the same crop
        while True:
            added = False
            for pt in list(group):
                for dy, dx in deltas:
                    candidate = (pt[0] + dy, pt[1] + dx)
                    if candidate in group:
                        continue
                    if candidate[0] < 0 or candidate[1] < 0 or candidate[0] >= len(lines) or candidate[1] >= len(lines[0]):
                        continue 
                    if lines[candidate[0]][candidate[1]] == crop:
                        added = True
                        group.add(candidate)
            if not added:
                for y, x in group:
                    lines[y][x] = None
                groups.append(group)
                break       

def part1(groups: List[Set[Tuple[int,int]]]):
    
    return sum([perimiter(g) * len(g) for g in groups])

def part2(groups: List[Set[Tuple[int,int]]]):

    return sum([num_sides(g) * len(g) for g in groups])

if __name__ == "__main__":

    INPUTFILE = "input.txt"
    if len(argv) > 1:
        if argv[1] in ("--test", "-t"):
            print("----- TEST MODE -----")
            INPUTFILE = "sample_input.txt"

    with open(INPUTFILE) as ifile:
        lines = ifile.read().splitlines()
        groups = find_groups([list(s) for s in lines])


    print(f"Part 1: {part1(groups)}")
    print(f"Part 2: {part2(groups)}")
