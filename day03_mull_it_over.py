# Day 3: Mull It Over
# https://adventofcode.com/2024/day/3

import re
from typing import List

from utils.input import read_input_file_lines


def parse_inputs():
    lines = read_input_file_lines("day03_input.txt")
    return "".join(lines)


# Pattern for mul(a,b) in expression
MULL_PATTERN = r"mul\([0-9]*,[0-9]*\)"

# Patterns for do(), don't() sections in expression
# First pattern ends at first don't()
FIRST_DO_PATTERN = r"^.*?don\'t\(\)"
# Middle patterns are lazy searchs for do()...don't()
MIDDLE_DO_PATTERN = r"do\(\).*?don\'t\(\)"
# Last pattern for any do() to end of expr
LAST_DO_PATTERN = r"do\(\)((?!don\'t\(\)).)*$"


def calculate_mul(mul: str) -> int:
    # expect mul(a, b) -> a * b
    comma_idx = mul.find(",")
    a = int(mul[4:comma_idx])
    b = int(mul[comma_idx + 1 : -1])
    return a * b


def calculate_mul_total_for_expr(expr: str) -> int:
    muls = re.findall(MULL_PATTERN, expr)
    total_sum = 0
    for mul in muls:
        total_sum += calculate_mul(mul)
    return total_sum


def filter_do_sections(expr: str):
    # Starting section
    first: List[str] = re.findall(FIRST_DO_PATTERN, expr)

    # Middle sections
    middle: List[str] = re.findall(MIDDLE_DO_PATTERN, expr)

    # Add if ending section
    last: List[str] = re.findall(LAST_DO_PATTERN, expr)

    return "".join(first + middle + last)


def part1():
    expr = parse_inputs()
    return calculate_mul_total_for_expr(expr)


def part2():
    # chop up and extra only sections of do's
    expr = parse_inputs()
    expr = filter_do_sections(expr)
    return calculate_mul_total_for_expr(expr)


s1 = part1()
print("Solution Part 1:", s1)
s2 = part2()
print("Solution Part 2:", s2)
