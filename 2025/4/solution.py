from typing import List
from sys import argv

INPUTFILE = "input.txt"
if len(argv) > 1:
    if argv[1] in ("--test", "-t"):
        print("----- TEST MODE -----")
        INPUTFILE = "sample_input.txt"

with open(INPUTFILE) as ifp:
    lines = [list(row) for row in ifp.read().split("\n")]

def count_rolls(board) -> int:
    count = 0
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            if lines[y][x] == "@": count += 1

    return count

def remove_rolls(board) -> List:

    new_board = []

    for y in range(len(board)):
        new_row = board[y].copy()
        for x in range(len(board[0])):
            if board[y][x] != "@": continue
            surrounding = 0
            for dy,dx in [
                (y-1, x-1), (y-1, x), (y-1, x+1),
                (y, x-1), (y, x+1),
                (y+1, x-1), (y+1, x), (y+1, x+1),
            ]:
                if dy < 0 or dy > len(board)-1 or dx < 0 or dx > len(board[0])-1:
                    continue
                if board[dy][dx] == "@":
                    surrounding += 1

            if surrounding < 4:
                new_row[x] = "."
        
        new_board.append(new_row)

    return new_board

starting_rolls = count_rolls(lines)
lines = remove_rolls(lines)
print(f"part 1: {starting_rolls - count_rolls(lines)}")

while True:
    initial = count_rolls(lines)
    lines = remove_rolls(lines)
    if count_rolls(lines) == initial:
        print(f"part 2: {starting_rolls - count_rolls(lines)}")
        break
