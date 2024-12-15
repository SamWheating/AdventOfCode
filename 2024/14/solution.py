from sys import argv
from dataclasses import dataclass
from typing import List, Dict, Set, Tuple, Any
import re
import time

@dataclass
class Robot:
    x: int
    y: int
    d_x: int
    d_y: int

    def move(self, steps, max_x, max_y):
        self.x = (self.x + self.d_x*steps) % max_x
        self.y = (self.y + self.d_y*steps) % max_y

r = Robot(3,3,1,1)
r.move(1, 6, 6)
assert (r.x, r.y) == (4,4)
r.move(2, 6, 6)
assert (r.x, r.y) == (0,0)

class Floor:

    def __init__(self, lines, max_x, max_y):
        self.robots: List[Robot] = []
        self.max_x = max_x
        self.max_y = max_y
        for line in lines:
            g = re.match("p=(\d+),(\d+)\ v=(-?\d+),(-?\d+)", line).groups()
            self.robots.append(Robot(int(g[0]), int(g[1]), int(g[2]), int(g[3])))
    
    def do_steps(self, count):
        for r in self.robots:
            r.move(count, self.max_x, self.max_y)

    @property
    def safety_factor(self):
        q1, q2, q3, q4 = 0, 0, 0, 0
        for r in self.robots:
            if r.x < self.max_x // 2:
                if r.y < self.max_y // 2: # top left
                    q1 += 1
                elif r.y > self.max_y // 2: # bottom left
                    q2 += 1
            elif r.x > self.max_x // 2:
                if r.y < self.max_y // 2: # top right
                    q3 += 1
                elif r.y > self.max_y // 2: # bottom right
                    q4 += 1

        return q1*q2*q3*q4
    
    def __repr__(self):
        out = [([" "] * self.max_x) for _ in range(self.max_y)]
        for x in range(self.max_x):
            for y in range(self.max_y):
                for r in self.robots:
                    if r.x == x and r.y == y:
                        out[y][x] = "#"

        new_out = []
        for row in out:
            r = "".join(row)
            new_out.append(r)
        return "\n".join(new_out)

f = Floor([], 100, 100)
f.robots.append(Robot(1,1,0,0))
f.robots.append(Robot(2,2,0,0))
f.robots.append(Robot(60,1,0,0))
f.robots.append(Robot(1,60,0,0))
f.robots.append(Robot(60,60,0,0))
assert f.safety_factor == 2

def part1(lines, max_x, max_y):
    f = Floor(lines, max_x, max_y)
    f.do_steps(100)
    return f.safety_factor

def part2(lines, max_x, max_y):
    f = Floor(lines, max_x, max_y)
    # manual inspection determined that the lowest-entropy frames are cyclic,
    # defined by t_i = 82 + 101*i
    # so we only need to print these frames for furhter inspection
    f.do_steps(82)
    for i in range(100):
        print(f"\n{i*101 + 82} seconds elapsed:")
        print(f)
        f.do_steps(101)

if __name__ == "__main__":

    INPUTFILE = "input.txt"
    MAX_X = 101
    MAX_Y = 103
    if len(argv) > 1:
        if argv[1] in ("--test", "-t"):
            print("----- TEST MODE -----")
            INPUTFILE = "sample_input.txt"
            MAX_X = 11
            MAX_Y = 7

    with open(INPUTFILE) as ifile:
        lines = ifile.read().splitlines()

    print(f"Part 1: {part1(lines, MAX_X, MAX_Y)}")
    print(f"Part 2: {part2(lines, MAX_X, MAX_Y)}")
