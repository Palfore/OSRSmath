""" These are the possible, reputable, sources of max hits and accuracy.
		1. Bitterkoekje: Seems to be 2 years (as of 2020) out of date.
			I think this link only works for me: https://docs.google.com/spreadsheets/d/1llfZAUzUeApmg_m5VNa3YmXeOEw6MVKxpzHWFimWgTs/edit#gid=158500257
		2. That other thing: Gui is much more difficult to automate.
		3. Updated version of Bitterkoekje. https://docs.google.com/spreadsheets/d/1wBXIlvAmqoQpu5u9XBfD4B0PW7D8owyO_CnRDiTHBKQ/edit#gid=158500257

	Calculator needs to have opponent manually set to "Custom NPC"

	pywin32 requires windows, could not find a reasonable alternative.

	The idea here is that we need to create a dataset to test the osrsmath implementation of the combat equations.
	The dependences are:
		Weapon & attack style
		Player stats
		Player equipment bonuses
		Opponent stats
		Opponent equipment bonuses

		Potions
		Prayer
		Special sets
		Special weapons
		For magic, ranged, and melee
	where the latter 3 are more advanced, and will be handled at a later date. Note that for Player equipment bonus, 
	there is no need to handle individual normal equipment since custom amount can be entered.
"""

from time import sleep
import pyperclip
import win32gui
import pyautogui
import re

pyautogui.FAILSAFE = True

class WindowMgr:
    def find_window_wildcard(self, wildcard):
        self._handle = None
        win32gui.EnumWindows(self.window_enum_callback, wildcard)

    def window_enum_callback(self, hwnd, wildcard):
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) != None:
            self._handle = hwnd ##pass back the id of the window

    def set_foreground(self):
        win32gui.SetForegroundWindow(self._handle)

def focus_window(title):
	w = WindowMgr()
	w.find_window_wildcard(title)
	w.set_foreground()

def move(direction, amount):
	[pyautogui.press(direction) for _ in range(amount)]

def move_to(cell):
	pyautogui.hotkey('alt', '/')
	pyautogui.typewrite("go to range\n")
	sleep(0.1)
	pyautogui.typewrite('\n'+cell+'\n') # Not sure why but '\n' is needed before.

def read_text_from(cell):
	move_to(cell)
	return read_text()

def write_text_to(cell, text):
	move_to(cell)
	write_text(text)
	sleep(0.1)

def read_text():
	pyautogui.hotkey('ctrl', 'c')
	sleep(0.2)
	return pyperclip.paste()

def write_text(text):
	pyautogui.write(text)
	pyautogui.press('enter')

def clear():
	pyautogui.press('esc')
	pyautogui.press('backspace')


