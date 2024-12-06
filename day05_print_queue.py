# Day 5: Print Queue
# https://adventofcode.com/2024/day/5


from collections import defaultdict
from typing import Dict, List, Set

from utils.input import read_input_file_lines


def parse_inputs():
    lines = read_input_file_lines("day05_input.txt")
    rules = []
    orderings = []
    for l in lines:
        if "|" in l:
            rules.append([int(x) for x in l.split("|")])
        elif "," in l:
            orderings.append([int(x) for x in l.split(",")])
    return rules, orderings


def check_ordering(ordering: List[int], after_dict: dict):
    l = len(ordering)
    for i in range(l):
        for j in range(i + 1, l):
            if ordering[j] not in after_dict[ordering[i]]:
                return False
    return True


def sort_ordering(ordering: List[int], after_dict: dict):
    def mergesort(ordr):
        l = len(ordr)
        if l <= 1:
            return ordr

        o1, o2 = ordr[: l // 2], ordr[l // 2 :]
        o1 = mergesort(o1)
        o2 = mergesort(o2)

        res = []
        i, j = 0, 0
        while i < len(o1) and j < len(o2):
            n1 = o1[i]
            n2 = o2[j]
            if n2 in after_dict[n1]:
                res.append(n1)
                i += 1
            else:
                res.append(n2)
                j += 1

        while i < len(o1):
            n1 = o1[i]
            res.append(n1)
            i += 1

        while j < len(o2):
            n2 = o2[j]
            res.append(n2)
            j += 1

        return res

    return mergesort(ordering)


def part1():
    rules, orderings = parse_inputs()
    after_dict = defaultdict(set)
    for before, after in rules:
        after_dict[before].add(after)

    middle_sum = 0
    for ordering in orderings:
        if check_ordering(ordering, after_dict):
            middle_sum += ordering[len(ordering) // 2]
    return middle_sum


def part2():
    rules, orderings = parse_inputs()
    after_dict = defaultdict(set)
    for before, after in rules:
        after_dict[before].add(after)

    middle_sum = 0
    for ordering in orderings:
        if not check_ordering(ordering, after_dict):
            ordering = sort_ordering(ordering, after_dict)
            middle_sum += ordering[len(ordering) // 2]
    return middle_sum


s1 = part1()
print("Solution Part 1:", s1)
s2 = part2()
print("Solution Part 2:", s2)
