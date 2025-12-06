#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 06:32:12 2023

@author: stjse
"""

import re
from timeit import default_timer as timer

from aoc_class import AOC

class Today(AOC):

    def parse_lines(self):
        lines = self.lines
        return lines

    def part1(self):
        lines = self.parse_lines()
        self.number_lines = [[int(i) for i in re.findall(r'-?\d+', line)] for line in lines[:-1]]
        self.operations = re.findall(r'[+\-*/]', lines[-1])
        results = []
        for i, op in enumerate(self.operations):
            nums = [nums[i] for nums in self.number_lines]
            if op == '+':
                res = sum(nums)
            elif op == '*':
                res = 1
                for n in nums:
                    res *= n
            results.append(res)
        self.result1 = sum(results)
        self.time1 = timer()
        return self.result1

    def part2(self):
        lines = self.parse_lines()
        splits = [i for i, char in enumerate(lines[-1]) if char != ' ']
        results = []
        self.operations = re.findall(r'[+\-*/]', lines[-1])
        for i, split in enumerate(splits):
            op = self.operations[i]
            char_range = (split, splits[i+1]-1) if i+1 < len(splits) else (split, len(lines[-1]))
            nums = []
            for j in range(*char_range)[::-1]: 
                num = [line[j] for line in lines[:-1]]
                nums.append(int(''.join(num).strip()))
            if op == '+':
                res = sum(nums)
            elif op == '*':
                res = 1
                for n in nums:
                    res *= n
            results.append(res)
        self.result2 = sum(results)
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
# simple part 2
    today.set_lines(simple=True)
    today.part2()
    print(f'Part 2 <SIMPLE> result is: {today.result2}')
# =============================================================================

# =============================================================================
# hard part 2
    today.set_lines(simple=False)
    today.part2()
    print(f'Part 2 <HARD> result is: {today.result2}')
    today.stop()
    today.print_final()
# =============================================================================
