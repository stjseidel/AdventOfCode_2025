#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 08:39:05 2024

@author: stjseidel
"""

import re
import sys
from collections import defaultdict
from datetime import datetime
from functools import reduce
from math import gcd
from pathlib import Path
from shutil import copy2
from timeit import default_timer as timer

from bs4 import BeautifulSoup
from dotenv import get_key
import requests
import numpy as np


class AOC:
    def __init__(self, day="", simple=True):
        if day == "":
            try:
                day = Path(sys.modules[self.__module__].__file__).stem
            except Exception as e:
                print("Tried to set day from __file__: ", e)
                day = str(datetime.today().day).zfill(2)
        if "_" in day:
            day = day.split("_")[-1]
        self.year = "2025"
    
        self.riddle_count = 12 if self.year >= "2025" else 24
            
        self.day = str(day).zfill(2)
        print("Working on day: ", self.day)
        self.template = Path("template.py")
        self.beginning_of_time = timer()
        self.start()
        self.input_folder = Path("input")
        self.input = self.input_folder / f"{self.day}.txt"
        self.input_simple = self.input_folder / f"{self.day}_simple.txt"
        self.simple = simple
        self.passed_days = min(datetime.now(), datetime(int(self.year), 12, self.riddle_count)).day
        if int(self.day) <= int(self.passed_days):
            self.create_txt_files()
            self.read_both_files()
            self.set_lines(simple=simple)
        self.this_list = []

    def start(self):
        self.beginning = timer()

    def stop(self):
        self.end = timer()
        print(f"{round(self.end - self.beginning, 2)} Seconds needed for execution")
        self.start()

    def read_both_files(self):
        file_path = self.input_folder / f"{self.day}_simple.txt"
        if not file_path.exists():
            print("no such file: ", file_path)
            self.lines_simple = []
        else:
            self.lines_simple = self.read_lines(file_path)
        file_path = self.input_folder / f"{self.day}.txt"
        if not file_path.exists():
            print("no such file: ", file_path)
            self.lines_real = []
        else:
            self.lines_real = self.read_lines(file_path)

    def set_lines(self, simple=False):
        self.simple = simple
        if simple:
            self.lines = self.lines_simple
        else:
            self.lines = self.lines_real

    def read_lines(self, file_path=""):
        file_path = Path(file_path)
        if not file_path.exists():
            file_path = self.input_folder / file_path
        with open(file_path) as fp:
            lines = fp.readlines()
        self.lines = [line.replace("\n", "") for line in lines]
        self.lines = [
            re.sub(" +", " ", line) for line in self.lines
        ]  # trim doubled spaces
        return self.lines

    def chunk_lines(self, n):
        self.lines = [self.chunk_line(line, n) for line in self.lines]

    def chunk_line(self, line, n):
        """Yield successive n-sized chunks from lst."""
        return [line[i : i + n] for i in range(0, len(line), n)]

    # =============================================================================
    #         for i in range(0, len(line), n):
    #             yield line[i:i + n]
    # =============================================================================

    def extract_numbers_from_lines(self, lines):
        # pattern = re.compile('\d+\.[.\d]+')
        return [str("".join(filter(str.isdigit, line))) for line in lines]

    def extract_numbers_from_string(self, line):
        # pattern = re.compile('\d+\.[.\d]+')
        return str("".join(filter(str.isdigit, line)))

    def extract_patterns_from_string(self, line, pattern):
        # pattern = re.compile('\d+\.[.\d]+')
        matches = re.findall(pattern, string=line)
        if matches:
            return [match for match in matches]
        else:
            return []

    def extract_only_selected_characters(self, line, pattern):
        # character_class = '[^mul(),\d]'
        return re.sub(pattern, "", line)

    def replace_with_dict(self, text, conversion_dict, before=None):
        before = before or str.lower
        t = before(text)
        for key, value in conversion_dict.items():
            t = t.replace(key, value)
        return t

    def create_txt_files(self):
        if not self.input.exists():
            self.fetch_input(int(self.day))
        if not self.input_simple.exists():
            self.fetch_input_simple(int(self.day))

    def get_soup(self, url):
        """Helper function to fetch the BeautifulSoup object for the day's page."""
        # url = f"https://adventofcode.com/{self.year}/day/{day}"
        session_cookie = get_key(".env", "SESSION_COOKIE")
        # Set up the headers with the session cookie
        HEADERS = {"Cookie": f"session={session_cookie}"}
        response = requests.get(url, headers=HEADERS)
        session_cookie = None
        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")
        else:
            print(f"Failed to fetch page for day {self.day}: {response.status_code}")
            return None

    def fetch_input_simple(self, day: int):
        """Fetch and store the code from the <code> tag into 'day_simple.txt'."""
        url = f"https://adventofcode.com/{self.year}/day/{day}"
        soup = self.get_soup(url)
        if soup:
            code_tag = soup.find("code")
            if code_tag:
                code_content = code_tag.get_text()

                file_path = self.input_simple
                with open(file_path, "w") as file:
                    file.write(code_content)
                print(f"Saved simple code for day {day} to {file_path}")
            else:
                print(f"No <code> tag found for day {day}")

    def fetch_input(self, day: int):
        """Fetch and store the input from the <pre> tag into 'day.txt'."""
        url = f"https://adventofcode.com/{self.year}/day/{day}/input"
        soup = self.get_soup(url)
        if soup:
            file_path = self.input
            file_path.parent.mkdir(exist_ok=True, parents=True)
            with open(file_path, "w") as file:
                file.write(soup.text)
            print(f"Saved input for day {day} to {file_path}")
        else:
            print(f"No input found for day {day}")

    def copy_template(self):
        this_file = Path(f"day_{str(self.day).zfill(2)}.py")
        if not this_file.exists():
            copy2(self.template, this_file)

    def copy_all_templates(self):
        days = [str(i).zfill(2) for i in range(1, self.riddle_count + 1)]
        for day in days:
            this_file = Path(f"day_{str(day).zfill(2)}.py")
            if not this_file.exists():
                copy2(self.template, this_file)

    def lcm(self, denominators):
        # return least common denominator of a list of integers
        return reduce(lambda a, b: a * b // gcd(a, b), denominators)

    def transpose_lines(self, lines):
        lines_split = [
            [char for char in line] for line in lines
        ]  # split lines into chars
        lines_T = pd.DataFrame(lines_split).T.values.tolist()
        lines_T = [
            "".join(line) for line in lines_T
        ]  # combine the split chars to strings
        return lines_T

    def border_coordinates(self, x_max, y_max):
        """Return a list of all coordinates at the border of a rectangle x,y (length of lines, line)"""
        border = []

        # Top and bottom borders
        for x in range(x_max):
            border.append((x, 0))  # Top border
            border.append((x, y_max - 1))  # Bottom border

        # Left and right borders (excluding corners to avoid duplicates)
        for y in range(1, y_max - 1):
            border.append((0, y))  # Left border
            border.append((x_max - 1, y))  # Right border
        return border

    def border_coordinates_of_lines(self, lines=""):
        lines = lines or self.lines
        return self.border_coordinates(len(lines[0]), len(lines))

    def flatten_lists(self, lists):
        return [item for sublist in lists for item in sublist]

    def grid_make_empty(self):
        self.grid = [["." for c in row] for row in self.lines]

    def grid_make_lines_copy(self):
        self.grid = [[c for c in row] for row in self.lines]

    def grid_make_empty_x_y(self, rows=6, cols=6):
        self.grid = [["." for c in range(cols + 1)] for row in range(rows + 1)]

    def grid_get_position_tuple_list_x_y(self, rows=6, cols=6):
        return [(row, c) for c in range(cols + 1) for row in range(rows + 1)]

    def grid_enter_result(self, this_list=None, term=None, print_grid=False):
        this_list = this_list or self.this_list
        if this_list == []:
            return None
        term = term or self.term
        if type(term) != list:
            term = list(term)
        if len(term) < len(this_list):
            term = term[0] * len(this_list)
        for c, char in enumerate(term):
            pair = this_list[c]
            # self.grid[pair[0]][pair[1]] = char
            self.grid[pair[0]][pair[1]] = char or self.lines[pair[0]][pair[1]]
            if print_grid:
                self.print_grid()

    def print_grid(self, grid=None):
        grid = grid or self.grid
        for line in grid:
            print("".join(line))

    # =============================================================================
    #     def grid_extract_all_character_positions_to_dict(self, lines=None, ignore_chars=['.']):
    #         lines = lines or self.lines
    #         positions = defaultdict(lambda: [])
    #         for row, line in enumerate(lines):
    #             for col, char in enumerate(line):
    #                 if char not in ignore_chars:
    #                     positions[char].append((row, col))
    #         return positions
    # =============================================================================
    def grid_extract_all_character_positions_to_dict(
        self, lines=None, ignore_chars=["."]
    ):
        lines = lines or self.lines
        positions = defaultdict(
            lambda: np.empty((0, 2), dtype=int)
        )  # Default to empty NumPy array
        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                if char not in ignore_chars:
                    new_pos = np.array(
                        [[row, col]]
                    )  # Create a new NumPy array for the position
                    positions[char] = np.vstack(
                        (positions[char], new_pos)
                    )  # Stack positions
        return positions

    def grid_make_all_positions(self, lines=None, ignore_chars=[]):
        """create a set of all possile positions in the grid. leave out positions with ignore_chars."""
        lines = lines or self.lines
        positions = set()
        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                if char not in ignore_chars:
                    positions.add((row, col))
        return positions


if __name__ == "__main__":
    today = AOC(day='01')
    today.copy_all_templates()

    # day = '02'
    # today = AOC(day=day)
    # today.create_txt_files()
    # today.start()
    # today.stop
