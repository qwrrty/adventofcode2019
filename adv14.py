#! /usr/bin/env python3

import math

# A reaction is expressed as:
#   - Reaction.chemical (the output chemical)
#   - Reaction.quantity (the output quantity)
#   - Reaction.ingredients (a hash of chemicals and quantities
#     that go into this reaction)

class Reaction(object):
    def __init__(self, chemical, quantity, ingredients):
        self.chemical = chemical
        self.quantity = quantity
        self.ingredients = ingredients

    def __repr__(self):
        return "<Reaction {} quantity={} ingredients={}>".format(
            self.chemical, self.quantity, self.ingredients)


class ReactionChart(object):

    def __init__(self, text):
        chart = {}
        for line in text.split("\n"):
            if not line:
                continue
            requirement, result = line.split(" => ")
            chemical, amt = ReactionChart.parse_reactant(result)
            ingredients = {}
            for s in requirement.split(", "):
                c, q = ReactionChart.parse_reactant(s)
                ingredients[c] = q
            chart[chemical] = Reaction(chemical, amt, ingredients)
        self.chart = chart

    def from_file(filename="adv14_input.txt"):
        with open(filename, "r") as f:
            return ReactionChart(f.read())

    def parse_reactant(s):
        amt, chem = s.split(" ")
        return chem, int(amt)
    

def calculate_requirements(chart,
                           target_chemical="FUEL",
                           target_quantity=1):
    orders = []
    orders.append((target_chemical, target_quantity))

    supply = {}        # Leftover chemicals from previous reactions
    ore = 0
    
    while orders:
        chem, quantity = orders.pop(0)
        if chem == "ORE":
            ore += quantity
            continue
        
        reaction = chart.chart[chem]

        # If we have any of this chem on hand, reduce it appropriately
        if chem in supply:
            supply_amt = supply[chem]
            if supply_amt >= quantity:
                # We have enough on hand to satisfy this order
                supply[chem] -= quantity
                if supply_amt == quantity:
                    del supply[chem]
                continue
            elif supply_amt < quantity:
                quantity -= supply_amt
                del supply[chem]

        # How many times must this reaction be run to obtain the necessary quantity?
        multiple = math.ceil(quantity / reaction.quantity)
        # How much chemical will be left over after it runs?
        leftover = (reaction.quantity * multiple) - quantity
        # Place orders for the new ingredients, adjusting supply on hand as necessary
        for ingredient_chem, ingredient_amt in reaction.ingredients.items():
            orders.append((ingredient_chem, ingredient_amt * multiple))

        # Record any excess of this chemical after this order is fulfilled
        if leftover:
            supply[chem] = leftover

    return ore
    

def part1():
    chart = ReactionChart.from_file()
    print(calculate_requirements(chart))

def part2():
    chart = ReactionChart.from_file()
    print(calculate_requirements(chart, target_quantity=2521844))
