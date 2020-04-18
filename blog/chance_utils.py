import math
import random
import cairo
from .utils import num
import re
import collections
from django.utils.datastructures import MultiValueDictKeyError
from fractions import Fraction

def square(ctx, square_size, squash, offset_x, offset_y, fillcolour):

		ctx.move_to(offset_x+0, offset_y / squash +0)
		ctx.line_to(offset_x+square_size, offset_y / squash+0)  # Line to (x,y)
		ctx.line_to(offset_x+square_size, offset_y / squash+square_size / squash)  # Line to (x,y)
		ctx.line_to(offset_x+0, offset_y / squash + square_size / squash)  # Line to (x,y)
		ctx.line_to(offset_x+0, offset_y / squash+0)
		ctx.close_path()

		ctx.set_source_rgb(0, 0, 0)  # Solid color
		ctx.set_line_width(square_size/20)
		ctx.stroke_preserve()
		ctx.set_source_rgba(fillcolour[0], fillcolour[1], fillcolour[2], fillcolour[3] )  # Solid color
		ctx.fill()

def rect(ctx, square_size, offset_x, offset_y, range_y, fillcolour):

		rect_depth = square_size
		#offset_y = rect_depth
		ctx.move_to(offset_x+0, offset_y+0)
		ctx.line_to(offset_x+square_size, offset_y+0)  # Line to (x,y)
		ctx.line_to(offset_x+square_size, offset_y+rect_depth)  # Line to (x,y)
		ctx.line_to(offset_x+0, offset_y+rect_depth)  # Line to (x,y)
		ctx.line_to(offset_x+0, offset_y+0)
		ctx.close_path()

		ctx.set_source_rgb(0, 0, 0)  # Solid color
		ctx.set_line_width(min(square_size/20,0.002))
		ctx.stroke_preserve()
		ctx.set_source_rgba(fillcolour[0], fillcolour[1], fillcolour[2], fillcolour[3] )  # Solid color
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
		square(ctx, square_size, 1, offset_x*gridcell_x, offset_y*gridcell_y, fillcolour)

def cell1(ctx, square_size, squash, offset_x, offset_y, gridcell_x, gridcell_y, chance, count, alive_x, repeat_mode="repeats"):
		rnd = random.random()
		if repeat_mode == "removes" and not(alive_x[offset_x]):
			fillcolour = (0.0, 0.0, 0.0, 1.0)
		elif (rnd < chance):
			if repeat_mode == "removes":
				alive_x[offset_x] = False
			fillcolour = (1.0, 0.6, 0.2, 1.0)
		else:
			fillcolour = (0.2, 0.6, 0.1, 1.0)
		square(ctx, square_size, squash, offset_x*gridcell_x, offset_y*gridcell_y, fillcolour)

def cell_drawonly(ctx, cell_value, square_size, squash, offset_x, offset_y, gridcell_x, gridcell_y):
		if cell_value == None:
			fillcolour = (0.0, 0.0, 0.0, 1.0)
		elif cell_value == 1:
			fillcolour = (1.0, 0.65, 0.22, 1.0)
		elif cell_value == 2:
			fillcolour = (0.5, 0.8, 0.5, 1.0)
		elif cell_value == 3:
			fillcolour = (0.3, 0.6, 0.7, 1.0)
		elif cell_value == 4:
			fillcolour = (0.3, 0.4, 0.8, 1.0)
		elif cell_value == 5:
			fillcolour = (0.5, 0.8, 0.2, 1.0)
		elif cell_value == 6:
			fillcolour = (0.5, 0.5, 0.5, 1.0)
		else:
			fillcolour = (0.12, 0.36, 0.064, 1.0)
		square(ctx, square_size, squash, offset_x*gridcell_x, offset_y*gridcell_y, fillcolour)

def equalchance(params, repetition):
	return params[0]

def expchance(params, repetition):
	p = params[0] * (1+params[1])**repetition
	return p

def constant(params, repetition):
	return params[0]

def increase(params, repetition):
	p = params[0] * (1+params[1])**repetition
	return p

def decrease(params, repetition):
	p = (params[0]*(1-params[1])**(repetition))
	return p

def escchance(params, repetition):
	p = params[0] * (1+params[1])**repetition
	return (p/(1+p))

