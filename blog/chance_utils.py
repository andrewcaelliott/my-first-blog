import math
import random
import cairo
import re
import collections
from django.utils.datastructures import MultiValueDictKeyError
from fractions import Fraction
from .utils import num
from .grid_utils import draw_count_grid

def equalchance(params, repetition, item):
    return params[0]

def expchance(params, repetition, item):
    p = params[0] * (1+params[1])**repetition
    return p

def constant(params, repetition, item):
    return params

def increase(params, repetition, item):
    p = params[0] * (1+params[1])**repetition
    return p

def increase2(params, repetition, item):
    p = params[0] * (1+params[1])**repetition * (1+params[2])** item
    return p

def decrease(params, repetition, item):
    p = (params[0]*(1-params[1])**(repetition))
    return p

def decrease2(params, repetition, item):
    p = (params[0]*(1-params[1])**(repetition) *(1-params[1])**(item))
    return p

def escchance(params, repetition, item):
    p = params[0] * (1+params[1])**repetition
    return (p/(1+p))

def mort1(params, repetition, item):
    p = params[0] * (1+params[1])**repetition + params[2]
    return (p/(1+p))

def mort2(params, repetition, item):
    child_p = (params[3]*4**(-repetition))
    adult_p = params[0] * (1+params[1])**repetition + params[2]
    p = child_p + adult_p
    return (p/(1+p))


def cell_outcome(chance_functions, repetition = 0, item=0):
    remaining_prob = 1
    for i in range(len(chance_functions)):
        if remaining_prob <= 0: 
            continue
        rnd = random.random()
        chance_f = chance_functions[i][0]
        params = chance_functions[i][1]
        raw_prob = chance_f(params[0], repetition, item) 
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
    exposure = trial["exposure"]
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
            if offset_x+(offset_y * range_x) < exposure:
                outcome = cell_outcome(pairs, offset_y, offset_x)
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
    return c

def replace_cell_m(c, pairs):
    for pair in pairs:
        if c == pair[0]:
            return pair[1]
    return c


