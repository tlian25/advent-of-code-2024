# Day 2: Red Nosed Reports
# https://adventofcode.com/2024/day/2

from typing import List

from utils.input import read_input_file_lines


def parse_inputs():
    lines = read_input_file_lines("day02_input.txt")
    reports = []
    for l in lines:
        reports.append([int(x) for x in l.split()])
    return reports


def check_report_is_safe(report: List[int]) -> bool:
    if report[0] < report[1]:
        increasing = True
    else:
        increasing = False

    diffmin, diffmax = 1, 3
    for i in range(1, len(report)):
        n1, n2 = report[i - 1], report[i]
        if increasing:
            if not (n1 < n2 and diffmin <= n2 - n1 <= diffmax):
                return False
        else:
            if not (n1 > n2 and diffmin <= n1 - n2 <= diffmax):
                return False
    return True


def check_dampened_report_is_safe(report: List[int]) -> bool:
    for i in range(len(report)):
        # Remove i-th element from report and check if safe
        dampened_report = report[:i] + report[i + 1 :]
        if check_report_is_safe(dampened_report):
            return True
    return False


def part1():
    reports = parse_inputs()

    safe_count = 0
    for report in reports:
        if check_report_is_safe(report):
            safe_count += 1
    return safe_count


def part2():
    reports = parse_inputs()

    safe_count = 0
    for report in reports:
        if check_report_is_safe(report):
            safe_count += 1
        elif check_dampened_report_is_safe(report):
            safe_count += 1
    return safe_count


s1 = part1()
print("Solution Part 1:", s1)
s2 = part2()
print("Solution Part 2:", s2)
