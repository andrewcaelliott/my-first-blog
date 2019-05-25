import math
import cairo

def square(ctx, square_size, offset_x, offset_y, fillcolour):

		ctx.move_to(offset_x+0, offset_y+0)
		ctx.line_to(offset_x+square_size, offset_y+0)  # Line to (x,y)
		ctx.line_to(offset_x+square_size, offset_y+square_size)  # Line to (x,y)
		ctx.line_to(offset_x+0, offset_y+square_size)  # Line to (x,y)
		ctx.line_to(offset_x+0, offset_y+0)
		ctx.close_path()

		ctx.set_source_rgb(0, 0, 0)  # Solid color
		ctx.set_line_width(square_size)
		ctx.stroke_preserve()
		ctx.set_source_rgb(fillcolour[0], fillcolour[1], fillcolour[2])  # Solid color
		ctx.fill()

def rect(ctx, square_size, offset_x, offset_y, fillcolour):

		rect_depth = 0.5
		ctx.move_to(offset_x+0, offset_y+0)
		ctx.line_to(offset_x+square_size, offset_y+0)  # Line to (x,y)
		ctx.line_to(offset_x+square_size, offset_y+rect_depth)  # Line to (x,y)
		ctx.line_to(offset_x+0, offset_y+rect_depth)  # Line to (x,y)
		ctx.line_to(offset_x+0, offset_y+0)
		ctx.close_path()

		ctx.set_source_rgb(0, 0, 0)  # Solid color
		ctx.set_line_width(min(square_size/20,0.002))
		ctx.stroke_preserve()
		ctx.set_source_rgb(fillcolour[0], fillcolour[1], fillcolour[2])  # Solid color
		ctx.fill()

def colour_band(count, rule_params):
	bands = rule_params[0]
	fillcolour = (1,1,1)
	for colour in bands:
		if count < colour[0]:
			fillcolour = colour[1]
			break
	return fillcolour

def colour_div(count, rule_params):
	fillcolours = rule_params[0]
	fillcolour = (1,1,1)
	if (count % 2 ==0):
		fillcolour=fillcolours[1]
	elif (count % 3 ==0):
		fillcolour=fillcolours[2]
	elif (count % 5 ==0):
		fillcolour=fillcolours[3]
	elif (count % 7 ==0):
		fillcolour=fillcolours[4]
	elif (count % 11 ==0):
		fillcolour=fillcolours[5]
	return fillcolour


def cell(ctx, square_size, offset_x, offset_y, gridcell_x, gridcell_y, colour_rule, count):
		fillcolour = colour_rule[0](count, colour_rule[1])
		square(ctx, square_size, offset_x*gridcell_x, offset_y*gridcell_y, fillcolour)

def cell2(ctx, square_size, offset_x, offset_y, gridcell_x, gridcell_y, hits, count):
		if (count < hits):
			fillcolour = (1.0, 0.6, 0.2)
		else:
			fillcolour = (0.2, 0.6, 0.1)
		rect(ctx, square_size, offset_x*gridcell_x, offset_y*gridcell_y, fillcolour)

def grid(ctx, range_x, range_y, colour_rule, xy=False):
		square_size = 0.9/range_x
		gridcell_x = 0.9/range_x
		gridcell_y = gridcell_x
		count = 0

		if xy:
			for offset_x in range(0,range_x):
				for offset_y in range(0,range_y):
					cell(ctx, square_size, offset_x, offset_y, gridcell_x, gridcell_y, colour_rule, count)
					count+=1
		else:
			for offset_y in range(0,range_y):
				for offset_x in range(0,range_x):
					cell(ctx, square_size, offset_x, offset_y, gridcell_x, gridcell_y, colour_rule, count)
					count+=1

def grid2(ctx, range_x, range_y, hits, xy=False):
		square_size = 0.9/range_x
		gridcell_x = 0.9/range_x
		gridcell_y = gridcell_x
		count = 0

		if xy:
			for offset_x in range(0,range_x):
				for offset_y in range(0,range_y):
					cell2(ctx, square_size, offset_x, offset_y, gridcell_x, gridcell_y, hits, count)
					count+=1
		else:
			for offset_y in range(0,range_y):
				for offset_x in range(0,range_x):
					cell2(ctx, square_size, offset_x, offset_y, gridcell_x, gridcell_y, hits, count)
					count+=1
def fillcolours():
		fillcolour0 = (1, 1, 1)  # Solid color
		fillcolour1 = (0, 0.5, 0.6)  # Solid color
		fillcolour2 = (0.6, 0.2, 0)  # Solid color
		fillcolour3 = (0.2, 0.6, 0.1)  # Solid color
		fillcolour4 = (0.8, 0.8, 0.1)  # Solid color
		fillcolour5 = (0.8, 0.1, 0.8)  # Solid color
		return (fillcolour0, fillcolour1, fillcolour2, fillcolour3, fillcolour4, fillcolour5)

def fillcolours_graded_blue():
		fillcolour0 = (0, 0, 0)  # Solid color
		fillcolour1 = (0, 0, 0.2)  # Solid color
		fillcolour2 = (0, 0, 0.4)  # Solid color
		fillcolour3 = (0, 0, 0.6)  # Solid color
		fillcolour4 = (0, 0, 0.8)  # Solid color
		fillcolour5 = (0, 0, 1)  # Solid color
		return (fillcolour0, fillcolour1, fillcolour2, fillcolour3, fillcolour4, fillcolour5)


def drawgrid(range_x, range_y, colour_rule, xy=False):
		WIDTH, HEIGHT = 1500, 1500
		surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
		ctx = cairo.Context(surface)
		ctx.scale(WIDTH, HEIGHT)  # Normalizing the canvas
		ctx.translate(0.05, 0.05)  # Changing the current transformation matrix
		grid(ctx, range_x, range_y, colour_rule, xy)
		return surface

def drawgrid2(range_x, range_y, hits, xy=False):
		WIDTH, HEIGHT = 1500, 100
		surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
		ctx = cairo.Context(surface)
		ctx.scale(WIDTH, HEIGHT)  # Normalizing the canvas
		ctx.translate(0.05, 0.05)  # Changing the current transformation matrix
		grid2(ctx, range_x, range_y, hits, xy)
		return surface


def odds(proportion, maxerror=0.0):
	oddson= False
	scale = 1
	if proportion > 0.5:
		proportion = 1 - proportion
		oddson = True
	while proportion < 0.01:
		scale *= 10
		proportion *=10
	acceptable = [1, 2, 3, 4, 5, 10]
	best_error = proportion
	for odds2 in acceptable:
		odds1 = scale*int(round(odds2 * (1 / proportion - 1 ),0))
		error = (odds2 / (odds1 + odds2)) - proportion/scale
		error_adjusted = abs(error)*(1 + odds2/10)
		#print(odds1, "to", odds2, "=", odds2 / (odds1 + odds2), "with error", error, error_adjusted)
		if error_adjusted < best_error:
			best_odds2 = odds2
			best_odds1 = odds1
			best_error = error_adjusted
		if best_error < maxerror:
			break
	#best_odds1 = scale * best_odds1
	if oddson:
		return (best_odds2, best_odds1)
	else:
		return (best_odds1, best_odds2)




