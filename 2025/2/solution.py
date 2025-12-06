from sys import argv

INPUTFILE = "input.txt"
if len(argv) > 1:
    if argv[1] in ("--test", "-t"):
        print("----- TEST MODE -----")
        INPUTFILE = "sample_input.txt"

seqs = [(int(p[0]), int(p[1])) for p in [p.split("-") for p in open(INPUTFILE).read().split(",")]]

def is_invalid_p1(i: int) -> bool:
    s = str(i)
    return s[:len(s)//2]*2 == s

assert is_invalid_p1(1111)
assert is_invalid_p1(2020)
assert is_invalid_p1(55)
assert is_invalid_p1(500500)

assert not is_invalid_p1(123)

def is_invalid_p2(i: int) -> bool:
    s = str(i)
    for l in range(1, 1+len(s)//2):
        if s[0:l]*(len(s)//l) == s:
            return True
    return False

assert is_invalid_p2(121212)
assert is_invalid_p2(824824824)
assert is_invalid_p2(1188511885)
assert is_invalid_p2(111)

total_1 = 0
total_2 = 0
for seq in seqs:
    for i in range(seq[0], seq[1]+1):
        if is_invalid_p1(i):
            total_1 += i
            total_2 += i
            continue
        if is_invalid_p2(i):
            total_2 += i

print(f"Part 1 solution: {total_1}")
print(f"Part 1 solution: {total_2}")
