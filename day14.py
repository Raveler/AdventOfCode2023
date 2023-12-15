import math
from collections import defaultdict
import re
from collections import Counter
from functools import lru_cache, cache
from pprint import pprint

def roll_to(grid, w, h, dir):

    #print("Roll in dir " + str(dir))
    if dir[0] == 0 and dir[1] == -1:
        for y in range(0, h):
            for x in range(0, w):
                if grid[(x, y)] == 'O':

                    roll_value = y - 1
                    while roll_value >= 0 and grid[(x, roll_value)] == '.':
                        grid[(x, roll_value + 1)] = '.'
                        grid[(x, roll_value)] = 'O'
                        roll_value -= 1

    elif dir[0] == 0 and dir[1] == 1:
        for y in range(h-1, -1, -1):
            for x in range(0, w):
                if grid[(x, y)] == 'O':

                    roll_value = y + 1
                    while roll_value < h and grid[(x, roll_value)] == '.':
                        grid[(x, roll_value - 1)] = '.'
                        grid[(x, roll_value)] = 'O'
                        roll_value += 1

    elif dir[0] == -1 and dir[1] == 0:
        for x in range(0, w):
            for y in range(0, h):
                if grid[(x, y)] == 'O':

                    roll_value = x - 1
                    while roll_value >= 0 and grid[(roll_value, y)] == '.':
                        grid[(roll_value + 1, y)] = '.'
                        grid[(roll_value, y)] = 'O'
                        roll_value -= 1

    elif dir[0] == 1 and dir[1] == 0:
        for x in range(w - 1, -1, -1):
            for y in range(0, h):
                if grid[(x, y)] == 'O':

                    roll_value = x + 1
                    while roll_value < w and grid[(roll_value, y)] == '.':
                        grid[(roll_value - 1, y)] = '.'
                        grid[(roll_value, y)] = 'O'
                        roll_value += 1


def calculate_Load(grid, w, h):
    load = 0
    for y in range(0, h):
        for x in range(0, w):
            if grid[(x, y)] == 'O':
                load += h - y

    return load


def get_grid_hash(grid, w, h):
    s = ""
    for y in range(0, h):
        for x in range(0, w):
            s += grid[(x, y)]
    return s


def print_grid(grid, w, h):
    for y in range(0, h):
        for x in range(0, w):
            print(grid[(x, y)], end='')
        print("")

    print("")

def perform_cycle(grid, w, h):
    dir = (0, -1)
    for k in range(0, 4):
        roll_to(grid, w, h, dir)
        dir = (dir[1], -dir[0])


def puzzle(path):
    lines = open(path).readlines()
    lines.append("")

    grid = {}
    w = len(lines[0].strip())
    h = 0

    for line in lines:

        if len(line.strip()) > 0:
            for x in range(0, w):
                grid[(x, h)] = line[x]

            h += 1

    print_grid(grid, w, h)

    hashes = {}
    n_cycles = 1000000000
    for i in range(0, n_cycles):
        print("Perform cycle " + str(i))
        perform_cycle(grid, w, h)

        hash = get_grid_hash(grid, w, h)

        if hash in hashes:
            print("We have a match at " + str(i) + " and " + str(hashes[hash]))
            print("The cycle is " + str(i - hashes[hash]))
            cycle_length = i - hashes[hash]

            # now we skip the number of cycles that fits in the remaining number
            n_cycles_skip = (n_cycles - i) // cycle_length
            i += n_cycles_skip * cycle_length
            print("We skip straight to cycle " + str(i))
            for k in range(i+1, n_cycles):
                print("Perform cycle " + str(k))
                perform_cycle(grid, w, h)
            break

        hashes[hash] = i


    sum = calculate_Load(grid, w, h)



    print("The weight is " + str(sum))


puzzle("input14-2.txt")
