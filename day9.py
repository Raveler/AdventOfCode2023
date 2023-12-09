import math
from collections import defaultdict
import re
from collections import Counter

def extrapolate(sequence, index, sign):

    print(sequence)
    # get the difference between subsequent numbers
    diff_sequence = []
    all_zeroes = True
    for i in range(0, len(sequence)-1):
        diff = sequence[i+1] - sequence[i]
        diff_sequence.append(diff)
        if diff != 0:
            all_zeroes = False


    # bottom case - we add nothing to the last value, so we just return the last value
    if all_zeroes:
        return sequence[index]

    else:
        return sequence[index] + sign * extrapolate(diff_sequence, index, sign)




def puzzle1():
    path = "input9-2.txt"
    lines = open(path).readlines()

    sum = 0
    prev_sum = 0
    for line in lines:
        sequence = [int(x) for x in line.split(" ")]
        print(sequence)
        next_value = extrapolate(sequence, -1, 1)
        prev_value = extrapolate(sequence, 0, -1)
        sum += next_value
        prev_sum += prev_value
        print("Next value is " + str(next_value))


    print("Total sum of extrapolations: " + str(sum))
    print("Total sum of prev values: " + str(prev_sum))








puzzle1()
