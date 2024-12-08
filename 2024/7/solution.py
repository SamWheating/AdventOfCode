from sys import argv
from typing import List

# define the availabel operators as a list of callables,
# not great for readability but it can be easily extended.
OPS = [
    lambda x, y: x + y,
    lambda x, y: x * y,
    lambda x, y: int(str(x) + str(y))
]

def verify(target: int, nums: List[int], operators: List[callable]):
    # recursively see if tthe target can be found by applying the available
    # operators left-to-right

    if len(nums) == 1:
        return nums[0] == target
    
    if nums[0] > target:
        return False # early exit, since operators can only increase the value
    
    for op in operators:
        if verify(target, [op(nums[0], nums[1])] + nums[2:], operators):
            return True
    
    return False
    
assert verify(12, [12,], OPS)
assert not verify(13, [12,], OPS)

assert verify(20, [12, 8], OPS[:2]) # 12 + 8
assert verify(292, [11, 6, 16, 20], OPS[:2]) # 11 + 6 * 16 + 20
assert verify(7290, [6, 8, 6, 15], OPS) # 6 * 8 || 6 * 15

def get_total(lines: List[str], operators: List[callable]):
    total = 0
    for line in lines:
        target = int(line.split(":")[0])
        nums = [int(n) for n in line.split(":")[1].split()]
        if verify(target, nums, operators):
            total += target

    return total

if __name__ == "__main__":

    INPUTFILE = "input.txt"
    if len(argv) > 1:
        if argv[1] in ("--test", "-t"):
            print("----- TEST MODE -----")
            INPUTFILE = "sample_input.txt"

    with open(INPUTFILE) as ifile:
        lines = ifile.readlines()
        line = ifile.read()

    print(f"Part 1: {get_total(lines, OPS[:2])}")
    print(f"Part 2: {get_total(lines, OPS)}")
