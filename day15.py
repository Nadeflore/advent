import os
import time
from intcodecomputer import IntcodeComputer

walls = set()
oxygen = set()


def display(currentpos=(0, 0)):
    if not walls:
        return

    os.system('clear')
    x_coordinates = [p[0] for p in walls]
    y_coordinates = [p[1] for p in walls]

    for y in range(min(y_coordinates), max(y_coordinates) + 1):
        line = ""
        for x in range(min(x_coordinates), max(x_coordinates) + 1):
            if (x, y) in walls:
                line += "#"
            elif (x, y) in oxygen:
                line += "O"
            elif (x, y) == currentpos:
                line += "S"
            else:
                line += " "

        print(line)
    time.sleep(0.05)


def move(pos, direction):
    if direction == 1:
        return (pos[0], pos[1] - 1)
    elif direction == 2:
        return (pos[0], pos[1] + 1)
    elif direction == 3:
        return (pos[0] - 1, pos[1])
    elif direction == 4:
        return (pos[0] + 1, pos[1])
    else:
        raise Exception("Unknown direction {}".format(direction))


def step_required(computer, pos, pastpos):
    display(pos)
    before_move_state = computer.savestate()
    best_result = None
    for direction in range(1, 5):
        # Check moving in this directions is going going back to a previous position
        targetpos = move(pos, direction)
        if targetpos in pastpos:
            continue

        # Move in this direction
        status = computer.execute([direction])[0]

        if status == 0:
            # Hit a wall
            result = None
            walls.add(targetpos)
        elif status == 2:
            # Found it
            result = 0
            oxygen.add(targetpos)
        elif status == 1:
            # Nothing special, continue recursively
            result = step_required(computer, targetpos, pastpos + [pos])

        if result is not None and (best_result is None or result < best_result):
            best_result = result

        computer.loadstate(before_move_state)

    if best_result is not None:
        best_result += 1

    return best_result


with open("input15") as f:

    intcode = [int(v) for v in f.read().split(',')]

    computer = IntcodeComputer(intcode)

    # part 1
    steps = step_required(computer, (0, 0), [])
    print("{} steps to oxygen".format(steps))

    # part 2
    propagated = True
    minutes = -1
    while propagated:
        propagated = False
        newoxygen = set()
        for pos in oxygen:
            for direction in range(1, 5):
                targetpos = move(pos, direction)
                if targetpos not in walls and targetpos not in oxygen:
                    newoxygen.add(targetpos)
                    propagated = True

        oxygen |= newoxygen
        minutes += 1
        display()

    print("{} steps to oxygen".format(steps))
    print("took {} minutes for o2 to propagate".format(minutes))