def mort1(params, repetition):
	p = params[0] * (1+params[1])**repetition + params[2]
	return (p/(1+p))

def mort2(params, repetition):
	child_p = (params[3]*4**(-repetition))
	adult_p = params[0] * (1+params[1])**repetition + params[2]
	p = child_p + adult_p
	return (p/(1+p))


def cell_outcomex(chance_f, params = {}, repetition = 1):
		rnd = random.random()
		if (rnd < chance_f(params, repetition)):
			return 1
		else:
			return 0

def cell_outcome(chance_functions, repetition = 1):
		for i in range(len(chance_functions)):
			rnd = random.random()
			chance_f = chance_functions[i][0]
			params = chance_functions[i][1]
			if (rnd < chance_f(params, repetition)):
				return 1+i
		return 0

def count_cell(ctx, square_size, offset_x, offset_y, gridcell_x, gridcell_y, range_y, hits, exposed, count, invert=False):
	if invert:
		if (count < (exposed-hits)):
			fillcolour = (0.2, 0.6, 0.1, 1.0)
		elif (count < exposed):
			fillcolour = (1.0, 0.6, 0.2, 1.0)
		else:
			fillcolour = (0.0, 0.0, 0.0, 0.0)
	else:
		if (count < hits):
			fillcolour = (1.0, 0.6, 0.2, 1.0)
		elif (count < exposed):
			fillcolour = (0.2, 0.6, 0.1, 1.0)
		else:
			fillcolour = (0.0, 0.0, 0.0, 0.0)
	if count < exposed:
		rect(ctx, square_size, offset_x*gridcell_x, offset_y*gridcell_y, range_y, fillcolour)

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

def grid1(ctx, range_x, range_y, chance, repeat_mode="repeats", xy=False):
		square_size = 0.9/range_x
		gridcell_x = 0.9/range_x
		gridcell_y = gridcell_x
		squash = 1.0 * range_y / range_x
		count = 0
		alive_x = [True] * range_x


		if xy:
			for offset_x in range(0,range_x):
				for offset_y in range(0,range_y):
					cell1(ctx, square_size, squash, offset_x, offset_y, gridcell_x, gridcell_y, chance, count, alive_x, repeat_mode=repeat_mode)
					count+=1
		else:
			for offset_y in range(0,range_y):
				for offset_x in range(0,range_x):
					cell1(ctx, square_size, squash, offset_x, offset_y, gridcell_x, gridcell_y, chance, count, alive_x, repeat_mode=repeat_mode)
					count+=1

def grid_drawonly(ctx, grid, range_x, range_y, xy=False, top_down= False):
		square_size = 0.9/range_x
		gridcell_x = 0.9/range_x
		gridcell_y = gridcell_x
		squash = 1.0 * range_y / range_x
		count = 0
		alive_x = [True] * range_x
		if xy:
			for offset_x in range(0,range_x):
				for offset_y in range(0,range_y):
					if top_down:
						cell_y = offset_y
					else:
						cell_y = (range_y-1)-offset_y
					cell_drawonly(ctx, grid[cell_y][offset_x], square_size, squash, offset_x, offset_y, gridcell_x, gridcell_y)
					count+=1
		else:
			for offset_y in range(0,range_y):
				for offset_x in range(0,range_x):
					if top_down:
						cell_y = offset_y
					else:
						cell_y = (range_y-1)-offset_y
					cell_drawonly(ctx, grid[cell_y][offset_x], square_size, squash, offset_x, offset_y, gridcell_x, gridcell_y)
					count+=1


