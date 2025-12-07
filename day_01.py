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
        lines = [(-1 if line[0] == "L" else 1, int(line[1:])) for line in lines]

        return lines

    def part1(self):
        lines = self.parse_lines()
        start_pos = 50
        pos = start_pos
        password = 0
        # print("Start pos:", pos)
        for line in lines:
            # print(pos, line)
            pos = abs((pos + line[0] * line[1]) % 100)
            if pos == 0:
                password += 1
            # print(pos, password)
        self.result1 = password
        self.time1 = timer()
        return self.result1

    def part2(self):
        lines = self.parse_lines()
        start_pos = 50
        pos = start_pos
        password = 0
        for line in lines:
            new_pos = pos + line[0] * line[1]

            if (new_pos <= 0 and pos != 0) or new_pos > 99:
                password += 1

            direction, steps = line[0], line[1]
            if direction == 1:
                distance_to_threshold = 100 - pos
            else:
                distance_to_threshold = pos
            steps_after_threshold = steps - distance_to_threshold
            if steps_after_threshold > 0:
                password += steps_after_threshold // 100
            pos = abs((pos + line[0] * line[1]) % 100)
        self.result2 = password
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
