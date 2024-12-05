# This is the boilerplate I usually start with
from sys import argv

def check_rule(update: list, rule: tuple):
    if rule[0] in update and rule[1] in update:
        if update.index(rule[1]) < update.index(rule[0]):
            return False
    
    return True

assert check_rule([1,2,3,4,5], (3,4))
assert check_rule([1,2,3,4,5], (9,10))
assert not check_rule([1,2,3,4,5], (4,3))

def check_update(update: list, rules: list):
    for rule in rules:
        if not check_rule(update, rule):
            return False
    else:
        return True
    
def sort_update(update: list, rules: list):

    while True:
        for rule in rules:
            if rule[0] in update and rule[1] in update:
                l_idx = min([update.index(rule[1]), update.index(rule[0])])
                r_idx = max([update.index(rule[1]), update.index(rule[0])])
                update[l_idx] = rule[0]
                update[r_idx] = rule[1]

        if check_update(update, rules):
            return update
        
assert sort_update([1,2,3,4,5,6], [(6,5), (3,2)]) == [1,3,2,4,6,5]

def part1(rules, updates):

    total = 0
    for update in updates:
        if check_update(update, rules):
            total += update[len(update)//2]

    return total

def part2(rules, updates):
    
    total = 0
    for update in updates:
        if not check_update(update, rules):
            total += sort_update(update, rules)[len(update)//2]

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

    rules = []
    updates = []
    for line in lines:
        if "|" in line:
            rules.append((int(line.split("|")[0]), int(line.split("|")[1])))
        elif "," in line:
            updates.append([int(c) for c in line.split(",")])

    print(f"Part 1: {part1(rules, updates)}")
    print(f"Part 2: {part2(rules, updates)}")
