# from jsoncomment import JsonComment
# from osrsmath.apps.optimize import get_sets, get_best_set
# from osrsmath.combat.experience import combat_level
# from osrsmath.combat.monsters import Monster
# from osrsmath.combat.player import PlayerBuilder, get_equipment_data
# from osrsmath.combat.experience import get_time_to_level, time_dependent_model_xp
# from osrsmath.combat.boosts import BoostingSchemes, Potions
# from osrsmath.combat import successful_hits
# from dijkstar import Graph, find_path
# from multiprocessing import Pool
# from pprint import pprint
# import numpy as np
# import copy
# import os

# ## Multi-processing boiler plate
# _func = None
# def worker_init(func):
#   global _func
#   _func = func
# def worker(x):
#   return _func(x)
# def xmap(func, iterable, processes=None):
#   with Pool(processes, initializer=worker_init, initargs=(func,)) as p:
#     return p.map(worker, iterable)

# def get_opponents():
# 	king_roald_hard = Monster({'attack': 140, 'strength': 120, 'defence': 30, 'prayer': 1, 'hitpoints': 150, 'magic': 1, 'ranged': 1})
# 	king_roald_hard.attack_style = 'crush'
# 	defenders = {
# 		'easy': {
# 			'Count Draynor': Monster.from_id(6393),
# 			'King Roald': Monster.from_id(6389),
# 			'Me': Monster.from_id(6381),
# 			'Tree Spirit': Monster.from_id(6380),
# 			'Khazard Warlord': 	Monster.from_id(6390),
# 		}, 'hard': {
# 			'Count Draynor': Monster.from_id(6332),
# 			'King Roald': king_roald_hard,
# 			'Me': Monster.from_id(6320),
# 			'Tree Spirit': Monster.from_id(6319),
# 			'Khazard Warlord': Monster.from_id(6329),
# 		}
# 	}
# 	return defenders


# from collections import defaultdict
# class Tree:
# 	def __init__(self, start, end, print_progress=True):
# 		def recur(parents):
# 			if parents:
# 				children = self.give_birth(parents)
# 				self.nodes.extend(children)
# 				if print_progress:
# 					print(len(self.nodes), len(children))
# 				recur(children)

# 		self.nodes = []
# 		self.start = start
# 		self.end = end

# 		recur([ ((None, None, None), self.start) ])

# 		# print(f"Number of Vertices: {self.num_vertices(self.start, self.end):,}")
# 		# print(f"Number of Edges: {self.num_edges(self.start, self.end):,}")


# 	@staticmethod
# 	def num_vertices(start, end):
# 		a, b, c = [e - s for e, s in zip(end, start)]
# 		return (a+1)*(b+1)*(c+1)

# 	@staticmethod
# 	def num_edges(start, end):
# 		a, b, c = [e - s for e, s in zip(end, start)]
# 		return (3*a*b*c) + (2*a*b + 2*a*c + 2*b*c) + (a + b + c)

# 	def get_children(self, parent):
# 		a, s, d = parent
# 		end_a, end_s, end_d = self.end
# 		children = []
# 		if a < end_a:
# 			children.append((a+1, s, d))
# 		if s < end_s:
# 			children.append((a, s+1, d))
# 		if d < end_d:
# 			children.append((a, s, d+1))
# 		return children

# 	def get_parents(self, child):
# 		a, s, d = child
# 		start_a, start_s, start_d = self.start
# 		parents = []
# 		if a > start_a:
# 			parents.append((a-1, s, d))
# 		if s > start_s:
# 			parents.append((a, s-1, d))
# 		if d > start_d:
# 			parents.append((a, s, d-1))
# 		return parents

# 	def give_birth(self, parents):
# 		children = []
# 		seen = []
# 		end_a, end_s, end_d = self.end
# 		for _, init_levels in parents:
# 			if init_levels in seen:
# 				continue
# 			seen.append(init_levels)
# 			c = self.get_children(init_levels)
# 			children.extend(list(zip([init_levels]*len(c), c)))
# 		return children

# 	@staticmethod
# 	def assign_edge(parent, child, boost_function, defenders, equipment_data, equipment=None):
# 		""" Returns (parent_string, child_string, (edge_cost, additional_information)),
# 			where additional_information may contain optimal equipment loadouts, attack styles etc.
# 			@oaram equipment One of:
# 					1) A list of equipment.
# 					2) A function | (a, s, d) => A list of equipment.
# 					3) None. In which case an optimization over possible equipment will be performed. """
# 		def f(pair):
# 			return f"{pair[0]}-{pair[1]}-{pair[2]}"
# 		(old_a, old_s, old_d), (new_a, new_s, new_d) = parent, child
# 		training_skill = 'attack' if new_a > old_a else 'strength'
# 		diffs = [i for i, (x, y) in enumerate(zip(parent, child)) if y > x]
# 		assert len(diffs) == 1, f"{list(enumerate(list(zip(parent, child))))} - {diffs}"
# 		training_skill = ['attack', 'strength', 'defence'][diffs[0]]

# 		if equipment:
# 			if hasattr(equipment, '__call__'):
# 				equipment = equipment(old_a, old_s, old_d)
# 			player = PlayerBuilder({"attack": old_a, "strength": old_s, 'defence': old_d}, equipment_data).equip(equipment).get()
# 			t = float('inf')
# 			optimal_stance = (None, None)
# 			for name, stance in player.get_stances().items():
# 				if stance['experience'] == training_skill:
# 					player.combat_style = stance['combat_style']
# 					level_time = get_time_to_level(player, training_skill, boost_function(player), defenders)
# 					if level_time < t:
# 						t = level_time
# 						optimal_stance = (player.combat_style, time_dependent_model_xp(boost_function(player), defenders))

