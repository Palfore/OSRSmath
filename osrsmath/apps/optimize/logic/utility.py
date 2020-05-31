from pprint import pprint

def get_maximum_sets(groups, getter=None):
	''' Takes in a list of tuples and returns the subset containing the unique maximums.
		@param groups: [(A, B), (C, D), ... (Y, Z)]
		@param getter: A function which accesses the element of (A) to be compared.
		@return [(A, B), (E, F), (M, N)]
		@note When the group elements are single-length tuples,
				this degenerates into the max function.
		@warning Fails if there are duplicate items. '''
	def is_better(element, other):
		if getter:
			element = getter(element)
			other = getter(other)
		if all(o == e for e, o in zip(element, other)):
			return False
		return not any(o > e for e, o in zip(element, other))

	def someone_is_better(element, others):
		return any(is_better(other, element) for other in others
		           if element is not other)

	return [element for element in groups if not someone_is_better(element, groups)]


if __name__ == '__main__':
	print(get_maximum_sets([(1, 4), (1, 5), (1, 5)]), [(1, 5)])
	print(get_maximum_sets([(1, 4), (1, 5)]), [(1, 5)])
	print(get_maximum_sets([(1, 4), (1, 5), (2, 6)]), [(2, 6)])
	print(get_maximum_sets([
		{
			'name': 'test1',
			'values': (1, 4),
		}, {
			'name': 'test2',
			'values': (1, 5),
		}, {
			'name': 'test3',
			'values': (2, 6),
		},
	], lambda x: x['values']))

	print(get_maximum_sets([(1, 4), (1, 5), (3, 4)]), [(1, 5), (3, 4)])

	print(get_maximum_sets([
		(0.16, -4, 85),
		(0.16, -2, 85),
		(0.16, 2, 0),
		(0.16, 11, 13),
		(0.16, 12, 68),
	]))