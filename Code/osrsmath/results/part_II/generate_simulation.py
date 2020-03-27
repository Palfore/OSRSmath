""" All this file does, is evaluate the simulation model in a given range of max hits and starting healths.
	It also stores the results in a file, so that it can be quickly loaded.
	Otherwise re-evaluating them can take hours or days. """

from multiprocessing import Pool
import inspect
import json
import os
import osrsmath.config as config
from osrsmath.model.successful_hits import Simulation

## Multi-processing boiler plate, that allows for lambda's
_func = None
def worker_init(func):
  global _func
  _func = func
def worker(x):
  return _func(x)
def xmap(func, iterable, processes=None):
  with Pool(processes, initializer=worker_init, initargs=(func,)) as p:
    return p.map(worker, iterable)

def create_dataset(file_path, N, max_hits, healths, final_health=0):
	print("Creating Dataset")
	dataset = {
		"N": N,
		"source": inspect.getsource(Simulation(N).hinv),
		"data": {
			str(h): {
				str(m): hinv  for m, hinv in xmap(lambda m: (str(m), Simulation(N).hinv(final_health, h, m)), max_hits, processes=12)
			} for h in healths
		}
	}
	print("Saving Dataset")
	with open(file_path, 'w') as f:
		json.dump(dataset, f)

def load_dataset(N, max_hits=None, healths=None, final_health=0):
	if final_health == 0:
		file_path = os.path.join(config.DATA_PATH, f"simulations/simulation.{N}.dat")
	else:
		file_path = os.path.join(config.DATA_PATH, f"simulations/simulation.{N}.{final_health}.dat")

	if not os.path.exists(file_path):
		if max_hits is None or healths is None:
			raise ValueError(f"The dataset at {file_path} needs to be created, please supply the max_hits and healths.")
		create_dataset(file_path, N, max_hits, healths)
	return json.load(open(file_path))['data']

if __name__ == '__main__':
	N = 100_000
	m_min, m_max = (1, 110)
	h_min, h_max = (1, 255)
	x = np.array(range(m_min, m_max+1))
	y = np.array(range(h_min, h_max+1))
	create_dataset(N, x, y)

