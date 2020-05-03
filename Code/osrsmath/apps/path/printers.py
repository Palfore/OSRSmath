# from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os

class SchemePrinter:
	# Skill Cape Colors
	ATTACK_COLOR = (140, 42, 34)
	STRENGTH_COLOR = (13, 135, 88)
	DEFENCE_COLOR = (150, 165, 218)
	SKILL_VALUES = {'a': 0, 's': 1, 'd': 2}

	def __init__(self):
		self.schemes = []

	def training_scheme(self, path):
		leveled_skill = []
		prev_a, prev_s, prev_d = [int(x) for x in path.nodes[0].split('-')]
		for n, cost in zip(path.nodes[1:], path.costs):
			a, s, d = [int(x) for x in n.split('-')]
			print((prev_a, prev_s, prev_d), (a, s, d), cost)
			if a > prev_a:
				leveled_skill.append(SchemePrinter.SKILL_VALUES['a'])
			elif s > prev_s:
				leveled_skill.append(SchemePrinter.SKILL_VALUES['s'])
			elif d > prev_d:
				leveled_skill.append(SchemePrinter.SKILL_VALUES['d'])
			else:
				assert False, f"A level was not gained: {path.nodes}"
			prev_a, prev_s, prev_d = a, s, d
		print(path.total_cost)
		return path.nodes[0], path.nodes[-1], leveled_skill

	def add_path(self, label, path):
		self.schemes.append((label, self.training_scheme(path)))

	def print(self, file_name=None, colors={'a': ATTACK_COLOR, 's': STRENGTH_COLOR, 'd': DEFENCE_COLOR}):
		assert self.schemes
		normalized_colors = {key: [v/255 for v in value] for key, value in colors.items()}

		fig, axes = plt.subplots(len(self.schemes), 1)
		if len(self.schemes) == 1:
			axes = [axes]
		plt.xlabel("Levels Obtained")
		for axis, (name, (start, end, scheme)) in zip(axes, self.schemes):
			axis.set_title(name, loc='center')
			axis.set_yticklabels([])
			axis.tick_params(axis='y', which='both', left=False, right=False, labelbottom=False)
			axis.set_xticklabels([start, str(end)])
			axis.set_xticks([0, len(scheme)])
			used_colors = [rgb for skill, rgb in normalized_colors.items() if SchemePrinter.SKILL_VALUES[skill] in scheme]
			axis.pcolor(np.array([scheme, ]), cmap=mpl.colors.ListedColormap(used_colors), edgecolors='black')

		plt.tight_layout()
		if file_name:
			plt.savefig(f"{file_name}.pdf")
			os.system(f"pdfcrop {file_name}.pdf")
			os.rename(f"{file_name}-crop.pdf", f"{file_name}.pdf")
		plt.show()

