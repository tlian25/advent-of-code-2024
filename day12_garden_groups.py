# Day 12: Garden Groups
# https://adventofcode.com/2024/day/12

from utils.input import read_input_file_lines
from collections import deque
from typing import List


def parse_inputs():
    lines = read_input_file_lines("day12_input.txt")
    grid = [list(l) for l in lines]
    return grid


class CardDir:
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"


DIRS = [
    (0, 1, CardDir.RIGHT),
    (1, 0, CardDir.DOWN),
    (0, -1, CardDir.LEFT),
    (-1, 0, CardDir.UP),
]


def floodfill(grid: List[List[int]], r: int, c: int, part2: bool = False) -> int:
    """Return cost of a flood fill"""
    # For perimeter, track border to figure out number of sides
    # Track count for area
    LETTER = grid[r][c]
    seen = {(r, c)}
    border = set()  # track border squares
    nrows, ncols = len(grid), len(grid[0])
    area = 0
    perimeter = 0
    q = deque([(r, c)])
    while q:
        r, c = q.popleft()
        area += 1

        for dr, dc, cardir in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < nrows and 0 <= nc < ncols:
                if (nr, nc) in seen:
                    continue
                elif grid[nr][nc] == LETTER:
                    seen.add((nr, nc))
                    q.append((nr, nc))
                else:
                    border.add((r, c, cardir))
                    perimeter += 1
            else:
                border.add((r, c, cardir))
                perimeter += 1

    if part2:
        perimeter = calculate_sides(border)
    cost = perimeter * area
    # print(LETTER, perimeter, area, cost)
    return cost, seen


def part1():
    grid = parse_inputs()
    nrows, ncols = len(grid), len(grid[0])

    total_cost = 0
    global_seen = set()
    for r in range(nrows):
        for c in range(ncols):
            if (r, c) not in global_seen:
                cost, seen = floodfill(grid, r, c)
                total_cost += cost
                global_seen = global_seen.union(seen)

    return total_cost


def calculate_sides(border: set) -> int:
    sides = 0

    while border:
        # check a random border and removing any on the same left
        sides += 1
        row, col, cardir = border.pop()

        if cardir in (CardDir.DOWN, CardDir.UP):
            # check left and right and remove any other border squares
            dir = (0, 1)
        else:
            dir = (1, 0)

        nr, nc = row + dir[0], col + dir[1]
        # Remove all squares on the same edge moving one direction
        while (nr, nc, cardir) in border:
            border.remove((nr, nc, cardir))
            nr, nc = nr + dir[0], nc + dir[1]

        nr, nc = row - dir[0], col - dir[1]
        # Remove all squares on the same edge moving the other direction
        while (nr, nc, cardir) in border:
            border.remove((nr, nc, cardir))
            nr, nc = nr - dir[0], nc - dir[1]

    return sides


def part2():
    grid = parse_inputs()
    nrows, ncols = len(grid), len(grid[0])

    total_cost = 0
    global_seen = set()
    for r in range(nrows):
        for c in range(ncols):
            if (r, c) not in global_seen:
                cost, seen = floodfill(grid, r, c, True)
                total_cost += cost
                global_seen = global_seen.union(seen)

    return total_cost


s1 = part1()
print("Solution Part 1:", s1)
s2 = part2()
print("Solution Part 2:", s2)
