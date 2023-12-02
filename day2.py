

def puzzle1():
    f = open("input2-1.txt")
    lines = f.readlines()

    sum = 0
    power_sum = 0

    for line in lines:

        split = line.split(":")
        print(split)
        game_id = int(split[0].split(" ")[1])

        draw_set_strings = split[1].split(";")

        print("Game: " + str(game_id))
        max_hand = {
            'red': 12,
            'green': 13,
            'blue': 14
        }

        min_hand = {
            'red': 0,
            'green': 0,
            'blue': 0
        }

        ok = True
        for draw_set_string in draw_set_strings:
            draws_string = draw_set_string.split(", ")

            for draw_string in draws_string:
                draw_split = draw_string.strip().split(" ")
                print(draw_split)
                n = int(draw_split[0])
                color = draw_split[1]

                min_hand[color] = max(min_hand[color], n)

                if n > max_hand[color]:
                    ok = False

        power_sum += min_hand['red'] * min_hand['green'] * min_hand['blue']
        if ok:
            sum += game_id



    print("The sum of possible games is " + str(sum))
    print("The power sum is " + str(power_sum))


puzzle1()