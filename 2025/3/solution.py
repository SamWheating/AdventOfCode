from sys import argv

INPUTFILE = "input.txt"
if len(argv) > 1:
    if argv[1] in ("--test", "-t"):
        print("----- TEST MODE -----")
        INPUTFILE = "sample_input.txt"

banks = []
with open(INPUTFILE) as ifp:
    for line in ifp.read().split("\n"):
        banks.append([int(c) for c in line])

def lowest_joltage(bank, n):

    val = 0
    for b in range(n):
        d = max(bank[:-(n-b-1) or None])
        bank = bank[bank.index(d)+1:]
        val *= 10
        val += d
    return val

assert lowest_joltage([int(c) for c in "987654321111111"], 2) == 98
assert lowest_joltage([int(c) for c in "811111111111119"], 2) == 89
assert lowest_joltage([int(c) for c in "234234234234278"], 2) == 78
assert lowest_joltage([int(c) for c in "818181911112111"], 2) == 92

assert lowest_joltage([int(c) for c in "987654321111111"], 12) == 987654321111
assert lowest_joltage([int(c) for c in "811111111111119"], 12) == 811111111119
assert lowest_joltage([int(c) for c in "234234234234278"], 12) == 434234234278
assert lowest_joltage([int(c) for c in "818181911112111"], 12) == 888911112111

print(f"part 1: {sum([lowest_joltage(b, 2) for b in banks])}")
print(f"part 1: {sum([lowest_joltage(b, 12) for b in banks])}")
