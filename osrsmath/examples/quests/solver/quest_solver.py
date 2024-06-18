""" There are two important inverse problems to solve.
	1. Get to a skill level through the least amount of training possible.
	> [quests, training, quests, training, ...]

	2. Complete a set of quests through the least amount of training possible.

	Both of these are subsets of a common problem:
	Get a player P to (at least) state G in the least amount of training possible.
	Since both of these are vectors, the problem is P_i+1 = T_iP_i | min sum_i_training T_i.
"""
from osrsmath.examples.quests.model.quest import Player, Skills
import numpy as np
import textwrap

def get_questcape():
	""" Implements an algorithm that tries to finish the quest cape.
		I ignore the time it takes to complete a quest, since they all need to be finished.
		This neglects the fact that some quests may be faster with higher stats (particularly combat).
		Then, I would need a grid of skill training times.
		For now, I assume that all skills are trained at the same rate.

		For the algorithm, I want to train my skills to complete the nearest quest.
		This isn't correct, since it may be better to strive for a quest with a large payout.
		But this is a first attempt.
		
		Algorithm:
			Start with a blank player
			The player can perform two actions: complete_possible or train_to_nearest.
			Every iteration, complete_possible then train_to_nearest until all quests are completed.
			The sum of experience is the cost of the algorithm, multiplying by an average xp rate could yield a time cost. 
	"""

	def find_nearest_quest(player) -> tuple[str, list[float], float]:
		def prerequisites_are_satisfied(player, quest):  # Should move to quest/player class.
			# Q00100101 (The encoding for the quest requirements)
			# P11001001 (The encoding for the player's completed quests)
			# R11011011 (Whether the requirement is met)

			# If a == 0 -> 1
			# Else if a == b -> 1
			# Else 0

			# Truth Table
			# QPR
			# 001
			# 011
			# 100
			# 111
			# This is "logical implication": https://sites.millersville.edu/bikenaga/math-proof/truth-tables/truth-tables.html
			# Which is the same as "not(a) or b": https://stackoverflow.com/questions/16405892/is-there-an-implication-logical-operator-in-python
			p_encoding = player.quest_book.as_one_hot()
			q_encoding = quest.get_quest_requirement_as_encoding()
			return all(not(q) or p for q, p in zip(q_encoding, p_encoding))

		nearest_xp = np.inf
		nearest = None
		valid_quests = [quest for quest in player.quest_book.get_completed(False) if prerequisites_are_satisfied(player, quest)]
		for quest in valid_quests:
			distance = np.linalg.norm(
				np.array(player.skills.as_xp_vector()) -
				np.array(quest.get_skill_requirement_as_skills().as_xp_vector())
			)
			if distance < nearest_xp:  # Could be <=
				nearest_xp = distance
				nearest = quest

		xp_required = np.maximum(  # Training to the skill requirements
			np.array(nearest.get_skill_requirement_as_skills().as_xp_vector()) - np.array(player.skills.as_xp_vector()), 0
		)
		cost = sum(xp_required)
		return nearest.name, xp_required, cost

	# Get a quest cape by only training when you need to and by using the nearest quest as the training target.
	player = Player.create_new_player()
	cost = 0
	iteration = 0
	while not player.quest_book.is_complete():
		player.complete_possible()
		
		nearest, xp_required, penalty = find_nearest_quest(player)
		player.skills += Skills(xp_required)
		player.complete_if_possible(nearest)
		cost += penalty

		# print("Completed Quests")
		print(iteration, len(player.quest_book.get_completed(True)), f"{penalty:,}", f"{cost:,}", nearest)
		# print(textwrap.fill(str(player.skills.as_dict()), initial_indent='\t', subsequent_indent='\t', width=130))

		iteration += 1


if __name__ == '__main__':
	player = Player.create_new_player()
	# remaining_count = player.quest_book.get_completed(False)
	# while not player.quest_book.is_complete():
	# print("Completing", len(player.quest_book.get_completed(True)))
	# player.complete_possible()
	# print("Completing", len(player.quest_book.get_completed(True)))
	# player.complete_possible()
	# print(player.skills)
	# for q in player.quest_book.get_completed(False):
	# 	print(q)

		
		# if player.quest_book.get_completed(False) == remaining_count:
		# 	break


		


	get_questcape()