def do_trial(trial, params, repeat_mode="repeats", seed = None, verbose=False):
	if seed:
		random.seed(seed)
	range_x = trial["items"]
	range_y = trial["repetitions"]
	chance = trial["probability"]
	probability = chance
	chance_f = equalchance
	chance_function_name = "equalchance"
	chance_params = {}
	chance_params["chance"] = chance

	if "chance_function" in params.keys():
		chance_function = params["chance_function"]
	elif "chance_function" in trial.keys():
		chance_function = trial["chance_function"]
	else:
		chance_function = "equalchance"

	chance_functions = parse_chance_functions(chance_function).split("|")
	pairs = []
	for function in chance_functions:
		chance_function_name, chance_function_params = parse_chance_function(function)
		print("chance function", function, chance_function_name, chance_function_params)
		function_pair =(eval(chance_function_name), eval(chance_function_params+","))
		pairs.append(function_pair)

	print("chance_functions", pairs)

	count_hits_x = [0] * range_x
	count_hits_y = [0] * range_y
	count_hits = 0
	outcomes = [[None] * range_x for i in range(range_y)]
	alive_x = [True] * range_x
	for offset_y in range(0,range_y):
		for offset_x in range(0,range_x):
			outcome = cell_outcome(pairs, offset_y)
			if alive_x[offset_x]:
				outcomes[offset_y][offset_x] = outcome
				count_hits+=int(outcome>0)
#				count_hits_x[offset_x]+=int(outcome>0)
				count_hits_x[offset_x]+=outcome
				count_hits_y[offset_y]+=int(outcome>0)
				if repeat_mode == "removes" and outcome>0:
					alive_x[offset_x] = False
			
	if verbose:
		return count_hits, count_hits_x, count_hits_y, outcomes
	else:
		return count_hits, count_hits_x, count_hits_y

def count_grid(ctx, range_x, range_y, hits, exposed, xy=False, invert=False):
		square_size = 0.9/range_x
		gridcell_x = 0.9/range_x
		gridcell_y = gridcell_x
		count = 0
		if xy:
			for offset_x in range(0,range_x):
				for offset_y in range(0,range_y):
					count_cell(ctx, square_size, offset_x, offset_y, gridcell_x, gridcell_y, range_y, hits, exposed, count, invert=invert)
					count+=1
		else:
			for offset_y in range(0,range_y):
				for offset_x in range(0,range_x):
					count_cell(ctx, square_size, offset_x, offset_y, gridcell_x, gridcell_y, range_y, hits, exposed, count, invert=invert)
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

def drawgrid1x(range_x, range_y, chance, repeat_mode="repeats", seed = None, xy=False):
		if seed:
			random.seed(seed)
			print("seed", seed)
		WIDTH, HEIGHT = 1500, int(1500.0 * range_y / range_x)
#		WIDTH, HEIGHT = 1500, 1500
		surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
		ctx = cairo.Context(surface)
		ctx.scale(WIDTH, HEIGHT)  # Normalizing the canvas
		ctx.translate(0.05, 0.0)  # Changing the current transformation matrix
		grid1(ctx, range_x, range_y, chance, repeat_mode, xy)
		return surface

def draw_chance_grid(grid, range_x, range_y, xy=False, top_down=False):
		WIDTH, HEIGHT = 1500, int(1500.0 * range_y / range_x)
		surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
		ctx = cairo.Context(surface)
		ctx.scale(WIDTH, HEIGHT)  # Normalizing the canvas
		ctx.translate(0.05, 0.0)  # Changing the current transformation matrix
		grid_drawonly(ctx, grid, range_x, range_y, xy, top_down)
		return surface

def compute_chance_grid(range_x, range_y, chance, params, repeat_mode="repeats", seed = None, xy=False):
	if seed:
		random.seed(seed)
	trial = {
		"items": range_x,
		"repetitions": range_y,
		"probability": chance
	}
	return do_trial(trial, params, repeat_mode=repeat_mode, verbose = True)

def draw_count_grid(range_x, range_y, hits, exposed, xy=False, invert=False):
		WIDTH, HEIGHT = 2000, max(200, 10 * range_y)
		surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
		ctx = cairo.Context(surface)
		ctx.scale(WIDTH, WIDTH*max(1, 20/range_y))  # Normalizing the canvas
		ctx.translate(0.05, 0.0)  # Changing the current transformation matrix
		count_grid(ctx, range_x, range_y, hits, exposed, xy, invert=invert)
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
#	acceptable = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
	acceptable = range(1,100)
	best_error = proportion
	for odds2 in acceptable:
		odds1 = scale*int(round_money(odds2 * (1 / proportion - 1 ),0))
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

def odds2(proportion, tolerance=0.01):
	odds_on = False
	if proportion > 0.5:
		odds_on = True
		proportion = 1 - proportion
	if proportion == 0:
		return (1,0)
	if proportion ==1:
		return (0,1)
