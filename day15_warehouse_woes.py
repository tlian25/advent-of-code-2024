# Day 15: Warehouse Woes
# https://adventofcode.com/2024/day/15

from typing import *
from collections import *
from utils.input import read_input_file_lines


WALL = "#"
BOX = "O"
BOX_LEFT = "["
BOX_RIGHT = "]"
ROBOT = "@"
SPACE = "."

DIRS = {"^": (-1, 0), "v": (1, 0), ">": (0, 1), "<": (0, -1)}


def parse_inputs():
    lines = read_input_file_lines("day15_input.txt")
    grid = []
    moves = []
    for l in lines:
        if WALL in l:
            grid.append(list(l))
        elif l:
            moves += list(l)
    return grid, moves


def parse_inputs_2():
    DOUBLE = {
        WALL: WALL * 2,
        ROBOT: ROBOT + SPACE,
        SPACE: SPACE * 2,
        BOX: BOX_LEFT + BOX_RIGHT,
    }
    lines = read_input_file_lines("day15_input.txt")
    grid = []
    moves = []
    for l in lines:
        if WALL in l:
            grid.append(
                list(
                    l.replace(WALL, DOUBLE[WALL])
                    .replace(SPACE, DOUBLE[SPACE])
                    .replace(BOX, DOUBLE[BOX])
                    .replace(ROBOT, DOUBLE[ROBOT])
                )
            )
        elif l:
            moves += list(l)
    return grid, moves


class Grid:
    def __init__(self, grid):
        self.grid = grid
        self.nrows = len(grid)
        self.ncols = len(grid[0])
        self._pos = self._locate_robot()

    def _itercells(self):
        for r in range(self.nrows):
            for c in range(self.ncols):
                yield (r, c)

    def _locate_robot(self):
        for r, c in self._itercells():
            if self.grid[r][c] == ROBOT:
                return r, c

    def move(self, dir: str):
        r, c = self._pos
        if self._move(r, c, dir):
            dr, dc = DIRS[dir]
            nr, nc = r + dr, c + dc
            self.grid[r][c] = SPACE
            self._pos = (nr, nc)
            assert self.grid[nr][nc] == ROBOT
        # Else can't move

    def _move(self, r, c, dir: str) -> bool:
        """Recursive to shift all boxes in direction.
        Return True if can move. Else False."""
        dr, dc = DIRS[dir]
        nr, nc = r + dr, c + dc
        if self.grid[nr][nc] == WALL:
            return False
        elif self.grid[nr][nc] == SPACE:
            self.grid[nr][nc] = self.grid[r][c]
            return True
        # If next space is a Box, try to recursively move the Box
        elif self._move(nr, nc, dir):
            self.grid[nr][nc] = self.grid[r][c]
            return True
        return False

    def calculate_gps_sum(self):
        s = 0
        for r, c in self._itercells():
            if self.grid[r][c] == BOX:
                s += self._get_gps_coordinates(r, c)
        return s

    def _get_gps_coordinates(self, r, c):
        return r * 100 + c

    def __str__(self):
        s = "\n".join(["".join(g) for g in self.grid]) + "\n"
        return s


class Grid2:
    def __init__(self, grid):
        self.grid = grid
        self.nrows = len(grid)
        self.ncols = len(grid[0])
        self._pos = self._locate_robot()

    def _itercells(self):
        for r in range(self.nrows):
            for c in range(self.ncols):
                yield (r, c)

    def _locate_robot(self):
        for r, c in self._itercells():
            if self.grid[r][c] == ROBOT:
                return r, c

    def move(self, dir: str):
        r, c = self._pos
        if dir in ("<", ">"):
            if self._move_horizontal(r, c, dir):
                dr, dc = DIRS[dir]
                nr, nc = r + dr, c + dc
                self.grid[r][c] = SPACE
                self._pos = (nr, nc)
            return

        moves = {}
        if self._check_move_vertical(r, {c}, dir, moves):
            self._move_vertical(dir, moves)
            dr, dc = DIRS[dir]
            nr, nc = r + dr, c + dc
            self.grid[r][c] = SPACE
            self._pos = (nr, nc)

    def _move_horizontal(self, r, c, dir: str) -> bool:
        """Recursive to shift all boxes in direction.
        Return True if can move. Else False."""
        assert dir in {"<", ">"}
        dr, dc = DIRS[dir]
        nr, nc = r + dr, c + dc
        if self.grid[nr][nc] == WALL:
            return False
        # If next space is a Box, find both cells of box and try to move both recursively
        elif self.grid[nr][nc] == SPACE or self._move_horizontal(nr, nc, dir):
            self.grid[nr][nc] = self.grid[r][c]
            self.grid[r][c] = SPACE
            return True
        return False

    def _check_move_vertical(self, r, cs: Set[int], dir: str, moves: dict) -> bool:
        moves[r] = cs.copy()
        assert dir in {"^", "v"}
        dr, dc = DIRS[dir]
        nr = r + dr
        ncs = cs

        spaces = set()
        to_add = set()
        for c in ncs:
            if self.grid[nr][c] == WALL:
                return False
            elif self.grid[nr][c] == SPACE:
                spaces.add(c)
            elif self.grid[nr][c] == BOX_LEFT:
                to_add.add(c + 1)
            elif self.grid[nr][c] == BOX_RIGHT:
                to_add.add(c - 1)
            else:
                raise RuntimeError("Unexpecated symbol", self.grid[nr][c])

        # No walls, all next moves are spaces
        if spaces == ncs:
            return True

        # Recurisvely check all remaining
        ncs = (ncs - spaces).union(to_add)

        return self._check_move_vertical(nr, ncs, dir, moves)

    def _move_vertical(self, dir: str, moves: dict):
        assert dir in ("v", "^")
        rows = list(moves.keys())
        rows.sort(reverse=dir == "v")

        dr, dc = DIRS[dir]
        for r in rows:
            for c in moves[r]:
                nr = r + dr
                assert self.grid[nr][c] == SPACE
                self.grid[nr][c] = self.grid[r][c]
                self.grid[r][c] = SPACE

    def calculate_gps_sum(self):
        s = 0
        for r, c in self._itercells():
            if self.grid[r][c] == BOX_LEFT:
                s += self._get_gps_coordinates(r, c)
        return s

    def _get_gps_coordinates(self, r, c):
        return r * 100 + c

    def __str__(self):
        s = "\n".join(["".join(g) for g in self.grid]) + "\n"
        return s


def part1():
    grid, moves = parse_inputs()
    grid = Grid(grid)

    for m in moves:
        grid.move(m)

    # print(grid)
    return grid.calculate_gps_sum()


def part2():
    grid, moves = parse_inputs_2()
    grid = Grid2(grid)

    for m in moves:
        grid.move(m)
        # print(grid)
        # input()

    return grid.calculate_gps_sum()


s1 = part1()
print("Solution Part 1:", s1)
s2 = part2()
print("Solution Part 2:", s2)
