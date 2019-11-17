# The Mathematics and Optimization of OSRS Combat
## Purpose
	The purpose of this project is to accurately model [https://oldschool.runescape.com/](Old School Runescape) combat. This game is played over long periods of time (months or years) and so players are often seeking the most optimal route to their desired accomplishments. Many attempts have been made to model combat, but certain details and high level treatment are often omitted. In addition to this, the tools have been built by the community, however they focus on ease of access, which limits their ability to solve more complex tasks. An common example of this, letting players compare two sets of gear, but not saying ``this is the optimal setup''. This project aims to solve by of these by using a relatively high level mathematical description coupled with a clear and powerful codebase.

## Technologies
	The document is written in Latex, and the code is written in Python 3.6. There are no external dependencies so far.

## Usage
	Several files have a main function which typically generates some figure, or numbers used in the text. There is no primary ``start'' at this point. Although often omitted from naming, most functionalities are calculating expected values.