class Calculator:
	player_stat_order = ['attack', 'strength', 'defence', 'magic', 'ranged', 'hitpoints', 'prayer']
	opponent_stat_order = ['attack', 'strength', 'defence', 'magic', 'ranged', 'hitpoints']
	opponent_bonus_order = ['stab', 'slash', 'crush', 'magic', 'ranged']
	cells = {
		"player_stats": "E8",
		"maxhit": "M9",
		"accuracy": "M11",

		"opponent_stats": "T5",
		"opponent_bonuses": "Z5", # bonuses are at AB5, but multiple letters aren't handled.
		
		"weapon": "E19",
		"spell": "E21",
		"custom_attack": "G32",
		"custom_strength": "H32",
	}

	@staticmethod
	def get_list_of_weapons(download=False):
		if not download:
			# "Dart" is in the excel sheet, but I have no idea what it's supposed to be, so its removed.
			return ["3rd age longsword", "Abyssal bludgeon", "Abyssal dagger", "Abyssal tentacle", "Abyssal whip", "Adamant pickaxe", "Ancient mace", "Arclight", "Armadyl godsword", "Bandos godsword", "Barrelchest anchor", "Black salamander", "Bone dagger", "Brine sabre", "Crystal halberd", "Darklight", "Dharok's greataxe", "Dinh's Bulwark", "Dragon 2h sword", "Dragon battleaxe", "Dragon claws", "Dragon dagger", "Dragon halberd", "Dragon hasta", "Dragon hunter lance", "Dragon longsword", "Dragon mace", "Dragon pickaxe", "Dragon scimitar", "Dragon spear", "Dragon sword", "Dragon warhammer", "Elder maul", "Event rpg", "Fixed device", "Gadderhammer", "Ghrazi rapier", "Granite hammer", "Granite longsword", "Granite maul", "Guthan's warspear", "Hill giant club", "Keris", "Leaf-bladed spear", "Leaf-bladed sword", "Leaf-bladed battleaxe", "Maple blackjack", "Maple blackjack (o)", "Maple blackjack (d)", "Obsidian dagger", "Obsidian mace", "Obsidian maul", "Obsidian sword", "Rune 2h sword", "Rune battleaxe", "Rune claws", "Rune dagger", "Rune halberd", "Rune hasta", "Rune longsword", "Rune mace", "Rune scimitar", "Rune spear", "Rune sword", "Rune pickaxe", "Rune warhammer", "Saradomin's blessed sword", "Saradomin godsword", "Saradomin sword", "Scythe of Vitur (uncharged)", "Scythe of Vitur", "Slayer's staff", "Staff of light", "Enchanted slayer's staff", "Red topaz machete", "Staff of the dead", "Torag's hammers", "Wolfbane", "Verac's flail", "Viggora's chainmace", "Zamorakian spear", "Zamorakian hasta", "Zamorak godsword", "Adamant scimitar", "Mithril scimitar", "Black scimitar", "White scimitar", "Steel scimitar", "Iron scimitar", "Bronze scimitar", "3rd age bow", "Armadyl crossbow", "Black chinchompa", "Chinchompa", "Crystal bow", "Craw's bow", "Dark bow", "Dorgeshuun crossbow", "Dragon crossbow", "Dragon hunter crossbow", "Dragon thrownaxe", "Rune crossbow", "Hunter's crossbow", "Adamant crossbow", "Mithril crossbow", "Steel crossbow", "Iron crossbow", "Bronze crossbow", "Bluerite crossbow", "Rune thrownaxe", "Heavy ballista", "Karil's crossbow", "Knife", "Light ballista", "Magic compositebow", "Magic longbow", "Magic shortbow", "Magic shortbow (i)", "Yew shortbow", "Maple shortbow", "Willow shortbow", "Oak shortbow", "Shortbow", "Red chinchompa", "Seercull", "Toxic blowpipe", "Twisted bow", "Ahrim's staff", "Ancient staff", "God staff", "Iban staff (u)", "Kodai wand", "Master wand", "Thammaron's sceptre", "Sanguinesti staff", "Trident of the seas", "Trident of the swamp", "Toxic staff of the dead", "3rd age wand", "Void knight mace", "Mystic smoke staff", "Smoke battlestaff", "Mystic lava staff", "Mystic mud staff", "Mystic dust staff", "Mystic mist staff", "Mystic steam staff", "Air battlestaff", "Water battlestaff", "Earth battlestaff", "Fire battlestaff"]
		weapons = []
		move_to(Calculator.cells['weapon'])
		text = None
		i = 2
		while text != 'Fire battlestaff':  # Last item in list
			clear()
			pyautogui.press('enter')
			for _ in range(i):
				pyautogui.press('down')
			pyautogui.press('enter')
			pyautogui.press('up')
			text = read_text().strip()
			print(text)
			i += 1
		return weapons

	def set_player_levels(self, stats: dict):
		move_to(self.cells['player_stats'])
		for stat in self.player_stat_order:
			pyautogui.press('esc')
			pyautogui.press('backspace')
			write_text(str(stats[stat])+'\n')

	def set_opponent_levels(self, stats: dict):
		move_to(self.cells["opponent_stats"])
		for stat in self.opponent_stat_order:
			pyautogui.press('esc')
			pyautogui.press('backspace')
			write_text(str(stats[stat])+'\n')

	def set_opponent_bonuses(self, bonuses: dict):
		move_to(self.cells["opponent_bonuses"])
		move('right', 1)
		for stat in self.opponent_bonus_order:
			clear()
			write_text(str(bonuses[stat])+'\n')

	def set_player_weapon(self, weapon, style):
		# Chance weapon and style
		write_text_to(self.cells['weapon'], weapon)
		clear()
		write_text(f'\n*{style}*')
		sleep(0.2)
		pyautogui.press('esc')

		# Error Checking
		move('right', 1)
		move('up', 2)
		sleep(2)
		error = read_text()
		if 'N/A' in error:
			raise ValueError(f"Weapon '{weapon}' could not be evaluated.")
		move('down', 1)
		error = read_text()
		if 'N/A' in error:
			raise ValueError(f"Weapon '{weapon}' could not be evaluated.")

	def set_player_bonuses(self, attack_bonus, strength_bonus):
		move_to(self.cells['custom_attack'])
		write_text(str(attack_bonus))
		move('right', 1)
		move('up', 1)
		write_text(str(strength_bonus))

	def get_summary(self):
		m = int(read_text_from(self.cells['maxhit']))
		move('down', 2)
		a = float(read_text().strip('%'))
		return m, a

