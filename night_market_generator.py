#!/usr/bin/env python3

from random import randrange

# Market categories and their possible stock.
market_types = ['Food and Drugs', 'Personal Electronics', 'Weapons and Armor', 'Cyberware',
		'Clothing and Fashionware', 'Survival Gear']
food_list = ['Canned Goods, 10eb', 'Packaged goods, 10eb', 'Frozen Goods, 10eb', 'Bags of Grain, 20eb',
		 'Kibble Pack, 10eb', 'Bags of Prepak, 20eb', 'Street Drugs of 20eb or less',
		 'Poor Quality Alcohol, 10eb', 'Alcohol, 20eb', 'Excellent Quality Alcohol, 100eb', 'MRE, 10eb',
		 'Live Chicken, 50eb', 'Live Fish, 50eb', 'Fresh Fruits, 50eb', 'Fresh Vegetables, 50eb',
		 'Root Vegetables, 20eb', 'Live Pigs, 100eb', 'Exotic Fruits, 100eb', 'Exotic Vegetables, 100eb',
		 'Street Drugs of exactly 50eb']
electro_list = ['Agent, 100eb', 'Programs or Hardware of 100eb or less', 'Audio Recorder, 100eb',
		'Bug Detector, 500eb', 'Chemical Analyzer, 1000eb', 'Computer, 50eb', 'Cyberdeck, 500eb',
		'Disposable Cell Phone, 50eb', 'Electric Guitar or Other Instrument, 500eb',
		'Programs or Hardware of exactly 500eb', 'Medscanner, 1000eb', 'Homing Tracer, 500eb',
		'Radio Communicator, 100eb', 'Techscanner, 1000eb', 'Smart Glasses, 500eb', 'Radar Detector, 500eb',
		'Scrambler/Descrambler, 500eb', 'Radio Scanner/Music Player, 50eb', 'Braindance Viewer, 1000eb',
		'Virtuality Goggles, 100eb']
weapons_list = ['Medium Pistol', 'Heavy Pistol or Very Heavy Pistol', 'SMG', 'Heavy SMG', 'Shotgun', 'Assault Rifle',
		'Sniper Rifle', 'Bows or Crossbow', 'Grenade Launcher or Rocket Launcher', 'Light Melee Weapon',
		'Medium Melee Weapon', 'Heavy Melee Weapon', 'Very Heavy Melee Weapon', 'A single Exotic Weapon of GM\'s choice',
		'Ammunition of 500eb or less', 'Armor of 100eb or less', 'Armor of exactly 500eb', 'Armor of exactly 1000eb',
		'Weapon Attachments of 100eb or less', 'Weapon Attachments of 500eb or higher']
cyberware_list = ['Cybereye, 100eb', 'Cyberaudio Suite, 500eb', 'Neural Link, 500eb', 'Cyberarm, 500eb', 'Cyberleg, 100eb',
		  'External Cyberware of exactly 1000eb', 'External Cyberware of 500eb or less',
		  'Internal Cyberware of exactly 1000eb', 'Internal Cyberware of 500eb or less',
		  'Cybereye Option of exactly 1000eb', 'Cybereye Option of 500eb or less',
		  'Cyberaudio Option of exactly 1000eb', 'Cyberaudio Option of 500eb or less',
		  'Neuralware Option of exactly 1000eb', 'Neuralware Option of 500eb or less',
		  'Cyberlimb Option of exactly 1000eb', 'Cyberlimb Option of 500eb or less', 'Fashionware of GM\'s Choice',
		  'Borgware of GM\'s Choice', 'Any Cyberware of GM\'s Choice']
clothes_list = ['Bag Lady Chic', 'Gang Colors', 'Generic Chic', 'Bohemian', 'Leisurewear', 'Nomad Leather', 'Asia Pop',
		'Urban Flash', 'Businesswear', 'High Fashion', 'Biomonitor, 100eb', 'Chemskin, 100eb', 'EMP Threading, 10eb',
		'Light Tatoo, 100eb', 'Shift Tacts, 100eb', 'Skinwatch, 100eb', 'Techhair, 100eb', 'Generic Chic',
		'Leisurewear', 'Gang Colors']
survival_list = ['Anti-Smog Breathing Mask, 20eb', 'Auto-Level Dampening Ear Protectors, 1000eb', 'Binoculars, 50eb',
		 'Carryall, 20eb', 'Flashlight, 20eb', 'Duct Tape, 20eb', 'Inflatable Bed & Sleep-bag, 20eb',
		 'Lock-Picking Set, 20eb', 'Handcuffs, 50eb', 'Medtech Bag, 100eb', 'Tent and Camping Equipment, 50eb',
		 'Rope (60m), 20eb', 'Techtool, 100eb', 'Personal CarePack, 20eb', 'Radiation Suit, 1000eb',
		 'Road Flare, 10eb', 'Grapple Gun, 100eb', 'Tech Bag, 500eb', 'Shovel or Axe, 50eb', 'Airhypo, 50eb']
market_types_lists = [food_list, electro_list, weapons_list, cyberware_list, clothes_list, survival_list]
quality_list = ['Poor', 'Average', 'Excellent']

gun_dict = {
	'Medium Pistol': 50,
	'Heavy Pistol or Very Heavy Pistol' : 100,
	'SMG': 100,
	'Heavy SMG': 100,
	'Shotgun': 500,
	'Assault Rifle': 500,
	'Sniper Rifle': 500,
	'Bows or Crossbow': 100,
	'Grenade Launcher or Rocket Launcher': 500,
	'Light Melee Weapon': 50,
	'Medium Melee Weapon': 50,
	'Heavy Melee Weapon': 100,
	'Very Heavy Melee Weapon': 100,
	'A single Exotic Weapon of GM\'s choice' : 0,
	'Armor of 100eb or less': 100,
	'Armor of exactly 500eb': 500,
	'Armor of exactly 1000eb': 1000,
	'Ammunition of 500eb or less' : 500,
	'Weapon Attachments of 100eb or less': 100,
	'Weapon Attachments of 500eb or higher': 500}

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
			self.quality = 0  # Poor
		elif roll > 7:
			self.quality = 2  # Excellent
		else:
			self.quality = 1  # Average
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
	if (roll > 13):
		gun.update_gun(weapons_list[roll], gun_dict[weapons_list[roll]], 1)
	else:
		gun.update_gun(weapons_list[roll], gun_dict[weapons_list[roll]], 0)
	return (gun)

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
	first_category = randrange(6)
	second_category = randrange(6)
	while second_category == first_category:
		second_category = randrange(6)
	category_indexes = [first_category, second_category]

	item_counts = [randrange(10) + 1, randrange(10) + 1]
	selected_items = [fill_list(count, 20) for count in item_counts]
	contains_weapons = check_guns(category_indexes)

	output = 'Welcome, choomba!\nThis Night Market is selling:\n'
	for category_index in category_indexes:
		output += f'**{market_types[category_index]}**\n'
	output += (
		f"\nThere's {item_counts[0]} items of the first category, "
		f"and {item_counts[1]} items of the second.\n"
		'\nOn the stand, you can find:\n\n'
	)

	for category_index, item_indexes in zip(category_indexes, selected_items):
		output += format_category_items(category_index, item_indexes)

	if contains_weapons:
		output += (
			"\n\nA little reminder for you, choom: a Poor Quality weapon jam on a roll of one, "
			"and an Excellent Quality weapon gives you +1 on all attack checks.\n"
		)
	return output
