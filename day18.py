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
    xs = set()
    ys = set()
    prev_dir = None
    edge_sum = 0
    mini_grid = set()
    mini_step_size = 1
    mini_step_size = 100000
    corners = []
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

        xs.add(pos[0])
        xs.add(old_pos[0])
        ys.add(pos[1])
        ys.add(old_pos[1])

        min_y = min(min_y, pos[1])
        max_y = max(max_y, pos[1])

        # we now calculate the borders by offsetting them a bit to the edges of the tile
        side_dir = (-dir[1] * 0.5, dir[0] * 0.5)
        edge_old_pos = (old_pos[0] + side_dir[0], old_pos[1] + side_dir[1])
        edge_pos = (pos[0] + side_dir[0], pos[1] + side_dir[1])
        borders.append((edge_old_pos, edge_pos))


        mini_steps = round(steps / mini_step_size)
        mini_pos = (round(old_pos[0] / mini_step_size), round(old_pos[1] / mini_step_size))
        mini_grid.add(mini_pos)
        for i in range(0, mini_steps):
            mini_pos = (mini_pos[0] + dir[0], mini_pos[1] + dir[1])
            mini_grid.add(mini_pos)


        # immediately count the volume of the borders
        volume += steps

        edge_sum += (pos[0] - old_pos[0]) * (pos[1] + old_pos[1])

    if edge_sum > 0:
        print("Edge sum is " + str(edge_sum) + " so we are counter-clockwise")
    else:
        print("Edge sum is " + str(edge_sum) + " so we are clockwise")

    print("Final pos: " + str(pos))

    def clamp01(v):
        return min(1, max(-1, v))

    pprint(borders)

    # correct the edges
    for i in range(0, len(borders)):
        prev_i = (i-1+len(borders)) % len(borders)
        prev_line = borders[prev_i]
        next_line = borders[i]
        prev_dir = (clamp01(prev_line[1][0] - prev_line[0][0]), clamp01(prev_line[1][1] - prev_line[0][1]))
        next_dir = (clamp01(next_line[1][0] - next_line[0][0]), clamp01(next_line[1][1] - next_line[0][1]))

        next_dir_rot = (next_dir[1], -next_dir[0])
        if prev_dir != next_dir_rot:
            borders[i] = ((next_line[0][0] - next_dir[0] * 0.5, next_line[0][1] - next_dir[1] * 0.5), borders[i][1])
            borders[prev_i] = (borders[prev_i][0], (prev_line[1][0] + prev_dir[0] * 0.5, prev_line[1][1] + prev_dir[1] * 0.5))

        else:

            borders[i] = ((next_line[0][0] + next_dir[0] * 0.5, next_line[0][1] + next_dir[1] * 0.5), borders[i][1])
            borders[prev_i] = (borders[prev_i][0], (prev_line[1][0] - prev_dir[0] * 0.5, prev_line[1][1] - prev_dir[1] * 0.5))



    pprint(borders)

    mini_min_x = min([x[0] for x in mini_grid])
    mini_max_x = max([x[0] for x in mini_grid])
    mini_min_y = min([x[1] for x in mini_grid])
    mini_max_y = max([x[1] for x in mini_grid])
    print(mini_min_x)
    print(mini_min_y)
    print(mini_max_x)
    print(mini_max_y)

    for y in range(mini_max_y, mini_min_y - 1, -1):
        s = ""
        for x in range(mini_min_x, mini_max_x + 1):
            if (x, y) in mini_grid:
                s += "#"
            else:
                s += "."
        print(s)

    xs = list(xs)
    ys = list(ys)
    xs.sort()
    ys.sort()

    def in_range(border, y):
        border_min_y = min(border[0][1], border[1][1])
        border_max_y = max(border[0][1], border[1][1])
        return border_min_y < y < border_max_y

    def out_of_range(border, y):
        border_max_y = max(border[0][1], border[1][1])
        return border_max_y < y

    def ends_at(border, y):
        return border[0][1] == y or border[1][1] == y


    # sort by min y
    borders.sort(key=lambda x: min(x[0][1], x[1][1]))
    active_edges = []

    volume = 0
    for y in range(min_y, max_y+1):
        y_offset = y - min_y
        if ()
        print("Y: " + str(y))

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

        active_edges.sort(key=lambda x: x[0][0] + x[1][0])
        intervals = []
        for active_edge in active_edges:
            intervals.append((min(active_edge[0][0], active_edge[1][0]), max(active_edge[0][0], active_edge[1][0])))

        #print(intervals)
        line_volume = 0
        in_trench = True
        for i in range(0, len(intervals)-1):
            x_start = intervals[i][1]
            x_end = intervals[i+1][0]
            if x_start <= x_end:
                if in_trench:
                    new_volume = round(x_end - x_start)
                    #print("New volume " + str(new_volume) +  " from " + str(x_start) + " to " + str(x_end))
                    line_volume += new_volume
                in_trench = not in_trench


        volume += line_volume
        #print(line_volume)




    print("The total volume is " + str(volume))




puzzle("input18-2.txt")
