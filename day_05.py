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
        split = lines.index("")

        self.ranges = lines[:split]
        self.items = {int(char) for char in lines[split + 1 :]}
        return lines

    def part1(self):
        _ = self.parse_lines()
        fresh = set()
        ranges = []
        for range_line in self.ranges:
            limits = [int(char) for char in range_line.split("-")]
            ranges.append(range(limits[0], limits[1] + 1))

        for item in self.items:
            for r in ranges:
                if item in r:
                    fresh.add(item)
                    break
        self.result1 = len(fresh)
        self.time1 = timer()
        return self.result1

    def part2(self):
        _ = self.parse_lines()
        ranges = []
        for range_line in self.ranges:
            limits = [int(char) for char in range_line.split("-")]
            ranges.append([limits[0], limits[1] + 1])
        ranges_sorted = sorted(ranges, key=lambda r: r[0])
        ranges_merged = []
        last_start = ranges_sorted[0][0]
        last_stop = ranges_sorted[0][1]
        for start, stop in ranges_sorted:
            if start > last_stop:
                ranges_merged.append([last_start, last_stop])
                last_start = start
            last_start = min(start, last_start)
            last_stop = max(stop, last_stop)
        ranges_merged.append([last_start, last_stop])
        self.result2 = sum([stop - start for start, stop in ranges_merged])
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
