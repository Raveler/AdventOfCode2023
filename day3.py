
def is_adjacent_to_symbol(y, start_x, stop_x, lines, w, h):
    x1 = start_x - 1
    x2 = stop_x + 1
    y1 = y - 1
    y2 = y + 1
    for x in range(x1, x2+1):
        for y in range(y1, y2+1):
            if x < 0 or x >= w:
                continue
            if y < 0 or y >= h:
                continue

            c = lines[y][x]
            if c.isdigit() or c == '.':
                continue
            return True
    return False


def get_gear(y, start_x, stop_x, lines, w, h):
    x1 = start_x - 1
    x2 = stop_x + 1
    y1 = y - 1
    y2 = y + 1
    for x in range(x1, x2+1):
        for y in range(y1, y2+1):
            if x < 0 or x >= w:
                continue
            if y < 0 or y >= h:
                continue

            c = lines[y][x]
            if c == '*':
                return (x, y)
    return None

def puzzle1():
    f = open("input3-2.txt")
    lines = f.readlines()

    h = len(lines)
    w = len(lines[0].strip())

    gears = {}
    sum = 0
    for y in range(0, h):
        has_num = False
        num = 0
        num_length = 0
        for x in range(0, w+1):

            # we are still parsing digits
            if x < w and lines[y][x].isdigit():
                num = num * 10 + int(lines[y][x])
                num_length += 1
                has_num = True

            elif has_num:

                gear_coord = get_gear(y, x-num_length, x-1, lines, w, h)
                if gear_coord is not None:
                    if gear_coord not in gears:
                        gears[gear_coord] = []

                    gears[gear_coord].append(num)

                if is_adjacent_to_symbol(y, x-num_length, x-1, lines, w, h):
                    sum += num

                has_num = False
                num = 0
                num_length = 0


    print("The sum of valid numbers is " + str(sum))

    gear_sum = 0
    for gear_coord in gears:

        gear_nums = gears[gear_coord]
        if len(gear_nums) == 2:
            gear_sum += gear_nums[0] * gear_nums[1]

    print("The gear sum is " + str(gear_sum))


puzzle1()