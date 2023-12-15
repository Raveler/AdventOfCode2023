import math
from collections import defaultdict
import re
from collections import Counter
from functools import lru_cache, cache
from pprint import pprint

def calculate_hash(s):
    value = 0
    for c in s.strip():
        value += ord(c)
        value *= 17
        value %= 256
    return value


def puzzle(path):
    lines = open(path).readlines()
    line = lines[0]

    split = line.split(",")

    sum = 0
    boxes = defaultdict(lambda: [])
    for s in split:


        # this is a replace command
        if '=' in s:

            cmd_split = s.split("=")
            label = cmd_split[0]
            hash = calculate_hash(label)
            focal_length = int(cmd_split[1])

            box = boxes[hash]
            found = False
            for i in range(0, len(box)):
                if box[i]["label"] == label:
                    box[i]["focal_length"]  = focal_length
                    found = True
                    break

            if not found:
                box.append({
                    "label": label,
                    "focal_length": focal_length
                })

        else:
            label = s[:-1]
            hash = calculate_hash(label)

            box = boxes[hash]
            for i in range(0, len(box)):
                if box[i]["label"] == label:
                    boxes[hash].pop(i)
                    break

    focusing_power = 0
    for box_index in range(0, 256):
        box = boxes[box_index]
        for i in range(0, len(box)):
            focusing_power += (1 + box_index) * (i + 1) * box[i]["focal_length"]

    print("The focusing power is " + str(focusing_power))



puzzle("input15-2.txt")
