# This is the boilerplate I usually start with
from sys import argv
from typing import List, Tuple
import dataclasses

@dataclasses.dataclass
class Block:
    idx: int # ID of the file associated with this block (None if empty)
    size: int 

class Disk:

    def __init__(self, dense: str) -> None:
        is_file = True
        file_idx = 0
        self.disk = []
        for c in dense:
            n = int(c)
            if is_file:
                self.disk.append(Block(file_idx, n))
                file_idx += 1
            else:
                self.disk.append(Block(None, n))
            is_file = not is_file

    def __repr__(self) -> str:
        out = []
        for block in self.disk:
            if block.idx is None:
                out.extend(["."] * block.size)
            else:
                out.extend([str(block.idx)] * block.size)

        return "".join(out)

    def compact_bitwise(self) -> None:
        max_block = max([b.idx for b in self.disk if b.idx != None])

        for b_idx in range(max_block,-1,-1):
            b = 0
            while True:
                if self.disk[b].idx == b_idx:
                    break
                b += 1
            
            block = dataclasses.replace(self.disk[b]) # create a copy
            self.disk[b].idx = None # replace the previous location with a gap
            for i in range(len(self.disk)):

                if self.disk[i].idx is not None:
                    continue

                if self.disk[i].size < block.size: # gap can only fit part of block
                    self.disk[i].idx = block.idx
                    block.size -= self.disk[i].size
                    continue

                if self.disk[i].size == block.size: # a perfect fit
                    self.disk[i].idx = block.idx # replace the gap with this file
                    break

                if self.disk[i].size > block.size:
                    self.disk[i].size -= block.size # shrink the gap by size of block
                    self.disk[b].idx = None
                    self.disk.insert(i, block)
                    break

    def compact_blockwise(self) -> None:
        max_block = max([b.idx for b in self.disk if b.idx != None])

        for b_idx in range(max_block,-1,-1):
            b = 0
            while True:
                if self.disk[b].idx == b_idx:
                    break
                b += 1
            
            block = dataclasses.replace(self.disk[b])

            # look for a suitably big opening
            for i in range(len(self.disk)):

                if self.disk[i] == block:
                    # nothing to the left, give up
                    break

                if self.disk[i].idx is not None:
                    continue

                if self.disk[i].size < block.size: # gap is too small
                    continue

                if self.disk[i].size == block.size: # a perfect fit
                    self.disk[i].idx = block.idx # replace the gap with this file
                    self.disk[b].idx = None
                    break

                if self.disk[i].size > block.size:
                    self.disk[i].size -= block.size # shrink the gap by size of gap
                    self.disk[b].idx = None
                    self.disk.insert(i, block)
                    break

    def checksum(self) -> int:
        total = 0
        idx = 0
        for block in self.disk:
            if block.idx is None:
                idx += block.size
            else:
                for _ in range(block.size):
                    total += idx * block.idx
                    idx += 1

        return total

def part1(line):
    disk = Disk(line)
    disk.compact_bitwise()
    return disk.checksum()

def part2(line):
    disk = Disk(line)
    disk.compact_blockwise()
    return disk.checksum()

if __name__ == "__main__":

    INPUTFILE = "input.txt"
    if len(argv) > 1:
        if argv[1] in ("--test", "-t"):
            print("----- TEST MODE -----")
            INPUTFILE = "sample_input.txt"

    with open(INPUTFILE) as ifile:
        line = ifile.read()

    print(f"Part 1: {part1(line)}")
    print(f"Part 2: {part2(line)}")
