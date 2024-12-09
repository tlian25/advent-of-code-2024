# Day 8. Resonant Collinearity
# https://adventofcode.com/2024/day/8

from collections import defaultdict
from itertools import combinations

from utils.input import read_input_file_lines

ANTINODE = "#"
SPACE = "."


def parse_inputs():
    lines = read_input_file_lines("day08_input.txt")
    grid = [list(l) for l in lines]
    return grid


def get_positions(grid) -> dict:
    positions_dict = defaultdict(set)
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            symbol = grid[r][c]
            if symbol != SPACE:
                positions_dict[symbol].add((r, c))
    return positions_dict


def place_antinode(grid, pos1, pos2, part2: bool = False):
    # Part 2 indicates we continue placing along same line
    r1, c1 = pos1
    r2, c2 = pos2
    if r1 > r2:
        r1, c1, r2, c2 = r2, c2, r1, c1

    nrows, ncols = len(grid), len(grid[0])

    dr, dc = r2 - r1, c2 - c1
    new_antinodes = set()
    # Antinode 1
    ar1, ac1 = r1 - dr, c1 - dc
    while 0 <= ar1 < nrows and 0 <= ac1 < ncols:
        grid[ar1][ac1] = ANTINODE
        new_antinodes.add((ar1, ac1))
        if not part2:
            break
        ar1 -= dr
        ac1 -= dc

    # Antinode 2
    ar2, ac2 = r2 + dr, c2 + dc
    while 0 <= ar2 < nrows and 0 <= ac2 < ncols:
        grid[ar2][ac2] = ANTINODE
        new_antinodes.add((ar2, ac2))
        if not part2:
            break
        ar2 += dr
        ac2 += dc


def place_antinodes(grid, positions_dict: dict):
    for symbol, positions in positions_dict.items():
        for p1, p2 in combinations(positions, 2):
            place_antinode(grid, p1, p2)


def place_antinodes_2(grid, positions_dict):
    # Extend to grid edge in both directions
    for symbol, positions in positions_dict.items():
        for p1, p2 in combinations(positions, 2):
            place_antinode(grid, p1, p2, True)


def count_antinodes(grid):
    # Count new antinodes only. Don't count antennas.
    count = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == ANTINODE:
                count += 1
    return count


def count_antinodes_2(grid):
    # Count antennas as well as antinodes. Anything not a space.
    count = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] != SPACE:
                count += 1
    return count


def part1():
    grid = parse_inputs()
    positions_dict = get_positions(grid)
    place_antinodes(grid, positions_dict)
    count = count_antinodes(grid)
    return count


def part2():
    grid = parse_inputs()
    positions_dict = get_positions(grid)
    place_antinodes_2(grid, positions_dict)
    count = count_antinodes_2(grid)
    return count


s1 = part1()
print("Solution Part 1:", s1)
s2 = part2()
print("Solution Part 2:", s2)
