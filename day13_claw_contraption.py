# Day 13: Claw Contraption
# https://adventofcode.com/2024/day/13

from utils.input import read_input_file_lines
from typing import Tuple
from heapq import heappush, heappop


def parse_inputs():
    lines = read_input_file_lines("day13_input.txt")
    games = []
    curr_game = []
    for l in lines:
        if l == "":
            games.append(curr_game)
            curr_game = []
        else:
            curr_game.append(l)

    if curr_game:
        games.append(curr_game)

    return games


class Game:
    def __init__(
        self, buttonAstr: str, buttonBstr: str, prizeStr: str, offset: int = 0
    ):
        # parse strings
        self._A = self._parseButton(buttonAstr, 3)
        self._B = self._parseButton(buttonBstr, 1)
        self._prize = self._parsePrize(prizeStr, offset)
        # print(self._A, self._B, self._prize)

    def _parseButton(self, buttonstr: str, cost: int) -> Tuple[int, int]:
        s = buttonstr.split()
        x = int(s[2][2:-1])
        y = int(s[3][2:])
        return (cost, x, y)

    def _parsePrize(self, prizeStr: str, offset: int) -> Tuple[int, int]:
        s = prizeStr.split()
        x = int(s[1][2:-1]) + offset
        y = int(s[2][2:]) + offset
        return (x, y)

    def find_cheapest_path(
        self, startcost: int = 0, startx: int = 0, starty: int = 0, seen: dict = {}
    ):
        # cost, x_pos, y_pos
        h = [(startcost, startx, starty)]
        while h:
            c, x, y = heappop(h)
            if (x, y) == self._prize:
                return c

            for dc, dx, dy in (self._A, self._B):
                nc, nx, ny = c + dc, x + dx, y + dy
                if nx > self._prize[0] or ny > self._prize[1]:

                    continue
                if (nx, ny) not in seen or seen[(nx, ny)] > nc:
                    seen[(nx, ny)] = nc
                    heappush(h, (nc, nx, ny))

        return -1

    def find_cheapest_path2(self):
        # Solve for linear equation
        """
        n * a1 + m * b1 = x
        n * a2 + m * b2 = y

        n = (x - m * b1) / a1

        (x - m * b1) * a2 / a1 + m * b2 = y
        (x - m * b1) * a2 + (m * a1 * b2) = a1 * y
        (a2 * x) - (m * b1 * a2) + (a1 * b2 * m) = a1 * y
        m * (a1 * b2 - a2 * b1) = (a1 * y - a2 * x)
        m = (a1 * y - a2 * x) / (a1 * b2 - a2 * b1)
        """
        x, y = self._prize
        c1, a1, a2 = self._A
        c2, b1, b2 = self._B

        m = (a1 * y - a2 * x) / (a1 * b2 - a2 * b1)
        n = (x - m * b1) / a1

        if m == int(m) and n == int(n) and m >= 0 and n >= 0:
            assert x == n * a1 + m * b1
            assert y == n * a2 + m * b2
            return int(c1 * n + c2 * m)
        return -1


def part1():
    games = parse_inputs()
    total_cost = 0
    for g in games:
        gm = Game(*g)
        cost = gm.find_cheapest_path()
        if cost >= 0:
            total_cost += cost

    return total_cost


def part2():
    games = parse_inputs()
    total_cost = 0
    offset = 10000000000000
    for g in games:
        gm = Game(*g, offset)
        cost = gm.find_cheapest_path2()
        if cost >= 0:
            total_cost += cost

    return total_cost


s1 = part1()
print("Solution Part 1:", s1)
s2 = part2()
print("Solution Part 2:", s2)
