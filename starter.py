from sys import argv
from dataclasses import dataclass
from typing import List, Dict, Set, Tuple, Any
import re

def part1(lines):
    pass

def part2(lines):
    pass

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
