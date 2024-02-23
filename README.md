# The Mathematics and Optimization of OSRS

The purpose of this project is to study the game mechanics of [Old School Runescape](https://oldschool.runescape.com/) to optimize player decisions and analyze game play. This game is played over long periods of time (months or years) and so players are often seeking the most optimal route to their desired accomplishments. The central focus is the combat system since it is particularly interesting. This project is currently in progress, so things are likely to be wip or quick work.

If you are looking for more content please consider these:
##### a) You can check out the [Runescape Universe Interactive Visualization](https://osrsmath.palfore.com/) of all the quests.
1. See Acknowledgements below for the [community progress on this](https://github.com/Palfore/OSRSmath?tab=readme-ov-file#quest-tree).

##### b) You can also check out these reddit posts:
1. [A Physicist's Guide to Re-balancing Combat - Damage Distributions (3.4k upvotes)](https://www.reddit.com/r/2007scape/comments/mwvjzc/a_physicists_guide_to_rebalancing_combat_damage/)
2. [I made a "Quest Tree" for OSRS (1.1k upvotes)](https://www.reddit.com/r/2007scape/comments/kbu6a8/mathematical_model_of_wintertodt_time_to_99/)
3. [Mathematical Model of Wintertodt & Time to 99 (~450 upvotes)](https://www.reddit.com/r/2007scape/comments/kbu6a8/mathematical_model_of_wintertodt_time_to_99/)
4. [Mathematically Optimal Order to Train Melee Combat (~350 upvotes)](https://www.reddit.com/r/2007scape/comments/ffctp0/mathematically_optimal_order_to_train_melee_combat/)
5. [The Mathematics of OSRS Combat (~50 upvotes)](https://www.reddit.com/r/2007scape/comments/faz5et/the_mathematics_of_osrs_combat/)

##### c) You can watch the [Video Series](https://www.youtube.com/watch?v=7N9UJX70Z5I&list=PLm3INE_scU5s8NQWmw0fxKtA_6SVxDOc7) if you would prefer watching a video.

##### d) You can join the [Discord](https://discord.gg/4SXcKQh) to discuss anything! 

##### e) You can read the [Mathematical Solutions (pdf/Latex)](https://github.com/Palfore/OSRSmath/blob/master/osrsmath/docs/latex/main.pdf) if you want more detail. 

##### f) You can see more on the OSRSmath page on [My Website](https://palfore.com/).

There are three components to this project:

### 1. Applications

These applications provide useful functionalities for players. Once installed, they can be run using the command: `python -m [Module Location]`. 

| Application        | Module Location           | Description  |
| ------------- |:-------------:| :-----|
| Optimize | `osrsmath.apps.optimize` | (Currently disabled) What is the most efficient equipment to wear when fighting a given opponent? |
| Wintertodt | `osrsmath.firemaking.wintertodt` | How many kills are required to reach a given firemaking level? |

[//]: # (| Path | `osrsmath.apps.path` | What is the most mathematically efficient way to get from a set of starting attack, strength, and defence levels, to a final set of levels? This is currently not user-friendly. |)

![The optimize app.](https://github.com/Palfore/OSRSmath/blob/master/osrsmath/apps/optimize/images/interface.png "The optimize app.")

### 2. Library

For developers, they can use the basic functionalities to build their own applications. The code is available on [PyPi](https://pypi.org/project/osrsmath/), and can be installed using `pip3 install osrsmath`. Within their own code the can import functionalities using `import osrsmath.[module_of_interest]`. Download the source, and check out the documentation for the modules at `OSRSmath/osrsmath/docs/html/osrsmath/index.html` to see what can be done.

### 3. Documentation

Documentation doesn't really exist regarding the math behind osrs. This project aims to provide a [document](https://github.com/Palfore/OSRSmath/blob/master/osrsmath/docs/latex/main.pdf) that attempts to fill this gap.

## Installing

### User

This application was written in the programming language [`Python`](https://www.python.org/), which has two major version. `python3` is the version used here, more specifically any version greater than `3.6.3` should work (the latest is best). The pip library is outdated and might not have all the features.

1. To install `Python` simply visit the [download page](https://www.python.org/downloads/).
2. Once it is installed, open a terminal (MacOS/Linux) or command prompt (Windows). 
3. Type the command `pip3 install --upgrade pip` then `pip3 install osrsmath` to install this program.
4. Then type `python3 -m osrsmath.apps.[app_name]` to run an application. For example, replace `[app_name]` with `optimize` to run the optimize application.

### Developer

1. Download the github source code, unzip it, and place it anywhere.
2. Open a terminal in that directory (which contains setup.py).
3. Make sure pip is Run `pip3 install -e .`

### GUI Development:
These are instructions for creating & modifying the graphical interface in the apps:

1. Use [QT designer](https://build-system.fman.io/qt-designer-download).
2. Create or modify a `.ui` file in QT designer.
3. Run `python -m osrsmath.apps.GUI.shared.util make` to compile them.

Linux may require `sudo apt-get install python3-pyqt5`

### Documentation
To compile the latex document a latex compiler needs to be installed. [MiKTeX](https://miktex.org/download) is a good cross-platform option. Alternatively, on linux you could simply type `sudo apt-get install texlive-full`. The central document can be compiled with `pdflatex main.tex`.

### Tests

The `unittest` module is used for testing. Navigate to the `tests` directory and run the command `python3 -m unittest`. If you are knowledgeable about combat game mechanics (max hit & accuracy calculations, tick manipulation, etc), and you are interested consider joining the discord to help out with tests/validation.

## Authors

* **Nawar Ismail** - [Palfore](https://www.palfore.com/)

If you are interested in contributing, check out the [issues section](https://github.com/Palfore/OSRSmath/issues) on GitHub or join the Discord.

## License

This open-source project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 

## Acknowledgments
### Code

* [osrsbox](https://pypi.org/project/osrsbox/) - Provides Data files
* [dijkstar](https://pypi.org/project/Dijkstar/) - Implements Dijkstra's Algorithm in Python

### Knowledge

#### Combat
* [OSRSBox melee dps](https://www.osrsbox.com/blog/2019/01/22/calculating-melee-dps-in-osrs/)
* [DPS Calculator by Bitterkoekje](https://docs.google.com/spreadsheets/d/1wzy1VxNWEAAc0FQyDAdpiFggAfn5U6RGPp2CisAHZW8/)
* [Forum Post by Bitterkoekje](https://web.archive.org/web/20190905124128/http://webcache.googleusercontent.com/search?q=cache:http://services.runescape.com/m=forum/forums.ws?317,318,712,65587452)
* [Overkill by Nukelawe](https://www.reddit.com/r/2007scape/comments/4d6l7j/effects_of_overkill_on_dps/)
* [Accuracy & Xp Rate Discussion by MachOSRS](https://www.reddit.com/r/2007scape/comments/40bvk6/accuracy_and_exphr_combat_formula/)
* [Accuracy Discussion](https://www.reddit.com/r/2007scape/comments/5lrty0/math_inside_corrected_accuracy_formula/)

#### Quest Tree
* [(2015) I made a graph of how all ...](https://www.reddit.com/r/2007scape/comments/3aj2vj/i_made_a_graph_of_how_all_of_the_quests_in/)
* [(2017) My Map of all Runescape's Quests](https://www.reddit.com/r/runescape/comments/5ekds7/my_map_of_all_runescapes_quests/)
* [(2019) Quest progression tree](https://www.reddit.com/r/runescape/comments/akpq6k/quest_progression_tree/)
* [(2020) Interactive network of all OSRS quests](https://i.imgur.com/EpvGKZ4.png)
* [(2021) I made a "Quest Tree" for OSRS](https://www.reddit.com/r/2007scape/comments/loa4uw/i_made_a_quest_tree_for_osrs/)
* [(2024) New Interactive Quest Visualizer OSRS](https://www.reddit.com/r/2007scape/comments/1ay2opj/new_interactive_quest_visualizer_osrs_the/)

  
