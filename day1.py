

def puzzle1():
    f = open("input1-1.txt")
    lines = f.readlines()

    digitStrings = [
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine"
    ]

    sum = 0
    for line in lines:

        digits = []

        for i in range(0, len(line)):
            if line[i].isdigit():
                print(line[i])
                digits.append(line[i])

            else:
                for k in range(0, len(digitStrings)):
                    digitLen = len(digitStrings[k])
                    if i + digitLen <= len(line):
                        if digitStrings[k] == line[i:i+digitLen]:
                            i = i+digitLen
                            digits.append(k+1)

        print(digits)
        sum += int(digits[0]) * 10 + int(digits[-1])


    print("Sum: " + str(sum))


puzzle1()