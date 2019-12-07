def get_wire_coordinates(wire):
    coordinates = []
    x = 0
    y = 0
    for move in wire:
        direction = move[0]
        length = int(move[1:])

        x_inc = 0
        y_inc = 0
        if direction == 'R':
            x_inc = 1
        elif direction == 'L':
            x_inc = -1
        elif direction == 'U':
            y_inc = 1
        elif direction == 'D':
            y_inc = -1

        for v in range(length):
            x += x_inc
            y += y_inc
            coordinates.append((x, y))

    return coordinates


with open("input3") as f:
    data = list(f.readlines())
    wire1 = data[0].strip().split(',')
    wire2 = data[1].strip().split(',')

    coordinates1 = get_wire_coordinates(wire1)
    coordinates2 = get_wire_coordinates(wire2)

    print(coordinates1)
    print(coordinates2)

    intersections = set(coordinates1).intersection(set(coordinates2))
    print(intersections)

    print(min([abs(inter[0]) + abs(inter[1]) for inter in intersections]))
