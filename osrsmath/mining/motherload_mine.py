""" Motherload mine.

Since the probabilities to obtain bonus experience while cleaning paydirt are not known,
they are not considered. Future considerations (perhaps as a subclass of `Miner`) could 
add mining_level and mining_experience attributes to update `Miner.get_experience_after_mining`.
"""

from typing import Tuple

MIN_LEVEL = 30
NUGGET_CHANCE = 2.74 / 100
XP_PER_PAYDIRT = 60
FULL_SET_BOOST = 0.5 / 100
PROSPECTOR = {
	"Helmet": {
		"xp_boost": 0.4 / 100,
		"cost": 40
	},
	"Jacket": {
		"xp_boost": 0.8 / 100,
		"cost": 60
	},
	"Legs": {
		"xp_boost": 0.6 / 100,
		"cost": 50
	},
	"Boots": {
		"xp_boost": 0.2 / 100,
		"cost": 30
	}
}

class Miner:
	""" A miner class, tailored for motherload mine. """
	
	def __init__(self):
		self.current_boost = 1
		""" The current experience boost multipler. """

		self.experience_gained = 0
		""" The amount of experience gained after obtaining all the current prospector gear. """
		
		self.total_ores_mined = 0
		""" The total number of ores mined after obtaining all the current prospector gear. """

		self._kit = []

	def get_experience_after_mining(self, num_ores: int) -> float:
		""" Returns the experience obtained after mining a given number of ores.
		
		Since the bonus experience due to cleaning is not known, it is simply ignored.

		Args:
			num_ores: The number of ores mined in motherload mine.

		Returns:
			The amount of experience obtained on average.
		"""
		return XP_PER_PAYDIRT * num_ores * self.current_boost

	def obtain(self, item: str) -> None:
		""" Updates the miner based on the effect of obtaining a piece of the prospector kit. 

		Args:
			item: One of the keys in the `PROSPECTOR` dictionary. This is the piece obtained.
		"""
		ores_mined = PROSPECTOR[item]['cost'] / NUGGET_CHANCE
		self.total_ores_mined += ores_mined
		self.experience_gained += self.get_experience_after_mining(ores_mined)
		self.current_boost += PROSPECTOR[item]['xp_boost']
		self._kit.append(item)

	def kit(self) -> Tuple[str]:
		""" Returns the current worn prospector equipment. """
		return tuple(self._kit)


def base_xp() -> float:
	""" Returns the xp gained while obtaining the prospector kit without boosts. """
	return sum(v['cost'] / NUGGET_CHANCE * XP_PER_PAYDIRT for v in PROSPECTOR.values())
