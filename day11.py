import math
from collections import defaultdict
import re
from collections import Counter
from pprint import pprint


def is_empty_horizontal(lines, w, h, x):
    for y in range(0, h):
        if lines[y][x] == '#':
            return False
    return True


def is_empty_vertical(lines, w, h, y):
    for x in range(0, w):
        if lines[y][x] == '#':
            return False
    return True


def puzzle(path):
    lines = open(path).readlines()

    # so that we have a proper bottom-to-top orientation
    lines.reverse()

    w = len(lines[0].strip())
    h = len(lines)
    size = (w, h)

    # construct the expanded grid
    skip_amount = 1000000
    skip_verticals = set()
    for y in range(0, h):
        if is_empty_vertical(lines, w, h, y):
            skip_verticals.add(y)

    skip_x = 0
    galaxies = []
    print("Skip these verticals:")

    print(skip_verticals)
    for x in range(0, w):
        if is_empty_horizontal(lines, w, h, x):
            skip_x += skip_amount - 1
            print("Skip " + str(x) + " a second time!")

        skip_y = 0
        for y in range(0, h):
            if y in skip_verticals:
                skip_y += skip_amount - 1

            real_x = x + skip_x
            real_y = y + skip_y

            if lines[y][x] == '#':
                coord = (real_x, real_y)
                galaxies.append(coord)


    sum = 0
    for i in range(0, len(galaxies)):
        for j in range(i+1, len(galaxies)):
            coord1 = galaxies[i]
            coord2 = galaxies[j]

            manhattan_distance = abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])
            sum += manhattan_distance

    print("The distance sum is " + str(sum))




puzzle("input11-2.txt")
