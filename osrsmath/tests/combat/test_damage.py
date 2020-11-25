from osrsmath.combat.fighter import NoAmmoPolicyFoundError, can_attack
from osrsmath.combat.items import ITEM_DATABASE
import unittest

class RequirementsTest(unittest.TestCase):
	def test_no_ranged_weapons_fail_while_determining_attackability(self):
		try:
			for weapon_id in ITEM_DATABASE.get_slot('weapon') + ITEM_DATABASE.get_slot('2h'):
				weapon = ITEM_DATABASE.get(weapon_id)
				for ammo_id in ITEM_DATABASE.get_slot('ammo'):
					ammo = ITEM_DATABASE.get(ammo_id)

					for stance in weapon['weapon']['stances'].values():
						a = can_attack(stance, {'weapon': weapon,'ammo': ammo})
		except NoAmmoPolicyFoundError as e:
			self.fail(f"{e} {weapon['name']}, {ammo['name']}")
