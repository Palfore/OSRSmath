# Runescape Quest Visualizer

This package implements an interactive quest graph.

## Overview

- Quest.py: Models Skill, Skills, Quest, QuestBook, and Player
- Wiki_quest_parser.py: Implements WikiQuestParser for wiki web scraping.
	- There are two versions of this, one for OSRS and one for RS3.
- Quest_view: Implements the graph generation.

## Usage

1) To generate the data for new quests, simply run `python osrs_wiki_quest_parser.py --overwrite` and `python rs3_wiki_quest_parser.py --overwrite`.
2) Then to generate the HTML rendering, simply run `python quest_view.py --osrs` and `python quest_view.py --rs3` to compile the both osrs and rs3 graphs.
- The output files are "by_quest.pdf", "by_requirement.pdf", and "quest_viewer.html" for each game.
- Note: To host quest_viewer.html, you could replace the javascript contents of the `<script>` tag with [a minified version](https://www.toptal.com/developers/javascript-minifier)- Please note that the output files are generated, so modifications may get deleted, instead modify the generating code or template.js files.

## Next Steps

- Map of Gielinor, pin quests are start locations.
- Extract the javascript code from the single file into its own .js file. Automate the minify through post request.
- See if the json can be extracted and loaded with fetch. Currently, the json has `"title: htmlTitle(...)"`, so it needs to be processed further to do this.

