# The Mathematics and Optimization of OSRS

The purpose of this project is to model the game mechanics of [Old School Runescape](https://oldschool.runescape.com/) for the purpose of optimizing player decisions or analyzing game play. This game is played over long periods of time (months or years) and so players are often seeking the most optimal route to their desired accomplishments. Combat is a particularly rewarding application since it has many layers. This project is currently in progress, so if you notice anything please feel free to open a ticket or join the discord and let me know!

If you're interested, you can join the [discord](https://discord.gg/4SXcKQh) to discuss anything! Or if you would prefer watching a video, you can checkout the [video series](https://www.youtube.com/watch?v=7N9UJX70Z5I&list=PLm3INE_scU5s8NQWmw0fxKtA_6SVxDOc7).

There are three components to this project:

### 1. Applications

These applications provide useful functionalities for players (a.k.a. end users). Once installed, they can be run using the command: `python -m [Module Location]`.
Note: The combat code/app is currently being rewritten (after an exploration phase), the `pip` library won't be updated until the app is working again. You can still install the old version using the latest version of the `pip` libary. In the meantime, download the codebase to explore other code like firemaking. Some of the following instructions may be out of date.

| Application        | Module Location           | Description  |
| ------------- |:-------------:| :-----|
| Optimize | `osrsmath.apps.optimize` | What is the most efficient equipment to wear when fighting a given opponent? |
| Wintertodt | `osrsmath.firemaking.wintertodt` | How many kills are required to reach a given firemaking level? |

[//]: # (| Path | `osrsmath.apps.path` | What is the most mathematically efficient way to get from a set of starting attack, strength, and defence levels, to a final set of levels? This is currently not user-friendly. |)

![The optimize app.](https://github.com/Palfore/OSRSmath/blob/master/osrsmath/apps/optimize/images/interface.png "The optimize app.")

### 2. Library

For developers, they can use the basic functionalities to build their own applications. The code is available on [PyPi](https://pypi.org/project/osrsmath/), and can be installed using `pip3 install osrsmath`. Within their own code the can import functionalities using `import osrsmath.[module_of_interest]`. Download the source, and check out the documentation for the modules at `OSRSmath/osrsmath/docs/html/osrsmath/index.html` to see what can be done.

### 3. Documentation

Documentation doesn't really exist regarding the math behind osrs. This project aims to provide a [document](https://github.com/Palfore/OSRSmath/blob/master/osrsmath/docs/latex/main.pdf) that attempts to fill this gap. This project also documents its source code (mostly), which can be viewed by downloading the source and navigating to `osrsmath/docs/html/osrsmath/index.html`. In future, it would be nice to host this online.

## Installing

### User

This application was written in the programming language [`Python`](https://www.python.org/), which has two major version. `python3` is the version used here, more specifically any version greater than `3.6.3` should work (the latest is best). 

1. To install `Python` simply visit the [download page](https://www.python.org/downloads/).
2. Once it is installed, open a terminal (MacOS/Linux) or command prompt (Windows). 
3. Type the command `pip3 install --upgrade pip` then `pip3 install osrsmath` to install this program.
4. Then type `python3 -m osrsmath.apps.[app_name]` to run an application. For example, replace `[app_name]` with `optimize` to run the optimize application.

### Developer
1. Open a terminal/command prompt.
2. Make sure you have `python3.6+` installed (type `python --version`)
3. Make sure `pip3` is installed (type `pip3 --version`).
4. Update pip `pip3 install --upgrade pip`
5. Update setuptools `pip3 install --upgrade setuptools`

To install the apps, or to use as a library:
1. `pip3 install osrsmath`

To develop the code:
1. Download the github source code, unzip it and place it anywhere.
2. Open a terminal in that directory (which contains setup.py).
3. Run `pip3 install -e .`

Run the desired application with: `python3 -m osrsmath.apps.[app_name]`. Linux may require `sudo apt-get install python3-pyqt5`

These installation methods have been tested on:
	`Ubuntu 20.04` (using [wsl1](https://docs.microsoft.com/en-us/windows/wsl/about) on windows),
	`MacOS` (Catalina 15.15.5),
	and
	`Windows 10` (v1909)

## Developing

### GUI Development:
These are instructions for creating & modifying the GUI design:
1. Use [QT designer](https://build-system.fman.io/qt-designer-download).
2. Create or modify a `.ui` file in QT designer.
3. Run `python -m osrsmath.apps.GUI.shared.util make` to compile them.

### Documentation
To compile the latex documents a latex compiler needs to be installed. [MiKTeX](https://miktex.org/download) is a good cross-platform option. Alternatively, on linux you could simply type `sudo apt-get install texlive-full`.

The central document can be compiled with `pdflatex main.tex`.
The html documentation uses [`pdoc3`](https://pypi.org/project/pdoc3/) which can be installed with `pip3 install pdoc3`. Then the documentation can be compiled by naviating to the top directory (containing `setup.py`) and type:
	
	pdoc --html osrsmath -o osrsmath/docs/html -c latex_math=True --force
	python osrsmath/docs/compile.py


### Tests

The `unittest` module is used for testing. Navigate to the `tests` directory and run the command `python3 -m unittest`. The tests are currently out of date, and are being re-written. If anyone is knowledgeable about combat game mechanics (max hit & accuracy calculations, tick manipulation), feel free to message me as I'm not too familiar and would appreciate the help.

## Authors

* **Nawar Ismail** - [Palfore](https://www.palfore.com/)

If you are interested in contributing, check out the [issues section](https://github.com/Palfore/OSRSmath/issues) on GitHub or join the Discord.

<!-- See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project. -->

## License

This open-source project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 

## Acknowledgments
### Code

* [osrsbox](https://pypi.org/project/osrsbox/) - Provides Data files
* [dijkstar](https://pypi.org/project/Dijkstar/) - Implements the Dijkstra Algorithm in Python

### Knowledge
* [OSRSBox melee dps](https://www.osrsbox.com/blog/2019/01/22/calculating-melee-dps-in-osrs/)
* [DPS Calculator by Bitterkoekje](https://docs.google.com/spreadsheets/d/1wzy1VxNWEAAc0FQyDAdpiFggAfn5U6RGPp2CisAHZW8/)
* [Forum Post by Bitterkoekje](https://web.archive.org/web/20190905124128/http://webcache.googleusercontent.com/search?q=cache:http://services.runescape.com/m=forum/forums.ws?317,318,712,65587452)
* [Overkill by Nukelawe](https://www.reddit.com/r/2007scape/comments/4d6l7j/effects_of_overkill_on_dps/)
* [Accuracy & Xp Rate Discussion by MachOSRS](https://www.reddit.com/r/2007scape/comments/40bvk6/accuracy_and_exphr_combat_formula/)
* [Accuracy Discussion](https://www.reddit.com/r/2007scape/comments/5lrty0/math_inside_corrected_accuracy_formula/)
