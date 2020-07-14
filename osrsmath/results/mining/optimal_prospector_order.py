from osrsmath.mining.motherload_mine import Miner, base_xp, PROSPECTOR
import itertools

if __name__ == '__main__':
	import cairo
	from pprint import pprint
	from PyPDF2 import PdfFileWriter, PdfFileReader

	def normalize(dic):
		m, M = min(dic.values()), max(dic.values())
		return {k: round((v - m) / (M - m), 12) for k, v in dic.items()}

	file_name='optimal_order.pdf'
	experience = {}
	for item1, item2, item3, item4 in itertools.permutations(PROSPECTOR):
		miner = Miner()
		miner.obtain(item1)
		miner.obtain(item2)
		miner.obtain(item3)
		miner.obtain(item4)
		experience[miner.kit()] = miner.experience_gained - base_xp()
	best_order = sorted(experience.items(), key=lambda x: x[1])[-1][0]

	pprint(normalize(experience))
	print(best_order)

	with cairo.PDFSurface(file_name, 300, 300) as surface:
		context = cairo.Context(surface)
		context.scale(250, 250)

		xs = [i / 6 for i in range(1, 6+1)]
		ys = list(reversed([i / 6 for i in range(1, 6+1)]))
		xl, xr = xs[0], xs[-1]
		yb, yt = ys[0], ys[-1]

		def draw(order, item):
			i = list(PROSPECTOR).index(item) + 1
			if order == 1:
				context.move_to(xl, ys[i])
			elif order == 2:
				context.line_to(xs[i], yt)
			elif order == 3:
				context.line_to(xr, ys[i])
			elif order == 4:
				context.line_to(xs[i], yb)
			else:
				assert False

		normalized = normalize(experience)
		for item1, item2, item3, item4 in itertools.permutations(PROSPECTOR):
			kit = (item1, item2, item3, item4)
			context.set_line_width( normalized[kit]*normalized[kit] / 50 )
			context.set_source_rgb( normalized[kit], 0, 0 )
			draw(1, item1)
			draw(2, item2)
			draw(3, item3)
			draw(4, item4)
			context.stroke()

	# Add images of the equipment over top of the lines
	helmet_page = PdfFileReader('Prospector_helmet_detail.pdf').getPage(0)
	jacket_page = PdfFileReader('Prospector_jacket_detail.pdf').getPage(0)
	legs_page = PdfFileReader('Prospector_legs_detail.pdf').getPage(0)
	boots_page = PdfFileReader('Prospector_boots_detail.pdf').getPage(0)
	page = PdfFileReader(file_name).getPage(0)

	# Left
	page.mergeScaledTranslatedPage(helmet_page, 0.07, 5, 85)
	page.mergeScaledTranslatedPage(jacket_page, 0.07, 5, 125)
	page.mergeScaledTranslatedPage(legs_page, 0.07, 5, 165)
	page.mergeScaledTranslatedPage(boots_page, 0.07, 5, 205)

	# Top
	page.mergeScaledTranslatedPage(helmet_page, 0.07, 65, 270)
	page.mergeScaledTranslatedPage(jacket_page, 0.07, 110, 270)
	page.mergeScaledTranslatedPage(legs_page, 0.07, 155, 270)
	page.mergeScaledTranslatedPage(boots_page, 0.07, 190, 265)

	# Right
	page.mergeScaledTranslatedPage(helmet_page, 0.07, 260, 85)
	page.mergeScaledTranslatedPage(jacket_page, 0.07, 260, 125)
	page.mergeScaledTranslatedPage(legs_page, 0.07, 260, 165)
	page.mergeScaledTranslatedPage(boots_page, 0.07, 260, 205)

	# Bottom
	page.mergeScaledTranslatedPage(helmet_page, 0.07, 65, 20)
	page.mergeScaledTranslatedPage(jacket_page, 0.07, 110, 20)
	page.mergeScaledTranslatedPage(legs_page, 0.07, 150, 20)
	page.mergeScaledTranslatedPage(boots_page, 0.07, 190, 20)

	# Write to output
	pdf_writer = PdfFileWriter()
	pdf_writer.addPage(page)
	with open(file_name, 'wb') as out:
		pdf_writer.write(out)




					
