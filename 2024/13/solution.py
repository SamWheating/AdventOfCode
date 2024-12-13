# This is the boilerplate I usually start with
from sys import argv
from dataclasses import dataclass
from typing import List, Tuple
from re import match

import numpy as np

@dataclass
class Claw:
    a: Tuple[int,int]
    b: Tuple[int,int]
    prize: Tuple[int,int]

    def solution(self):
        a = np.array([[self.a[0], self.b[0]], [self.a[1], self.b[1]]])
        b = np.array([self.prize[0], self.prize[1]])
        a_press, b_press = (round(n) for n in np.linalg.solve(a, b))
        if a_press*self.a[0] + b_press*self.b[0] == self.prize[0]:
            if a_press*self.a[1] + b_press*self.b[1] == self.prize[1]:
                return 3*a_press + b_press
        
        return 0
        
def parse_input(lines: List[str]) -> List[Claw]:
    
    claws = []
    for i in range((len(lines)//4)+1):
        a_x, a_y = (int(n) for n in match("Button\ A:\ X\+(\d+),\ Y\+(\d+)", lines[i*4]).groups())
        b_x, b_y = (int(n) for n in match("Button\ B:\ X\+(\d+),\ Y\+(\d+)", lines[i*4+1]).groups())
        p_x, p_y = (int(n) for n in match("Prize:\ X=(\d+), Y=(\d+)", lines[i*4+2]).groups())
        claws.append(Claw((a_y, a_x), (b_y, b_x), (p_y, p_x)))

    return claws

def part1(claws: List[Claw]):
    return sum([c.solution() for c in claws])

def part2(claws: List[Claw]):
    total = 0
    for claw in claws:
        claw.prize = (claw.prize[0]+10000000000000, claw.prize[1]+10000000000000)
        total += claw.solution()
    return total

if __name__ == "__main__":

    INPUTFILE = "input.txt"
    if len(argv) > 1:
        if argv[1] in ("--test", "-t"):
            print("----- TEST MODE -----")
            INPUTFILE = "sample_input.txt"

    with open(INPUTFILE) as ifile:
        lines = ifile.read().splitlines()

    claws = parse_input(lines)

    print(f"Part 1: {part1(claws)}")
    print(f"Part 2: {part2(claws)}")
