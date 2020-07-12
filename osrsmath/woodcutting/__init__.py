""" This module contains code that models and optimizes the woodcutting skill.

Assumptions:
	1. There is a 1 in x possibility that a tree is cut down, where x depends on the tree, and x=8 is typical. 
		Each tree then has a respawn timer. This will be ignored, which means wherever the player chooses to 
		woodcut, there will be a negligible distance between trees.

	2. Banking/dropping time is constant regardless of the tree.

	3. No tick manipulation.

	4. Linear interpolations are not floored.

	5. No boosts like dragon axe, lumberjack outfit, woodcutting guild, kandarin headgear 2+

	6. Player equips the axe. This doesn't play a role now, but may in future since it reduces the inventory
	    size from 28 to 27. 

	7. The estimates for higher level trees are sufficient.


Information:
	Axes has progressive improvements:
		Bronze: Base
		Iron: 2x
		Steel: 1.5x
		...
		Dragon: ...

	Every 4 game ticks (2.4s), a roll is made to determine if a log is obtained.
	The roll depends on the tree, axe, and woodcutting level.
	There is a (theoretical) level 1 probability, and a level 99 probability. Levels in between are linearly interpolated.
	Call this $r_1$ and $r_{99}$, then r_{n} = (r_{99} - r_{1}) / 98 * n + r_{1} ## This is a placeholder equation and incorrect.
	Let r^{axe_type} = (r^{axe_type}_1, r^{axe_type}_{99}).
	It's possible that flooring plays a role, however assumption 4 ignores this.

	The only known rates are a teak log with a dragon axe r^{dragon} = (60, 190)/255.
	We can use the axe progressions to determine teak efficiency at any level, with any axe.
	The other probabilities will have to be estimated.

Items/Boosts:
	Lumberjack
	Maple tree + diary.
	Dragon/crystal axe special





"""