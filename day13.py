import os
import time
from intcodecomputer import IntcodeComputer


def display(screen, score):
    os.system('clear')
    x_coordinates = [p[0] for p in screen.keys()]
    y_coordinates = [p[1] for p in screen.keys()]

    for y in range(min(y_coordinates), max(y_coordinates) + 1):
        line = ""
        for x in range(min(x_coordinates), max(x_coordinates) + 1):
            if (x, y) in screen:
                val = screen[(x, y)]
                if val == 1:
                    line += "W"
                elif val == 2:
                    line += "B"
                elif val == 3:
                    line += "_"
                elif val == 4:
                    line += "0"
                elif val == 0:
                    line += " "

            else:
                    line += " "

        print(line)

    print(score)


with open("input13") as f:
    intcode = [int(v) for v in f.read().split(',')]

    computer = IntcodeComputer(intcode)
    computer.write(0, 2)

    screen = {}
    score = 0
    cmd = 0
    while not computer.terminated:
        res = computer.execute([cmd])

        for i in range(0, len(res), 3):
            x = res[i]
            y = res[i + 1]
            val = res[i + 2]

            if x == -1 and y == 0:
                score = val
            else:
                screen[(x, y)] = val
                if val == 4:
                    ballxpos = x
                elif val == 3:
                    paddlexpos = x

        display(screen, score)

        time.sleep(0.05)

        if ballxpos > paddlexpos:
            cmd = 1
        elif ballxpos < paddlexpos:
            cmd = -1
        else:
            cmd = 0

    # part1
    print(sum([1 if v == 2 else 0 for v in screen.values()]))
