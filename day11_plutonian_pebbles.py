# Day 11: Plutonian Pebbles
# https://adventofcode.com/2024/day/11

from utils.input import read_input_file_lines
from typing import List, Dict
from itertools import chain
from functools import lru_cache


def parse_inputs():
    lines = read_input_file_lines("day11_input.txt")
    stones = [int(x) for x in lines[0].split()]
    return stones


class Stone:
    def __init__(self, val=None, next=None):
        self.val = val
        self.next = next

    def blink(self):

        if self.val == 0:
            self.val = 1
            return self.next

        s = str(self.val)
        l = len(s)
        if l % 2 == 0:
            # Split, return pointer to next
            self.val = int(s[: l // 2])
            next = self.next
            self.next = Stone(int(s[l // 2 :]), next)
            return next

        self.val *= 2024
        return self.next

    def __str__(self):
        return str(self.val)


def blink(head: Stone):
    curr = head.next
    while curr:
        curr = curr.blink()


def count_stones(head: Stone):
    count = 0
    curr = head.next
    while curr:
        count += 1
        curr = curr.next
    return count


def print_stones(head: Stone):
    curr = head.next
    while curr:
        print(f"{curr} ", end="")
        curr = curr.next
    print()


def part1():
    stones = parse_inputs()
    head = curr = Stone()
    for s in stones:
        curr.next = Stone(s)
        curr = curr.next

    for _ in range(25):
        blink(head)

    return count_stones(head)


def gener(head):
    curr = head.next
    while curr:
        yield curr
        curr = curr.next


@lru_cache(maxsize=None)
def dfs(stone: int, depth: int, max_depth: int) -> int:
    while depth < max_depth:
        depth += 1
        if stone == 0:
            stone = 1
            continue

        s = str(stone)
        l = len(s)
        if l % 2 == 0:
            return dfs(int(s[: l // 2]), depth, max_depth) + dfs(
                int(s[l // 2 :]), depth, max_depth
            )

        # else
        stone *= 2024

    return 1


def part2():
    stones = parse_inputs()
    MAX_DEPTH = 75
    return sum(dfs(s, 0, MAX_DEPTH) for s in stones)


s1 = part1()
print("Solution Part 1:", s1)
s2 = part2()
print("Solution Part 2:", s2)
