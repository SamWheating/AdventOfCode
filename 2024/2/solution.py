from sys import argv

def validate_line(line: list) -> bool:
    if line[0] < line[-1]:
        # asc
        for i in range(1,len(line)):
            if line[i] - line[i-1] not in (1,2,3):
                return False
        else:
            return True
    if line[0] > line[-1]:
        # desc
        for i in range(1,len(line)):
            if line[i] - line[i-1] not in (-1,-2,-3):
                return False
        else:
            return True
        
assert validate_line([1,3,5])
assert not validate_line([1,3,8])
assert validate_line([5,4,1])
assert not validate_line([9,2,1])

def part1(lines):
    valid = 0
    
    for line in lines:
        if validate_line(line):
            valid += 1
    
    return valid

assert part1([
    [7, 6, 4, 2, 1], # valid
    [1, 3, 2, 4, 5], # invalid
    [1, 3, 6, 7, 9]  # valid
]) == 2

def part2(lines):
    valid = 0
    for line in lines:
        # try all different leave-one-out options
        for l in range(len(lines)):
            if validate_line(line[:l] + line[l+1:]):
                valid += 1
                break
        
    return valid

assert part2([
    [7, 6, 4, 2, 1], # valid
    [1, 3, 2, 4, 5], # valid
    [1, 3, 6, 7, 9]  # valid
]) == 3

if __name__ == "__main__":

    INPUTFILE = "input.txt"
    if len(argv) > 1:
        if argv[1] in ("--test", "-t"):
            print("----- TEST MODE -----")
            INPUTFILE = "sample_input.txt"

    with open(INPUTFILE) as ifile:
        lines = ifile.readlines()
        lines = [[int(num) for num in line.split()] for line in lines]
        line = ifile.read()

    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
