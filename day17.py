import math
from collections import defaultdict
import re
from collections import Counter
from functools import lru_cache, cache
from pprint import pprint
from queue import PriorityQueue
import random


class _Wrapper:
    def __init__(self, item, key):
        self.item = item
        self.key = key

    def __lt__(self, other):
        return self.key(self.item) < other.key(other.item)

    def __eq__(self, other):
        return self.key(self.item) == other.key(other.item)


class KeyPriorityQueue(PriorityQueue):
    def __init__(self, key):
        self.key = key
        super().__init__()

    def _get(self):
        wrapper = super()._get()
        return wrapper.item

    def _put(self, item):
        super()._put(_Wrapper(item, self.key))


def print_grid(energized, w, h):
    for y in range(h-1, -1, -1):
        s = ""
        for x in range(0, w):
            if (x, y) in energized:
                s += "#"
            else:
                s += "."
        print(s)



def puzzle(path):
    lines = open(path).readlines()

    w = len(lines[0].strip())
    h = len(lines)

    pending = KeyPriorityQueue(key=lambda x: x[1]["tie_breaker"])

    tie_breaker = 0


    grid = {}
    for x in range(0, w):
        for y in range(0, h):
            grid[(x, y)] = int(lines[y][x])


    def get_point(pos, dir, prev_cost, steps, visited):
        nonlocal tie_breaker
        tie_breaker += 1
        return {
            "pos": pos,
            "dir": dir,
            "cost": prev_cost + grid[pos],
            "steps": steps,
            "tie_breaker": tie_breaker,
            "visited": visited
        }


    def add_point(pos, dir, prev_cost, steps, visited):
        visited = visited.copy()
        visited.append(pos)
        point = get_point(pos, dir, prev_cost, steps, visited)
        pending.put((point["cost"], point))


    def try_add_point_in_dir(pos, dir, prev_cost, steps, visited):

        if steps > 3:
            return

        pos = (pos[0] + dir[0], pos[1] + dir[1])

        if not is_valid(pos):
            return

        if pos in visited:
            return

        add_point(pos, dir, prev_cost, steps, visited)


    def is_valid(pos):
        return 0 <= pos[0] < w and 0 <= pos[1] < h


    add_point((1, 0), (1, 0), 0, 1, list())
    add_point((0, 1), (0, 1), 0, 1, list())
    min_cost = 0
    min_visited = list()

    dist = {}
    prev = {}
    Q = []
    for x in range(0, w):
        for y in range(0, h):
            dist[(x, y)] = -1
            prev[(x, y)] = None
            Q.append((x, y))

    dist[(0, 0)] = 0



    while len(Q) > 0:

        Q.sort(key=lambda x: dist[x])
        u = Q.pop(0)

        # otherwise, we keep adding points
        try_add_point_in_dir(point["pos"], point["dir"], point["cost"], point["steps"] + 1, point["visited"])
        clockwise_dir = (-point["dir"][1], point["dir"][0])
        try_add_point_in_dir(point["pos"], clockwise_dir, point["cost"], 1, point["visited"])
        anticlockwise_dir = (point["dir"][1], -point["dir"][0])
        try_add_point_in_dir(point["pos"], anticlockwise_dir, point["cost"], 1, point["visited"])




    while not pending.empty():

        point_tuple = pending.get()
        point = point_tuple[1]

        # reached the end
        if point["pos"] == (w-1, h-1):
            min_cost = round(point["cost"])
            min_visited = point["visited"]
            break


        # otherwise, we keep adding points
        try_add_point_in_dir(point["pos"], point["dir"], point["cost"], point["steps"] + 1, point["visited"])
        clockwise_dir = (-point["dir"][1], point["dir"][0])
        try_add_point_in_dir(point["pos"], clockwise_dir, point["cost"], 1, point["visited"])
        anticlockwise_dir = (point["dir"][1], -point["dir"][0])
        try_add_point_in_dir(point["pos"], anticlockwise_dir, point["cost"], 1, point["visited"])




    print("The min cost to reach the end is " + str(min_cost))

    pprint(min_visited)









puzzle("input17-1.txt")
