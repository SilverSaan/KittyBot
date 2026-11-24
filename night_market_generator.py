#!/usr/bin/env python3

import json
from pathlib import Path
from random import randrange

with (Path(__file__).parent / "jsons" / "night_market.json").open(encoding="utf-8") as data_file:
    market_data = json.load(data_file)

market_types = [category["name"] for category in market_data["categories"]]
market_types_lists = [category["items"] for category in market_data["categories"]]
food_list, electro_list, weapons_list, cyberware_list, clothes_list, survival_list = market_types_lists
gun_dict = market_data["weapon_prices"]
quality_list = ['Poor', 'Average', 'Excellent']

QUALITY_MULTIPLIERS = {
    0: {50: 20, 100: 50, 500: 100},      # Poor
    1: {50: 50, 100: 100, 500: 500},     # Average (same)
    2: {50: 100, 100: 500, 500: 1000}    # Excellent
}

class Weapon:
    """A generated weapon and the market quality that determines its price."""

    def __init__(self):
        self.type = ''
        self.price = 0
        roll = randrange(10)
        if roll < 4:
            self.quality = 0
        elif roll > 7:
            self.quality = 2
        else:
            self.quality = 1
        self.quality_trig = 1

    def update_gun(self, gun_type, price, trigger_quality):
        self.type = gun_type
        if trigger_quality:
            self.quality_trig = 0
            return

        self.price = QUALITY_MULTIPLIERS.get(self.quality, {}).get(price, price)


def fill_list(number_of_items, number_of_options):
    """Select unique option indexes using the original repeated-roll method."""
    selected = set()
    while len(selected) < number_of_items:
        selected.add(randrange(number_of_options))
    return list(selected)


def gun_generator(roll):
    gun = Weapon()
    gun_type = weapons_list[roll]
    gun.update_gun(gun_type, gun_dict[gun_type], int(roll > 13))
    return gun


def gun_reader(gun_list):
    lines = []
    for gun in gun_list:
        line = f'- {gun.type}'
        if gun.quality_trig:
            line += f'({quality_list[gun.quality]} Quality), sold at '
            line += f'{int(gun.price)}eb\n' if gun.price else 'the appropriate price\n'
        else:
            line += ' \n'
        lines.append(line)
    return ''.join(lines)


def check_guns(mtvar):
    return int(2 in mtvar)


def gen_gun_list(gun_numbers):
    return gun_reader([gun_generator(number) for number in gun_numbers])


def format_category_items(category_index, item_indexes):
    """Format selected stock, applying weapon quality rules when applicable."""
    if category_index == 2:
        return gen_gun_list(item_indexes)
    return ''.join(
        f'- {market_types_lists[category_index][item_index]}\n'
        for item_index in item_indexes
    )


def main():
    """Generate and format a market with two distinct categories."""
    first_category = randrange(len(market_types))
    second_category = randrange(len(market_types))
    while second_category == first_category:
        second_category = randrange(len(market_types))
    category_indexes = [first_category, second_category]

    item_counts = [randrange(10) + 1 for _ in category_indexes]
    selected_items = [fill_list(count, 20) for count in item_counts]
    contains_weapons = check_guns(category_indexes)

    output = 'Welcome, choomba!\nThis Night Market is selling:\n'
    output += ''.join(f'**{market_types[index]}**\n' for index in category_indexes)
    output += (
        f"\nThere's {item_counts[0]} items of the first category, "
        f"and {item_counts[1]} items of the second.\n"
        '\nOn the stand, you can find:\n\n'
    )
    output += ''.join(
        format_category_items(category_index, item_indexes)
        for category_index, item_indexes in zip(category_indexes, selected_items)
    )

    if contains_weapons:
        output += (
            "\n\nA little reminder for you, choom: a Poor Quality weapon jam on a roll of one, "
            "and an Excellent Quality weapon gives you +1 on all attack checks.\n"
        )
    return output
