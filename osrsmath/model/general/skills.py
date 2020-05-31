def get_skills(lower=False):
	''' Returns a list of the skill names in the order listed on the highscores.
		@see https://secure.runescape.com/m=hiscore_oldschool/overall
		@param lower If the skills should be lowercase or titlecase. '''
	skills = [
		"Attack",
		"Defence",
		"Strength",
		"Hitpoints",
		"Ranged",
		"Prayer",
		"Magic",
		"Cooking",
		"Woodcutting",
		"Fletching",
		"Fishing",
		"Firemaking",
		"Crafting",
		"Smithing",
		"Mining",
		"Herblore",
		"Agility",
		"Thieving",
		"Slayer",
		"Farming",
		"Runecraft",
		"Hunter",
		"Construction"
	]
	return [s.lower() for s in skills] if lower else skills

def get_combat_skills(lower=False):
	''' Returns a list of the skills that contribute to combat level in no particular order.
		@param lower If the skills should be lowercase or titlecase. '''
	skills = [
		"Attack",
		"Strength",
		"Defence",
		"Hitpoints",
		"Ranged",
		"Magic",
		"Prayer"
	]
	return [s.lower() for s in skills] if lower else skills
