from osrsmath.model.player import PlayerBuilder
from osrsmath.model.experience import xp_rate
import time

def mmap(f, items, callback, interval=0.025):
	# def g(*x):
	# 	try:
	# 		return f(*x)
	# 	except KeyboardInterrupt:
	# 		# Prevents killing main process, leaving children to never join (app hangs).
	# 		raise KeyboardInterruptError()
	results = []
	start = time.time()
	import multiprocess
	with multiprocess.Pool() as pool:
	# with pathos.pools.ProcessPool() as pool:
		for i, result in enumerate(pool.imap_unordered(f, items), 1):
			# QtCore.QCoreApplication.processEvents()  # Prevents app from hanging (especially windows)
			results.append(result)
			now = time.time()
			if now-start >= interval:
				start = now
				callback(i/len(items)*100)
		callback(100)
		# pool.clear()  # Using close/join crashes the app on the next iteration, ProcessPool must effect the global space.
	return results

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
		print(s, '|', f"{xp/1000:.2f}")
		return s, xp, combat_style
	except Exception as e:
		import traceback as tb
		print(e, tb.format_exc())




