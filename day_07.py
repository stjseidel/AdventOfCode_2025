#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 06:32:12 2023

@author: stjse
"""

from timeit import default_timer as timer

from aoc_class import AOC
from dataclasses import dataclass
from typing import ClassVar
from collections import defaultdict, deque

queue_beams = deque()
queue_splits = deque()

@dataclass
class Spot:
    x: int
    y: int 
    is_free: bool = False
    is_beam: bool = False
    is_splitter: bool = False
    has_emitted: bool = False

    _by_row: ClassVar[defaultdict] = defaultdict(list)
    _by_coords: ClassVar[dict] = {}
    _row_counter: ClassVar[int] = 0
    _row_width: ClassVar[int] = 0
    _split_counter: ClassVar[int] = 0
    _print_grid: ClassVar[bool] = False
    _split_beam_counter: ClassVar[int] = 1


    def __post_init__(self):
        self._by_row[(self.y)].append(self)
        self._by_coords[(self.x, self.y)] = self

    @classmethod
    def get_row(cls, y: int):
        return cls._by_row[y]
    
    @classmethod
    def get_spot(cls, x: int, y: int):
        return cls._by_coords.get((x, y))
    
    def turn_to_beam(self):
        self.is_free = False
        self.is_beam = True
        self.is_splitter = False
        self.update_grid(symbol='|')

    def turn_to_splitter(self):
        self.is_free = False
        self.is_beam = False
        self.is_splitter = True
        self.update_grid(symbol='^')

    def split_beam(self):
        directions = [-1, 1]
        Spot._split_counter += 1
        for direction in directions:
            new_x = self.x + direction
            new_y = self.y + 1
            target_spot = Spot.get_spot(new_x, new_y)
            if not target_spot:
                print('missing target Spot! at ', new_x, new_y)
                raise ValueError
            if new_x < 0 or new_x >= Spot._row_width:
                continue
            if target_spot.is_free:
                target_spot.turn_to_beam()
                queue_splits.append(target_spot)
                
                # print(f'{Spot._split_counter} Splitter at ({self.x}, {self.y}) splitting to ({new_x}, {new_y})')
                # pass
    
    def emit(self):
        if self.has_emitted:
            return None
        if self.y == Spot._row_counter:
            return None
        self.has_emitted = True
        new_y = self.y + 1

        target_spot = Spot.get_spot(self.x, new_y)
        if not target_spot:
            print('missing target Spot! at ', self.x, new_y)
            raise ValueError
        if target_spot.is_free:
            target_spot.turn_to_beam()
            queue_beams.append(target_spot)
        elif target_spot.is_beam:
            return None
        elif target_spot.is_splitter:
            self.split_beam()
            return None
    
    def update_grid(self, symbol=''):
        if symbol == '':
            if self.is_free:
                symbol = '.'
            elif self.is_beam:
                symbol = '|'
            elif self.is_splitter:
                symbol = '^'
        today.grid_enter_result(this_list=[(self.y, self.x)], term=symbol, print_grid=Spot._print_grid)

    @classmethod
    def clear_registry(cls):
        """Clear all registered spots"""
        cls._by_row.clear()
        cls._by_coords.clear()
        cls._row_counter = 0
        cls._split_counter = 0

def setup_spots(lines):
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            spot = Spot(x=x, y=y, is_free=True)
            if char == '.':
                continue
            elif char == 'S':
                spot.turn_to_beam()
            elif char == '^':
                spot.turn_to_splitter()
            else:
                print('unknown char:', char)
                raise ValueError
    Spot._row_width = len(lines[0])
    Spot._row_counter = len(lines) - 1

def emit_beams():
    for spot in Spot._by_row[0]:
        if spot.is_beam:
            queue_splits.append(spot)
    # for spot in spots:
    #     if spot.is_beam:
    #         queue.append(spot)
    while queue_splits:
        current_spot = queue_splits.popleft()
        current_spot.emit()
        while queue_beams:
            current_spot = queue_beams.popleft()
            current_spot.emit()
            
        
class Today(AOC):

    def parse_lines(self):
        lines = self.lines
        self.grid_make_empty()
        Spot._print_grid = False
        setup_spots(lines)
        
        return lines

    def part1(self):
        lines = self.parse_lines()
        Spot._print_grid = False
        emit_beams()
        self.result1 = Spot._split_counter
        self.time1 = timer()
        Spot.clear_registry()
        return self.result1

    def part2(self):
        lines = self.parse_lines()
        self.result2 = self.result1 ** 2
        self.time2 = timer()
        return self.result2


if __name__ == "__main__":
    # prep
    today = Today(day="", simple=True)
    today.create_txt_files()

    # simple part 1
    today.set_lines(simple=True)

    today.part1()
    today.print_grid()
    print(f"Part 1 <SIMPLE> result is: {today.result1}")

# =============================================================================
# hard part 1
    today.set_lines(simple=False)
    today.part1()
    today.print_grid()
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
# # hard part 2
#     today.set_lines(simple=False)
#     today.part2()
#     print(f'Part 2 <HARD> result is: {today.result2}')
#     today.stop()
#     today.print_final()
# =============================================================================
