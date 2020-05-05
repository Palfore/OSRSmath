from osrsmath.model.player import PlayerBuilder
from osrsmath.model.experience import xp_rate
from multiprocessing import Value
import pathos.pools as pp
import time

class Eval:
	INTERVAL = 0.025  # How frequently the progress is updated (in seconds).
	completed = Value('i', 0)

	@classmethod
	def start(cls, f, items, callback):
		evaluator = Eval(f, len(items))
		values = cls.map(evaluator, items)
		evaluator.monitor_progress(callback)
		return list(values)

	@staticmethod
	def map(f, items):
		return pp.ProcessPool().imap(f, items)

	def __init__(self, f, num_items):
		self.num_items = num_items
		self.f = f
		with self.completed.get_lock():
			self.completed.value = 0

	def __call__(self, x):
		result = self.f(x)
		with self.completed.get_lock():
			self.completed.value += 1
		return result

	def monitor_progress(self, callback):
		callback(0)
		while self.completed.value < self.num_items:
			callback(self.completed.value/self.num_items*100)
			time.sleep(self.INTERVAL)
		callback(self.completed.value/self.num_items*100)


def eval_set(player_stats: dict, training_skill, states, defenders, s, include_shared_xp=True):
	try:
		combat_style, s = s
		player = PlayerBuilder(player_stats).equip(s.values()).get()
		stance = player.get_stances()[combat_style]
		player.combat_style = stance['combat_style']
		xp = xp_rate(
			stance['attack_type'],
			player.get_stats()['attack_speed'],
			states(player),
			defenders,
			'MarkovChain'
		)
		# print(s, '|', f"{xp/1000:.2f}")
		return s, xp, combat_style
	except Exception as e:
		import traceback as tb
		print(e, tb.format_exc())




