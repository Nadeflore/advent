from intcodecomputer import IntcodeComputer

with open("input11") as f:
    intcode = [int(v) for v in f.read().split(',')]

    computer = IntcodeComputer(intcode)

    pos = (0, 0)
    orientation = 0
    # part 1
    # whitepanels = set()
    # part 2
    whitepanels = {(0, 0)}
    paintedpanels = set()

    while not computer.terminated:
        currentpanelcolor = 1 if pos in whitepanels else 0
        color, turn = computer.execute([currentpanelcolor])

        paintedpanels.add(pos)

        if color == 1:
            whitepanels.add(pos)
        else:
            whitepanels.discard(pos)

        if turn == 1:
            orientation = (orientation + 1) % 4
        else:
            orientation = (orientation - 1) % 4

        if orientation == 0:
            pos = (pos[0], pos[1] - 1)
        elif orientation == 1:
            pos = (pos[0] + 1, pos[1])
        elif orientation == 2:
            pos = (pos[0], pos[1] + 1)
        elif orientation == 3:
            pos = (pos[0] - 1, pos[1])

    # part1
    print(len(paintedpanels))

    # part2
    x_coordinates = [p[0] for p in whitepanels]
    y_coordinates = [p[1] for p in whitepanels]

    for y in range(min(y_coordinates), max(y_coordinates) + 1):
        line = ""
        for x in range(min(x_coordinates), max(x_coordinates) + 1):
            line += "#" if (x, y) in whitepanels else " "

        print(line)
