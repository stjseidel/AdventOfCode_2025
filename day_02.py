#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 06:32:12 2023

@author: stjse
"""

from timeit import default_timer as timer

from aoc_class import AOC


class Today(AOC):

    def parse_lines(self):
        lines = self.lines
        lines = lines[0].split(",")
        return lines

    def part1(self):
        lines = self.parse_lines()
        self.invalid = []
        for line in lines:
            a, b = [int(x) for x in line.split("-")]
            self.check_range(a, b)
        self.result1 = sum(self.invalid)
        self.time1 = timer()
        return self.result1

    def check_range(self, a, b):
        for i in range(a, b + 1):
            if len(str(i)) % 2 != 0:
                continue
            digits = len(str(i)) // 2

            if str(i)[:digits] == str(i)[-digits:]:
                self.invalid.append(i)
                # print(a, b, i, str(i)[:digits], str(i)[-digits:])

    def part2(self):
        lines = self.parse_lines()
        self.invalid = []
        for line in lines:
            a, b = [int(x) for x in line.split("-")]
            self.check_range_any(a, b)
        self.result2 = sum(self.invalid)
        self.time2 = timer()
        return self.result2

    def check_range_any(self, a, b):
        for i in range(a, b + 1):
            found = False
            for d in range(1, len(str(i)) // 2 + 1):
                if str(i)[:d] * (len(str(i)) // d) == str(i):
                    self.invalid.append(i)
                    found = True
                    break
            if found:
                continue


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
    print(f"Part 1 <HARD> result is: {today.result1}")
    today.stop()
    # =============================================================================

    # =============================================================================
    # simple part 2
    today.set_lines(simple=True)
    today.part2()
    print(f"Part 2 <SIMPLE> result is: {today.result2}")
    # =============================================================================

    # =============================================================================
    # hard part 2
    today.set_lines(simple=False)
    today.part2()
    print(f"Part 2 <HARD> result is: {today.result2}")
    today.stop()
    today.print_final()
# =============================================================================