class TreePrinter:
	DEFAULT_FILE_NAME = "tree"
	DEFAULT_GRID_THICKNESS = 1.8
	DEFAULT_GRID_COLOR = "black"
	DEFAULT_GRID_SPACING = (2.0, 1.0)
	COMPILATION_COMMAND = lambda file_path: f"lualatex -shell-escape -interaction=batchmode {file_path}.tex"  # -se improves memory usage
	# COMPILATION_COMMAND = lambda file_path: f"lualatex -shell-escape  {file_path}.tex"  # -se improves memory usage
	CLEAN_UP_COMMAND = lambda file_path: f"rm {file_path}.tex {file_path}.aux {file_path}.log"
	PREAMBLE = R"""
		\RequirePackage{luatex85}  % https://tex.stackexchange.com/questions/315025/lualatex-texlive-2016-standalone-undefined-control-sequence
		\documentclass[tikz, margin=0mm]{standalone}
		\usepackage{tkz-graph}
		\usetikzlibrary{calc}
		\renewcommand*{\EdgeLineWidth}{0.15pt}
	""".replace('\t', '').split('\n')[1:] + ['\n']
	BEGIN_DOCUMENT = R"""
		\begin{document}
	""".replace('\t', '').split('\n')

	END_DOCUMENT = R"""
		\end{document}
	""".replace('\t', '').split('\n')

	TIKZ_START = R"""
		\begin{tikzpicture}
		\GraphInit[vstyle=Empty]
	""".replace('\t', '').split('\n')

	TIKZ_END = R"""
		\end{tikzpicture}
	""".replace('\t', '').split('\n')

	POSTAMBLE = R"""
	""".replace('\t', '').split('\n')

	def __init__(self, start, end):
		self.start = start
		self.end = end

		# Latex Contents
		self.vertices = []
		self.edges = []
		self.paths = []
		self.marks = []


	def _to_level(self, depth, index, defence):
		""" Converts the depth (row #) and vertex index (from left to right) to the corresponding attack and strength levels. """
		sa, ss, _ = self.start
		return sa+depth-index-1, ss+index, defence

	def _to_vertex(self, attack, strength, defence):
		""" Converts an attack strength to the corresponding vertex representation. """
		sa, ss, sd = self.start
		size = attack + strength - sa - ss + 1
		i = strength - ss
		return size, i, defence

	def format(self, depth, index, defence):
		""" Returns the string format using as the vertex identifier for a depth index pair. """
		return f"{depth}-{index}-{defence}"

	def unformat(self, representation):
		""" Returns the string format using as the vertex identifier for a depth index pair. """
		return [int(l) for l in representation.split('-')]

	def add_grid(self, cost_function=lambda p, c: (TreePrinter.DEFAULT_GRID_THICKNESS, TreePrinter.DEFAULT_GRID_COLOR),
				 draw_dots=False, spacing=DEFAULT_GRID_SPACING, add_text=False):
		""" cost_function ([pa, ps, pd], [ca, cs, cd]) => (thickness, color),
				where p, c is parent, child and a, s, d are attack, strength, and defence levels. """
		sa, ss, sd = self.start
		ea, es, ed = self.end
		assert sd == ed, f"Cannot print in 3 dimensions yet. Make start and end defence levels the same."

		for size in range(1, 2*(max(es, ea)-min(sa, ss))+1+1):
			lines = []
			edges = []
			edges_levels = []
			for i in range(size):
				l, r, d = self._to_level(size, i, sd)
				if l > ea or r > es: continue;  # This could be more efficient, but its not limiting.
				x, y, text = (size / 2 - i )*spacing[0], -size*spacing[1], f"${l}, {r}$" if add_text else "$$"
				self.vertices.append(Rf"\Vertex[x={x}, y={y}, L={{{text}}}]{{{self.format(size, i, d)}}}")
				if draw_dots:
					self.vertices.append(Rf"\filldraw({(size / 2 - i )*spacing[0]}, {-size*spacing[1]}) circle[radius=2pt];")

				if size > 1:
					child = (size, i, d)
					parent = None
					if i >= 1:
						parent = (size-1, i-1, d)
						thickness, color = cost_function(list( self._to_level(*parent) ), list( self._to_level(*child) ))
						self.edges.append(Rf"\draw[-,line width={thickness:f}pt,color={color}] ({self.format(*child)}) --  ({self.format(*parent)});")
					if i < size - 1:
						parent = (size-1, i, d)
						thickness, color = cost_function(list(self._to_level(*parent)), list(self._to_level(*child)))
						self.edges.append(Rf"\draw[-,line width={thickness:f}pt,color={color}] ({self.format(*child)}) --  ({self.format(*parent)});")

	def mark_level(self, level, size=10, color='black'):
		self.marks.append(Rf"\filldraw[color={color}]({self.format(*self._to_vertex(*level))}) circle[radius={size}pt];")

	def add_paths(self, solution_paths, color="red", color_if_best=None):
		if color_if_best:
			costs = [s.total_cost for s in solution_paths]
			best_index = costs.index(min(costs))
		for i, solution_path in enumerate(solution_paths):
			if color_if_best and i == best_index:
				self.add_path(solution_path, color_if_best)
			else:
				self.add_path(solution_path, color)

	def add_path(self, solution_path, color='black', thickness='6', circle_start=True, circle_end=True):
		equipment = {}
		seen_equipment = set()
		path_latex = []
		for i, (node, (_, details)) in enumerate(zip(solution_path.nodes, solution_path.edges)):
			diff = set(details['equipment'].items()) ^ set(equipment.items())
			new = [e for e in equipment.values() if e not in seen_equipment]
			if new:
				[seen_equipment.add(e) for e in new]
				self.mark_level(self.unformat(node), color='green')
			elif diff:
				equipment = details['equipment']
				self.mark_level(self.unformat(node), color='blue')
			a = self.format(*self._to_vertex(*self.unformat(solution_path.nodes[i])))
			b = self.format(*self._to_vertex(*self.unformat(solution_path.nodes[i+1])))

			path_latex.append(Rf"\draw[-,line width={thickness}pt,color={color}] ({a}) --  ({b});")
			if circle_start and i == 0:
				path_latex.append(Rf"\filldraw({a}) circle[radius=10pt];")
		if circle_end:
			path_latex.append(Rf"\filldraw({b}) circle[radius=10pt];")
		self.paths.append(path_latex)

	def print(self, file_path=DEFAULT_FILE_NAME, clean=True, animate=False):
		assert self.edges, "Must add a grid before printing"
		with open(file_path+'.tex', 'w') as f:
			f.writelines('\n'.join(self.PREAMBLE))
			# if animate:
				# f.write(R"\usepackage{animate}" + '\n')
			f.writelines('\n'.join(self.BEGIN_DOCUMENT))
			# if animate:
				# f.write(R"\pgfmathtruncatemacro\N{10}" + '\n')
				# f.write(R"\begin{animateinline}[controls,autoplay,loop]{2}" + '\n')
			for i, path in enumerate(self.paths):
				# if animate and i != 0:
					# f.write(R"\newframe" + '\n')
				f.writelines('\n'.join(self.TIKZ_START) + '\n')
				f.writelines('\n'.join(self.vertices) + '\n')
				f.writelines('\n'.join(self.edges) + '\n')
				f.writelines('\n'.join(path) + '\n')
				f.writelines('\n'.join(self.marks) + '\n')
				f.writelines('\n'.join(self.TIKZ_END) + '\n')
			# if animate:
				# f.write(R"\end{animateinline}" + '\n')
			f.writelines('\n'.join(self.END_DOCUMENT) + '\n')
			f.writelines('\n'.join(self.POSTAMBLE) + '\n')

		os.system(TreePrinter.COMPILATION_COMMAND(file_path))
		if animate:
			os.system(f"convert -density 300 -delay 20 -loop 0 -alpha remove {file_path}.pdf {file_path}.gif")
		if clean:
			os.system(TreePrinter.CLEAN_UP_COMMAND(file_path))
