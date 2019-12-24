import copy
import itertools
from collections import defaultdict


DEFAULTMAP = [['.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.'], ['.', '.', '?', '.', '.'], ['.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.']]

def displaymap(areamap):
    for line in areamap:
        print(''.join(line))

    print()


def displaymaps(areamaps):
    sortedbylevel = sorted(areamaps.items(), key=lambda e: e[0])
    for level, areamap in sortedbylevel:
        print("Level {}".format(level))
        displaymap(areamap)


def getpositon(areamap, x, y):
    """return None if x, y is out of range,
    else return value in map
    """
    if x < 0 or y < 0:
        return None
                    
    try:
        return areamap[y][x]
    except IndexError:
        return None


def getlevel(areamaps, level):
    if level in areamaps:
        return areamaps[level]

    return DEFAULTMAP


def nextstepforlevel(areamaps, level):
    areamap = areamaps[level]
    newmap = copy.deepcopy(areamap)

    for y, line in enumerate(areamap):
        for x, tile in enumerate(line):
            if tile == '?':
                continue

            adjacentbugs = 0
            for offsetx, offsety in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                content = getpositon(areamap, x + offsetx, y + offsety)
                if content == '?':
                    # Inner map
                    innermap = getlevel(areamaps, level + 1)
                    if offsetx == 0:
                        innery = 0 if offsety == 1 else -1
                        contents = [innermap[innery][innerx] for innerx in range(5)]
                    else:
                        innerx = 0 if offsetx == 1 else -1
                        contents = [innermap[innery][innerx] for innery in range(5)]

                    adjacentbugs += sum([1 if c == '#' else 0 for c in contents])
                else:

                    if content is None:
                        # Outer map
                        outermap = getlevel(areamaps, level - 1)
                        content = outermap[2 + offsety][2 + offsetx]

                    if content == '#':
                        adjacentbugs += 1


            if tile == '#':
                if adjacentbugs != 1:
                    newmap[y][x] = '.'

            else:
                if adjacentbugs in [1, 2]:
                    newmap[y][x] = '#'

    return newmap


def nextstep(areamaps):
    newmaps = {}
    for level, areamap in areamaps.items():
        newmaps[level] = nextstepforlevel(areamaps, level)

    # Add new levels of map if boudaries maps contains bugs
    minlevel = min(areamaps.keys())
    if countbugs(areamaps[minlevel]):
        newmaps[minlevel - 1] = DEFAULTMAP

    maxlevel = max(areamaps.keys())
    if countbugs(areamaps[maxlevel]):
        newmaps[maxlevel + 1] = DEFAULTMAP

    return newmaps


def countbugs(areamap):
    count = 0
    for line in areamap:
        for tile in line:
            if tile == '#':
                count += 1

    return count


def counttotalbugs(areamaps):
    count = 0
    for areamap in areamaps.values():
        count += countbugs(areamap)

    return count


def main():
    with open("input24") as f:
        initialareamap = [list(line.strip()) for line in f.readlines()]
        initialareamap[2][2] = '?'
        areamaps = {}
        areamaps[0] = initialareamap
        areamaps[-1] = DEFAULTMAP
        areamaps[1] = DEFAULTMAP

        for i in range(200):
            areamaps = nextstep(areamaps)

        displaymaps(areamaps)

        print(counttotalbugs(areamaps))


main()
