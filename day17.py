from intcodecomputer import IntcodeComputer

orientations = ["^", ">", "v", "<"]


def calculatetargetcoords(position, orientation):
    if orientation == '^':
        return (position[0], position[1] - 1)

    if orientation == 'v':
        return (position[0], position[1] + 1)

    if orientation == '<':
        return (position[0] - 1, position[1])

    if orientation == '>':
        return (position[0] + 1, position[1])


def calculatetargetorientation(orientation, turn):
    orientation_int = orientations.index(orientation)
    turn_int = -1 if turn == "L" else 1

    return orientations[(orientation_int + turn_int) % 4]


def aggregatesones(commands):
    count = 0
    for cmd in commands:
        if cmd == '1':
            count += 1
        else:
            if count != 0:
                yield str(count)
            count = 0
            yield cmd

    if count != 0:
        yield str(count)


def commandstostring(commands):
    return ','.join(commands)


def isfitinmemory(commands):
    return len(commandstostring(commands)) <= 20


def updatemaskwithpatternuses(data, pattern, mask):
    """ Return a new mask (Does not mutate existing) with True where the pattern apply
    """
    mask = mask.copy()
    for i in range(len(data) - len(pattern) + 1):
        if data[i:i + len(pattern)] == pattern and not any(mask[i:i + len(pattern)]):
            mask[i:i + len(pattern)] = [True] * len(pattern)

    return mask


def getrepeatpatternlength(data, i, j, mask):
    """Return the length of repeated pattern from index i and j that does not overlap mask
    """
    initialj = j
    length = 0
    while i < len(data) and j < len(data) and i < initialj and not mask[i] and not mask[j] and data[i] == data[j]:
        length += 1
        i += 1
        j += 1

    return length


def findrepeatingpatterns(data, mask):
    """return all possible repeating patterns with size >= 4 and fitting in memory, that does not overlap mask
    """
    for i in range(len(data)):
        for j in range(i):
            patternlength = getrepeatpatternlength(data, j, i, mask)
            pattern = data[i:i + patternlength]
            if patternlength >= 4 and isfitinmemory(pattern):
                yield pattern


def findpatternscoverall(data, mask, maxpatterns):
    """Attemps to find a maximum of maxpatterns patterns that covers the whole data where mask is False

    Returns a list of patterns covering the data or None if no matching set of patterns could be found
    """
    # Display
    coveredcommands = ""
    for cmd, cov in zip(data, mask):
        color = '\033[92m' if cov else '\033[91m'
        coveredcommands += color + cmd + ', ' + '\033[0m'

    print(coveredcommands)

    # Find repeating patterns
    possiblepatterns = list(findrepeatingpatterns(data, mask))

    # Order by size desc
    possiblepatterns.sort(key=lambda e: len(e), reverse=True)
    for pattern in possiblepatterns:
        newmask = updatemaskwithpatternuses(data, pattern, mask)

        # Check if everything is covered
        if all(newmask):
            return [pattern]

        # Check if we can still try to add more patterns
        if maxpatterns > 1:
            # Try to add more patterns recursively
            subpatterns = findpatternscoverall(data, newmask, maxpatterns - 1)

            if subpatterns is not None:
                return [pattern] + subpatterns

        # If subpatern was not successful, try next pattern

    # Tried all pattern with no luck
    return None


def main():
    with open("input17") as f:

        intcode = [int(v) for v in f.read().split(',')]

        computer = IntcodeComputer(intcode)

        res = computer.execute([])

        view_str = ''.join([chr(v) for v in res])

        lines = view_str.splitlines()

        for line in lines:
            print(line)

        position = None
        orientation = None

        # Part 1
        total = 0
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                try:
                    if (char == '#' and
                       lines[y - 1][x] == '#' and
                       lines[y + 1][x] == '#' and
                       lines[y][x - 1] == '#' and
                       lines[y][x + 1] == '#'):
                        total += x * y
                except IndexError:
                    pass

                if char in orientations:
                    position = (x, y)
                    orientation = char

        print(total)

        # Part 2
        # Find path
        commands = []
        while True:
            tx, ty = calculatetargetcoords(position, orientation)
            try:
                target = lines[ty][tx]
            except IndexError:
                target = None
                pass

            if target == "#":
                commands.append('1')
                position = (tx, ty)
            else:
                for turn in ['L', 'R']:
                    targetorienation = calculatetargetorientation(orientation, turn)
                    tx, ty = calculatetargetcoords(position, targetorienation)
                    try:
                        target = lines[ty][tx]
                    except IndexError:
                        target = None
                        pass

                    if target == "#":
                        # This direction looks promising
                        commands.append(turn)
                        orientation = targetorienation
                        break
                else:
                    # Could not find anywhere to get next, must be the end
                    break

        commands = list(aggregatesones(commands))

        # Attempt to divide the commands in 3 routines covering everything
        routines = findpatternscoverall(commands, [False] * len(commands), 3)

        routinecalls = []
        i = 0
        while i < len(commands):
            # Find routine to use
            for routineid, routine in enumerate(routines):
                if commands[i:i + len(routine)] == routine:
                    routinecalls.append(['A', 'B', 'C'][routineid])
                    i += len(routine)
                    break
            else:
                raise Exception("Could not find routine")

        # Add robot subroutines to call
        robotinputs = commandstostring(routinecalls) + "\n"

        # Add commands for each subroutines
        for routine in routines:
            robotinputs += commandstostring(routine) + "\n"

        # Add continous video feed 'no'
        robotinputs += "n\n"

        print(robotinputs)

        # Send this to the robot
        computer = IntcodeComputer(intcode)
        computer.write(0, 2)
        res = computer.execute([ord(c) for c in robotinputs])

        view_str = ''.join([chr(v) for v in res[:-1]])
        print(view_str)

        # Final ouput value
        print(res[-1])


main()
