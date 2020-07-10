# The Mathematics and Optimization of OSRS

The purpose of this project is to accurately model [Old School Runescape](https://oldschool.runescape.com/) mechanics in order to optimize or analyze game play. This game is played over long periods of time (months or years) and so players are often seeking the most optimal route to their desired accomplishments. In particular, combat is a particularly rewarding application, as very complex problems that were previously unsolved for decades can now be.

If you're interested, you can join the [discord](https://discord.gg/4SXcKQh) to discuss anything!

There are three components to this project:

### 1. Applications

These application provide useful functionalities for end users. Once installed, they can be run using the command: `python -m [Module Location]`.

| Application        | Module Location           | Description  |
| ------------- |:-------------:| :-----|
| Optimize | `osrsmath.apps.optimize.main` | What is the most efficient equipment to wear when fighting a given opponent? |

[//]: # (| Path | `osrsmath.apps.path.main` | What is the most mathematically efficient way to get from a set of starting attack, strength, and defence levels, to a final set of levels? This is currently not user-friendly. |)

![The optimize app.](https://github.com/Palfore/OSRSmath/blob/master/osrsmath/apps/optimize/images/interface.png "The optimize app.")

### 2. Library

For developers, they can use the basic functionalities (like modeling combat or potion boosts) to build their own applications. The code is available on [PyPi](https://pypi.org/project/osrsmath/), and can be installed using `pip3 install osrsmath`. Within their own code the can import functionalities using `import osrsmath.[module_of_interest]`. Download the source, and check out the documentation for the modules at `OSRSmath/osrsmath/docs/html/osrsmath/index.html` to see what can be done.

### 3. Documentation

Coherent and comprehensive documentation doesn't really exist regarding the math behind osrs. This project provides a [document](https://github.com/Palfore/OSRSmath/blob/master/osrsmath/docs/latex/main.pdf) that attempts to fill this gap. It also documents its source code, which can be viewed by downloading the source and navigating to `osrsmath/docs/html/osrsmath/index.html`. In future, it would be nice to host this online.

## Installing

### User

This application was written in the programming language [`Python`](https://www.python.org/), which has two major version. `python3` is the version used here, more specifically any version greater than `3.6.3` should work (the latest is best). 

1. To install `Python` simply visit the [download page](https://www.python.org/downloads/).
2. Once it is installed, open a terminal (MacOS/Linux) or command prompt (Windows). 
3. Type the command `pip3 install --upgrade pip` then `pip3 install osrsmath` to install this program.
4. Then type `python3 -m osrsmath.apps.[app_name].main` to run an application. For example, replace `[app_name]` with `optimize` to run the optimize application.

You might also consider trying the executables directly, although there are currently installation issues, particularly on MacOS so this isn't currently recommended. To do this, navigate to [GitHub releases](https://github.com/Palfore/OSRSmath/releases) and download the latest version (Asset) for your system. Unzip, and run!

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

Run the desired application with: `python3 -m osrsmath.apps.[app_name].main`. Linux may require `sudo apt-get install python3-pyqt5`

These installation methods have been tested on:
	`Ubuntu 20.04` (using [wsl1](https://docs.microsoft.com/en-us/windows/wsl/about) on windows),
	`MacOS` (Catalina 15.15.5),
	and
	`Windows 10` (v1909)

## Developing
### Packaging:
These are instructions for creating app executables:
1. Type `pip3 install PyInstaller`
2. On MacOS, `python<=3.6.3` is required since PyInstaller on macos isn't supported after that.
   On Windows, the app store version of Python (3.8) doesn't work.
3. Navigate to the `Application` folder of the app you want to create an executable for.
4. Type `python3 package.py`.
5. Symbolic links should then be created to `dist/main/main[.exe]`, the should be named osrsmath-[app_name].

On MacOS, the application has to be signed. I don't know the Mac ecosystem very well, however these websites helped me:
1. https://github.com/pyinstaller/pyinstaller/wiki/Recipe-OSX-Code-Signing
2. https://stackoverflow.com/questions/16845169/error-when-trying-to-obtain-a-certificate-the-specified-item-could-not-be-found
3. https://apple.stackexchange.com/questions/254380/why-am-i-getting-an-invalid-active-developer-path-when-attempting-to-use-git-a

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

The `unittest` module is used for testing. Navigate to the `tests` directory and run the command `python3 -m unittest`

## Authors

* **Nawar Ismail** - [Palfore](https://www.palfore.com/)

If you are interested in contributing, check out the [issues section](https://github.com/Palfore/OSRSmath/issues) on GitHub.

<!-- See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project. -->

## License

This open-source project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 

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
