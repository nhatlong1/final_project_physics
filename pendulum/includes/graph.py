def coordinates_process(lines, count):
    if not lines:
        temp_1 = []
    else:
        temp_1 = [i.strip() for i in lines.split(" ")]

    if not count:
        temp_2 = []
    else:
        temp_2 = [i.strip() for i in count.split(' ')]

    if not temp_1 or not temp_2:
        return (), ()

    position_x = [int(i) for i in temp_1]
    position_y = [int(i) for i in temp_2[:len(temp_1)]]
    return position_x, position_y