from collections import defaultdict
import re



def puzzle1():
    f = open("input6-2.txt")
    lines = f.readlines()
    times = [int(x) for x in re.findall("[0-9]+", lines[0])]
    records = [int(x) for x in re.findall("[0-9]+", lines[1])]

    total = 1
    for race_index in range(0, len(times)):

        time = times[race_index]
        record = records[race_index]

        n_wins = 0
        for speed in range(1, time+1):
            time_left = time - speed
            distance = time_left * speed

            if distance > record:
                n_wins += 1

        print("Race " + str(race_index) + " has " + str(n_wins) + " wins")
        total *= n_wins

    print("Total: " + str(total))

def puzzle2():
    f = open("input6-2.txt")
    lines = f.readlines()

    time = int(re.findall("[0-9]+", lines[0].replace(" ", ""))[0])
    record  = int(re.findall("[0-9]+", lines[1].replace(" ", ""))[0])

    print("Time: " + str(time) + ", record: " + str(record))

    n_wins = 0
    for speed in range(1, time + 1):
        time_left = time - speed
        distance = time_left * speed

        if distance > record:
            n_wins += 1

    print("Number of wins: " + str(n_wins))







puzzle1()
puzzle2()