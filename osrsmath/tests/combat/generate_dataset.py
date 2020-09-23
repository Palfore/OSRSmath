""" These are the possible, reputable, sources of max hits and accuracy.
		Bitterkoekje: Seems to be 2 years (as of 2020) out of date.
		That other thing: Gui is much more difficult to automate.

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
		
		"weapon": "E17",
		"spell": "E19",
		"custom_attack": "G30",
		"custom_strength": "H30",

	}

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

	def set_player_bonuses(self, weapon, style, attack_bonus, strength_bonus):
		write_text_to(cells['weapon'], weapon)
		clear()
		write_text('\n*'+style+'*')
		move('right', 1)
		move('up', 2)
		sleep(0.3)
		error = read_text()
		if 'N/A' in error:
			raise
		move('down', 1)
		error = read_text()
		if 'N/A' in error:
			raise

		move_to(cells['custom_attack'])
		write_text(str(attack_bonus))
		move('right', 1)
		move('up', 1)
		write_text(str(strength_bonus))
		

	def get_summary(self):
		m = int(read_text_from(cells['maxhit']))
		move('down', 2)
		a = float(read_text().strip('%'))
		return m, a


# 1. get list of weapons and associated attack styles
# 2. generate a random player, and opponent.
# 3. select a random sample of weapons and evaluate them,
# 4. goto 2, until satisfied.
focus_window("Copy of DPS calculator by Bitterkoekje")
calculator = Calculator()
# calculator.set_player_levels({
# 	'attack': 70,
# 	'strength': 99,
# 	'defence': 99,
# 	'magic': 99,
# 	'ranged': 99,
# 	'hitpoints': 99,
# 	'prayer': 99,
# })
# calculator.set_opponent_levels({
# 	'attack': 70,
# 	'strength': 99,
# 	'defence': 99,
# 	'magic': 99,
# 	'ranged': 99,
# 	'hitpoints': 99,
# })
# calculator.set_opponent_bonuses({
# 	'stab': 25,
# 	'slash': 50,
# 	'crush': 75,
# 	'magic': 38,
# 	'ranged': 20
# })
# calculator.set_player_bonuses(
# 	'Dragon Sword',
# 	'aggressive',
# 	40, 50
# )
print(calculator.get_summary())
