import copy
import itertools


def displaymap(areamap):
    for line in areamap:
        print(''.join(line))

    print()


def getpositon(areamap, x, y):
    """return '.' if x, y is out of range,
    else return value in map
    """
    if x < 0 or y < 0:
        return '.'
                    
    try:
        return areamap[y][x]
    except IndexError:
        return '.'


def calculatebiodiversity(areamap):
    biodiversity = 0
    index = 0
    for line in areamap:
        for tile in line:
            if tile == '#':
                biodiversity += 2 ** index 

            index += 1

    return biodiversity


def nextstep(areamap):
    newmap = copy.deepcopy(areamap)

    for y, line in enumerate(areamap):
        for x, tile in enumerate(line):
            adjacentbugs = 0
            for offsetx, offsety in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                content = getpositon(areamap, x + offsetx, y + offsety)
                if content == '#':
                    adjacentbugs += 1

            if tile == '#':
                if adjacentbugs != 1:
                    newmap[y][x] = '.'

            else:
                if adjacentbugs in [1, 2]:
                    newmap[y][x] = '#'

    return newmap




def main():
    with open("input24") as f:
        areamap = [list(line.strip()) for line in f.readlines()]
        displaymap(areamap)

        previousstates = []
        while areamap not in previousstates:
            previousstates.append(areamap)
            areamap = nextstep(areamap)
            displaymap(areamap)

        print("repeated state")
        print(calculatebiodiversity(areamap))



main()
