from osrsmath.combat.fighter import Fighter
from osrsmath.combat.experience import xp_rate
import multiprocess
import time

def mmap(f, items, callback, interval=0.025, num_cores=0):
	""" num_cores: None or 0 mean maximum ("the number returned by `os.cpu_count()`"). 
			@see https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool
	"""
	results = []
	start = time.time()
	with multiprocess.Pool(num_cores if num_cores != 0 else None) as pool:
		for i, result in enumerate(pool.imap_unordered(f, items), 1):
			results.append(result)
			now = time.time()
			if now-start >= interval:
				start = now
				callback(i/len(items)*100)
		callback(100)
	# pool.clear()  # Using close/join crashes the app on the next iteration, ProcessPool must effect the global space.
	return results

def eval_set(fighter, training_skill, states, defenders, s, include_shared_xp=True):
	combat_style, s = s
	fighter.equipment.wear(*s.values())
	fighter.set_stance(combat_style)
	xp = xp_rate(
		fighter.get_attack_style(),
		fighter.get_attack_speed(),
		states(fighter),
		defenders,
		'MarkovChain'
	)
	print(s, '|', f"{xp/1000:.2f}")
	return s, xp, combat_style




