import itertools
import math
from collections import defaultdict
import re
from collections import Counter
from functools import lru_cache, cache
from pprint import pprint
from queue import PriorityQueue
import random
import heapq


input_map = {
    'R': (1, 0),
    'U': (0, 1),
    'D': (0, -1),
    'L': (-1, 0)
}

neighbour_dirs = [
    (1, 0),
    (0, -1),
    (-1, 0),
    (0, 1),
]

def puzzle(path):
    lines = open(path).readlines()

    w = len(lines[0].strip())
    h = len(lines)

    #grid = defaultdict(lambda: False)
    pos = (0, 0)
    #grid[pos] = True

    min_pos = (10000000, 10000000)
    max_pos = (-10000000, -10000000)

    grid_rows = {}

    def add_interval(y, x1, x2):
        if y not in grid_rows:
            grid_rows[y] = list()
        grid_rows[y].append((x1, x2))

    #add_pos((0, 0))

    def add_pos(pos):
        y = pos[1]
        x = pos[0]
        if y not in grid_rows:
            grid_rows[y] = list()
        grid_rows[y].append(x)

    for line in lines:
        split = line.split(" ")
        dir = input_map[split[0]]
        steps = int(split[1])
        color = split[2]
        print(color)

        #dir = neighbour_dirs[int(color[7])]
        #steps = int(color[2:7], 16)
        print("Move " + str(steps) + " in dir " + str(dir))

        # we move horizontally - only add the end point
        if dir[1] == 0:
            add_pos(pos)
            pos = (pos[0] + dir[0] * steps, pos[1] + dir[1] * steps)
            add_pos(pos)

        else:

            if dir[1] == 1:
                add_pos(pos)

            for i in range(0, steps):
                pos = (pos[0] + dir[0], pos[1] + dir[1])
                add_pos(pos)
                print(pos)

                min_pos = (min(min_pos[0], pos[0]), min(min_pos[1], pos[1]))
                max_pos = (max(max_pos[0], pos[0]), max(max_pos[1], pos[1]))

    volume = 0
    print(grid_rows)
    for y in grid_rows:
        intervals = grid_rows[y]
        intervals.sort(key=lambda x: x[1])

        in_trench = False
        prev_x2 = None
        print(intervals)
        for i in range(0, len(intervals)):
            interval = intervals[i]
            x1 = interval[0]
            x2 = interval[1]

            # we moved along the x-axis - we are full part of the volume
            if x1 != x2:
                volume += x2 - x1 + 1

            # vertical movement
            else:
                if in_trench:
                    volume += x2 - prev_x2 + 1
                in_trench = not in_trench
s
            prev_x2 = x2


    print("The total volume is " + str(volume))







puzzle("input18-1.txt")