from osrsmath.combat.items import ITEM_DATABASE
from pprint import pprint

focus_window("Copy of DPS Calculator - Google Sheets")
calculator = Calculator()
print('(1) Starting')
print('(2) Getting List of Weapons')
weapons = calculator.get_list_of_weapons()
# print('(3) Setting Player Levels')
# calculator.set_player_levels({
# 	'attack': 70,
# 	'strength': 99,
# 	'defence': 99,
# 	'magic': 99,
# 	'ranged': 99,
# 	'hitpoints': 99,
# 	'prayer': 99,
# })
# print('(4) Setting Opponent Levels')
# calculator.set_opponent_levels({
# 	'attack': 70,
# 	'strength': 99,
# 	'defence': 99,
# 	'magic': 99,
# 	'ranged': 99,
# 	'hitpoints': 99,
# })
# print('(5) Setting Player Bonuses')
# calculator.set_player_bonuses(40, 50)
# print('(6) Setting Opponent Bonuses')
# calculator.set_opponent_bonuses({
# 	'stab': 25,
# 	'slash': 50,
# 	'crush': 75,
# 	'magic': 38,
# 	'ranged': 20
# })

print('(7) Evaluating Weapons...')
conversion = {  # Excel capitalizes some words, among other differences
	"Dinh's Bulwark": "Dinh's bulwark",
	"Obsidian dagger": "Toktz-xil-ek",
	"Obsidian mace": "Tzhaar-ket-em",
	"Obsidian maul": "Tzhaar-ket-om",
	"Obsidian sword": "Toktz-xil-ak",
	"Maple blackjack (o)": "Maple blackjack(o)",
	"Maple blackjack (d)": "Maple blackjack(d)",
	"Scythe of Vitur (uncharged)": "Scythe of vitur (uncharged)",
	"Scythe of Vitur": "Scythe of vitur",
}
for name in weapons:
	database_name = conversion.get(name, name)
	
	try:
		attributes = ITEM_DATABASE.find(database_name)
	except Exception as e:
		print('Failed', name, e)
		continue

	for stance in attributes['weapon']['stances'].values():
		try:
			pyautogui.press('esc')
			calculator.set_player_weapon(
				name, stance['attack_style']
			)

			from osrsmath.combat.damage import damage
			from osrsmath.combat.fighter import Fighter
			m = damage(stance, {
					'weapon': attributes, 
					None: ITEM_DATABASE.create_dummy({
						'attack_slash': 40,
						'melee_strength': 50,
						'attack_ranged': 40,
						'ranged_strength': 50,
				})}, Fighter(100, {}, []), {
					'strength': 118, 'ranged': 112,
				}, None
			)

			sleep(1)
			excel_m, excel_a = calculator.get_summary()
			if excel_m != m:
				raise ValueError(f'Disagreement: {excel_m}, {m}')
			print(name, stance['combat_style'], excel_m, m, )
		except pyautogui.FailSafeException:
			pass
		except Exception as e:
			import sys
			exc_type, exc_obj, exc_tb = sys.exc_info()
		    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print('Failed:', name, stance['attack_style'], exc_type, fname, exc_tb.tb_lineno)

print('(7) Finished')