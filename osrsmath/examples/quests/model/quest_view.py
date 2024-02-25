from osrsmath.examples.quests.model.quest import Player, QuestBook
from matplotlib.lines import Line2D
from matplotlib import pyplot as plt
from pyvis.network import Network
from datetime import datetime
import networkx as nx
import numpy as np
import webbrowser
import pathlib
import os


class QuestViewer:
	def __init__(self, player, colors, options):
		self.player = player
		self.player.quest_book.clear()
		self.colors = colors
		self.options = options
		self.assign_shells()
		self.assign_graph()

	def assign_shells(self):
		self.shells = []
		to_complete = self.player.get_doable_quests()
		while to_complete:
			self.shells.append(to_complete)
			[self.player.force_complete(quest) for quest in to_complete]
			to_complete = self.player.get_doable_quests()

		self.shell_lookup = {}
		for shell, shell_quests in enumerate(self.shells):
			for quest in shell_quests:
				self.shell_lookup[quest] = shell

	def assign_graph(self):
		def chunk(lst, n):
		    """Yield successive n-sized chunks from lst."""
		    for i in range(0, len(lst), n):
		        yield lst[i:i + n]

		class Formatter:
			def format_requires(prereqs):
				return prereqs

			def format_progresses(prereqs):
				return prereqs

			def format_needs(prereqs):
				return [f"{level} {skill}" for level, skill in prereqs]

			def format_rewards(prereqs):
				return [f"{xp:,} {skill} xp" for skill, xp in prereqs]

			@classmethod
			def format(cls, prereqs, kind):
				match kind:
					case 'requires':
						value = cls.format_requires(prereqs)
					case 'progresses':
						value = cls.format_progresses(prereqs)
					case 'needs': 
						value = cls.format_needs(prereqs)
					case 'rewards':
						value = cls.format_rewards(prereqs)
					case _:
						assert False, f'An invalid kind was specified: {kind}'
				return SPACE + ' | '.join(value)


		self.graph = nx.MultiDiGraph()
		all_quest_names = sum(self.shells, [])
		all_quests = [self.player.quest_book[name] for name in all_quest_names]
		sorted_quests = sorted(all_quests, key=lambda quest: datetime.strptime(quest.released, "%d %B %Y"))
		for i, quest in enumerate(sorted_quests, 1):
			shell = self.shell_lookup[quest.name]	
			print(f"Loading Quest #{i}: {quest.name} ({quest.released})")

			SPACE = "&emsp;"
			hover_details = '<br>'.join([
				f"<b>{quest.name} " + 
					("<span style='color:gold;'>m </span>" if quest.members else "") + 
					("<span style='color:red;'>! </span>" if quest.combat else "") + 
					f"</b><span style='color:{self.colors['difficulty'][quest.difficulty]};'>" +
					"&#x25CD;"*(list(self.colors['difficulty'].keys()).index(quest.difficulty)+1) + "</span>",
				f"<i>Tier</i> {self.shell_lookup[quest.name]}{' - ' + quest.series if quest.series != 'None' else ''}",
				f"<i>Length:</i> {quest.length}",
				f"<i>Released:</i> {quest.released}",
				f"<i>Developer(s):</i> {', '.join(quest.developer)}",
				"<hr>",
				"<b>Requires:</b>", *[Formatter.format(prereqs, 'requires') for prereqs in chunk(list(quest.quest_requirements), 2)],
				"<b>Progresses:</b>", *[Formatter.format(prereqs, 'progresses') for prereqs in chunk(list(self.player.quest_book.get_quests_requiring(quest.name)), 2)],
				"<b>Needs:</b>", *[Formatter.format(prereqs, 'needs') for prereqs in chunk(list(quest.skill_requirements.items()), 2)],
				"<b>Rewards:</b>", *[Formatter.format(prereqs, 'rewards') for prereqs in chunk(list(quest.rewards.items()), 2)],
			])
			self.graph.add_node(quest.name, title=hover_details, url=quest.url,
				shell=shell, tier=shell, difficulty=quest.difficulty, length=quest.length, series=quest.series.split(', #')[0], 
				released=quest.released, combat=quest.combat, members=quest.members,
				main_developer=quest.developer[0], year=int(quest.released.split(' ')[-1]),
				level=shell+1, group=quest.series, size=15 + 50*list(self.colors['length']).index(quest.length)/len(self.colors['length']),  # Size by quest length
			)

			# Add only the direct requirements (top level).
			for this_prereq in quest.quest_requirements:
				# Get the quest requirements for the prereqs except for this_prereq.
				other_prereqs = [self.player.quest_book[opr].quest_requirements for opr in quest.quest_requirements if opr != this_prereq]
				
				# As long as this_prereq isn't required by another prereq, you can add it.
				if not any(this_prereq in opr for opr in other_prereqs):
					self.graph.add_edge(quest.name, this_prereq)

	def save_pdf(self, connections_are_quest_color=False):
		label_dict = {quest: quest.replace("Recipe for Disaster", "RFD") for quest in self.graph}
		node_colors = [self.colors['shell'][self.shell_lookup[quest]] for quest in self.graph]
		edge_colors = []
		for left, right, info in self.graph.edges:
			choice = [left, right][connections_are_quest_color]
			edge_colors.append(self.colors['shell'][self.shell_lookup[choice]])

		layout = {}
		for quest in sum(self.shells, []):
			shell = self.shell_lookup[quest]
			x = shell / len(self.shells)
			y = (self.shells[shell].index(quest)+1) / (len(self.shells[shell])+1)
			layout[quest] = np.array([x, y])

		plt.figure(figsize=(60, 80))
		plt.title("Old School Runescape Quest Tree\n"+("(colored by quest)" if connections_are_quest_color else "(colored by requirement)"),
			fontsize=150, fontweight="bold"
		)
		nx.draw_networkx(self.graph,
			arrows=True,
			pos=layout,
			node_size=1200,
			font_size=40,
			verticalalignment='bottom',
			width=2,
			arrowsize=50,
			arrowstyle='-|>' if connections_are_quest_color else '<|-',
			edge_color=edge_colors,
			node_color=node_colors,
			labels=label_dict,
			font_weight=1000,
		)
		plt.legend(
			[Line2D([0], [0], color=c, linewidth=20, linestyle='-') for c in self.colors['shell']],
			[f"Tier {i} Quest" for i in range(len(self.shells))],
			fontsize=80
		)
		plt.axis('off')
		plt.tight_layout()
		plt.savefig(f"output/by_{'quest' if connections_are_quest_color else 'requirement'}.pdf", format="pdf")


	def save_graph(self, file='quest_viewer.html', title="The Old School Runescape Universe", show=True):
		dates = {quest: datetime.strptime(self.graph.nodes.get(quest)['released'], '%d %B %Y').timestamp() for quest in self.graph.nodes}
		quests_by_release = [k for k, v in sorted(dates.items(), key=lambda x: x[1])]
		temp_file = file.split('.')[0] + '-temp.html'
		nt = Network('90%', '100%')
		nt.from_nx(self.graph)
		nt.set_options("{}")
		nt.save_graph(temp_file)

		## We will take the default graph, and apply replacements and add new code.
		with open(temp_file, "r") as f:
			contents =  [
				l.strip(  # Spaces make it harder to match by exact line
					' '
				).replace(  # We need full height
					'<div class="card" style="width: 100%">', 
					'<div class="card" style="width: 100%; height: 100%;">'
				).replace(  # We don't want padding
					'<div id="mynetwork" class="card-body"></div>',
					'<div id="mynetwork" class="card-body" style="padding:0;"></div>'
				).replace(  # We need to wrap the titles in the htmlTitle() js function.
					'"title": ', '"title": htmlTitle(', 
				).replace(  # Assuming consistent key order, url marks the end of htmlTitle; we need an end ')'.
					', "url": ', '), "url": '
				) for l in f.readlines()
			]

		contents.insert(
			contents.index("// This method is responsible for drawing the graph, returns the drawn network\n"),
			'function htmlTitle(html) {const container = document.createElement("div");container.innerHTML = html;return container;}\n\n'
		)

		contents.insert(contents.index("<html>\n")+1, '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
		contents.insert(contents.index("<head>\n")+1, '\n'.join([
			'<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>', 
			'',
			'<script src="https://cdn.jsdelivr.net/npm/popper.js@1.14.7/dist/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>', 
			'<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>', 
			'<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">', 			
			'<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.1/font/bootstrap-icons.css"><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis.css" type="text/css" />', 
			'',
			'<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">',
			'<link href="https://db.onlinewebfonts.com/c/4c8754090a7936fac2f8c5f3043db9ee?family=RuneScape+UF+Regular" rel="stylesheet">',
			'<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>',
			'',
		]))
		contents.insert(contents.index("</center>\n"), 
			f'<h1><span style="font-family: RuneScape UF Regular;color:yellow;">The Old School Runescape Universe</span> | <a href="https://github.com/Palfore/OSRSmath" target="_blank" style="font-size:50%;">by&nbsp;OSRSmath&nbsp;-&nbsp;Palfore</a> <a href="https://www.youtube.com/watch?v=yXP04J3Rc8g&ab_channel=Palfore" target="_blank" style="font-size:50%;">Explanation</a> <a href="https://www.youtube.com/watch?v=x90-35Bu2lo&t=38s&ab_channel=Palfore" target="_blank" style="font-size:50%;">Animation</a> </h1>'+"""
			<div class="w3-row-padding">
				<div class="w3-quarter">
					<button class="btn btn-info btn-lg" onclick="help()"><i class="bi bi-info-circle"></i></button>
					|
					<button class="btn btn-secondary" onclick="openWiki()" data-toggle="tooltip" title="Lookup the selected quest on the wiki.">Lookup</button>
                    <button class="btn btn-warning" style="color:white;" onclick="remove_selected()" data-toggle="tooltip" title="Completed the selected quest.">Complete</button>
				</div>
				<div class="w3-quarter">
					<select class="btn btn-primary" id="color_scheme" onchange="changeColor()" data-toggle="tooltip" title="Change the color scheme.">\n"""+
							'\n\t\t'.join(f"  <option value={option}>{option.replace('_', ' ').title()}</option>" for option in self.colors.keys() if option != 'background') + """
					</select>
					<label for="toggle_reverse" data-toggle="tooltip" title="Reverse the directions of the arrows.">Reverse</label>
                    <input type="checkbox" id="toggle_reverse" onclick="swapDirections()", class="btn btn-success" ></input>
                    
                    <label for="toggle_physics" data-toggle="tooltip" title="Turn the physics on.">Physics</label>
                    <input type="checkbox" id="toggle_physics" checked class="btn btn-light" style="color:white;background-color:orangered;"></input>
                    
                    <label for="show_names" data-toggle="tooltip" title="Show quest names.">Names</label>
                    <input type="checkbox" id="show_names" checked class="btn btn-light" style="color:white;background-color:orangered;"></input>
                    
                    <!--
                    <label for="toggle_tiered" data-toggle="tooltip" title="Diplay the quests in tiers.">Tiered</label>
                    //<input type="checkbox" id="toggle_tiered" class="btn btn-light" style="color:white;background-color:orangered;" onclick="toggle_tiered()" data-toggle="tooltip" title="Animate quests in order of release."></input>
                    -->
				</div>
				<div class="w3-quarter">
					<label for="quests_to_hide" data-toggle="tooltip" title="A list of quests that are completed.">Completed:</label>
					<input id="quests_to_hide" type="text" onfocusout="hideQuests()" data-toggle="tooltip" title="A list of quests that are completed.">
                    
                    <label for="toggle_completed" data-toggle="tooltip" title="Display or hide quests that are completed.">Hidden</label>
                    <input type="checkbox" id="toggle_completed" class="btn btn-light" style="color:white;background-color:orangered;" data-toggle="tooltip" title="Hide all quests."></input>

                    <label for="hide_all_quests" data-toggle="tooltip" title="Hide all quests.">Erase</label>
                    <button id="hide_all_quests" onclick=hide_all() class="btn btn-light" data-toggle="tooltip" title="Show or hide quests that are completed. Press ENTER in the complete box for this to register, then click on the webpage (not the graph) - need to fix."></button>
				</div>
				<div class="w3-quarter">
					<button class="btn btn-light" style="color:white;background-color:orangered;" onclick="animate_release()" data-toggle="tooltip" title="Animate quests in order of release.">Release</button>
					<button class="btn btn-light" style="color:white;background-color:orangered;" onclick="animate_quests(true)" data-toggle="tooltip" title="Animate the list of completed quests, by adding nodes.">+</button>
					<button class="btn btn-light" style="color:white;background-color:orangered;" onclick="animate_quests(false)" data-toggle="tooltip" title="Animate the list of completed quests, by removing nodes.">-</button>
					<input id="animation_speed" type="range" min="25" max="1000" value="500" class="slider" data-toggle="tooltip" title="The animation speed.">
				</div>
			</div>
		""")
		contents.insert(contents.index('<style type="text/css">\n')+1, f"""
			div.vis-network {{background-color: {self.colors['background']};}}
			body {{background-color: {self.colors['background']};}}
		""")
		contents.insert(contents.index("var options = {};\n")+1,
			f"var options = {self.options};".replace("True", "true").replace("False", "false")
		)
		contents.insert(contents.index("network = new vis.Network(container, data, options);\n")+1, 
			open('quest_view.js').read().\
				replace("COLORS", str(self.colors)).\
				replace("QUESTS_IN_ORDER", str(quests_by_release)).\
				replace("BACKGROUND_COLOR", f'''"{self.colors['background']}"''').\
				replace("HELP", "'"+str(
					'<ul style="text-align:left;">'+
	                '<li>To <b>View Quest Details</b>:<ul><li>Hover over a quest</li></ul></li>'+
	                '<li>To <b>Complete a Quest</b>:'+
	                        '<ul>'+
	                            '<li>Double click or hold it, or</li>'+
	                            '<li>Select it and press "Complete", or</li>'+
	                            '<li>Add the name to the completed quest list</li>'+
	                        '</ul>'+
	                    '</li>'+
	                '<li>To <b>Lookup a Quest</b> on the Wiki: <ul><li>Select a quest and press "Lookup"</li></ul></li>'+
	                '<li><b>Animations</b> can be stopped by double clicking on the background.</li>'+
	            '<ul>'+
	            "'",
			    )).\
				replace("True", "true").\
				replace("False", "false")
		)

		os.remove(temp_file)
		with open(file, "w") as f:
		    f.writelines(contents)
		if show:
			start = os.getcwd()
			try:
				os.chdir(pathlib.Path(file).parent)  # Apparently opening a "folder/file" path uses internet explorer?
				webbrowser.open(pathlib.Path(file).name)  # So split and cd, then open it.
			finally:
				os.chdir(start)


if __name__ == '__main__':
	qb = QuestBook.from_wiki_parser()
	colors = {
		'background': '#d8ccb4',

		'shell': ['black', 'indigo', 'blue', 'green', 'olive', 'yellow', 'orange', 'red'],
		'series': {s: c for s, c in zip(
			["Camelot", "Demon Slayer", "Dorgeshuun", "Dragonkin", "Elemental Workshop", "Elf", "Fairytale", "Fremennik", "Gnome", "Kharidian", "Great Kourend", "Mahjarrat", "Miscellania", "Myreque", "Order of Wizards", "Penguin", "Pirate", "Rag and Bone Man", "Red Axe", "Temple Knight", "Troll",],
			["#d3d3d3", "#556b2f", "#b22222", "#008000", "#008080", "#b8860b", "#9acd32", "#800080", "#ff0000", "#ffff00", "#7cfc00", "#9400d3", "#00fa9a", "#4169e1", "#00ffff", "#00bfff", "#0000ff", "#db7093", "#f0e68c", "#ff1493", "#ffa07a", "#ee82ee"]
		)},
		'difficulty': {
			"Novice": "green",
			"Intermediate": "gold",
			"Experienced": "orange",
			"Master": "red",
			"Grandmaster": "black",
			"Special": "blue",
		},
		'length': {
			"Very Short": "green",
			"Short": "yellow",
			"Medium": "orange",
			"Long": "red",
			"Very Long": "black",
		},
		'main_developer': {s: c for s, c in zip(list(set([node.developer[0] for node in qb])), ["#808080", "#c0c0c0", "#2f4f4f", "#556b2f", "#8b4513", "#228b22", "#7f0000", "#191970", "#808000", "#3cb371", "#b8860b", "#008b8b", "#d2691e", "#9acd32", "#cd5c5c", "#00008b", "#32cd32", "#8fbc8f", "#8b008b", "#b03060", "#9932cc", "#ff4500", "#ffa500", "#6a5acd", "#0000cd", "#00ff00", "#00fa9a", "#e9967a", "#dc143c", "#00ffff", "#adff2f", "#ff6347", "#da70d6", "#ff00ff", "#f0e68c", "#ffff54", "#6495ed", "#dda0dd", "#90ee90", "#afeeee", "#87cefa", "#7fffd4", "#ff69b4", "#ffe4c4", "#ffc0cb",])},
		'combat': {True: 'red', 'True': 'red', 'true': 'red'},
		'members': {True: 'red', 'True': 'red', 'true': 'red'},
		'year': {y: c for y, c in zip(
			list(reversed(sorted(list(set([int(node.released.split()[-1]) for node in qb]))))),
			["#04f2ff", "#12e4f0", "#19d6e1", "#1ec8d2", "#21bac3", "#23acb5", "#249fa7", "#259299", "#25858b", "#24787e", "#236b70", "#225f63", "#205357", "#1e474a", "#1b3c3e", "#183133", "#152627", "#111c1d", "#0a1112", "#000000"]
		)},
	}
	options = {
	  # "custom-background_color": background_color,
	  "configure": {
	    "enabled": False
	  },
	  "nodes": {
	    # "borderWidth": 10,
	    "borderWidthSelected": 50,
	    "font": {
	      "size": 60,
	      "strokeWidth": 11,
	      "strokeColor": colors['background'],
	    }
	  },
	  "edges": {
	    "arrows": {
	      "from": {
	        "enabled": False
	      },
	      "to": {
	        "enabled": True
	      }
	    },
	    "font": {
	      "size": 0, # Hide
	    },
	    "hoverWidth": 8,
	    "selectionWidth": 8,
	    "width": 4
	  },
	  "interaction": {
	    "hover": True,
	    "multiselect": False,
	    "navigationButtons": False,
	  },
	  "physics": {
	    "barnesHut": {
	      "gravitationalConstant": -13100,
	      "centralGravity": 0.5,
	      "springLength": 200+195
	    },
	    "stabilization": {
	    	"iterations": 400
	    },
	    "minVelocity": 0.35
	  }
	};


	player = Player.create_maxed()
	# player.quest_book.blocked.extend(player.quest_book.get_quests_with_level_req("Hitpoints", 10, "greater"))
	# for quest in player.quest_book.get_quests_with_level_req("Hitpoints", 10, "greater"):
	# 	player.quest_book.blocked.extend(player.quest_book[quest].unlocks)
	# player.quest_book.blocked.extend([q.name for q in player.quest_book if q.combat]) # block quest and anything that needs it.
	# for quest in [q.name for q in player.quest_book if q.combat]:
	# 	player.quest_book.blocked.extend(player.quest_book[quest].unlocks)
	QuestViewer(player, colors, options).save_graph(file="output/quest_viewer.html", show=True)
	QuestViewer(player, colors, options).save_pdf(True)
	QuestViewer(player, colors, options).save_pdf(False)
