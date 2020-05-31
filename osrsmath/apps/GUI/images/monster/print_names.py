from pathlib import Path
for path in Path('.').rglob('*.webp'):
	path = str(path).replace('.webp', '')
	print(f'<file alias="{path}.png">images/skill_icons/{path}.webp</file>')