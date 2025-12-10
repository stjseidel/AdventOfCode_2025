#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 06:32:12 2023

@author: stjse
"""

from itertools import combinations
from timeit import default_timer as timer

from aoc_class import AOC


class Today(AOC):

    @staticmethod
    def calc_area(a, b):
        return (abs(b[0] - a[0]) + 1) * (abs(b[1] - a[1]) + 1)

    def parse_lines(self):
        lines = self.lines
        lines = [tuple(int(x) for x in line.split(',')) for line in lines]
        return lines

    def part1(self):
        lines = self.parse_lines()
        combos = combinations(lines, 2)
        max_size = 0
        for combo in combos:
            area = self.calc_area(*combo)
            max_size = max(area, max_size)

        self.result1 = max_size
        self.time1 = timer()
        return self.result1

    def part2(self):
        lines = self.parse_lines()
        self.result2 = "TODO"
        self.time2 = timer()
        return self.result2


if __name__ == "__main__":
    # prep
    today = Today(day="", simple=True)
    today.create_txt_files()

    # simple part 1
    today.set_lines(simple=True)
    today.part1()
    print(f"Part 1 <SIMPLE> result is: {today.result1}")

# =============================================================================
# hard part 1
    today.set_lines(simple=False)
    today.part1()
    print(f'Part 1 <HARD> result is: {today.result1}')
    today.stop()
# =============================================================================


# =============================================================================
# # simple part 2
#     today.set_lines(simple=True)
#     today.part2()
#     print(f'Part 2 <SIMPLE> result is: {today.result2}')
# =============================================================================

# =============================================================================
# # hard part 2
#     today.set_lines(simple=False)
#     today.part2()
#     print(f'Part 2 <HARD> result is: {today.result2}')
#     today.stop()
#     today.print_final()
# =============================================================================
