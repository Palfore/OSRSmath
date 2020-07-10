from osrsmath.apps.path.path import *
from osrsmath.apps.path.printers import *
from osrsmath.combat.player import get_equipment_data
from osrsmath.combat.boosts import BoostingSchemes, Potions
from pprint import pprint
import copy

if __name__ == '__main__':
	def choose_equipment(attack, strength, defence):
		base = [
			# "Dharok's helm",
			# "Dharok's platebody",
			# "Dharok's platelegs",
			"Dragon Boots",
			# "Holy Blessing",
			"Barrows Gloves",
			# "Dragon Defender",
			"Berserker Ring (i)",
			"Amulet of Fury",
			"Fire Cape",
		]
		if (attack + strength >= 130) or (attack == 99) or (strength == 99):  # Warriors Guild
			if   defence >= 70 and attack >= 70: base.append("Avernic Defender");
			elif defence >= 60: base.append("Dragon Defender");
			elif defence >= 40 and attack >= 40: base.append("Rune Defender");
			elif defence >= 30 and attack >= 30: base.append("Adamant Defender");
			elif defence >= 20 and attack >= 20: base.append("Mithril Defender");
			elif defence >= 10 and attack >= 10: base.append("Black Defender");
			elif defence >=  5 and attack >=  5: base.append("Steel Defender");
			elif defence >=  0 and attack >=  0: base.append("Iron Defender");

		if   attack >= 75: base.append("Ghrazi Rapier");
		elif attack >= 70: base.append("Abyssal Dagger");
		elif attack >= 60: base.append("Dragon Scimitar");
		elif attack >= 50: base.append("Granite Hammer");
		elif attack >= 40: base.append("Brine Sabre");
		elif attack >= 30: base.append("Adamant Scimitar");
		elif attack >= 20: base.append("Mithril Scimitar");
		elif attack >= 10: base.append("Black Scimitar");
		elif attack >=  5: base.append("Steel Scimitar");
		elif attack >=  0: base.append("Iron Scimitar");
		return base

	def compare_paths(file_path, start, end, color_equipment_boost_zip):
		""" color_equipment_boost_zip: list with element e => ('red', equipment, lambda p: BoostingSchemes(p).overload()) """
		tree = Tree(start, end, print_progress=False)
		printer = TreePrinter(tree.start, tree.end)
		printer.add_grid(draw_dots=False)
		costs = {}
		for color, equipment, boost_function in color_equipment_boost_zip:
			print(color)
			path = get_solution(tree, boost_function, defenders_, equipment_data_, equipment)
			printer.add_path(path, color)
			costs[color] = path.total_cost
			pprint(path)
		printer.print(file_path, clean=False, animate=True)
		print(costs)

	equipment_data_ = get_equipment_data()
	defenders_ = get_opponents()['hard']
	equipment = choose_equipment(60, 60, 60)



	### Optimal Equipment
	from timeit import default_timer
	from osrsmath.combat.boosts import Prayers, Potions
	start = default_timer()
	tree = Tree((90, 90, 99), (99, 99, 99), print_progress=False)
	path = get_solution(tree, lambda p: BoostingSchemes(p, Prayers.none).constant(Potions.overload, ('damage', 'accuracy')), defenders_, equipment_data_, equipment=None)
	printer = TreePrinter(tree.start, tree.end)
	printer.add_grid()
	printer.add_path(path, 'red')
	pprint(list(zip(path.nodes, path.edges)), width=140)
	end = default_timer()
	current_equipment = {}
	for n, (t, d) in zip(path.nodes, path.edges):
		a = set(d['equipment'].items())
		b = set(current_equipment.items())
		diff = a - b
		if diff:
			print(n, diff)
		current_equipment = d['equipment']
	printer.print()

	print("total_cost:", path.total_cost, "calculated in:", end - start)
	import sys
	sys.stdout.write('\a')
	sys.stdout.flush()

	exit()

	start, end = (90, 90, 99), (99, 99, 99)
	### Timming first solution
	# from timeit import default_timer
	# for s in range(99, 1, -1):
	# 	tree = Tree((s, s, s), (99, 99, 99), print_progress=False)
	# 	start = default_timer()
	# 	path = get_solution(tree, lambda p: BoostingSchemes(p).overload(), defenders_, equipment_data_, equipment)
	# 	end = default_timer()
	# 	print(s, end-start)
	# exit()
	# printer = TreePrinter(tree.start, tree.end)
	# printer.add_grid(draw_dots=False, add_text=True)

	# solver = Solver(tree, lambda p, c: Tree.assign_edge(p, c, lambda p: BoostingSchemes(p).overload(), defenders_, equipment_data_, equipment))
	# # solver.__next__()
	# # printer.add_path(solver.get())

	# for solution in solver:
	# 	pass
	# printer.add_path(solution)
	# printer.print("tree1", clean=True, animate=True)
	# exit()

	### Comparison of different boosting schemes
	# compare_paths('tree1', (90, 90, 60), (99, 99, 60), [
	# 	('green', equipment, lambda p: BoostingSchemes(p).none()),
	# 	# ('blue', equipment, lambda p: BoostingSchemes(p).potion_when_skill_under(Potions.super, 'attack', 5)),
	# 	('red', equipment, lambda p: BoostingSchemes(p).overload()),
	# 	('green', equipment, lambda p: BoostingSchemes(p).none()),
	# 	# ('blue', equipment, lambda p: BoostingSchemes(p).potion_when_skill_under(Potions.super, 'attack', 5)),
	# 	('red', equipment, lambda p: BoostingSchemes(p).overload()),
	# 	('green', equipment, lambda p: BoostingSchemes(p).none()),
	# 	# ('blue', equipment, lambda p: BoostingSchemes(p).potion_when_skill_under(Potions.super, 'attack', 5)),
	# 	('red', equipment, lambda p: BoostingSchemes(p).overload()),
	# ])
	# exit()

	### Comparison of different weapons
	# equipment_no_weap = copy.copy(equipment)
	# equipment_no_weap.remove("Dragon Scimitar")
	# equipment2 = ["Bronze Dagger"] + equipment_no_weap
	# equipment3 = ["Ghrazi Rapier"] + equipment_no_weap
	# compare_paths('tree.tex', (60, 70, 60), (99, 99, 60), [
	# 	('green', equipment2, lambda p: BoostingSchemes(p).overload()),
	# 	('red', equipment, lambda p: BoostingSchemes(p).overload()),
	# 	('blue', equipment3, lambda p: BoostingSchemes(p).overload()),
	# ])
	# exit()

	### xp rate vs xp required
	# def cost_function(parent, child):
	# 		global equipment
	# 		_, _, (cost, details) = Tree.assign_edge(equipment,
	# 			parent, child, lambda p: BoostingSchemes(p).none(), defenders_, equipment_data_
	# 		)
	# 		degree = (details['xp_rate']/10000 - 4) / (7.5 - 4)  # Heuristic normalization
	# 		return cost, f"green!{degree*100}!red"
	# tree = Tree((60, 60, 60), (99, 99, 60), print_progress=False)
	# printer = TreePrinter(tree.start, tree.end)
	# printer.add_grid(draw_dots=False, cost_function=cost_function)
	# path = get_solution(tree, equipment, lambda p: BoostingSchemes(p).none(), defenders_, equipment_data_)
	# printer.add_path(path, 'red')
	# printer.print()
	# exit()

	### Comparison of many different starting places
	# s, ds = 1, 1
	# ea, es = 99, 99
	# printer = TreePrinter((s, s, 60), (ea, es, 60))
	# printer.add_grid(draw_dots=False)
	# for l in range(s, ea, ds):
	# 	for r in range(s, es, ds):
	# 		print(l, r)
	# 		tree = Tree((l, r, 60), (ea, es, 60), print_progress=False)
	# 		path = get_solution(tree, lambda p: BoostingSchemes(p).none(), defenders_, equipment_data_, equipment)
	# 		printer.add_path(path, 'black')
	# tree = Tree((s, s, 60), (ea, es, 60), print_progress=False)
	# path = get_solution(tree, lambda p: BoostingSchemes(p).none(), defenders_, equipment_data_, equipment)
	# printer.add_path(path, 'red')
	# printer.print()
	# exit()


	### Single Path Solution
	# tree = Tree((60, 60, 60), (99, 99, 60), print_progress=False)
	# path = get_solution(tree, lambda p: BoostingSchemes(p).overload(), defenders_, equipment_data_, equipment)
	# printer = TreePrinter(tree.start, tree.end)
	# printer.add_grid()
	# printer.add_path(path, 'red')
	# pprint(list(zip(path.nodes, path.edges)), width=120)
	# printer.print()
	# exit()

	### Equipment Switching Path Solution
	# tree = Tree((30, 30, 60), (99, 99, 60), print_progress=False)
	# printer = TreePrinter(tree.start, tree.end)
	# printer.add_grid()
	# path = get_solution(tree, lambda p: BoostingSchemes(p).overload(), defenders_, equipment_data_, choose_equipment(60, 60, 60))
	# printer.add_path(path, 'blue')
	# path = get_solution(tree, lambda p: BoostingSchemes(p).overload(), defenders_, equipment_data_, choose_equipment)
	# printer.add_path(path, 'red')
	# path = get_solution(Tree((60, 60, 60), (99, 99, 60)), lambda p: BoostingSchemes(p).overload(), defenders_, equipment_data_, choose_equipment(60, 60, 60))
	# printer.add_path(path, 'green')
	# for node, (t, details) in zip(path.nodes, path.edges):
	# 	print(node, t, details['stance'], details['xp_rate'], details['equipment'][-1])
	# printer.print()
	# exit()


	### Printing Training Scheme
	tree = Tree((90, 90, 90), (99, 99, 99), print_progress=True)
	path1 = get_solution(tree, lambda p: BoostingSchemes(p).overload(), defenders_, equipment_data_, equipment, start=(90, 90, 99), end=(99, 99, 99))
	path2 = get_solution(tree, lambda p: BoostingSchemes(p).overload(), defenders_, equipment_data_, equipment, start=(90, 99, 99), end=(99, 99, 99))

	# path4 = get_solution(tree, lambda p: BoostingSchemes(p).overload(), defenders_, equipment_data_, choose_equipment)
	# path2 = get_solution(Tree(tree.start, tree.end, print_progress=True),
	# 	lambda p: BoostingSchemes(p).potion_when_skill_under(Potions.super, 'attack', 5), defenders_, equipment_data_, equipment,
	# )
	printer = SchemePrinter()
	printer.add_path("Fixed-Overload", path1)
	printer.add_path("Fixed-Overload", path2)
	# printer.add_path("Fixed-Overload", path3)
	# printer.add_path("Fixed-Overload", path4)
	# printer.add_path("Upgrades-Overload", path2)
	printer.print()

	# from Helpers.graph import Graph
	# Graph("Results/time_to_level/time.agr", "test", [
	# 	(None, [
	# 		(None, 'xy', zip(list(range(len(time_for_next_level_data))), time_for_next_level_data))
	# 	])
	# ])

