import math
import random
import cairo
import re
import collections
from django.utils.datastructures import MultiValueDictKeyError
from fractions import Fraction
from .utils import num
from .grid_utils import draw_count_grid

'''
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

'''
def equalchance(params, repetition):
    return params[0]

def expchance(params, repetition):
    p = params[0] * (1+params[1])**repetition
    return p

def constant(params, repetition):
    return params

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


def cell_outcome(chance_functions, repetition = 1):
    remaining_prob = 1
    for i in range(len(chance_functions)):
        if remaining_prob <= 0: 
            continue
        rnd = random.random()
        chance_f = chance_functions[i][0]
        params = chance_functions[i][1]
        raw_prob = chance_f(params[0], repetition) 
        prob = raw_prob / remaining_prob
        remaining_prob = remaining_prob - raw_prob
        if (rnd < prob):
            return 1+i
    return 0

def do_trial(trial, params, repeat_mode="repeats", seed = None, verbose=False, include_none = False):
    if seed:
        random.seed(seed)
    range_x = trial["items"]
    range_y = trial["repetitions"]
    chance_function_str = trial["probability"]
    chance_functions = parse_chance_functions(chance_function_str).split("|")
    pairs = []
    for function in chance_functions:
        chance_function_name, chance_function_params = parse_chance_function(function)
        function_pair =(eval(chance_function_name), eval(('parse_probability("%s")' % chance_function_params)+","))
        pairs.append(function_pair)
    level_counts = {}
    for outcome in range(len(pairs)):
        stats = {}
        stats['hits']=0
        stats['x_hits'] = {}
        for offset_x in range(0,range_x):
            stats['x_hits'][offset_x] = 0
        stats['y_hits'] = {}
        for offset_y in range(0,range_y):
            stats['y_hits'][offset_y] = 0
        level_counts[outcome+1]=stats
    outcomes = [[None] * range_x for i in range(range_y)]
    alive_x = [True] * range_x
    for offset_y in range(0,range_y):
        for offset_x in range(0,range_x):
            outcome = cell_outcome(pairs, offset_y)
            if alive_x[offset_x]:
                outcomes[offset_y][offset_x] = outcome
                if outcome > 0:
                    if outcome in level_counts.keys():
                        level_counts[outcome]['hits'] += 1
                        level_counts[outcome]['x_hits']
                        if offset_x in level_counts[outcome]['x_hits']:
                            level_counts[outcome]['x_hits'][offset_x] += 1
                        else:    
                            level_counts[outcome]['x_hits'][offset_x] = 1
                        if offset_y in level_counts[outcome]['y_hits']:
                            level_counts[outcome]['y_hits'][offset_y] += 1
                        else:    
                            level_counts[outcome]['y_hits'][offset_y] = 1
                    else:
                        level_count = {}
                        level_count['hits'] = 1
                        level_count['x_hits'] = {offset_x : 1}
                        level_count['y_hits'] = {offset_y : 1}
                        level_counts[outcome] = level_count
                if repeat_mode == "removes" and outcome > 0:
                    alive_x[offset_x] = False
            
    if verbose:
        return level_counts, outcomes
    else:
        return level_counts

def replace_cell(c, a, b):
    if c == a:
        return b
    else:
        return c


def collect_left(outcomes_before, sort=False):
    outcomes_after = []
    rows_count_0 = []
    for y in range(len(outcomes_before)):
        outcomes_after_col = []
        newcol = [replace_cell(cell, 1000, 0) for cell in sorted([replace_cell(cell, 0, 1000) for cell in outcomes_before[y]])]
        rows_count_0.append(newcol.count(0))
        outcomes_after.append(newcol)
    if sort:
        outcomes_after = list(zip(*sorted(zip(rows_count_0,outcomes_after), reverse=True)))[1]        
    return outcomes_after

def collect_lower(outcomes_before, sort=False):
    outcomes_before = [[outcomes_before[j][i] for j in range(len(outcomes_before))] for i in range(len(outcomes_before[0]))] 
    outcomes_after = []
    rows_count_0 = []
    for y in range(len(outcomes_before)):
        outcomes_after_col = []
        newcol = [replace_cell(cell, 1000, 0) for cell in sorted([replace_cell(cell, 0, 1000) for cell in outcomes_before[y]])]
        rows_count_0.append(newcol.count(0))
        outcomes_after.append(newcol)
    if sort:
        outcomes_after = list(zip(*sorted(zip(rows_count_0,outcomes_after), reverse=True)))[1]        
    outcomes_after = [[outcomes_after[j][i] for j in range(len(outcomes_after))] for i in range(len(outcomes_after[0]))] 
    return outcomes_after

def collect_all(outcomes_before, sort=False):
    outcomes_before = [[outcomes_before[j][i] for j in range(len(outcomes_before))] for i in range(len(outcomes_before[0]))] 
    outcomes_after = []
    cells = flatten(outcomes_before)
    sorted_cells = [replace_cell(cell, 1000, 0) for cell in sorted([replace_cell(cell, 0, 1000) for cell in cells])]
    i = 0
    for y in range(len(outcomes_before)):
        outcomes_after_col = []
        for x in range(len(outcomes_before[y])):
            outcomes_after_col.append(sorted_cells[i])
            i+=1
        outcomes_after.append(outcomes_after_col)
    outcomes_after = [[outcomes_after[j][i] for j in range(len(outcomes_after))] for i in range(len(outcomes_after[0]))] 
    return outcomes_after

