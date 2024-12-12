# Day 10: Hoof It
# https://adventofcode.com/2024/day/10

from utils.input import read_input_file_lines
from collections import deque


def parse_inputs():
    lines = read_input_file_lines("day10_input.txt")
    grid = [[int(x) for x in l] for l in lines]
    return grid


DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def bfs(grid, r, c, part2: bool = False) -> int:
    nrows, ncols = len(grid), len(grid[0])
    q = deque()
    q.append((r, c, grid[r][c]))
    seen = set()
    seen.add((r, c))
    count = 0
    while q:
        r, c, lvl = q.popleft()

        if lvl == 9:
            count += 1
            continue

        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < nrows and 0 <= nc < ncols:
                if (nr, nc) not in seen and grid[nr][nc] == lvl + 1:
                    if not part2:
                        seen.add((nr, nc))
                    q.append((nr, nc, lvl + 1))

    return count


def part1():
    grid = parse_inputs()
    nrows, ncols = len(grid), len(grid[0])

    total_count = 0
    for r in range(nrows):
        for c in range(ncols):
            if grid[r][c] == 0:
                total_count += bfs(grid, r, c)
    return total_count


def part2():
    grid = parse_inputs()
    nrows, ncols = len(grid), len(grid[0])

    total_count = 0
    for r in range(nrows):
        for c in range(ncols):
            if grid[r][c] == 0:
                total_count += bfs(grid, r, c, True)
    return total_count


s1 = part1()
print("Solution Part 1:", s1)
s2 = part2()
print("Solution Part 2:", s2)
