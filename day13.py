import math
from collections import defaultdict
import re
from collections import Counter
from functools import lru_cache, cache
from pprint import pprint


def rotate(grid, w, h):

    new_grid = {}
    for x in range(0, w):
        for y in range(0, h):
            new_grid[(y, x)] = grid[(x, y)]

    return new_grid


def is_same_line(grid, w, h, x1, x2, smudges):
    for y in range(0, h):
        if grid[(x1, y)] != grid[(x2, y)]:
            if smudges > 0:
                return {"found": False}
            else:
                smudges += 1

    return {"found": True, "smudges": smudges}


def mirror_grid(grid, w, h, multiplier):

    sum = 0
    for mirror_x in range(1, w):

        all_ok = True
        smudges = 0
        for x in range(0, mirror_x):
            x1 = x
            x2 = mirror_x + (mirror_x - x1) - 1

            # out of range
            if x2 >= w:
                continue

            out = is_same_line(grid, w, h, x1, x2, smudges)

            if not out["found"]:
                all_ok = False

            else:
                smudges = out["smudges"]

        # don't allow the original line
        if smudges == 0:
            all_ok = False

        if all_ok:
            print("We mirrored between " + str(mirror_x-1) + " and " + str(mirror_x) + " with multiplier " + str(multiplier) + " and " + str(smudges) + " smudges")
            print("")
            sum += mirror_x * multiplier

    return sum


def get_grid_score(grid, w, h):
    sum = 0
    sum += mirror_grid(grid, w, h, 1)
    grid = rotate(grid, w, h)
    sum += mirror_grid(grid, h, w, 100)
    return sum


def  print_grid(grid, w, h):
    for y in range(0, h):
        s = ""
        for x in range(0, w):
            s += grid[(x, y)]
        print(s)
    print("")


def puzzle(path):
    lines = open(path).readlines()
    lines.append("")

    grid = {}
    w = 0
    h = 0

    sum = 0
    for line in lines:

        if len(line.strip()) == 0:

            if h > 0:
                print_grid(grid, w, h)
                sum += get_grid_score(grid, w, h)

            grid  = {}
            w = 0
            h = 0
            continue

        if w == 0:
            w = len(line.strip())

        for x in range(0, w):
            grid[(x, h)] = line[x]

        h += 1

    print("The sum is " + str(sum))


puzzle("input13-2.txt")
