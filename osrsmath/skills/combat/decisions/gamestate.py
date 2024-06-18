from dataclasses import dataclass, field
from numpy.random import randint

@dataclass
class Fighter:
	name: str
	H: int
	H_max: int
	m: int
	t_eat: int
	t_attack: int
	speed: int
	food: int  # This is for specific heal and delay. Add food_1, etc for more variety

	def draw(self):
		return randint(0, self.m + 1)



@dataclass
class GameState:
	fighter1: Fighter
	fighter2: Fighter
	
	def __post_init__(self):
		self.fighters = self.fighter1, self.fighter2
		self.fighters_by_name = {fighter.name: fighter for fighter in self.fighters}

	def get_fighter(self, name):
		return self.fighters_by_name[name]

	def start_tick(self):
		for fighter in self.fighters:
			if fighter.H <= 0:
				raise ValueError(f"{fighter.name} is already dead.")
			if fighter.t_attack > 0:
				fighter.t_attack -= 1
			if fighter.t_eat > 0:
				fighter.t_eat -= 1

	def end_tick(self):
		for fighter in self.fighters:
			pass

	def attack(self, attacker, defender):
		if attacker.t_attack == 0:
			damage = attacker.draw()
			defender.H = max(defender.H - damage, 0)
			attacker.t_attack = attacker.speed
			return damage
		
	def eat(self, fighter, amount, delay):
		if fighter.food <= 0:  # Eating when there is no food performs no action
			return

		if fighter.t_eat == 0:
			heal = min(amount, fighter.H_max - fighter.H)  # Heal, capped by max hp
			fighter.food -= 1  # Consume a food
			fighter.H += heal  # Heal
			fighter.t_eat = delay  # Delay next eat
			fighter.t_attack = fighter.speed  # Restart attack countdown
			return heal

	def winner(self):
		alive = [fighter for fighter in self.fighters if fighter.H > 0]
		if len(alive) == 2:
			return None
		elif len(alive) == 1:
			return alive[0].name
		elif len(alive) == 0:
			return list(self.fighters_by_name.keys())  # Draw
		
	def auto_finish(self, player_policy, opponent_policy, show=False, record_states=False, record_actions=False, timeout=None):
		actions = []
		states = [list(map(lambda x: Fighter(**vars(x)), self.fighters))]
		winner = None
		t = 0
		while winner is None:
			self.start_tick()
			player_outcome = player_policy(self)
			opponent_outcome = opponent_policy(self)
			self.end_tick()
			t += 1

			winner = self.winner()
			if record_actions:
				actions.append([player_outcome, opponent_outcome])
			if record_states:
				states.append(list(map(lambda x: Fighter(**vars(x)), self.fighters)))
			if show:
				print(f'{t} {self} O{opponent_outcome} P{player_outcome}')

			if timeout and t >= timeout:
				break

		if show:
			print(f'{self.winner()} wins {self.fighters}')
		return {
			'winner': winner,
			'states': states if record_states else None,
			'actions': actions if record_actions else None,
		}

def policy_ask(game_state):
	action = input('What action? (a)ttack, (e)at, (p)ass, (d)elay')
	if action == 'a':
		damage = game_state.attack(game_state.get_fighter('Player'), game_state.get_fighter('Opponent'))
		return 'a', damage
	elif action == 'e':
		heal = game_state.eat(game_state.get_fighter('Player'), 1, 3)
		return 'e', heal
	elif action == 'p':
		pass
	elif action == 'd':
		# game_state.delay()
		pass



def policy_min_hp(game_state, a, d, min_hp):
	if a.H != a.H_max and a.H <= min_hp and a.food != 0:
		heal = game_state.eat(a, *FOOD)
		return 'e', heal
	else:
		return policy_attack(game_state, a, d)

def policy_attack(game_state, a, d):
	damage = game_state.attack(a, d)
	return 'a', damage


def policy_network(game_state, a, d, sol_idx):
	global GANN_instance
	gs = game_state

	# if a.name == 'Player':
	game_values = [*list(gs.fighter1.__dict__.values())[1:], *list(gs.fighter2.__dict__.values())[1:]]
	# elif a.name == 'Opponent':
	# 	game_values = [*list(gs.fighter2.__dict__.values())[1:], *list(gs.fighter1.__dict__.values())[1:]]
	

	data_inputs = numpy.array([game_values])
	action = float(pygad.nn.predict(last_layer=GANN_instance.population_networks[sol_idx], data_inputs=data_inputs, problem_type="regression")[0][0])
	
	choice, value = None, None
	if action < 0:
		choice = 'a'
		value = gs.attack(a, d)
	else:
		choice = 'e'
		value = gs.eat(a, *FOOD)
	return choice, value
		

FOOD = 8, 3
def make_player():
	return Fighter("Player", 30, 30, 10, 0, 0, 4, 28)

def make_opponent():
	return Fighter("Opponent", 30, 30, 10, 0, 0, 4, 28)

