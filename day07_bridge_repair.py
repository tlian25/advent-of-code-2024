# Day 7: Bridge Repair
# https://adventofcode.com/2024/day/7

from typing import List, Tuple

from utils.input import read_input_file_lines


def parse_inputs() -> List[Tuple[int, List]]:
    lines = read_input_file_lines("day07_input.txt")
    equations = []
    for l in lines:
        test_val, nums = l.split(": ")
        test_val = int(test_val)
        nums = [int(x) for x in nums.split()]
        equations.append((test_val, nums))

    return equations


def concatenate(n1: int, n2: int) -> int:
    return int(str(n1) + str(n2))


def check_valid_operation_exists(test_val: int, nums: List[int]) -> bool:
    """DFS search of operations to see if we can find a combination
    that matches test_val"""

    # i = current index in nums
    # val = current operation val
    def dfs(i, val):
        if i == len(nums) - 1:
            if val == test_val:
                return True
            return False

        # Search forward ADD
        if dfs(i + 1, val + nums[i + 1]):
            return True
        # Search forward MULT
        if dfs(i + 1, val * nums[i + 1]):
            return True
        return False

    return dfs(0, nums[0])


def check_valid_operation_exists_part2(test_val: int, nums: List[int]) -> bool:
    """DFS search of operations to see if we can find a combination
    that matches test_val. Part2 allow || concatenation operation"""

    # i = current index in nums
    # val = current operation val
    def dfs(i, val):
        if i == len(nums) - 1:
            if val == test_val:
                return True
            return False

        # Search forward ADD
        if dfs(i + 1, val + nums[i + 1]):
            return True
        # Search forward MULT
        if dfs(i + 1, val * nums[i + 1]):
            return True
        # Search forward CONCAT
        if dfs(i + 1, concatenate(val, nums[i + 1])):
            return True
        return False

    return dfs(0, nums[0])


def part1():
    equations = parse_inputs()

    valid_sum = 0
    for test_val, nums in equations:
        if check_valid_operation_exists(test_val, nums):
            valid_sum += test_val
    return valid_sum


def part2():
    equations = parse_inputs()

    valid_sum = 0
    for test_val, nums in equations:
        if check_valid_operation_exists_part2(test_val, nums):
            valid_sum += test_val
    return valid_sum


s1 = part1()
print("Solution Part 1:", s1)
s2 = part2()
print("Solution Part 2:", s2)
