import re
import itertools
import copy
import math


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


with open("input12") as f:
    moons = []
    for line in f:
        res = re.search("<x=(-?\d+), y=(-?\d+), z=(-?\d+)>", line)

        moons.append({
            "pos": [int(res.group(1)), int(res.group(2)), int(res.group(3))],
            "vel": [0, 0, 0]
        })

    initialstate = copy.deepcopy(moons)

    # First part

    for j in range(1000):
        # update velocity
        for moon1, moon2 in itertools.combinations(moons, 2):
            for i in range(3):
                if moon1["pos"][i] < moon2["pos"][i]:
                    moon1["vel"][i] += 1
                    moon2["vel"][i] -= 1
                elif moon1["pos"][i] > moon2["pos"][i]:
                    moon1["vel"][i] -= 1
                    moon2["vel"][i] += 1

        # Update positions
        for moon in moons:
            for i in range(3):
                moon["pos"][i] += moon["vel"][i]

    print("moons {}".format(moons))

    # Energy
    energy = 0
    for moon in moons:
        pote = 0
        cine = 0
        for i in range(3):
            pote += abs(moon["pos"][i])
            cine += abs(moon["vel"][i])

        energy += pote * cine

    print(energy)

    # Second part
    moons = copy.deepcopy(initialstate)

    periods = [None] * 3

    for i in range(3):
        steps = 1
        while True:
            # update velocity
            for moon1, moon2 in itertools.combinations(moons, 2):
                    if moon1["pos"][i] < moon2["pos"][i]:
                        moon1["vel"][i] += 1
                        moon2["vel"][i] -= 1
                    elif moon1["pos"][i] > moon2["pos"][i]:
                        moon1["vel"][i] -= 1
                        moon2["vel"][i] += 1

            # Update positions
            for moon in moons:
                moon["pos"][i] += moon["vel"][i]

            if all([m["pos"][i] == mi["pos"][i] and m["vel"][i] == mi["vel"][i] for m, mi in zip(moons, initialstate)]):
                print("coordinate {} has a period of {} steps".format(i, steps))
                periods[i] = steps
                break

            steps += 1

    # steps = periods.copy()
    #
    # while not (steps[0] == steps[1] == steps[2]):
    #     mindim = steps.index(min(steps))
    #
    #     steps[mindim] += periods[mindim]
    #
    # print(steps)

    print(lcm(periods[0], lcm(periods[1], periods[2])))
