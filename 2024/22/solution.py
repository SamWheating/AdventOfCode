from sys import argv
from dataclasses import dataclass
from typing import List, Dict, Set, Tuple, Any
import re
from collections import defaultdict

def mix(a: int, b: int) -> int:
    return a ^ b

assert mix(42, 15) == 37

def prune(a: int) -> int:
    return a % 16777216

assert prune(100000000) == 16113920

def secret_number(secret: int):
    secret  = prune(mix(secret, secret*64))
    secret  = prune(mix(secret, secret//32))
    secret  = prune(mix(secret, secret*2048))
    return secret

assert secret_number(123) == 15887950 

def part1(nums: List[int]):
    total = 0
    for n in nums:
        for _ in range(2000):
            n = secret_number(n)
        total += n

    return total

def part2(nums: List[int]):

    prices: dict[str, int] = defaultdict(int)
    for n in nums:
        secrets = [n]
        seen = set()
        for _ in range(2000):
            n = secret_number(n)
            secrets.append(n)
            if len(secrets) >= 5:
                key = str([secrets[-j]%10 - secrets[-(j+1)]%10 for j in range(4,0,-1)])
                if key not in seen:
                    prices[key] += n % 10
                seen.add(key)


    return max(prices.values())

assert part2([1,2,3,2024]) == 23

if __name__ == "__main__":

    INPUTFILE = "input.txt"
    if len(argv) > 1:
        if argv[1] in ("--test", "-t"):
            print("----- TEST MODE -----")
            INPUTFILE = "sample_input.txt"

    with open(INPUTFILE) as ifile:
        nums = [int(i) for i in ifile.read().splitlines()]

    print(f"Part 1: {part1(nums)}")
    print(f"Part 2: {part2(nums)}")
