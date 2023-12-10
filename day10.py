import math
from collections import defaultdict
import re
from collections import Counter

mappings = {
    '.': [],
    '|': [(0, -1), (0, 1)],
    '-': [(-1, 0), (1, 0)],
    'L': [(0, 1), (1, 0)],
    'J': [(0, 1), (-1, 0)],
    '7': [(-1, 0), (0, -1)],
    'F': [(1, 0), (0, -1)],
}

neighbours = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def is_connected_to(grid, w, h, from_x, from_y, to_x, to_y):

    if to_x < 0 or to_x >= w or to_y < 0 or to_y >= h:
        return False

    dx = to_x - from_x
    dy = to_y - from_y

    c = grid[h-from_y-1][from_x]

    if c == 'S':
        return is_connected_to(grid, w, h, to_x, to_y, from_x, from_y)

    for (allowed_dx, allowed_dy) in mappings[c]:
        if allowed_dx == dx and allowed_dy == dy:
            return True

    return False


def double_to_normal(x, y):
    if x % 2 != 1 or y % 2 != 1:
        raise "Coord " + str(x) + "," + str(y) + " is not a valid normal coord!"

    return ((x-1)/2, (y-1)/2)


def normal_to_double(x, y):
    return (x*2 + 1, y*2 + 1)


def flood_fill(inside_map, w, h, x, y):

    to_fill = [(x,y)]
    while len(to_fill) > 0:
        coord = to_fill.pop(0)
        print(len(to_fill))
        print(coord)
        x = coord[0]
        y = coord[1]

        inside_map[(x, y)] = {
            "in_pipe": False,
            "flood_filled": True,
        }

        next_fill = []

        for neighbour in neighbours:
            new_x = x + neighbour[0]
            new_y = y + neighbour[1]

            # don't go too far outside
            if new_x < 0 or new_y < 0 or new_x > w or new_y > h:
                continue

            # already visited or part of pipe - don't flood fill further
            if inside_map[(new_x, new_y)]["in_pipe"] or inside_map[(new_x, new_y)]["flood_filled"]:
                continue

            if (new_x, new_y) in to_fill:
                continue

            next_fill.append((new_x, new_y))

        to_fill.extend(next_fill)



def puzzle1(path):
    lines = open(path).readlines()

    w = len(lines[0].strip())
    h = len(lines)

    to_explore = []
    start_x = 0
    start_y = 0
    for y in range(0, h):
        for x in range(0, w):
            if lines[h-y-1][x] == 'S':
                to_explore.append((x, y))
                start_x = x
                start_y = y

    grid_data = defaultdict(lambda: {'visited': False, 'distance': 10000000})
    inside_map = defaultdict(lambda: {"in_pipe": False, "flood_filled": False, "inside_pipe": False})
    distance = 0
    while len(to_explore) > 0:

        print("DISTANCE " + str(distance) + ":")
        next_explore = []

        for coord in to_explore:

            x = coord[0]
            y = coord[1]

            grid_data[(x, y)] = {
                'visited': True,
                'distance': distance,
            }

            inside_map[(x*2+1, y*2+1)] = {
                "in_pipe": True
            }

            print("Log " + str(x) + "," + str(y) + " at distance " + str(distance))

            for neighbour in neighbours:
                new_x = x + neighbour[0]
                new_y = y + neighbour[1]

                if grid_data[(new_x, new_y)]["visited"]:
                    continue

                if is_connected_to(lines, w, h, x, y, new_x, new_y):
                    next_explore.append((new_x, new_y))

                    inside_map[(x * 2 + 1 + neighbour[0], y * 2 + 1 + neighbour[1])] = {
                        "in_pipe": True
                    }

        distance += 1
        to_explore = next_explore

    distance -= 1

    print("The max distance is " + str(distance))

    dw = w*2+1
    dh = h*2+1

    for y in range(dh-1, -1, -1):
        s = ""
        for x in range(0, dw):
            if inside_map[(x,y)]["in_pipe"]:
                s += "O"
            else:
                s += "."
        print(s)

    print("")

    for x in [-1, dw]:
        for y in [-1, dh]:
            flood_fill(inside_map, dw, dh, x, y)

    for y in range(dh-1, -1, -1):
        s = ""
        for x in range(0, dw):
            if inside_map[(x,y)]["in_pipe"]:
                s += "X"
            elif inside_map[(x,y)]["flood_filled"]:
                s += "O"
            else:
                s += "I"
        print(s)

    print("")

    # now count the actual insides from the acual real map by skipping the doubles
    n_inside = 0
    for y in range(h-1, -1, -1):

        s = ""
        for x in range(0, w):

            double_x = x * 2 + 1
            double_y = y * 2 + 1

            if inside_map[(double_x,double_y)]["in_pipe"]:
                s += "X"
            elif inside_map[(double_x,double_y)]["flood_filled"]:
                s += "O"
            else:
                s += "I"
                n_inside += 1

        print(s)

    print("")

    print("Total inside: " + str(n_inside))






puzzle1("input10-3.txt")
