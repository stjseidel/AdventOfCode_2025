#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 06:32:12 2023

@author: stjse
"""

from collections import defaultdict, deque
from dataclasses import dataclass
from timeit import default_timer as timer
from typing import ClassVar

from aoc_class import AOC

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
    _split_beam_counter: ClassVar[int] = 1

    _splitter_path_registry: ClassVar[dict] = {}
    _origin_col: ClassVar[int] = 0

    def __post_init__(self):
        self._by_row[(self.y)].append(self)
        self._by_coords[(self.x, self.y)] = self

    @classmethod
    def get_row(cls, y: int):
        return cls._by_row[y]

    @classmethod
    def get_row_splitters(cls, y: int):
        return [spot for spot in cls.get_row(y) if spot.is_splitter]

    @classmethod
    def get_spot(cls, x: int, y: int):
        return cls._by_coords.get((x, y))

    def turn_to_beam(self):
        self.is_free = False
        self.is_beam = True
        self.is_splitter = False

    def turn_to_splitter(self):
        self.is_free = False
        self.is_beam = False
        self.is_splitter = True

    def split_beam(self):
        directions = [-1, 1]
        Spot._split_counter += 1
        for direction in directions:
            new_x = self.x + direction
            new_y = self.y + 1
            target_spot = Spot.get_spot(new_x, new_y)
            if not target_spot:
                print("missing target Spot! at ", new_x, new_y)
                raise ValueError
            if new_x < 0 or new_x >= Spot._row_width:
                continue
            if (
                not target_spot.is_splitter
            ):  # for part 1, is is_free... for part 2, we emit also for present beams
                Spot._split_beam_counter += 1
                target_spot.turn_to_beam()
                queue_splits.append(target_spot)

    def emit(self):
        if self.has_emitted:
            return None
        if self.y == Spot._row_counter:
            return None
        self.has_emitted = True
        new_y = self.y + 1

        target_spot = Spot.get_spot(self.x, new_y)
        if not target_spot:
            print("missing target Spot! at ", self.x, new_y)
            raise ValueError
        if target_spot.is_free:
            target_spot.turn_to_beam()
            queue_beams.append(target_spot)
        elif target_spot.is_beam:
            return None
        elif target_spot.is_splitter:
            self.split_beam()
            return None

    @classmethod
    def clear_registry(cls):
        """Clear all registered spots"""
        cls._by_row.clear()
        cls._by_coords.clear()
        cls._row_counter = 0
        cls._split_counter = 0
        cls._splitter_path_registry = {}

    @classmethod
    def setup_spots(cls, lines):
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                spot = Spot(x=x, y=y, is_free=True)
                if char == ".":
                    continue
                elif char == "S":
                    spot.turn_to_beam()
                    cls._origin_col = x
                elif char == "^":
                    spot.turn_to_splitter()
                else:
                    print("unknown char:", char)
                    raise ValueError
        cls._row_width = len(lines[0])
        cls._row_counter = len(lines) - 1

    @classmethod
    def emit_beams(cls):
        for spot in cls._by_row[0]:
            if spot.is_beam:
                queue_splits.append(spot)
        while queue_splits:
            current_spot = queue_splits.popleft()
            current_spot.emit()
            while queue_beams:
                current_spot = queue_beams.popleft()
                current_spot.emit()

    @classmethod
    def emit_backwards_traversal(cls):
        for y in range(cls._row_counter)[::-1]:
            emitters = cls.get_row_splitters(y)
            for emitter in emitters:
                cls._splitter_path_registry[(emitter.x, emitter.y)] = (
                    cls.traverse_emitter(emitter)
                )
        # getting the splitter that is being hit by the origin beam
        for y in range(cls._row_counter):
            spot = cls.get_spot(cls._origin_col, y)
            if spot.is_splitter:
                break
        return cls._splitter_path_registry[spot.x, spot.y]

    @classmethod
    def traverse_emitter(cls, spot):
        pos = (spot.x, spot.y)
        if pos in cls._splitter_path_registry:
            return cls._splitter_path_registry[pos]
        directions = [-1, 1]
        paths_total = 0
        for direction in directions:
            not_found = True
            new_y = spot.y + 1
            paths = 1
            while not_found and new_y < spot._row_counter:
                new_x = spot.x + direction
                target_spot = cls.get_spot(new_x, new_y)
                if not target_spot:
                    print("missing target Spot! at ", new_x, new_y)
                    raise ValueError
                if new_x < 0 or new_x >= cls._row_width:
                    not_found = False  # leaving the map, so result here is 1
                if target_spot.is_splitter:
                    # instead of 1, we replace it with the result of a previously found splitter result
                    paths = cls.traverse_emitter(target_spot)
                    not_found = False
                new_y = new_y + 1
            paths_total += paths
        Spot._splitter_path_registry[pos] = paths_total
        return paths_total


class Today(AOC):

    def parse_lines(self):
        lines = self.lines
        Spot.setup_spots(lines)

        return lines

    def part1(self):
        _ = self.parse_lines()
        Spot._split_beam_counter = 1
        Spot.emit_beams()
        self.result1 = Spot._split_counter
        self.time1 = timer()
        Spot.clear_registry()
        return self.result1

    def part2(self):
        _ = self.parse_lines()
        self.result2 = Spot.emit_backwards_traversal()
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
