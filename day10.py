import math


def calculateangle(source, pos):
    """ Return angle of pos view from source
        value is 0 at top, 90 on the right, 180 at bottom...
    """
    sourcex, sourcey = source
    posx, posy = pos

    angle = math.degrees(math.atan2(posy - sourcey, posx - sourcex))

    angle = (angle + 90) % 360

    return angle


def drawline(coord1, coord2):
    """ Returns whole number coordinates between two points
    """
    x1, y1 = coord1
    x2, y2 = coord2
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    coords = set()

    xdir = 1 if x1 <= x2 else -1
    ydir = 1 if y1 <= y2 else -1

    for y in range(1, abs(y2 - y1)):
        x = dx * y / dy
        if x.is_integer():
                coords.add((x1 + int(x) * xdir, y1 + y * ydir))

    for x in range(1, abs(x2 - x1)):
        y = dy * x / dx
        if y.is_integer():
                coords.add((x1 + x * xdir, y1 + int(y) * ydir))

    return coords


with open("input10") as f:
    asmap = [list(l.strip()) for l in f]

    asteroidcoords = [(x, y) for y, l in enumerate(asmap) for x, obj in enumerate(l) if obj == '#']

    results = []
    for coord in asteroidcoords:
        cansee = 0
        for coord2 in asteroidcoords:
            if coord == coord2:
                continue
            linecoords = drawline(coord, coord2)
            if not linecoords.intersection(set(asteroidcoords)):
                cansee += 1

        results.append((coord, cansee))

    best = max(results, key=lambda e: e[1])
    print("best is {}".format(best))

    # second part

    bestcoord = best[0]

    count = 0
    while len(asteroidcoords) > 1:
        destroyed = []
        for coord in asteroidcoords:
            if coord == bestcoord:
                continue
            linecoords = drawline(bestcoord, coord)
            if not linecoords.intersection(set(asteroidcoords)):
                destroyed.append(coord)

        for coord in sorted([(calculateangle(bestcoord, c), c) for c in destroyed], key=lambda e: e[0]):
            count += 1
            print("{} destroy {}".format(count, coord[1]))

        asteroidcoords = list(set(asteroidcoords) - set(destroyed))