# 			assert optimal_stance is not (None, None)
# 			return f(parent), f(child), (t, {
# 				'stance': optimal_stance[0],
# 				'xp_rate': optimal_stance[1],
# 				'equipment': equipment,
# 			})
# 		else:
# 			data = JsonComment().loadf("../../results/part_III/optimize/settings.json")
# 			player_stats = data['player_stats']
# 			player_stats.update({"attack": old_a, "strength": old_s, 'defence': old_d})
# 			player_stats.update({'cmb': combat_level(player_stats)})

# 			sets = get_sets(training_skill, defenders, player_stats, data['ignore'], data['adjustments'], equipment_data)
# 			sets = [{ slot: eq for slot, eq in s if eq is not None} for s in sets]

# 			best_equipment, best_xp_rate, best_stance = get_best_set(
# 				player_stats, training_skill, boost_function,
# 				defenders, sets, include_shared_xp=False
# 			)
# 			pprint({"attack": old_a, "strength": old_s, 'defence': old_d,
# 				"weapon": best_equipment["weapon"] if "weapon" in best_equipment else best_equipment["2h"]
# 			})
# 			player = PlayerBuilder(player_stats, equipment_data).equip(list(best_equipment.values())).get()
# 			player.combat_style = best_stance
# 			t = get_time_to_level(player, training_skill, boost_function(player), defenders)
# 			return f(parent), f(child), (t, {
# 				'stance': best_stance,
# 				'xp_rate': best_xp_rate,
# 				'equipment': best_equipment,
# 			})

# def get_solution(tree, boost_function, defenders, equipment_data, equipment=None, start=None, end=None):
# 	start = start if start else tree.start
# 	end = end if end else tree.end
# 	graph = Graph()
# 	nodes = xmap(lambda c: Tree.assign_edge(*c, boost_function, defenders, equipment_data, equipment), tree.nodes)

# 	cost_dict = {(tuple(int(x) for x in p.split('-')), tuple(int(x) for x in c.split('-'))): t for p, c, (t, _) in nodes}
# 	[graph.add_edge(*node) for node in nodes]

# 	return find_path(graph, '-'.join(str(s) for s in start), '-'.join(str(e) for e in end),
# 		cost_func=lambda u, v, edge, prev_edge: edge[0]
# 	)

# from collections import namedtuple
# PathInfo = namedtuple('PathInfo', ('nodes', 'edges', 'costs', 'total_cost'))
# class Solver:
# 	def __iter__(self):
# 		return self

# 	def get_path_costs(self, nodes):
# 		edges = []
# 		costs = []
# 		total_cost = 0
# 		for i in range(len(nodes) - 1):
# 			parent, child, (cost, details) = None, None, (0, {'equipment': []}) #self.cost_function(nodes[i], nodes[i+1])
# 			if (nodes[i], nodes[i+1]) in self.costs:
# 				parent, child, (cost, details) = self.costs[(nodes[i], nodes[i+1])]
# 			else:
# 				parent, child, (cost, details) = c = self.cost_function(nodes[i], nodes[i+1])
# 				self.costs[(nodes[i], nodes[i+1])] = c

# 			edges.append( (cost, details) )
# 			costs.append(cost)
# 			total_cost += cost
# 		return edges, costs, total_cost

# 	def is_out_of_bounds(self, node):
# 		return not all(s <= n <= e for n, s, e in zip(node, self.start, self.end))

# 	def __init__(self, tree, cost_function):
# 		self.tree = tree
# 		self.start = tree.start
# 		self.end = tree.end
# 		self.costs = {}
# 		self.cost_function = cost_function

# 		self.best_path = []
# 		sa, ss, sd = self.start
# 		ea, es, ed = self.end
# 		for s in range(ss, es+1):
# 			self.best_path.append((sa, s, sd))
# 		for a in range(sa+1, ea+1):
# 			self.best_path.append((a, es, sd))
# 		for d in range(sd+1, ed+1):
# 			self.best_path.append((ea, es, d))

# 		self.exclusions = [0]*(ea - sa)

# 	def __len__(self):
# 		return sum(e-s for e, s in zip(self.end, self.start))

# 	def __next__(self):
# 		def get_left_most_chain(excluded):
# 			if sum(excluded) == 0:
# 				return self.best_path

# 			path = [self.start]
# 			sa, ss, sd = self.start
# 			ea, es, ed = self.end
# 			c = 0
# 			for i in range(len(self)):
# 				a, s, d = path[-1]
# 				a_gain = a - self.start[0]
# 				s_gain = s - self.start[1]
# 				d_gain = d - self.start[2]
# 				if s < es - excluded[a_gain]:
# 					path.append((a, s+1, d))
# 				else:
# 					path.append((a+1, s, d))


# 			return path

# 		def increment_exclusions():
# 			largest_exclusion = self.end[0] - self.start[0]

# 			def inc(value):
# 				return value < largest_exclusion

# 			for i, ex in enumerate(self.exclusions):
# 				if inc(ex):
# 					self.exclusions[i] += 1
# 					break
# 				elif inc(self.exclusions[i + 1]):
# 					self.exclusions[i+1] += 1
# 					for j in range(i+1):
# 						self.exclusions[j] = self.exclusions[i+1]
# 					break

# 		# print(self.exclusions)
# 		chain = get_left_most_chain(self.exclusions)
# 		increment_exclusions()
# 		if self.exclusions[-1] == 1:
# 			raise StopIteration

# 		print(self.get_path_costs(chain)[-1])
# 		self.best_path = chain
# 		return self.get()

# 	def get(self):
# 		path = ['-'.join(str(x) for x in node) for node in self.best_path]
# 		return PathInfo(path, *self.get_path_costs(self.best_path))
