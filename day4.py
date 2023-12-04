from collections import defaultdict


def puzzle1():
    f = open("input4-2.txt")
    lines = f.readlines()

    total = 0
    copies = defaultdict(lambda: 1)
    for i in range(0, len(lines)):

        line = lines[i]
        split = line.split(":")[1].split("|")
        winning_numbers = [int(x) for x in split[0].strip().split()]
        numbers = [int(x) for x in split[1].strip().split()]

        if i not in copies:
            copies[i] = 1

        n_correct = 0
        score = 0
        for number in numbers:
            if number in winning_numbers:
                n_correct += 1
                if score == 0:
                    score = 1
                else:
                    score *= 2

        total += score

        for j in range(i+1, i+1+n_correct):
            copies[j] += copies[i]

    print(copies)

    print("The sum is " + str(total))
    print("The total number of scratch cards is " + str(sum(copies.values())))


puzzle1()