#	fineness = round(math.log10(proportion))-1
	frac = Fraction(1-proportion).limit_denominator(40)
	if (proportion > 0.01) and abs(frac - (1-proportion))<tolerance:
		print("close enough", frac, proportion)
		return(frac.numerator, frac.denominator - frac.numerator)

	fineness = min(math.log10(proportion)-1,-1.4)
	fineadjust = round(10 ** -fineness)
	limit = int(1.2*fineadjust)
	fracpair = (round(fineadjust*(1-proportion)), fineadjust)
	round_num = round_sigfigs(fracpair[0],0)
	print(fracpair)
	print(round_num , round(round_num * fracpair[1] / fracpair[0]))
	frac2 = Fraction(round_num / round(round_num * fracpair[1] / fracpair[0])).limit_denominator(limit)
	if odds_on:
		return frac2.denominator - frac2.numerator, frac2.numerator
	else:
		return frac2.numerator, frac2.denominator - frac2.numerator

def round_sigfigs(amount, level=1):
	scale = int(math.log10(amount))
	rounded = round(amount/10**(scale-level))
	return rounded * 10**(scale-level)


def round_money(amount, level=1):
	scale = int(math.log10(amount))
	rounded = round(amount/10**(scale-1))
	print(">>>>")
	print("odds", scale, amount, rounded)
	if rounded >= 195:
		rounded = int(0.5 + rounded/5.0) * 5
	elif rounded >= 126:
		rounded = int(0.5 + rounded/2.0) * 2
	else:
		rounded = int(rounded)

	return rounded * 10**(scale-1)


def parse_chance_function(chance_function):
	regex="^((?P<name>[a-z|A-Z|0-9]+)\((?P<params>.*)\),?)+$"
	p = re.compile(regex)
	m=p.match(chance_function)
	if (m!=None):
		try:
			name = m.group('name')
			params = m.group('params')
			return name, params
		except:
			return None

def parse_chance_functions(chance_functions):
	regex="^\[(?P<functions>.*)\]$"
	p = re.compile(regex)
	m=p.match(chance_functions)
	if (m!=None):
		try:
			functions = m.group('functions')
			return functions
		except:
			return None

def parse_probability(probability):
	probability = probability.replace("+"," ").replace(",","")
	regex_odds="^\s*(?P<miss>[0-9\.]+)\s*(:|to)\s*(?P<hit>[0-9\.]+)\s*$"
	p = re.compile(regex_odds)
	m=p.match(probability)
	if (m!=None):
		try:
			miss = num(m.group('miss'))
			hit = num(m.group('hit'))
			return hit/(hit+miss)
		except:
			return None
	regex_prop="^\s*(?P<hit>[0-9\.]+)\s*(\/|in)\s*(?P<all>[0-9\.]+)\s*$"
	p = re.compile(regex_prop)
	m=p.match(probability)
	if (m!=None):
		try:
			total = num(m.group('all'))
			hit = num(m.group('hit'))
			return hit/total
		except:
			return None
	regex_perc="^\s*(?P<perc>[0-9\.]+)\s*(%|pc|perc|percent|percentage)\s*$"
	p = re.compile(regex_perc)
	m=p.match(probability)
	if (m!=None):
		try:
			perc = num(m.group('perc'))
			return perc/100
		except:
			return None
	return num(probability)

def distribution(array):
	table = {}
	for item in array:
		try: 
			table[item]+=1
		except:
			table[item]=1
	sorted_table = collections.OrderedDict()
	for key in sorted(table.keys()):
		sorted_table[key]=table[key]

	return sorted_table

def summary(sorted_dist):
	k = list(sorted_dist.keys())
	m = len(k)
	t = 0
	j = None
	n = 0
	S = 0
	median = None
	for i in k:
		n+=sorted_dist[i]
		S+=sorted_dist[i] * i
	mean = S/n
	for i in k:
		t+=sorted_dist[i]
		if t > n / 2:
			if j:
				median = (i + j) /2
			else:
				median = i
		elif t == n/2:
			j = i
		if not(median==None):
			break
	return {"min":k[0], "max":k[-1], "mean": mean, "median": median}