if __name__ == '__main__':
	import numpy
	import pygad
	import pygad.nn
	import pygad.gann

	def fitness_func(solution, sol_idx):
		global GANN_instance
		
		num_attempts = 10
		points = 0
		for attempts in range(num_attempts):
			player = make_player()
			opponent = make_opponent()
			gs = GameState(player, opponent)
			if gs.auto_finish(
					lambda gs: policy_network(gs, gs.get_fighter('Player'), gs.get_fighter('Opponent'), sol_idx),
					lambda gs: policy_network(gs, gs.get_fighter('Opponent'), gs.get_fighter('Player'), sol_idx),
					# lambda gs: policy_attack(gs, gs.get_fighter('Opponent'), gs.get_fighter('Player')),
					# lambda gs: policy_min_hp(gs, gs.get_fighter('Opponent'), gs.get_fighter('Player'), 5),
					timeout=1000
				)['winner'] == 'Player':
				points += 1

		return points / num_attempts

	def callback_generation(ga_instance):
		global GANN_instance
	
		population_matrices = pygad.gann.population_as_matrices(population_networks=GANN_instance.population_networks, 
																population_vectors=ga_instance.population)
	
		GANN_instance.update_population_trained_weights(population_trained_weights=population_matrices)
	
		print(f"G{ga_instance.generations_completed}, {ga_instance.best_solution()[1]}")
		# print("Accuracy   = {fitness}".format(fitness=ga_instance.best_solution()[1]))
	
	

	
	GANN_instance = pygad.gann.GANN(num_solutions=100,
									num_neurons_input=14,
									num_neurons_hidden_layers=[32],
									num_neurons_output=1,
									hidden_activations=["relu"],
									output_activation="None")
	
	population_vectors = pygad.gann.population_as_vectors(population_networks=GANN_instance.population_networks)
	
	ga_instance = pygad.GA(num_generations=20, 
						   num_parents_mating=3, 
						   initial_population=population_vectors.copy(),
						   fitness_func=fitness_func,
						   mutation_percent_genes=5,
						   callback_generation=callback_generation)
	
	ga_instance.run()
	ga_instance.plot_result()
	solution, solution_fitness, solution_idx = ga_instance.best_solution()
	print(solution_fitness, solution_idx)
	
	player = make_player()
	opponent = make_opponent()
	gs = GameState(player, opponent)
	game_results = gs.auto_finish(
		lambda gs: policy_network(gs, gs.get_fighter('Player'), gs.get_fighter('Opponent'), solution_idx),
		lambda gs: policy_network(gs, gs.get_fighter('Opponent'), gs.get_fighter('Player'), solution_idx),
		# lambda gs: policy_network(gs, solution_idx),
		# lambda gs: policy_network(gs, solution_idx),
		# lambda gs: policy_attack(gs, gs.get_fighter('Opponent'), gs.get_fighter('Player')),
		# lambda gs: policy_min_hp(gs, gs.get_fighter('Opponent'), gs.get_fighter('Player'), 5),
		# lambda gs: policy_min_hp(gs, gs.get_fighter('Player'), gs.get_fighter('Opponent'), 5),
		# lambda gs: policy_min_hp(gs, gs.get_fighter('Opponent'), gs.get_fighter('Player'), 5),
		record_states=True,
		record_actions=True,
		show=True
	)
	game_states = game_results['states']
	game_actions = game_results['actions']

	from pprint import pprint
	import PySimpleGUI as sg
	from random import randint
	from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
	from matplotlib.figure import Figure

	def draw_figure(canvas, figure, loc=(0, 0)):
		figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
		figure_canvas_agg.draw()
		figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
		return figure_canvas_agg

	def main():
		NUM_DATAPOINTS = len(game_states)
		layout = [
			[sg.T(str(player))],
			[sg.T(str(opponent))],
			[sg.InputCombo(list(vars(player).keys()), default_value='H', key='-Y-AXIS-')],
			[	
				sg.Canvas(size=(640, 480), key='-CANVAS-'),
				sg.Table(
					values=[[str(i), str(p) if p[1] is not None else '', str(o) if o[1] is not None else ''] for i, (p, o) in enumerate(game_actions)], headings=['t', 'P', 'O'], 
					num_rows=26, auto_size_columns=False, col_widths=4, row_height=20, vertical_scroll_only=False, max_col_width=20,
					key='-Table-',
				)
			],
			[sg.Text('Progress through the data')],
			[sg.Slider(range=(0, NUM_DATAPOINTS), size=(60, 10), orientation='h', key='-SLIDER-')],
			[sg.Text('Number of data points to display on screen')],
		]

		# create the form and show it without the plot
		window = sg.Window('OSRS Combat Analyzer', layout, finalize=True)

		canvas_elem = window['-CANVAS-']
		slider_elem = window['-SLIDER-']
		canvas = canvas_elem.TKCanvas

		# draw the initial plot in the window
		fig = Figure()
		ax = fig.add_subplot(111)
		ax2 = ax.twiny()
		ax.grid()
		fig_agg = draw_figure(canvas, fig)

		for t in range(2, 10000000):
			t = min(t, len(game_states)-1)
			event, values = window.read(timeout=10)
			if event in ('Exit', None):
				exit(69)
			slider_elem.update(t)	   # slider shows "progress" through the data points
			ax.cla()					# clear the subplot
			ax2.cla()					# clear the subplot
			ax.grid()				   # draw the grid
			
			y_axis = window['-Y-AXIS-'].get()
			ax.plot(range(t+1), [getattr(s[0], y_axis) for s in game_states[:t+1]],  color='blue', label='Player')
			ax.plot(range(t+1), [getattr(s[1], y_axis) for s in game_states[:t+1]],  color='red', label='Opponent')
			
			ax.set_xlim(0)
			ax.legend()

			fig_agg.draw()
			new = [str(round(0.6*float(l.get_text()), 1)) for l in ax.get_xticklabels()]
			ax2.set_xticks(ax.get_xticks())
			ax2.set_xticklabels(new)
			ax2.set_xlabel("Seconds")
			ax.set_xlabel("Ticks")
			ax.set_ylabel(y_axis)
			fig_agg.draw()

			

		# window.close()


	main()
