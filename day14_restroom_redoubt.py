# Day 14: Restroom Redoubt
# https://adventofcode.com/2024/day/14

from typing import *
from collections import *
from enum import Enum
from utils.input import read_input_file_lines


def parse_inputs():
    lines = read_input_file_lines("day14_input.txt")
    robots = [l.split() for l in lines]
    return robots


class Robot:
    def __init__(self, pos: str, vel: str):
        self._pos = self._parse_pos(pos)
        self._vel = self._parse_vel(vel)

    def _parse_pos(self, pos: str) -> List[int]:
        s = pos.split(",")
        return [int(s[0][2:]), int(s[1])]

    def _parse_vel(self, vel: str) -> Tuple[int]:
        s = vel.split(",")
        return (int(s[0][2:]), int(s[1]))

    def move(self, times: int, dim: Tuple[int, int]):
        self._pos[0] = (self._pos[0] + self._vel[0] * times) % dim[0]
        self._pos[1] = (self._pos[1] + self._vel[1] * times) % dim[1]
        return self._pos


class Quad(Enum):
    TOP_LEFT = 1
    TOP_RIGHT = 2
    BOT_LEFT = 3
    BOT_RIGHT = 4
    NONE = 5


def find_quadrant(pos: Tuple[int, int], dim: Tuple[int, int]) -> Quad:
    midx = dim[0] // 2
    midy = dim[1] // 2

    if pos[0] < midx:
        if pos[1] < midy:
            return Quad.BOT_LEFT
        elif pos[1] > midy:
            return Quad.BOT_RIGHT
    elif pos[0] > midx:
        if pos[1] < midy:
            return Quad.TOP_LEFT
        elif pos[1] > midy:
            return Quad.TOP_RIGHT
    return Quad.NONE


def part1():
    robots = parse_inputs()
    quads = defaultdict(int)
    times = 100
    dim = (101, 103)
    for r in robots:
        robot = Robot(*r)
        pos = robot.move(times, dim)
        quad = find_quadrant(pos, dim)
        quads[quad] += 1

    return (
        quads[Quad.TOP_LEFT]
        * quads[Quad.BOT_LEFT]
        * quads[Quad.TOP_RIGHT]
        * quads[Quad.BOT_RIGHT]
    )


def move_all_robots(robot_list: List[Robot], dim: Tuple[int, int]):
    for robot in robot_list:
        robot.move(1, dim)


def print_robots(robot_list: List[Robot], dim: Tuple[int, int]) -> Tuple[str, bool]:
    """Create string representation of grid. Also return if grid is valid or not
    by checking if any of the robots overlap on the grid."""
    X = dim[0]
    Y = dim[1]
    grid = [[" " for _ in range(X)] for _ in range(Y)]

    for robot in robot_list:
        x, y = robot._pos
        # Can't have two robots on same square so end early
        if grid[y][x] == "#":
            return "", False
        grid[y][x] = "#"

    s = []
    for g in grid:
        s.append("".join(g) + "\n")
    return "".join(s), True


def part2():
    robots = parse_inputs()
    robot_list = [Robot(*r) for r in robots]
    dim = (101, 103)  # X, Y

    steps = 0
    while True:
        steps += 1
        print("\rSteps", steps, end="")
        move_all_robots(robot_list, dim)
        s, valid = print_robots(robot_list, dim)
        if valid:
            print(s)
            end = input("Enter any character to end:")
            if end:
                return steps


s1 = part1()
print("Solution Part 1:", s1)
s2 = part2()
print("Solution Part 2:", s2)
