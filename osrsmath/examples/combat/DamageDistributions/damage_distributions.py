from osrsmath.skills.combat.distributions import *
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
import matplotlib.image as mpimg

def plt_dscim():

	plt.rcParams.update({'font.size': 18})
	# c = scythe(10, 0.6)
	c = standard(7, 0.85)
	total = sum(c.values())
	c = {x: y/total for x, y in c.items()}
	avg = 0
	for d, p in c.items():
		print(d, p)
		avg += d*p

	# print(max(c.keys()), avg, c[0])
	# exit()


	miss = c[0]
	del c[0]
	linewidth=0
	plt.yticks([])
	plt.xticks([0, max(c.keys())], ['0', '$m$'])
	plt.ylabel("Probability", fontweight='bold')
	plt.xlabel("Damage", fontweight='bold')
	

	plt.bar(0, miss, width=1, color='lightcoral')
	plt.bar(0, c[1], width=1, color='limegreen')
	plt.bar(list(map(int, c.keys())), list(c.values()), width=1.1, color='limegreen', linewidth=0)
	# plt.bar(0, miss, width=1, color='none', edgecolor="black", linewidth=4)
	
	plt.text(0, (miss + c[1])/2, "Miss", horizontalalignment='center', fontstyle='italic')
	plt.text(max(c.keys())/2, c[1]/2, "Successful Hit", horizontalalignment='center', fontstyle='italic')
	
	plt.gca().add_patch(Rectangle((-0.5, c[1]), 1, miss - c[1], fill=False, linewidth=4, edgecolor='red'))
	plt.gca().add_patch(Rectangle((-0.5, 0), max(c.keys())+1, c[1], fill=False, linewidth=4, edgecolor='green'))


	arr_lena = mpimg.imread('Dragon_scimitar_detail.png')
	imagebox = OffsetImage(arr_lena, zoom=0.07)
	ab = AnnotationBbox(imagebox, (max(c.keys()) - 0.5, 0.9*miss), frameon=False)
	plt.gca().add_artist(ab)

	plt.gca().spines['right'].set_visible(False)
	plt.gca().spines['top'].set_visible(False)
	plt.gca().spines['left'].set_linewidth(4)
	plt.gca().spines['bottom'].set_linewidth(4)

	# plt.autoscale(enable=True, axis='x', tight=True)
	# plt.gca().set_xlim(left=0.5)

	plt.gca().annotate('▲', (avg, 0), color='yellow')

	plt.rcParams['axes.xmargin'] = 0
	plt.tight_layout()
	plt.savefig('dscim.pdf')
	



def plt_weapon(name, weapon_function):
	plt.cla()
	plt.rcParams.update({'font.size': 18})
	# c = scythe(10, 0.6)
	c = weapon_function(7, 0.95)
	
	total = sum(c.values())
	c = {x: y/total for x, y in c.items()}
	avg = 0
	for d, p in c.items():
		print(d, p)
		avg += d*p
	print('>', avg, max(c.keys()))

	x = list(c.keys())
	y = list(c.values())



	plt.yticks([])
	plt.xticks([0, max(c.keys())], ['0', '$m$'])
	plt.ylabel("Probability", fontweight='bold')
	plt.xlabel("Damage", fontweight='bold')
	# plt.ylim(bottom=0, top=plt.ylim()[1])

	xs = [x[0] - 0.5]
	ys = [0]
	for i in range(len(x)):
	    xs.append(x[i] - 0.5)
	    xs.append(x[i] + 0.5)
	    ys.append(y[i])
	    ys.append(y[i])
	xs.append(x[-1] + 0.5)
	ys.append(0)
	plt.plot(xs, ys, color='blue', linewidth=4)
	# optionally color the area below the curve
	plt.fill_between(xs, 0, ys, color='royalblue')


	arr_lena = mpimg.imread(f"icon_{name}.png")
	imagebox = OffsetImage(arr_lena, zoom=0.14)
	ab = AnnotationBbox(imagebox, (max(c.keys()) - 2, 0.8*max(c.values())), frameon=False)
	plt.gca().add_artist(ab)
	
	plt.gca().spines['right'].set_visible(False)
	plt.gca().spines['top'].set_visible(False)
	plt.gca().spines['left'].set_linewidth(4)
	plt.gca().spines['bottom'].set_linewidth(4)
	# plt.rcParams['axes.ymargin'] = 0
	# plt.rcParams['axes.xmargin'] = 0
	# plt.axis('tight')

	# X = np.array([[avg-0.5,-0.01], [avg,0], [avg+0.5, -0.01]])
	# t1 = plt.Polygon(X[:3,:], color='yellow', clip_on=False)
	# t1 = plt.arrow(avg, 0, 0, 0.1)
	# plt.gca().add_patch(t1)
	
	plt.gca().annotate('▲', (avg, 0), color='yellow')


	plt.gca().set_ylim(bottom=0)
	plt.tight_layout()
	plt.savefig(f'{name}.pdf')
	# plt.show()
	



