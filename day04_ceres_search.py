# Day 4: Ceres Search
# https://adventofcode.com/2024/day/4

from utils.input import read_input_file_lines


def parse_inputs():
    lines = read_input_file_lines("day04_input.txt")
    grid = [list(line) for line in lines]
    return grid


# For Part 1 search
DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
XMAS = ["X", "M", "A", "S"]


class XmasGrid:
    def __init__(self, grid):
        self.grid = grid
        self.nrows = len(grid)
        self.ncols = len(grid[0])
        self.count = 0

    def dfs_single_direction(self, r: int, c: int, i: int, dir: tuple) -> None:
        """DFS search keeping same direction"""
        if i == len(XMAS) - 1:
            self.count += 1
            return

        nr, nc = r + dir[0], c + dir[1]
        if 0 <= nr < self.nrows and 0 <= nc < self.ncols:
            if self.grid[nr][nc] == XMAS[i + 1]:
                self.dfs_single_direction(nr, nc, i + 1, dir)

    def dfs_all_directions(self, r: int, c: int, i: int) -> None:
        """Not used, but DFS search allowing change of directions"""
        if i == len(XMAS) - 1:
            self.count += 1
            return

        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.nrows and 0 <= nc < self.ncols:
                if self.grid[nr][nc] == XMAS[i + 1]:
                    self.dfs(nr, nc, i + 1)

    def search_all_xmas_single_direction(self) -> int:
        self.count = 0
        for r in range(self.nrows):
            for c in range(self.ncols):
                if self.grid[r][c] == XMAS[0]:
                    for dir in DIRS:
                        self.dfs_single_direction(r, c, 0, dir)
        return self.count

    def search_all_xmas_all_directions(self) -> int:
        self.count = 0
        for r in range(self.nrows):
            for c in range(self.ncols):
                if self.grid[r][c] == XMAS[0]:
                    for dir in DIRS:
                        self.dfs_all_directions(r, c, 0, dir)
        return self.count

    def search_xmas_shape(self, r, c) -> bool:
        """Look for the X-shaped MAS pattern instead by checking both diagonals

        M.S
        .A.
        M.S
        """
        diag1 = self.grid[r - 1][c - 1] + self.grid[r][c] + self.grid[r + 1][c + 1]
        diag2 = self.grid[r - 1][c + 1] + self.grid[r][c] + self.grid[r + 1][c - 1]
        for diag in (diag1, diag2):
            if diag not in ("MAS", "SAM"):
                return False
        return True

    def search_all_xmas_shapes(self) -> int:
        self.count = 0
        # since we are looking for X-shape, don't need to search outer edge
        for r in range(1, self.nrows - 1):
            for c in range(1, self.ncols - 1):
                if self.grid[r][c] == "A":
                    if self.search_xmas_shape(r, c):
                        self.count += 1
        return self.count


def part1():
    grid = parse_inputs()
    xmasGrid = XmasGrid(grid)
    return xmasGrid.search_all_xmas_single_direction()


def part2():
    grid = parse_inputs()
    xmasGrid = XmasGrid(grid)
    return xmasGrid.search_all_xmas_shapes()


s1 = part1()
print("Solution Part 1:", s1)
s2 = part2()
print("Solution Part 2:", s2)
