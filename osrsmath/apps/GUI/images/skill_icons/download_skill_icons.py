from osrsmath.general.skills import get_skills
import requests
from pprint import pprint

def download(url, filename):
	r = requests.get(url)
	with open(filename, 'wb') as f:
	    f.write(r.content)

def parse_html_link(html):
	start_of_line_with_link = '<li><a href="#filelinks">File usage</a></li></ul><div class="fullImageLink" id="file"><a href="'
	end_of_line_with_link = '"><img alt="'
	for line in html.split('\n'):
		line = line.strip('\t')
		if start_of_line_with_link in line:
			line = line.replace(start_of_line_with_link, '')
			line = line.split(end_of_line_with_link, 1)[0]
			return 'https://oldschool.runescape.wiki/' + line

	raise ValueError("Could not parse html for image link.")

def download_skill_icon(skill):
	url = f'https://oldschool.runescape.wiki/w/File:{skill.capitalize()}_icon.png'
	link_url = parse_html_link(requests.get(url).text)
	download(link_url, f'{skill}.png')


if __name__ == '__main__':
	skills = get_skills()
	for i, skill in enumerate(skills, 1):
		print(f'<file alias="{skill}.png">images/skill_icons/{skill}.png</file>')
		#print(f'Downloading {skill} Icon... ({i}/{len(skills)} - {100*i/len(skills):.1f}%)')
		#download_skill_icon(skill)


