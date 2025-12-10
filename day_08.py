#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 06:32:12 2023

@author: stjse
"""

from heapq import nlargest, nsmallest
from itertools import combinations
from timeit import default_timer as timer

import networkx as nx

from aoc_class import AOC


class Today(AOC):

    def parse_lines(self):
        lines = self.lines
        lines = [tuple([int(i) for i in line.split(',')]) for line in lines]
        return lines

    def part1(self):
        lines = self.parse_lines()
        G = nx.Graph()
        if self.simple:
            num_of_connections = 10
        else:
            num_of_connections = 1000

        selected_combos = nsmallest(num_of_connections, combinations(lines, 2), key=lambda combo: self.get_distance_between_tuples(*combo))
        added = set()
        for combo in selected_combos:
            to_add = set(combo) - added
            if to_add:
                for x in to_add:
                    G.add_node(x)
                    added.add(x)

            if not G.has_edge(*list(combo)):
                G.add_edge(*list(combo))

        components = list(nx.connected_components(G))
        top_3_groups = nlargest(len(lines), components, key=len)

        result = 1
        for g in top_3_groups[:3]:
            result *= len(g)
        self.result1 = result
        self.time1 = timer()
        return self.result1

    def part2(self):
        lines = self.parse_lines()
        combos_with_distances = [(combo, self.get_distance_between_tuples(*combo)) for combo in combinations(lines, 2)]
        combos_with_distances.sort(key=lambda x: x[1])
        G = nx.Graph()
        largest_size = 0
        i = -1
        while largest_size < len(lines):
            i += 1
            combo, _ = combos_with_distances[i]
            G.add_edge(combo[0], combo[1])
            largest_size = len(max(nx.connected_components(G), key=len))
        last_to_link = combo
        self.result2 = last_to_link[0][0] * last_to_link[1][0]
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
