from sys import argv
from dataclasses import dataclass
from typing import List, Dict, Set, Tuple, Any
import re

def check_towels(towels: List[str], pattern: str, memo: Dict[str, bool]) -> bool:

    if len(pattern) == 0:
        return True
    
    if pattern in memo:
        return memo[pattern]

    for towel in towels:
        if pattern.startswith(towel):
            if check_towels(towels, pattern[len(towel):], memo):
                memo[pattern] = True
                return True

    memo[pattern] = False        
    return False

assert check_towels(["a", "bb", "ccc"], "aacccbb", {})
assert not check_towels(["a", "bb", "ccc"], "aaccbb", {})

def count_towels(towels: List[str], pattern: str, memo: Dict[str, bool]) -> bool:

    if len(pattern) == 0:
        return 1
    
    if pattern in memo:
        return memo[pattern]

    subtotal = 0
    for towel in towels:
        if pattern.startswith(towel):
            subtotal += count_towels(towels, pattern[len(towel):], memo)

    memo[pattern] = subtotal        
    return subtotal

test_towels = ["r", "wr", "b", "g", "bwu", "rb", "gb", "br"]
assert count_towels(test_towels, "brwrr", {}) == 2
assert count_towels(test_towels, "bggr", {}) == 1
assert count_towels(test_towels, "gbbr", {}) == 4
assert count_towels(test_towels, "rrbgbr", {}) == 6

def part1(towels: List[str], patterns: List[str]) -> int:
    count = 0
    memo = {}
    for p in patterns:
        if check_towels(towels, p, memo):
            count += 1
    return count

def part2(towels: List[str], patterns: List[str]) -> int:
    total = 0
    memo = {}
    for p in patterns:
        total += count_towels(towels, p, memo)
    return total

if __name__ == "__main__":

    INPUTFILE = "input.txt"
    if len(argv) > 1:
        if argv[1] in ("--test", "-t"):
            print("----- TEST MODE -----")
            INPUTFILE = "sample_input.txt"

    with open(INPUTFILE) as ifile:
        lines = ifile.read().splitlines()
    
    towels = lines[0].split(", ")
    towels.sort(key=lambda t: len(t), reverse=True) # prioritize longer towels
    patterns = lines[2:]

    print(f"Part 1: {part1(towels, patterns)}")
    print(f"Part 2: {part2(towels, patterns)}")
