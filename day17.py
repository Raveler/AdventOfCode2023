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


pq = []                         # list of entries arranged in a heap
entry_finder = {}               # mapping of tasks to entries
REMOVED = '<removed-task>'      # placeholder for a removed task
counter = itertools.count()     # unique sequence count

def add_task(task, priority=0):
    'Add a new task or update the priority of an existing task'
    if task in entry_finder:
        remove_task(task)
    count = next(counter)
    entry = [priority, count, task]
    entry_finder[task] = entry
    heapq.heappush(pq, entry)

def remove_task(task):
    'Mark an existing task as REMOVED.  Raise KeyError if not found.'
    entry = entry_finder.pop(task)
    entry[-1] = REMOVED

def pop_task():
    'Remove and return the lowest priority task. Raise KeyError if empty.'
    while pq:
        priority, count, task = heapq.heappop(pq)
        if task is not REMOVED:
            del entry_finder[task]
            return (priority, task)
    raise KeyError('pop from an empty priority queue')


def puzzle(path):
    lines = open(path).readlines()

    w = len(lines[0].strip())
    h = len(lines)

    grid = {}
    for x in range(0, w):
        for y in range(0, h):
            grid[(x, y)] = int(lines[y][x])

    dist = {}

    def add_start_point(pos, dir):
        start_point = (pos, dir, 0)
        dist[start_point] = 0
        add_task(start_point, 0)

    add_start_point((0, 0), (1, 0))
    add_start_point((0, 0), (0, 1))


    def add_point(parent_pos, pos, dir, cost, steps):
        p = (pos, dir, steps)
        dist[p] = cost
        add_task(p, cost)
        #print("Add point " + str(pos) + " coming from " + str(parent_pos) + " with dir " + str(dir) + " and cost " + str(cost) + " and steps " + str(steps))


    def try_add_point_in_dir(pos, dir, cost, steps):

        old_pos = pos
        pos = (pos[0] + dir[0], pos[1] + dir[1])

        if not is_valid(pos):
            return

        p = (pos, dir, steps)
        new_cost = cost + grid[pos]


        if p in dist and new_cost >= dist[p]:
            return

        add_point(old_pos, pos, dir, new_cost, steps)


    def is_valid(pos):
        return 0 <= pos[0] < w and 0 <= pos[1] < h


    def solve(min, max):
        while pq:

            task = pop_task()
            #print(task)
            cost = task[0]
            u = task[1]

            pos = u[0]
            dir = u[1]
            steps = u[2]

            if pos == (w-1, h-1) and steps >= min:
                return cost

            #steps = steps_grid[u]

            # otherwise, we keep adding points
            if steps < max:
                try_add_point_in_dir(pos, dir, cost, steps + 1)

            if steps >= min:
                clockwise_dir = (-dir[1], dir[0])
                try_add_point_in_dir(pos, clockwise_dir, cost, 1)
                anticlockwise_dir = (dir[1], -dir[0])
                try_add_point_in_dir(pos, anticlockwise_dir, cost, 1)

    #min_cost = solve(0, 3)
    min_cost = solve(4, 10)
    print("The min cost to reach " + str(w-1) + "," + str(h-1) + " is " + str(min_cost))



puzzle("input17-2.txt")
