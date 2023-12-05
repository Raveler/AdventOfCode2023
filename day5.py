from collections import defaultdict
import re


def cut_number_range(number_range, cut_points):

    cut_number_ranges = [number_range]

    for i in range(0, len(cut_points)):
        cut_point = cut_points[i]

        new_cut_number_ranges = []
        for number_range in cut_number_ranges:
            if number_range[0] <= cut_point <= number_range[1]:
                print("Cut " + str(number_range) + " by cut point " + str(cut_point))

                # this is the START of a cut range
                if i % 2 == 1:
                    new_cut_number_ranges.append([number_range[0], cut_point])
                    if cut_point < number_range[1]:
                        new_cut_number_ranges.append([cut_point+1, number_range[1]])

                # this is the END of a cut range
                else:
                    if number_range[0] < cut_point:
                        new_cut_number_ranges.append([number_range[0], cut_point-1])
                    new_cut_number_ranges.append([cut_point, number_range[1]])

            # no cut!
            else:
                new_cut_number_ranges.append(number_range)

        cut_number_ranges = new_cut_number_ranges

    return cut_number_ranges


def cut_number_ranges(number_ranges, cut_points):
    all_cuts = []
    for number_range in number_ranges:
        cuts = cut_number_range(number_range, cut_points)
        for cut in cuts:
            all_cuts.append(cut)
    return all_cuts


def puzzle1():
    f = open("input5-2.txt")
    text = f.read()

    matches = re.findall("([a-z]+)-to-([a-z]+) map:\n([0-9 \n]+)", text)

    mappings = {}
    for match in matches:

        print(match)
        source = match[0]
        dest = match[1]

        mappings[source] = {
            'dest': dest,
            'ranges': [],
            'cut_points': [],
        }

        ranges = match[2].split("\n")

        cut_points = []
        cut_point_offsets = []
        for range_string in ranges:
            if len(range_string) == 0:
                continue

            range_data = [int(x) for x in range_string.split()]

            mappings[source]['ranges'].append(range_data)

            offset = range_data[0] - range_data[1]

            cut_points.append({'value': range_data[1], 'offset': offset})
            cut_points.append({'value': range_data[1] + range_data[2] - 1, 'offset': offset})

        #cut_points.sort(key=lambda x: x['value'])

        mappings[source]['cut_points'] = cut_points


    match = re.search("seeds: ([0-9 ]+)", text)
    seeds = [int(x) for x in match[1].split()]

    # part 1
    lowest_location = -1
    for seed in seeds:

        source = 'seed'
        number = seed

        while source in mappings:

            mapping = mappings[source]

            for r in mapping['ranges']:

                if r[1] <= number < r[1] + r[2]:
                    diff = number - r[1]
                    number = r[0] + diff
                    #print('Number is mapped from source ' + source + ' to dest ' + mapping['dest'] + ' to number ' + str(number))
                    break

            source = mapping['dest']

        # update the source so we proceed
        if lowest_location < 0:
            lowest_location = number
        else:
            lowest_location = min(lowest_location, number)

    print("The lowest location is " + str(lowest_location))

    # part 2
    number_ranges = []
    for i in range(0, len(seeds), 2):
        number_range = [seeds[i], seeds[i] + seeds[i+1]-1]
        number_ranges.append(number_range)

    source = 'seed'
    print("Original number ranges: " + str(number_ranges))
    while source in mappings:

        mapping = mappings[source]

        # cut all number ranges into pieces
        cut_points = mapping['cut_points']
        cut_point_numbers = [x['value'] for x in mapping['cut_points']]

        print("Cut points: " + str(cut_point_numbers))
        number_ranges = cut_number_ranges(number_ranges, cut_point_numbers)

        print("Cut number ranges: " + str(number_ranges))
        for number_range in number_ranges:

            for i in range(0, len(cut_points), 2):
                cut_min = cut_points[i]['value']
                cut_max = cut_points[i+1]['value']
                offset = cut_points[i]['offset']

                if cut_min <= number_range[0] and number_range[1] <= cut_max:
                    print("Offset number_range " + str(number_range) + " from cut " + str(cut_min) + " -> " + str(cut_max) + " by offset " + str(offset))
                    number_range[0] += offset
                    number_range[1] += offset
                    break

        source = mapping['dest']
        print("Transformed number ranges: " + str(number_ranges))

    lowest_location = 100000000000000000
    for number_range in number_ranges:
        lowest_location = min(lowest_location, number_range[0])

    print("The lowest RANGE number location is " + str(lowest_location))



puzzle1()