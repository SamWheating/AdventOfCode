# This is the boilerplate I usually start with
from sys import argv
from typing import List, Dict

def next_nums(n: int) -> List[int]:
    if n == 0:
        return [1]
    if len(str(n)) % 2 == 0:
        return [int(str(n)[:len(str(n))//2]), int(str(n)[len(str(n))//2:])]
    return [n*2024]

def blink_num(num: int, steps: int, memo: Dict[int, int]) -> int:
    # returns the number of descendants after "blinking" a number n times
    # recursive + memoized
    if steps == 0:
        return 1
    else:
        next = next_nums(num)
        size = 0
        for n in next:
            if (n, steps-1) not in memo:
                memo[(n, steps-1)] = blink_num(n, steps-1, memo)    
            size += memo[(n, steps-1)]
        return size
    
assert blink_num(1, 0, {}) == 1
assert blink_num(1, 2, {}) == 2 # 1 -> 2024 -> 20, 24
assert blink_num(1, 3, {}) == 4 # 1 -> 2024 -> 20, 24 -> 2,0,2,4
assert blink_num(0, 5, {}) == 4 # 0 -> 1 -> 2024 -> 20, 24 -> 2,0,2,4 -> 4048,1,4048,8096

def do_blinks(nums: List[int], blinks: int):

    memo = {}
    length = 0
    for n in nums:
        length += blink_num(n, blinks, memo)
    
    return length

assert do_blinks([125,17], 6) == 22

if __name__ == "__main__":

    INPUTFILE = "input.txt"
    if len(argv) > 1:
        if argv[1] in ("--test", "-t"):
            print("----- TEST MODE -----")
            INPUTFILE = "sample_input.txt"

    with open(INPUTFILE) as ifile:
        nums = [int(i) for i in ifile.read().split()]

    print(f"Part 1: {do_blinks(nums, 25)}")
    print(f"Part 2: {do_blinks(nums, 75)}")
