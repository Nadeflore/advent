def get_orbit_chain(obj, orbits):
    chain = []
    while obj != 'COM':
        chain.insert(0, obj)
        obj = orbits[obj]

    return [obj] + chain


with open("input6") as f:
    orbits = {line.split(')')[1].strip(): line.split(')')[0] for line in f}

    # 1st part
    total = 0
    for obj, orbit in orbits.items():
        total += len(get_orbit_chain(obj, orbits)) - 1

    print(total)

    # 2nd part
    youchain = get_orbit_chain("YOU", orbits)
    sanchain = get_orbit_chain("SAN", orbits)

    common_length = 0
    for you, san in zip(youchain, sanchain):
        if you != san:
            break
        common_length += 1

    print("found {}".format(len(youchain) + len(sanchain) - 2 * common_length - 2))
