# Runescape Quest Visualizer

This package implements an interactive quest graph.

## Overview

- Quest.py: Models Skill, Skills, Quest, QuestBook, and Player
- Wiki_quest_parser.py: Implements WikiQuestParser for wiki web scraping.
	- There are two versions of this, one for OSRS and one for RS3.
- Quest_view: Implements the graph generation.

## Usage

- To use this implementation run `python quest_view.py`, which will generate the output files. Add the flag `--rs3` to compile the runescape3 graph instead of the osrs graph.
- The output files are "by_quest.pdf", "by_requirement.pdf", and "quest_viewer.html".
- To host quest_viewer.html, you should replace the javascript contents of the `<script>` tag with [a minified version](https://www.toptal.com/developers/javascript-minifier). Please note that this file is generated, so modifications may get deleted, instead modify the generating code or template.js files.

## Next Steps

- RS3 Wiki Parser
- Map of Gielinor, pin quests are start locations.
- Extract the javascript code from the single file into its own .js file. Automate the minify through post request.
- See if the json can be extracted and loaded with fetch. Currently, the json has `"title: htmlTitle(...)"`, so it needs to be processed further to do this.

