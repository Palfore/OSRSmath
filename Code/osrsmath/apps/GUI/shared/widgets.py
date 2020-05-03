import collections
import json

class Savable:
	""" Handles the loading and saving of state.
		The Panel class should subclass this, and construct a dictionary 'entities'
		filled with calls to Savable.Entity. """
	@staticmethod
	def Entity(obj, default, setter, getter):
		return type('Entity', (object,), {
			'object': obj,
			'default': default,
			'set': lambda v: setter(obj, v),
			'get': lambda: getter(obj)
		})

	def import_defaults(self, file_name):
		self.state = {}
		try:
			self.state = json.load(open(file_name))
			for name, value in self.state.items():
				self.entities[name].set(value)
		except Exception as e:
			print(f'Unable to import_defaults for {file_name}: {e}')
			pass

	def export_defaults(self, file_name):
		for name, entity in self.entities.items():
			self.state[name] = entity.get()
		json.dump(self.state, open(file_name, 'w'), indent=4)
