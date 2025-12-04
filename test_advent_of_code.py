#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 21:35:13 2024

@author: stjseidel
"""
import importlib
import json
import time
import unittest
from datetime import datetime
from pathlib import Path


class TestAdventOfCode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load expected results once
        with open("expected_results.json", "r") as f:
            cls.expected_results = json.load(f)

    def test_all_days(self):
        # Iterate through all available solution files
        passed_days = min(datetime.now(), datetime(2025, 12, 12)).day
        for file in [
            Path(f"day_{str(i).zfill(2)}.py") for i in range(1, passed_days + 1)
        ]:
            day = file.stem  # Extract day, e.g., "01"
            if "_" in day:
                day = day.split("_")[-1]
            if not file.exists():
                file = Path(f"{day}.py")
            module_name = file.stem  # Remove ".py" for import

            with self.subTest(day=day):
                self._test_day(module_name, day)

    def _test_day(self, module_name, day):
        try:
            module = importlib.import_module(module_name)
            today = getattr(module, "Today")
            solver = today(day=day, simple=False)
            solver.set_lines(simple=False)

            for part in ("part1", "part2"):
                expected = self.expected_results.get(day, {}).get(part)
                if expected is not None:
                    start_time = time.perf_counter()
                    result = getattr(solver, part)()
                    end_time = time.perf_counter()
                    elapsed_time = end_time - start_time

                    self.assertEqual(result, expected, f"Failed on {day}.{part}")
                    print(
                        f"Day {day}, {part}: {result} (Expected: {expected}) - {elapsed_time:.4f}s"
                    )
                else:
                    print(f"Day {day}, {part}: No expected result stored.")
        except Exception as e:
            self.fail(f"Error testing day {day}: {e}")
    

if __name__ == "__main__":
    unittest.main()