def collect_corner(outcomes_before, sort=False):
    outcomes_before = [[outcomes_before[j][i] for j in range(len(outcomes_before))] for i in range(len(outcomes_before[0]))] 
    rows = len(outcomes_before)
    cols = len(outcomes_before[0])
    outcomes_after = [ [ 0 for i in range(cols) ] for j in range(rows) ]
    count_all = rows * cols
    cells = [cell for cell in flatten(outcomes_before) if cell != 0]
    sorted_cells = sorted(cells)
    ratio = math.sqrt(len(cells) / count_all)
    rows_count = math.ceil(rows * ratio)
    cols_count = math.ceil(cols * ratio)
    for i in range(len(cells)):
        outcomes_after[i // cols_count][i % cols_count] = sorted_cells[i]
    outcomes_after = [[outcomes_after[j][i] for j in range(len(outcomes_after))] for i in range(len(outcomes_after[0]))] 
    return outcomes_after



def kfillcolours():
        fillcolour0 = (1, 1, 1)  # Solid color
        fillcolour1 = (0, 0.5, 0.6)  # Solid color
        fillcolour2 = (0.6, 0.2, 0)  # Solid color
        fillcolour3 = (0.2, 0.6, 0.1)  # Solid color
        fillcolour4 = (0.8, 0.8, 0.1)  # Solid color
        fillcolour5 = (0.8, 0.1, 0.8)  # Solid color
        return (fillcolour0, fillcolour1, fillcolour2, fillcolour3, fillcolour4, fillcolour5)

def kfillcolours_graded_blue():
        fillcolour0 = (0, 0, 0)  # Solid color
        fillcolour1 = (0, 0, 0.2)  # Solid color
        fillcolour2 = (0, 0, 0.4)  # Solid color
        fillcolour3 = (0, 0, 0.6)  # Solid color
        fillcolour4 = (0, 0, 0.8)  # Solid color
        fillcolour5 = (0, 0, 1)  # Solid color
        return (fillcolour0, fillcolour1, fillcolour2, fillcolour3, fillcolour4, fillcolour5)



def compute_chance_grid(range_x, range_y, chance, params, repeat_mode="repeats", seed = None, xy=False):
    if seed:
        random.seed(seed)
    trial = {
        "items": range_x,
        "repetitions": range_y,
        "probability": chance
    }
    return do_trial(trial, params, repeat_mode=repeat_mode, verbose = True)

def odds(proportion, maxerror=0.0):
    oddson= False
    scale = 1
    if proportion > 0.5:
        proportion = 1 - proportion
        oddson = True
    while proportion < 0.01:
        scale *= 10
        proportion *=10
#   acceptable = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
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
#   fineness = round(math.log10(proportion))-1
    frac = Fraction(1-proportion).limit_denominator(40)
    if (proportion > 0.01) and abs(frac - (1-proportion))<tolerance:
        print("close enough", frac, proportion)
        if odds_on:
            return frac.denominator - frac.numerator, frac.numerator
        else:
            return frac.numerator, frac.denominator - frac.numerator

    fineness = min(math.log10(proportion)-1,-1.4)
    fineadjust = round(10 ** -fineness)
    limit = int(1.2*fineadjust)
    fracpair = (round(fineadjust*(1-proportion)), fineadjust)
    round_num = round_sigfigs(fracpair[0],0)
    frac2 = Fraction(round_num / round(round_num * fracpair[1] / fracpair[0])).limit_denominator(limit)
    if odds_on:
        print("odds_on")
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
    m=p.match(chance_function.strip())
    if (m!=None):
        try:
            name = m.group('name')
            params = m.group('params')
            return name, params
        except:
            return None
    return 'constant', chance_function

def parse_chance_functions(chance_functions):
    chance_functions = chance_functions.replace("[",'').replace("]",'')
    regex="^(?P<functions>.*)$"
    p = re.compile(regex)
    m=p.match(chance_functions)
    if (m!=None):
        try:
            functions = m.group('functions')
            return functions
        except:
            return None

def parse_probability(probability):
    probability_list=probability.split(",")
    if len(probability_list) > 1:
        return [parse_probability(p) for p in probability_list ]
    else:
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
        try:
            prob = num(probability)
        except:
            prob = 0
        return prob

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

def flatten(array):
    flat = []
    for row in array:
        for col in row:
            flat.append(col)
    return flat

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

def get_prob_summary(args):
    probability, prob, label, items, repetitions, repeat_mode = args
    if repeat_mode == "repeats":
        calc_hits = prob * items * repetitions
        calc_hits_item = prob * repetitions
        survival_prob = 1
        try:
            calc_wait = 1 / prob
        except:
            calc_wait = 0
    else:
        try:
            prob = prob[0]
        except:
            pass
        try:
            calc_wait = 1 / prob
        except:
            calc_wait = 0
        calc_hits = -1
        survival_prob = (1 - prob) ** repetitions
        calc_hits_item = (1 - survival_prob) * items

    try:
        fraction = Fraction(prob).limit_denominator(1000)
    except:
        fraction = Fraction(0)
    
    try:
        odds_raw = odds2(prob, tolerance=0.0005)
        print("odds raw", odds_raw)
        odds_fraction = (odds_raw[1], (odds_raw[0] + odds_raw[1]))
        percentage = prob * 100
    except:
        odds_raw = odds2(0, tolerance=0.0005)
        odds_fraction = (odds_raw[1], (odds_raw[0] + odds_raw[1]))
        percentage = 0
    equivalents = {
        "supplied": probability.strip(),
        "probability": prob,
        "percentage": percentage,
        "fraction": fraction,
        "odds": odds_raw,
        "odds_fraction": odds_fraction,
    }
    return {
        "repeat_mode": repeat_mode,
        "hits": calc_hits,
        "hits_item": calc_hits_item,
        "hits_text": label,
        "wait": calc_wait,
        "survival_prob":1,
        "equivalents":equivalents
        }

