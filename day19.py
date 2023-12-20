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

    workflows = {}
    idx = 0
    while idx < len(lines):

        line = lines[idx]

        # reached the one between workflows and parts
        if len(line.strip()) == 0:
            idx += 1
            break

        name = line.split("{")[0]

        rules_matches = re.findall("([a-z]+)([\<\>])([0-9]+):([a-zAR]+)", line)

        fallback_target = re.findall("([a-zAR]+)\}", line)[0]

        workflows[name] = {
            "rules": rules_matches,
            "fallback": fallback_target,
        }

        idx += 1

    pprint(workflows)

    print("Start at " + str(idx))
    parts = []
    while idx < len(lines):
        line = lines[idx]
        part = {}
        split = line.strip()[1:-1].split(",")
        for s in split:
            s_split = s.split("=")
            part[s_split[0]] = int(s_split[1])
        parts.append(part)

        idx += 1

    pprint(parts)


    def go_through_workflow(part, workflow):

        for rule in workflow["rules"]:

            property = rule[0]
            value = part[property]
            op = rule[1]
            comp_value = int(rule[2])
            target = rule[3]

            if op == '<':
                if value < comp_value:
                    return target

            elif op == '>':
                if value > comp_value:
                    return target

        return workflow["fallback"]



    accepted_parts_score = 0
    for part in parts:

        workflow = workflows["in"]
        new_target = go_through_workflow(part, workflow)
        while new_target != 'R' and new_target != 'A':
            workflow = workflows[new_target]
            new_target = go_through_workflow(part, workflow)

        if new_target == 'A':
            for value in part.values():
                accepted_parts_score += value


    print("The total value of accepted parts is " + str(accepted_parts_score))


    def get_accepted_ranges(workflow, incoming_range):

        incoming_range = incoming_range.copy()

        print("Explore incoming range " + str(incoming_range) + " with workflow " + str(workflow))

        # verify each incoming range value
        for range in incoming_range.values():
            if range[0] > range[1]:
                return []

        accepted_ranges = []
        for rule in workflow["rules"]:

            property = rule[0]
            property_range = incoming_range[property]
            op = rule[1]
            comp_value = int(rule[2])
            target = rule[3]

            new_range = incoming_range.copy()

            if op == '<':
                property_range = (property_range[0], min(property_range[1], comp_value-1))
                incoming_range[property] = (max(incoming_range[property][0], comp_value), incoming_range[property][1])
            elif op == '>':
                property_range = (max(property_range[0], comp_value+1), property_range[1])
                incoming_range[property] = (incoming_range[property][0], min(incoming_range[property][1], comp_value))

            # we have an invalid range now
            if property_range[0] > property_range[1]:
                continue

            new_range[property] = property_range

            # otherwise, we propagate the range to the target
            if target == 'A':
                print("Accepted range " + str(new_range))
                accepted_ranges.append(new_range)
            elif target != 'R':
                new_workflow = workflows[target]
                accepted_ranges.extend(get_accepted_ranges(new_workflow, new_range))

            # from now on, we CANNOT be satisfying this rule! or we would have progressed through the above workflow!


        fallback = workflow["fallback"]

        if fallback == 'A':
            print("Fallback accepted range " + str(incoming_range))
            accepted_ranges.append(incoming_range)
        elif fallback != 'R':
            fallback_workflow = workflows[fallback]
            accepted_ranges.extend(get_accepted_ranges(fallback_workflow, incoming_range))


        return accepted_ranges

    initial_ranges = {
        "x": (1, 4000),
        "m": (1, 4000),
        "a": (1, 4000),
        "s": (1, 4000)
    }

    accepted_ranges = get_accepted_ranges(workflows["in"], initial_ranges)
    print(accepted_ranges)

    total_possible_parts = 0
    for accepted_range in accepted_ranges:
        total_parts = 1
        for key in accepted_range:
            range = accepted_range[key]
            total_parts *= range[1] - range[0] + 1
        print(str(accepted_range) + " has " + str(total_parts) + " total parts")
        total_possible_parts += total_parts

    print("The total acceptable parts is " + str(total_possible_parts))


puzzle("input19-2.txt")
