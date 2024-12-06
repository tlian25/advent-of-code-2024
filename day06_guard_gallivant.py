# Day 6: Guard Gallivant
# https://adventofcode.com/2024/day/6


from collections import defaultdict
from typing import List, Tuple

from utils.input import read_input_file_lines


def parse_inputs():
    lines = read_input_file_lines("day06_input.txt")
    grid = [list(l) for l in lines]
    return grid


BLOCK = "#"
NEW_BLOCK = "X"
UNSEEN = "."
CROSS = "+"
DIRS = [(-1, 0, "^"), (0, 1, ">"), (1, 0, "v"), (0, -1, "<")]


def get_guard_starting_loc(grid) -> Tuple[int]:
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "^":
                return r, c


def get_next_diridx(i: int) -> int:
    return (i + 1) % 4


def move(grid: List[List[int]], r: int, c: int, i: int) -> Tuple[int, int]:
    """
    Starting at (r, c), move one step in direction of i and return next position and i.
    If blocked, then update i and return same position
    """
    dr, dc, symbol = DIRS[i]
    nr, nc = r + dr, c + dc
    if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
        if grid[nr][nc] == BLOCK:
            i = get_next_diridx(i)
            grid[r][c] = DIRS[i][2]
            return r, c, i
        else:
            if grid[nr][nc] == UNSEEN:
                grid[nr][nc] = symbol
            else:
                grid[nr][nc] = CROSS
            return nr, nc, i
    else:
        return -1, -1, i  # Move off grid indicated by -1


def move_thru_grid(grid) -> int:
    r, c = get_guard_starting_loc(grid)
    i = 0  # starting direction
    seen = {(r, c, i)}
    while r >= 0:
        r, c, i = move(grid, r, c, i)
        if (r, c, i) in seen:
            return -2  # Indicate a cycle by -2
        seen.add((r, c, i))
    return r


def print_grid(grid):
    for g in grid:
        print("".join(g))
    print()


def copy_grid(grid):
    gridcopy = [g.copy() for g in grid]
    return gridcopy


def part1():
    grid = parse_inputs()
    move_thru_grid(grid)

    # Count seen spaces
    seen_count = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] not in {UNSEEN, BLOCK}:
                seen_count += 1

    # print_grid(grid)
    return seen_count


def part2():
    originalgrid = parse_inputs()
    griddefault = copy_grid(originalgrid)

    move_thru_grid(griddefault)

    # Look at every possible place to put an obstable
    # Take every location the guard travels by default and try putting a block there
    obstacle_locations = set()
    for r in range(len(griddefault)):
        for c in range(len(griddefault[0])):
            # For crosses, try putting a block in all 4 directions
            if griddefault[r][c] == "+":
                for dr, dc, _ in DIRS:
                    nr, nc = r + dr, c + dc
                    obstacle_locations.add((nr, nc))
                continue

            # For non-crosses, put a block in front
            for dr, dc, symbol in DIRS:
                if griddefault[r][c] == symbol:
                    nr, nc = r + dr, c + dc
                    obstacle_locations.add((nr, nc))
                    break

    # For each possible obstacle location, try placing and seeing if it causes a loop
    count = 0
    for _r, _c in obstacle_locations:
        if 0 <= _r < len(originalgrid) and 0 <= _c < len(originalgrid[0]):
            if originalgrid[_r][_c] == UNSEEN:
                # Make a copy of original grid
                gridcopy = copy_grid(originalgrid)
                gridcopy[_r][_c] = BLOCK

                res = move_thru_grid(gridcopy)

                if res == -2:
                    count += 1

    return count


s1 = part1()
print("Solution Part 1:", s1)
s2 = part2()
print("Solution Part 2:", s2)
