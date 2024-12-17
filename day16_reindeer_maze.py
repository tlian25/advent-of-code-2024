# Day 16: Reindeer Maze
# https://adventofcode.com/2024/day/16

from typing import *
from collections import *
from utils.input import read_input_file_lines
import sys

sys.setrecursionlimit(10000)


START = "S"
END = "E"
WALL = "#"
SPACE = "."


def parse_inputs():
    lines = read_input_file_lines("day16_input.txt")
    grid = [list(l) for l in lines]
    return grid


UP, DN, LT, RT = "^", "v", "<", ">"
DIRS = {DN: (1, 0), UP: (-1, 0), RT: (0, 1), LT: (0, -1)}


def turn_right(dir: str) -> str:
    if dir == UP:
        return RT
    if dir == RT:
        return DN
    if dir == DN:
        return LT
    if dir == LT:
        return UP


def turn_left(dir: str) -> str:
    if dir == UP:
        return LT
    if dir == LT:
        return DN
    if dir == DN:
        return RT
    if dir == RT:
        return UP


class Grid:
    def __init__(self, grid):
        self.grid = grid
        self.nrows = len(grid)
        self.ncols = len(grid[0])
        self.pos, self.end = self._find_start_and_end()
        self.best_paths = []
        self.best_score = float("inf")

    def _find_start_and_end(self):
        start, end = None, None
        for r in range(self.nrows):
            for c in range(self.ncols):
                if self.grid[r][c] == START:
                    start = (r, c)
                elif self.grid[r][c] == END:
                    end = (r, c)
        return (start, end)

    def is_inbounds(self, r, c) -> bool:
        return 0 <= r < self.nrows and 0 <= c < self.ncols and self.grid[r][c] != WALL

    def search_path_bfs(self):
        min_seen = {}
        min_seen[(self.pos[0], self.pos[1], RT)] = 0
        q = deque([(self.pos[0], self.pos[1], RT, 0)])
        while q:
            r, c, dir, score = q.popleft()

            # try 3 directions - curr dir, turn rt, turn lt
            # curr dir
            dr, dc = DIRS[dir]
            nr, nc = r + dr, c + dc
            nscore = score + 1
            if self.is_inbounds(nr, nc):
                if (nr, nc, dir) not in min_seen or min_seen[(nr, nc, dir)] > nscore:
                    min_seen[(nr, nc, dir)] = nscore
                    q.append((nr, nc, dir, nscore))

            # turn rt
            ndir = turn_right(dir)
            dr, dc = DIRS[ndir]
            nr, nc = r + dr, c + dc
            nscore = score + 1000 + 1
            if self.is_inbounds(nr, nc):
                if (nr, nc, dir) not in min_seen or min_seen[(nr, nc, dir)] > nscore:
                    min_seen[(nr, nc, ndir)] = nscore
                    q.append((nr, nc, ndir, nscore))

            ndir = turn_left(dir)
            dr, dc = DIRS[ndir]
            nr, nc = r + dr, c + dc
            nscore = score + 1000 + 1
            if self.is_inbounds(nr, nc):
                if (nr, nc, dir) not in min_seen or min_seen[(nr, nc, dir)] > nscore:
                    min_seen[(nr, nc, ndir)] = nscore
                    q.append((nr, nc, ndir, nscore))

        min_score = float("inf")
        for dir in DIRS.keys():
            k = (self.end[0], self.end[1], dir)
            if k in min_seen:
                min_score = min(min_score, min_seen[k])
        return min_score

    def merge_cells_all_best_paths(self):
        cells = set()
        for path in self.best_paths:
            for r, c, dir in path:
                cells.add((r, c))
        return cells

    def search_path_dfs(self):
        path = []
        min_seen = {}
        min_seen[(self.pos[0], self.pos[1], RT)] = 0

        def dfs(r, c, dir, score):
            path.append((r, c, dir))

            if (r, c) == self.end:
                if score == self.best_score:
                    self.best_paths.append(path.copy())
                elif score < self.best_score:
                    self.best_paths = [path.copy()]
                    self.best_score = score
                path.pop()
                return

            # Search in next directions - curr, left, right
            for ndir, nscore in [
                (dir, score + 1),
                (turn_left(dir), score + 1001),
                (turn_right(dir), score + 1001),
            ]:
                dr, dc = DIRS[ndir]
                nr, nc = r + dr, c + dc
                if self.is_inbounds(nr, nc):
                    if (nr, nc, ndir) not in min_seen or min_seen[
                        (nr, nc, ndir)
                    ] >= nscore:
                        min_seen[(nr, nc, ndir)] = nscore
                        dfs(nr, nc, ndir, nscore)

            path.pop()
            return

        dfs(self.pos[0], self.pos[1], RT, 0)


def part1():
    grid = parse_inputs()
    grid = Grid(grid)
    return grid.search_path_bfs()


def part2():
    grid = parse_inputs()
    grid = Grid(grid)
    grid.search_path_dfs()
    cells = grid.merge_cells_all_best_paths()
    return len(cells)


s1 = part1()
print("Solution Part 1:", s1)
s2 = part2()
print("Solution Part 2:", s2)
