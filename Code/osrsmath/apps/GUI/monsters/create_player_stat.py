''' This is a one-time file to create the base xml for the player stats widget. '''

if __name__ == '__main__':
  basic = lambda r, c, skill: f"""\
     <item row="{r}" column="{2*c}">
      <widget class="QLabel" name="label_{skill}">
       <property name="text">
        <string/>
       </property>
       <property name="pixmap">
        <pixmap>../images/skill_icons/{skill.capitalize()}.png</pixmap>
       </property>
       <property name="alignment">
        <set>Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter</set>
       </property>
      </widget>
     </item>
     <item row="{r}" column="{2*c+1}">
      <widget class="QLineEdit" name="{skill}"/>
     </item>

  """

  skills = [
    ['attack', 'hitpoints', 'mining'],
    ['strength', 'agility', 'smithing'],
    ['defence', 'herblore', 'fishing'],
    ['ranged', 'thieving', 'cooking'],
    ['prayer', 'crafting', 'firemaking'],
    ['magic', 'fletching', 'woodcutting'],
    ['runecraft', 'slayer', 'farming'],
    ['construction', 'hunter'],
  ]


  new_text = []
  starting = '<layout class="QGridLayout" name="gridLayout">'
  ending = '</layout>'
  reading = False
  for line in open('player_stats.ui'):
    if (not reading) and (line.strip() == starting):
      reading = True
      new_text.append(line)
      for i in range(len(skills)):
        for j, skill in enumerate(skills[i]):
          new_text.append(basic(i, j, skills[i][j]))

    if line.strip() == ending:
      reading = False



    if not reading:
      new_text.append(line)

  with open('test.ui', 'w') as f:
    f.writelines(new_text)


