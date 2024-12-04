# Day 1: Historian Hysteria
# https://adventofcode.com/2024/day/1

from collections import Counter
from typing import List, Tuple

from utils.input import read_input_file_lines


def parse_inputs() -> Tuple[List[int], List[int]]:
    lines = read_input_file_lines("day01_input.txt")

    list1, list2 = [], []
    for l in lines:
        a, b = l.split()
        a, b = int(a), int(b)
        list1.append(a)
        list2.append(b)
    return list1, list2


def part1():
    list1, list2 = parse_inputs()
    list1.sort()
    list2.sort()

    dist = 0
    for n1, n2 in zip(list1, list2):
        dist += abs(n2 - n1)

    return dist


def part2():
    list1, list2 = parse_inputs()
    counts = Counter(list2)

    score = 0
    for n in list1:
        score += n * counts.get(n, 0)
    return score


s1 = part1()
print("Solution Part 1:", s1)
s2 = part2()
print("Solution Part 2:", s2)
