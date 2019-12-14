import math
from collections import defaultdict


reactions = {}


def calculate_ore_needed_for(material, qty_needed, inventory):
    if material == "ORE":
        return qty_needed

    # If there is enough leftovers in inventory, use that
    if inventory[material] >= qty_needed:
        inventory[material] -= qty_needed
        return 0

    # Use amount available in inventory
    qty_needed -= inventory[material]
    inventory[material] = 0

    # Produce
    ore_needed = 0
    reaction = reactions[material]
    # How many times this reaction needs to be made to produced desired qty
    multipier = math.ceil(qty_needed / reaction["out"])

    # for each input ingredient
    for qty, ingredient in reaction["in"]:
        ore_needed += calculate_ore_needed_for(ingredient, qty * multipier, inventory)

    produced = reaction["out"] * multipier

    leftovers = produced - qty_needed

    inventory[material] += leftovers

    return ore_needed


with open("input14") as f:
    for reaction_str in f:
        inputs_str, output_str = reaction_str.strip().split(' => ')
        inputs = [(int(input_str.split(' ')[0]), input_str.split(' ')[1]) for input_str in inputs_str.split(', ')]
        output = output_str.split(' ')
        reactions[output[1]] = {
            "in": inputs,
            "out": int(output[0])
        }

    print(reactions)

    # First part
    print(calculate_ore_needed_for("FUEL", 1, defaultdict(int)))

    # Second part
    bottom = 1
    top = 4000000
    while True:
        middle = (top + bottom) // 2
        needed = calculate_ore_needed_for("FUEL", middle, defaultdict(int))

        if needed > 1000000000000:
            top = middle
        else:
            bottom = middle

        if top - bottom == 1:
            break

    print (bottom)
