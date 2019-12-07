def calculate_fuel_required(mass):
    fuel = int(mass/3) - 2

    if fuel <= 0:
        return 0
    else:
        return fuel + calculate_fuel_required(fuel)


with open("input1") as f:
    values = [int(l) for l in f]

    print(values)

    total_fuel = sum([calculate_fuel_required(v) for v in values])
    print(total_fuel)
