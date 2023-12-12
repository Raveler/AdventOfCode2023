import math
from collections import defaultdict
import re
from collections import Counter
from functools import lru_cache, cache
from pprint import pprint

@cache
def cached_return_arrangements(springs, active_group, groups_str, total_springs_left, total_springs_left_in_groups):
    if len(groups_str) == 0:
        return calculate_arrangements(springs, active_group, [], total_springs_left, total_springs_left_in_groups)
    groups = [int(x) for x in groups_str.split(",")]
    return calculate_arrangements(springs, active_group, groups, total_springs_left, total_springs_left_in_groups)


def merge_groups(groups):
    return ','.join([str(x) for x in groups])


def calculate_arrangements(springs, active_group, groups, total_springs_left = None, total_springs_left_in_groups = None):

    if total_springs_left is None:
        total_springs_left = springs.count('#')
        total_springs_left_in_groups = sum(groups)

    #print("Total springs left " + str(total_springs_left) + " vs in groups " + str(total_springs_left_in_groups))

    # if, at some point, we have more springs left in the spring list than we have left in groups, we short-cut this as invalid
    if total_springs_left_in_groups < total_springs_left:
        #print("hum")
        return 0

    # we reached the end
    if len(springs) == 0:

        #print("Reached final state with " + str(springs) + " and " + str(groups))

        # there are still groups left - we couldn't assign all of them!
        if len(groups) > 0 or (active_group is not None and active_group > 0):
            return 0

        # we reached a valid state
        else:
            #print("We found a valid final state " + str(springs) + " with " + str(groups))
            return 1


    c = springs[0]
    all_arrangements = []

    if c == '?':
        all_arrangements = 0
        new_springs = '#' + springs[1:]
        all_arrangements += cached_return_arrangements(new_springs, active_group, merge_groups(groups), total_springs_left + 1, total_springs_left_in_groups)
        new_springs = '.' + springs[1:]
        all_arrangements += cached_return_arrangements(new_springs, active_group, merge_groups(groups), total_springs_left, total_springs_left_in_groups)
        return all_arrangements

    # at this point we always have . or #
    #print("Evaluate " + str(springs) + " with active group " + str(active_group) + " and groups " + str(groups))

    # we have a spring - we NEED to be in a group or activate one
    if c == '#':

        # no active group - activate one!
        if active_group is None:

            # can't
            if len(groups) == 0:
                #print("# but no groups")
                return 0

            # activate the next group!
            else:
                new_groups = groups.copy()
                new_active_group = new_groups.pop(0) - 1 # already got one # covered
                new_springs = springs[1:]
                return cached_return_arrangements(new_springs, new_active_group, merge_groups(new_groups), total_springs_left - 1, total_springs_left_in_groups - 1)


        else:

            # active group is empty! - bad
            if active_group == 0:
                #print("# but active group is empty")
                return 0

            else:
                new_springs = springs[1:]
                return cached_return_arrangements(new_springs, active_group - 1, merge_groups(groups), total_springs_left, total_springs_left_in_groups)

    # c == '.'
    else:

        if active_group is None:

            # we just continue like this since we can't activate
            new_springs = springs[1:]
            return cached_return_arrangements(new_springs, active_group, merge_groups(groups), total_springs_left, total_springs_left_in_groups)

        else:

            # active group is donezo - we de-activate it
            if active_group == 0:
                new_springs = springs[1:]
                return cached_return_arrangements(new_springs, None, merge_groups(groups), total_springs_left, total_springs_left_in_groups)

            #  else, bad! we can't skip because we have an active group
            else:
                #print(". but active group is not empty")
                return 0



def puzzle(path):
    lines = open(path).readlines()

    sum = 0
    repeats = 5
    for line in lines:
        split = line.split(" ")
        springs = split[0].strip()
        groups = [int(x) for x in split[1].split(",")]

        repeat_springs = ""
        repeat_groups = []
        for i in range(0, repeats):
            if i > 0:
                repeat_springs += "?"
            repeat_springs += springs
            repeat_groups.extend(groups)

        arrangements = calculate_arrangements(repeat_springs, None, repeat_groups)
        print("Task " + str(repeat_springs) + " with " + str(repeat_groups) + " groups has " + str(arrangements) + " valid states")
        sum += arrangements

    print("Total number of arrangements: " + str(sum))



puzzle("input12-2.txt")
