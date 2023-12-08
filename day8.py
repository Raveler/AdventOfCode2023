import math
from collections import defaultdict
import re
from collections import Counter


def is_end_node(node):
    return node[-1] == 'Z'


def find_end_steps_and_loop_size(node, steps, instructions):
    idx = 0
    start = node
    visited = set()
    done = False
    n_steps_to_end_node = {}
    n_steps = 0

    end_nodes_visited = {}

    loop_time = -1
    while not done:
        dir = 0
        if instructions[idx] == 'R':
            dir = 1
        idx = (idx + 1) % len(instructions)
        node = steps[node][dir]
        n_steps += 1

        if is_end_node(node):

            # for the state, we take the NEXT dir
            dir = 0
            if instructions[idx] == 'R':
                dir = 1

            state = (node, dir)

            # we found a loop between end nodes!
            if state in visited:

                # get the loop time
                n_steps_to_loop_start = n_steps_to_end_node[state]
                loop_time = n_steps - n_steps_to_loop_start

                # skip the ones that are NOT in the loop - we assume they are irrelevant here
                for existing_state in end_nodes_visited.keys():
                    if n_steps_to_loop_start[existing_state] < n_steps_to_loop_start:
                        end_nodes_visited.pop(existing_state)

                done = True

            else:
                n_steps_to_end_node[state] = n_steps
                visited.add(state)


    return (list(n_steps_to_end_node.values()), loop_time)


def is_valid_steps(n_steps, n_steps_to_end_node, loop_time):
    for step_candidate in n_steps_to_end_node:
        if (n_steps - step_candidate) % loop_time == 0:
            return True
    return False


def is_valid_steps(n_steps, loops):
    for (n_steps_to_end_node, loop_time) in loops:
        found = False
        for step_candidate in n_steps_to_end_node:
            if (n_steps - step_candidate) % loop_time == 0:
                found = True
                print("Step candidate " + str(step_candidate) + " with " + str(n_steps) + " steps and " + str(loop_time) + " loop time is done!")
                break

        if not found:
            print("Ne fail for " + str(loops))
            return False

    return True

def puzzle1():
    path = "input8-3.txt"
    lines = open(path).readlines()
    text = open(path).read()

    instructions = lines[0].strip()
    node_matches = re.findall("([A-Z0-9]+) = \(([A-Z0-9]+), ([A-Z0-9]+)\)", text)

    steps = {}
    for node_match in node_matches:
        steps[node_match[0]] = [node_match[1], node_match[2]]


    # idx = 0
    # node = 'AAA'
    # n_steps = 0
    # while node != 'ZZZ':
    #     dir = 0
    #     if instructions[idx] == 'R':
    #         dir = 1
    #     idx = (idx + 1) % len(instructions)
    #     node = steps[node][dir]
    #     n_steps += 1
    #
    # print("It took " + str(n_steps) + " to get to " + node)


    # find all nodes that end with A
    nodes = []
    for node_name in steps:
        if node_name[-1] == 'A':
            nodes.append(node_name)

    idx = 0
    n_steps = 0
    print(nodes)

    largest_loop_time = 0
    largest_loop = None
    loops = []
    lcm_loop_time = 1
    for node in nodes:
        print("Node: " + str(node))
        (n_steps_to_end_node, loop_time) = find_end_steps_and_loop_size(node, steps, instructions)

        loops.append((n_steps_to_end_node, loop_time))

        print(n_steps_to_end_node)
        print(loop_time)

        lcm_loop_time = math.lcm(loop_time, lcm_loop_time)

        if loop_time > largest_loop_time:
            largest_loop_time = loop_time
            largest_loop = n_steps_to_end_node

    print("Largest loop: " + str(largest_loop_time))
    print("LCM: " + str(lcm_loop_time))

    n_loops = 1
    done = False
    n_steps = 0
    while not done:

        n_steps = lcm_loop_time * n_loops
        print("Evaluate " + str(n_steps) + " steps:")
        if is_valid_steps(n_steps, loops):
            done = True
            print("DONE!")
            break

        n_loops += 1

    print("Final steps: " + str(n_steps))








puzzle1()
