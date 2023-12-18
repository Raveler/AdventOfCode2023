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

    min_y = 100000000
    max_y = -100000000

    borders = []

    volume = 0
    horizontal_edges = set()
    for line in lines:
        split = line.split(" ")
        dir = input_map[split[0]]
        steps = int(split[1])
        color = split[2]
        print(color)

        dir = neighbour_dirs[int(color[7])]
        steps = int(color[2:7], 16)
        print("Move " + str(steps) + " in dir " + str(dir))

        min_y = min(min_y, pos[1])
        max_y = max(max_y, pos[1])

        old_pos = pos
        pos = (pos[0] + dir[0] * steps, pos[1] + dir[1] * steps)

        min_y = min(min_y, pos[1])
        max_y = max(max_y, pos[1])

        if pos[1] == old_pos[1]:
            min_x = min(pos[0], old_pos[0])
            max_x = max(pos[0], old_pos[0])
            horizontal_edges.add((min_x, max_x, pos[1]))
        else:
            borders.append((old_pos, pos))

        # immediately count the volume of the borders
        volume += steps

    print("Final pos: " + str(pos))


    def in_range(border, y):
        border_min_y = min(border[0][1], border[1][1])
        border_max_y = max(border[0][1], border[1][1])
        return border_min_y <= y <= border_max_y

    def out_of_range(border, y):
        border_max_y = max(border[0][1], border[1][1])
        return border_max_y <= y

    def ends_at(border, y):
        return border[0][1] == y or border[1][1] == y


    # sort by min y
    borders.sort(key=lambda x: min(x[0][1], x[1][1]))
    active_edges = []

    for y in range(min_y, max_y+1):
        #print("Y: " + str(y))

        # pop old edges
        active_edges = [border for border in active_edges if in_range(border, y)]

        # add new edges
        while len(borders) > 0:
            if out_of_range(borders[0], y):
                borders.pop(0)
            elif in_range(borders[0], y):
                active_edges.append(borders.pop(0))

            else:
                break

        #print(active_edges)

        active_edges.sort(key=lambda x: min(x[0][0], x[1][0]))

        in_trench = False

        xs = []
        line_volume = 0
        i = 0

        while i < len(active_edges) - 1:

            edge1 = active_edges[i]
            edge2 = active_edges[i+1]

            if ends_at(edge1, y) and ends_at(edge2, y) and (edge1[0][0], edge2[0][0], y) in horizontal_edges:
                i += 1
                continue

            in_trench = not in_trench

            if in_trench:
                line_volume += edge2[0][0] - edge1[0][0] - 1

            i += 1

        volume += line_volume
        #print(line_volume)




    print("The total volume is " + str(volume))




puzzle("input18-1.txt")
