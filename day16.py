import math
from collections import defaultdict
import re
from collections import Counter
from functools import lru_cache, cache
from pprint import pprint



def raycast(visited, energized, grid, w, h, p, dir):

    while True:

        hash = (p[0], p[1], dir[0], dir[1])
        if hash in visited:
            break

        energized.add(p)

        visited.add(hash)

        p = (p[0] + dir[0], p[1] + dir[1])


        if p[0] < 0 or p[0] >= w or p[1] < 0 or p[1] >= h:
            print("")
            break

        #print("Move to " + str(p) + " from dir " + str(dir))

        c = grid[p[1]][p[0]]

        if c == '/':
            if dir == (1, 0):
                dir = (0, 1)
            elif dir == (0, -1):
                dir = (-1, 0)
            elif dir == (-1, 0):
                dir = (0, -1)
            elif dir == (0, 1):
                dir = (1, 0)

        if c == '\\':
            if dir == (1, 0):
                dir = (0, -1)
            elif dir == (0, -1):
                dir = (1, 0)
            elif dir == (-1, 0):
                dir = (0, 1)
            elif dir == (0, 1):
                dir = (-1, 0)

        elif c == '|':
            if dir == (1, 0) or dir == (-1, 0):
                #print("RAYCAST " + str(p) + " in dir " + str((0, 1)))
                raycast(visited, energized, grid, w, h, p, (0, 1))
                #print("RAYCAST " + str(p) + " in dir " + str((0, -1)))
                raycast(visited, energized, grid, w, h, p, (0, -1))
                break

        elif c == '-':
            if dir == (0, 1) or dir == (0, -1):
                #print("RAYCAST " + str(p) + " in dir " + str((1, 0)))
                raycast(visited, energized, grid, w, h, p, (1, 0))
                #print("RAYCAST " + str(p) + " in dir " + str((-1, 0)))
                raycast(visited, energized, grid, w, h, p, (-1, 0))
                break



def print_grid(energized, w, h):
    for y in range(h-1, -1, -1):
        s = ""
        for x in range(0, w):
            if (x, y) in energized:
                s += "#"
            else:
                s += "."
        print(s)


def get_energy_level(grid, w, h, p, dir):
    energized = set()
    visited = set()
    raycast(visited, energized, grid, w, h, p, dir)
    energized.remove(p)
    return len(energized)


def puzzle(path):
    lines = open(path).readlines()
    lines.reverse()

    w = len(lines[0].strip())
    h = len(lines)

    energized = set()
    visited = set()
    raycast(visited, energized, lines, w, h, (-1, h-1), (1, 0))
    energized.remove((-1, h-1))

    max_energization = 0
    for x in range(0, w):

        energy_level = get_energy_level(lines, w, h, (x, -1), (0, 1))
        max_energization = max(energy_level, max_energization)

        energy_level = get_energy_level(lines, w, h, (x, h), (0, -1))
        max_energization = max(energy_level, max_energization)

    for y in range(0, h):
        energy_level = get_energy_level(lines, w, h, (-1, y), (1, 0))
        max_energization = max(energy_level, max_energization)

        energy_level = get_energy_level(lines, w, h, (w, y), (-1, 0))
        max_energization = max(energy_level, max_energization)



    print("There are " + str(len(energized)) + " energized tiles")


    print("Max energy is " + str(max_energization))


puzzle("input16-2.txt")
