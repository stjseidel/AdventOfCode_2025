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
        voltage = 0
        for line in lines:
            voltage += self.get_voltage(line)
        self.result1 = voltage
        self.time1 = timer()
        return self.result1

    def get_voltage(self, line):
        bats = [int(char) for char in line]
        first_bat = max(bats[:-1])
        first_bat_pos = bats.index(first_bat)
        last_bat = max(bats[first_bat_pos + 1 :])
        return int(str(first_bat) + str(last_bat))

    def part2(self):
        lines = self.parse_lines()
        voltage = 0
        for line in lines:
            voltage += self.get_voltage_2(line)
        self.result2 = voltage
        self.time2 = timer()
        return self.result2

    def remove_smaller_numbers(self, bats):
        start_slice = bats.index(max(bats[:-12]))
        bats = bats[start_slice:]
        current_pos = 0
        while len(bats) > 12:
            while (
                int(bats[current_pos]) < int(bats[current_pos + 1])
                and len(bats) > 12
                and current_pos < len(bats) - 2
            ):
                bats.pop(current_pos)
            current_pos += 1
            if len(bats) <= 12 or current_pos >= 11:
                while len(bats) > 12:
                    bats.pop(bats.index(min(bats)))
                voltage = self.list_to_int(bats[:12])
                return voltage
        return self.list_to_int(bats[:12])

    def get_voltage_2(self, line):
        bats = [int(char) for char in line]
        bats = self.preselect_maxima(bats)
        voltage = self.remove_smaller_numbers(bats)
        return voltage

    def preselect_maxima(self, bats):
        # preselecting maximums until the tail is too short
        maxes = []
        tail = bats.copy()
        while len(maxes) < 12 and len(tail) > 12 - len(maxes):
            next_max = max(tail[: -(12 - len(maxes))])
            maxes.append(next_max)
            tail = tail[tail.index(next_max) + 1 :]
        new_bats = maxes + tail
        return new_bats

    def list_to_int(self, lst):
        return int("".join([str(elem) for elem in lst]))


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