if __name__ == '__main__':

	plt_dscim()
	plt_weapon('verac', verac)
	plt_weapon('scythe', scythe)
	plt_weapon('gadderhammer', gadderhammer)
	plt_weapon('keris', keris)


	plt_weapon('longsword', lambda m, a: {
		0: 0.25,
		1: 0.02,
		2: 0.058823529,
		3: 0.102941176,
		4: 0.147058824,
		5: 0.176470588,
		6: 0.19,
		7: 0.176470588,
		8: 0.147058824,
		9: 0.102941176,
		10: 0.058823529,
		11: 0.029411765,
		12: 0.01,
	})


	plt_weapon('flail', lambda m, a: {
i: x for i, x in enumerate([
0.5,
0.129517596,
0.241970725,
0.352065327,
0.398942283,
0.352065381,
0.241971468,
0.129525588,
0.054057882,
0.017964642,
0.006647773,
0.009636833,
0.027129313,
0.064774782,
0.120986849,
0.176032771,
0.199471146,
0.176032664,
0.120985362,
])})


	plt_weapon('blowpipe', lambda m, a: {
i: x for i, x in enumerate([
1.5,
0.7,
1.2,
2,
1,
0.666666667,
0.5,
0.4,
0.333333333,
0.285714286,
0.25,
0.222222222,
0.2,
0.181818182,
0.166666667,
0.153846154,
])})

	plt_weapon('maul', lambda m, a: {
i: x for i, x in enumerate([
4,
0.153846154,
0.166666667,
0.181818182,
0.2,
0.222222222,
0.25,
0.285714286,
0.333333333,
0.4,
0.5,
0.666666667,
0.7,
1,
1.2,
2,
])})


	plt_weapon('sol', lambda m, a: {
i-2: x for i, x in enumerate([
0.3,
0.5,
3,
1,
1,
1,
1,
1,
1,
1,
1,
])})



plt_weapon('claws', lambda m, a: {
i: x for i, x in enumerate([
0.691330305,
0.070482627,
0.667350904,
0.198561187,
0.332812476,
0.343788807,
0.529480697,
0.668094708,
0.734411284,
0.331451093,
0.857420238,
0.243242594,
0.024829737,
0.829398577,
0.501154266,
0.650703058,
0.45063263,
0.552205381,
])})



	

	# from osrsmath.skills.combat.temp.probabilities import Solution2
	# Showing that f=0 both methods agree
	# s2 = Solution2(c)
	# h = 50
	# Ls = list(range(1, 25))
	# plt.plot(Ls, [s2.P(h, L) for L in Ls], label=f"s1")
	# plt.plot(Ls, [dd.P(h, L, 0) for L in Ls], label=f"dd")


	# plt.title("Probability of Dying Against General Graardor after $L$ Attacks.")
	# plt.ylabel("Probability")
	# plt.xlabel("$L$")
	# plt.legend()
	# plt.show()
	# exit()

	# Showing that sample works
	# dd = DamageDistribution(scythe(50, 0.8))
	# plt.plot(list(range(0, dd.max+1)), [dd.c[i] for i in range(0, dd.max+1)], label='Pray=Melee')
	# plt.hist(dd.sample(10000), bins=range(1+dd.max+1), density=True)
	# plt.show()
	# exit()



	# Dm = DamageDistribution(graardor('melee'))
	# Dr = DamageDistribution(graardor('ranged'))
	# Dn = DamageDistribution(graardor(None))

	# Dm.plot()
	# plt.title('Probability of taking damage against General Graardor if piled')
	# plt.xlabel('Damage')
	# plt.ylabel('Damage Probability')
	# plt.show()

	# plt.plot(list(range(1, 100)), [100*Dm.cdf(h) for h in range(1, 100)], label='Pray=Melee')
	# plt.plot(list(range(1, 100)), [100*Dr.cdf(h) for h in range(1, 100)], label='Pray=Ranged')
	# plt.plot(list(range(1, 100)), [100*Dn.cdf(h) for h in range(1, 100)], label='Pray=None')
	# plt.title('Probability of being one-shot by General Graardor if piled\n(for a maxed player in high level gear)')
	# plt.xlabel('Player Health')
	# plt.ylabel('Death Probability')
	# plt.legend()
	# plt.show()

	# plt.plot(list(range(1, 100)), [100*(Dr.cdf(h) - Dm.cdf(h)) for h in range(1, 100)])
	# plt.title('Increase in survival probability between melee and ranged prayer')
	# plt.xlabel('Player Health')
	# plt.ylabel('Death Probability')
	# plt.show()
	# 