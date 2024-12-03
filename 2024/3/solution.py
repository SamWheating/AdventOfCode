from sys import argv
import re

def part1(lines):
    total = 0
    for line in lines:
        # match any groups which look like mul(1,2)
        matches = re.findall("mul\(\d+,\d+\)", line)
        for match in matches:
            groups = re.match("mul\((\d+),(\d+)\)", match).groups()
            arg1, arg2 = int(groups[0]), int(groups[1])
            total += arg1 * arg2
    return total

assert part1([
    "asfmul(1,3)asn",
    "mul(1,3)",
    "mulsaba(1,3)"]
) == 6

def part2(lines):
    total = 0
    enabled = True
    for line in lines:
        # match any groups which look like mul(1,2) OR do() OR don't()
        matches = re.findall("do\(\)|don't\(\)|mul\(\d+,\d+\)", line)
        for match in matches:
            if match == "do()":
                enabled = True
            elif match == "don't()":
                enabled = False
            else:
                groups = re.match("mul\((\d+),(\d+)\)", match).groups()
                arg1, arg2 = int(groups[0]), int(groups[1])
                total += arg1 * arg2 * enabled
    return total

assert part2([
    "asfmul(1,3)asn", # contains mul(1,3)
    "mdon't()mul(1,3)", # contains mul(1,3) but disabled
    "3)do()xmul(1,3)"] # re-enable and include mul(1,3)
) == 6

if __name__ == "__main__":

    INPUTFILE = "input.txt"
    if len(argv) > 1:
        if argv[1] in ("--test", "-t"):
            print("----- TEST MODE -----")
            INPUTFILE = "sample_input.txt"

    with open(INPUTFILE) as ifile:
        lines = ifile.readlines()
        line = ifile.read()

    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
