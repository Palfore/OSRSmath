def get_spell(spell_name: str):
	spell_name = spell_name.lower().strip()
	print(spell_name)
	try:
		return {**STANDARD, **ANCIENT}[spell_name]
	except KeyError as e:
		print(f"The spell '{spell_name}' could not be found.", e)

STANDARD = {
	'wind strike': {'level': 1, 'xp': '5.5', 'max_hit': 2},
	'water strike': {'level': 5, 'xp': '7.5', 'max_hit': 4},
	'earth strike': {'level': 9, 'xp': '9.5', 'max_hit': 6},
	'fire strike': {'level': 13, 'xp': '11.5', 'max_hit': 8},
	'wind bolt': {'level': 17, 'xp': '13.5', 'max_hit': 9},
	'water bolt': {'level': 23, 'xp': '16.5', 'max_hit': 10},
	'earth bolt': {'level': 29, 'xp': '19.5', 'max_hit': 11},
	'fire bolt': {'level': 35, 'xp': '22.5', 'max_hit': 12},
	'crumble undead': {'level': 39, 'xp': '24.5', 'max_hit': 15},
	'wind blast': {'level': 41, 'xp': '25.5', 'max_hit': 13},
	'water blast': {'level': 47, 'xp': '28.5', 'max_hit': 14},
	'iban blast': {'level': 50, 'xp': '30', 'max_hit': 25},
	'magic dart': {'level': 50, 'xp': '30', 'max_hit': 15},
	'earth blast': {'level': 53, 'xp': '31.5', 'max_hit': 15},
	'fire blast': {'level': 59, 'xp': '34.5', 'max_hit': 16},
	'saradomin strike': {'level': 60, 'xp': '61', 'max_hit': 20},
	'claws of guthix': {'level': 60, 'xp': '61', 'max_hit': 20},
	'flames of zamorak': {'level': 60, 'xp': '61', 'max_hit': 20},
	'wind wave': {'level': 62, 'xp': '36', 'max_hit': 17},
	'water wave': {'level': 65, 'xp': '37.5', 'max_hit': 18},
	'earth wave': {'level': 70, 'xp': '40', 'max_hit': 19},
	'fire wave': {'level': 75, 'xp': '42.5', 'max_hit': 20},
	'wind surge': {'level': 81, 'xp': '44.5', 'max_hit': 21},
	'water surge': {'level': 85, 'xp': '46.5', 'max_hit': 22},
	'earth surge': {'level': 90, 'xp': '48.5', 'max_hit': 23},
	'fire surge': {'level': 95, 'xp': '50.5', 'max_hit': 24},
}

ANCIENT = {
	'smoke rush': {'level': 50, 'xp': '30', 'max_hit': 13},
	'shadow rush': {'level': 52, 'xp': '31', 'max_hit': 14},
	'blood rush': {'level': 56, 'xp': '33', 'max_hit': 15},
	'ice rush': {'level': 58, 'xp': '34', 'max_hit': 16},
	'smoke burst': {'level': 62, 'xp': '36', 'max_hit': 17},
	'shadow burst': {'level': 64, 'xp': '37', 'max_hit': 18},
	'blood burst': {'level': 68, 'xp': '39', 'max_hit': 21},
	'ice burst': {'level': 70, 'xp': '40', 'max_hit': 22},
	'smoke blitz': {'level': 74, 'xp': '42', 'max_hit': 23},
	'shadow blitz': {'level': 76, 'xp': '43', 'max_hit': 24},
	'blood blitz': {'level': 80, 'xp': '45', 'max_hit': 25},
	'ice blitz': {'level': 82, 'xp': '46', 'max_hit': 26},
	'smoke barrage': {'level': 86, 'xp': '48', 'max_hit': 27},
	'shadow barrage': {'level': 88, 'xp': '49', 'max_hit': 28},
	'blood barrage': {'level': 92, 'xp': '51', 'max_hit': 29},
	'ice barrage': {'level': 94, 'xp': '52', 'max_hit': 30},
}


if __name__ == '__main__':
	book = 'ancient'

	from bs4 import BeautifulSoup # pip install beautifulsoup4
	from pprint import pprint
	import os
	if not os.path.exists('save.dat'):
		with open('save.dat', 'w') as f:
			import requests
			r = requests.get({
				'standard': "https://oldschool.runescape.wiki/w/Standard_spells",
				'ancient': "https://oldschool.runescape.wiki/w/Ancient_Magicks"
			}[book])
			if r.status_code != 200:
				raise ValueError("Unable to retrieve spell data.")
			text = r.text
			f.write(text)

	with open('save.dat', 'r') as f:
		text = f.read()

	soup = BeautifulSoup(text, 'html.parser')
	spellbook = {}
	for i, x in enumerate(soup.find_all('table')):
		if book == 'ancient' and i == 0:
			continue
		for y in x.find_all('tr'):
			for i, z in enumerate(y.find_all('td')):  # list(find_all('td'))[0] fails ??
				z = z.text.strip()
				if i == 2:
					name = z
					spellbook[name] = {}
				if i == 3:
					spellbook[name]['level'] = int(z)
				if (i == 5 and book == 'standard') or (i == 6 and book == 'ancient'):
					spellbook[name]['xp'] = z.replace('+', '')
				if (i == 6 and book == 'standard') or (i == 7 and book == 'ancient'):
					try:
						spellbook[name]['max_hit'] = int(z)
					except:
						del spellbook[name]
		break
	for x, y in sorted(spellbook.items(), key=lambda x: x[1]['level']):
		print(f"'{x.lower()}': {y},")