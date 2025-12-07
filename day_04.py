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
        return lines

    def part1(self):
        lines = self.parse_lines()
        positions = self.grid_make_all_positions(ignore_chars=".")
        movable = []
        for pos in positions:
            neighbors = self.get_neighbors_rose(position=pos).intersection(positions)
            if len(neighbors) < 4:
                movable.append(pos)

        self.result1 = len(movable)
        self.time1 = timer()
        return self.result1

    def part2(self):
        lines = self.parse_lines()
        positions = self.grid_make_all_positions(ignore_chars=".")
        base_count = len(positions)
        intermediate_count = base_count
        new_count = 0
        while intermediate_count != new_count:
            intermediate_count = len(positions)
            ref_list = positions.copy()
            for pos in ref_list:
                neighbors = self.get_neighbors_rose(position=pos).intersection(
                    positions
                )
                if len(neighbors) < 4:
                    positions.remove(pos)
            new_count = len(positions)

        self.result2 = base_count - len(positions)
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