def collect_left(outcomes_before, sort=False):
    outcomes_after = []
    rows_count_0 = []
    for y in range(len(outcomes_before)):
        outcomes_after_col = []
        newcol = [replace_cell_m(cell, [(1000, 0),(1001, None)]) for cell in sorted([replace_cell_m(cell, [(0, 1000),(None, 1001)]) for cell in outcomes_before[y]])]
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
    sorted_cells = [replace_cell_m(cell, [(1000, 0),(1001, None)]) for cell in sorted([replace_cell_m(cell, [(0, 1000),(None, 1001)]) for cell in cells])]
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
    outcomes_after = [ [ None for i in range(cols) ] for j in range(rows) ]
    count_all = rows * cols
    all_cells = [cell for cell in flatten(outcomes_before) if cell is not None]
    filled_cells = [cell for cell in flatten(outcomes_before) if cell != 0 and cell is not None]
    sorted_cells = sorted(filled_cells)
    ratio = math.sqrt(len(filled_cells) / count_all)
    rows_count = math.ceil(rows * ratio)
    cols_count = math.ceil(cols * ratio)
    for i in range(len(all_cells)):
        outcomes_after[i // cols][i % cols] = 0
    for i in range(len(filled_cells)):
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



def compute_chance_grid(range_x, range_y, exposure, chance, params, repeat_mode="repeats", seed = None, xy=False):
    if seed:
        random.seed(seed)
    trial = {
        "items": range_x,
        "repetitions": range_y,
        "probability": chance,
        "exposure": exposure
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

def odds2a(proportion, tolerance=0.01):
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

def coarse_round(n, acceptable_n):
    diff = [abs(n - item) for item in acceptable_n]
    return acceptable_n[diff.index(min(diff))]

def fraction2(proportion):
    print("fraction2", proportion)
    acceptable_d = collections.OrderedDict()
    for a in [1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
        for b in [1, 2, 5, 10]:
            acceptable_d[a * b] = None
    for c in [7, 9, 11, 13, 14, 17, 18, 19, 38, 52, 70, 71, 80, 90]:
        acceptable_d[c] = None

    acceptable_n_s = set()
    for a in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        for b in [0, 1, 2, 5, 7, 10]:
            acceptable_n_s.add(a * b)          
    acceptable_n = sorted(list(acceptable_n_s))

    candidates = sorted(list(acceptable_d.keys()))
    scaled = [item * proportion for item in candidates]
    rounded2 = [coarse_round(item, acceptable_n) for item in scaled] # Consider coarser rounding
    diff = [round(abs(item - coarse_round(item, acceptable_n))/max(0.0001,item), 5) for item in scaled]
    best = diff.index(min(diff))
    fraction = Fraction(int(rounded2[best]), int(candidates[best]))
    return fraction


def odds2(prop, tolerance=0.01):
    odds_on = False
    if prop > 0.5:
        odds_on = True
        prop = 1 - prop
    if prop == 0:
        return (1,0)
    if prop ==1:
        return (0,1)

    proportion = prop / (1-prop)

    scale_up = 1
    if proportion < 0.01:
        while proportion < 0.01:
            scale_up = scale_up * 100
            proportion = proportion * 100


    acceptable_d = collections.OrderedDict()
    for a in [1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
        for b in [1, 2, 5, 10]:
            acceptable_d[a * b] = None
    for c in [7, 9, 11, 13, 14, 17, 18, 19, 36, 37, 51, 70, 80, 90]:
        acceptable_d[c] = None
    
    acceptable_n_s = set()
    for a in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        for b in [1, 2, 3, 4, 5]:
            acceptable_n_s.add(a * b)          
    acceptable_n = sorted(list(acceptable_n_s))

    candidates = sorted(list(acceptable_d.keys()))
    scaled = [item * proportion for item in candidates]
    rounded = [round(item, 0) for item in scaled] # Consider coarser rounding
    rounded2 = [coarse_round(item, acceptable_n) for item in scaled] # Consider coarser rounding
    diff0 = [round(abs(item - round(item, 0))/item, 5) for item in scaled]
    diff = [round(abs(item - coarse_round(item, acceptable_n))/item, 5) for item in scaled]
    best = diff.index(min(diff))
    fraction = Fraction(int(rounded2[best]), int(candidates[best]))
    if odds_on:
        return (fraction.numerator, fraction.denominator * scale_up)    
    return (fraction.denominator * scale_up, fraction.numerator)
    #print([abs(item - round(item * proportion)) for item in candidates])




def round_sigfigs(amount, level=1):
    scale = int(math.log10(amount))
    rounded = round(amount/10**(scale-level))
    return rounded * 10**(scale-level)

def format_round_sigfigs(amount, level=1):
    if amount == 0:
        return "0"
    scale = math.ceil(math.log10(amount)+0.00000000001)
    print(math.log10(amount)-0.000000001, scale)
    rounded = round(amount/10**(scale-level))
    if scale < 0:
        return(''.join(["0.", "0"*(-(scale)), str(rounded).strip("0")]))
    return(str(rounded * 10**(scale-level)))


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
            return name, params.replace(":",',')
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

def get_single_prob_summary(args):
    probability, prob, label, items = args
    calc_hits = prob * items
    survival_prob = 1
    try:
        calc_wait = 1 / prob
    except:
        calc_wait = 0
    try:
        fraction = Fraction(prob).limit_denominator(1000)
    except:
        fraction = Fraction(0)
    fraction = fraction2(prob)
    try:
        odds_raw = odds2(prob, tolerance=0.0005)
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
        "hits": calc_hits,
        "hits_text": label,
        "wait": calc_wait,
        "survival_prob":1,
        "equivalents":equivalents
        }

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

    #try:
    #    fraction = Fraction(prob).limit_denominator(1000)
    #except:
    #    fraction = Fraction(0)

    fraction = fraction2(prob)

    try:
        odds_raw = odds2(prob, tolerance=0.0005)
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
    #print("equiv")
    #print(equivalents)
    return {
        "repeat_mode": repeat_mode,
        "hits": calc_hits,
        "hits_item": calc_hits_item,
        "hits_text": label,
        "wait": calc_wait,
        "survival_prob":1,
        "equivalents":equivalents
        }

