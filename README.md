# The Mathematics and Optimization of OSRS

The purpose of this project is to accurately model [Old School Runescape](https://oldschool.runescape.com/) mechanics in order to optimize or analyze game play. This game is played over long periods of time (months or years) and so players are often seeking the most optimal route to their desired accomplishments. In particular, combat is a particularly rewarding application, as very complex problems that were previously unsolved for decades can now be.

There are three components to this project:

### 1. Applications

These application provide useful functionalities for end users. Once installed, they can be run using the command: `python -m [Module Location]`.

| Application        | Module Location           | Description  |
| ------------- |:-------------:| :-----|
| Path | `osrsmath.apps.path.main` | What is the most mathematically efficient way to get from a set of starting attack, strength, and defence levels, to a final set of levels? This is currently not user-friendly. |
| Optimize | `osrsmath.apps.optimize.main` | What is the most efficient equipment to wear when fighting a given opponent? |


### 2. Library

For developers, they can use the basic functionalities (like modeling combat or potion boosts) to build their own applications. Within their own code the can import functionalities using `import osrsmath.model.[module_of_interest]`. Check out a [list of modules](https://github.com/Palfore/OSRSmath/osrsmath/docs/html/osrsmath/model/index.html) to see what can be done.

### 3. Documentation

Coherent and comprehensive documentation doesn't really exist regarding the math behind osrs. This project provides a [document](https://github.com/Palfore/OSRSmath/osrsmath/docs/latex/main.pdf) that attempts to fill this gap.

## Installing
There are two methods. The **User** method is the easiest - but if it doesn't work please let me know and you can use the **Developer** instructions instead, which should still be easy to follow.

### User
This has been tested on:
	`Ubuntu 20.04` (using [wsl1](https://docs.microsoft.com/en-us/windows/wsl/about) on windows),
	`MacOS` (Catalina 15.15.5),
	`Windows 10` (v1909)

Navigate to [FILL IN THIS LINK] and download the executables.

### Developer
Open a terminal/command prompt.
Make sure you have `python3.6+` installed (type `python --version`)
Make sure `pip3` is installed (type `pip3 --version`).
Update pip `pip3 install --upgrade pip`
Update setuptools `pip3 install --upgrade setuptools`

To install the apps, or to use as a library:
	`pip3 install osrsmath`

To develop the code:
	Download the github source code, unzip it and place it anywhere.
	Open a terminal in that directory (which contains setup.py).
	Run `pip3 install -e .`

Run the desired application with: `python3 -m osrsmath.apps.[app_name].main`. Linux may require `sudo apt-get install python3-pyqt5`

## Developing
### Packaging:
These are instructions for creating app executables:
1. Type `pip3 install PyInstaller`
2. On MacOS, `python<=3.6.3` is required since PyInstaller on macos isn't supported after that.
   On Windows, the app store version of Python (3.8) doesn't work.
3. Navigate to the `Application` folder of the app you want to create an executable for.
4. Type `python3 package.py`.

### GUI Development:
These are instructions for creating & modifying the GUI design:
1. Use [QT designer](https://build-system.fman.io/qt-designer-download).
2. Create or modify a `.ui` file in QT designer.
3. Run `python -m osrsmath.apps.GUI.shared.util make` to compile them.

### Latex
To compile the latex documents a latex compiler needs to be installed. [MiKTeX](https://miktex.org/download) is a good cross-platform option. Alternatively, on linux you could simply type `sudo apt-get install texlive-full`.

The central document can be compiled with `pdflatex main.tex`.
The html documentation uses [`pdoc3`](https://pypi.org/project/pdoc3/) which can be installed with `pip3 install pdoc3`. Then the documentation can be compiled by naviating to the top directory (containing `setup.py`) and type:
	
	pdoc --html osrsmath -o osrsmath/docs/html -c latex_math=True --force
	python osrsmath/docs/compile.py


### Tests

The `unittest` module is used for testing. Navigate to the `tests` directory and run the command `python3 -m unittest`

## Authors

* **Nawar Ismail** - [Palfore](https://github.com/Palfore)

If you are interested in contributing, here is a good list of tasks:

Beginner:
* Update and add testing code.
* Add documentation
* Model simpler problems like:
	* [Barbarian fishing](https://oldschool.runescape.wiki/w/Barbarian_Training#Barbarian_Fishing)
	* [Prospector kit order](https://oldschool.runescape.wiki/w/Prospector_kit#Cheap_first)
* Add contributions to the [Wiki](https://oldschool.runescape.wiki/)


Advanced:
* Refactor `player.py` and `monster.py` code.
* Add range & mage support to `apps.optimize`.
* Solve advanced problems:
	* Loop `apps.optimize` over all monsters to find best monster to fight!
	* Add opponent damage to `apps.optimize`, so that your defences matter and optimize that.

<!-- See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project. -->

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments
### Code

* [osrsbox](https://pypi.org/project/osrsbox/) - Provides Data files
* [dijkstar](https://pypi.org/project/Dijkstar/) - Implements the dijkstra Algorithm

### Knowledge
* [OSRSBox melee dps](https://www.osrsbox.com/blog/2019/01/22/calculating-melee-dps-in-osrs/)
* [DPS Calculator by Bitterkoekje](https://docs.google.com/spreadsheets/d/1wzy1VxNWEAAc0FQyDAdpiFggAfn5U6RGPp2CisAHZW8/)
* [Forum Post by Bitterkoekje](https://web.archive.org/web/20190905124128/http://webcache.googleusercontent.com/search?q=cache:http://services.runescape.com/m=forum/forums.ws?317,318,712,65587452)
* [Overkill by Nukelawe](https://www.reddit.com/r/2007scape/comments/4d6l7j/effects_of_overkill_on_dps/)
* [Accuracy & Xp Rate Discussion by MachOSRS](https://www.reddit.com/r/2007scape/comments/40bvk6/accuracy_and_exphr_combat_formula/)
* [Accuracy Discussion](https://www.reddit.com/r/2007scape/comments/5lrty0/math_inside_corrected_accuracy_formula/)
