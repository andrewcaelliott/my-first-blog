from math import sqrt
from json import loads
from fractions import Fraction
from random import choice,seed as set_seed,randint,sample
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django import forms
from .models import Post
from .models import NumberFact
from .models import ChanceFact
from .models import NumberQuery
from .utils import numberFactsLikeThis,biggestNumberFact, smallestNumberFact,spuriousFact,neatFacts, facts_matching_ratio, resolve_country_code, get_all_stats_for, get_stat
from .forms import PostForm 
from .forms import FactForm 
from .forms import QueryForm 
from .forms import ChanceForm, SimpleChanceForm, SingleChanceForm, ScreenChanceForm 
from .chance_case import SimpleChanceCase, SingleChanceCase, ScreenChanceCase
from .forms import FreeForm,FreeFormCountry
from .forms import ConvertForm 
from .forms import FilterFactsForm 
from .convert import convertToDefaultBase 
from .convert import convertToDefault
from .convert import convertToUnit 
from .config import reference_lists
from .config import unit_choice_lists
from .config import quip_lists, choose_quote
from .config import conversion_target_lists
from .config import conversion_quip_lists
from .utils import num
from .utils import get_article
from .utils import parseBigNumber, randomFact, resolve_link, poke_link, save_links, summarise_country_list, make_number2
from django.utils.text import slugify
from .dummycontent import storySelection
from .tumblr import tumblrSelection
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from .chance_utils import odds2, do_trial,parse_probability, distribution,summary
from .chance_utils import compute_chance_grid, get_prob_summary, get_single_prob_summary, collect_lower, collect_left, collect_all, collect_corner
from .grid_utils import draw_chance_grid, draw_count_grid, get_palette, draw_grid_legend
from .utils import getParamDefault
from user_agents import parse

contexts = ["nitn", "ftlon", "ggb", "lmk"]
titles = [""]

def watcot_home(request):
    freeForm = FreeForm()
    freeForm.fields["number"].label="What are the chances of this?"
    widgets = []
    for section in ["news", "chance", "education"]:
        widget = buildSection(section)
        widgets += [widget]
    dyk=spuriousFact(NumberFact,3)  
    promote = choice(["watcot-book"])
    return render(request, 'blog/watcot_home.html', {'widgets':sample(widgets,3), 'freeForm':freeForm, 'quote': choose_quote('s'), "dyk":dyk, "promote":promote})

def buildSection(section):
    widget = {}
    if section == "news":
        widget["title"] = "Numbers In The News"
        widget["subtitle"] = "Notable numbers we have spotted recently"
        widget["context"] = "nitn"
    elif section == "passion":
        widget["title"] = "For the Love of Numbers"
        widget["subtitle"] = "Number-led writings for the truly geeky"
        widget["context"] = "ftlon"
    elif section == "education":
        widget["title"] = "Getting to Grips with Big"
        widget["subtitle"] = "Stop worrying and learn to love big numbers"
        widget["context"] = "ggb"
    elif section == "chance":
        widget["title"] = "The Uncertain World"
        widget["subtitle"] = "Chance would be a fine thing"
        widget["context"] = "tuw"
    else:
        widget["title"] = "Landmark Numbers"
        widget["subtitle"] = "Prominent and memorable numbers"
        widget["context"] = "lmk"

    widget["stories"] = tumblrSelection(section)
    return widget



def article(article_name, request):
    content=get_article(article_name)
    dyk=spuriousFact(NumberFact,3)
#    promote = choice(["sponsor","donate"])
#    return render(request, 'blog/article.html', {'quote': choose_quote('s'), 'article_title':title, 'article_subtitle':subtitle, "content": content, "dyk":dyk})
    return render(request, 'blog/watcot_article.html', {'quote': choose_quote('s'), "content": content, "dyk":dyk})

def chance_fact_list(request):
    params = request.GET
    try: 
        search = params["search"]
    except:
        search = None
    if search == None:
        facts = ChanceFact.objects.filter(fact_type = 'fact').order_by('title')  
    else:
        facts = ChanceFact.objects.filter(fact_type = 'fact', title__icontains = search).order_by('title')  
    form = FilterFactsForm(initial={'search': search})
    dyk=spuriousFact(NumberFact,3)
    promote = choice(["book", "book", "sponsor","donate","click"])
    return render(request, 'blog/chancefact_list.html', {'fact_type': 'chances', 'form': form, 'facts':facts, 'quote': choose_quote('n'), "dyk":dyk, "promote":promote})

def chance_example_list(request):
    params = request.GET
    try: 
        search = params["search"]
    except:
        search = None
    if search == None:
        facts = ChanceFact.objects.filter(fact_type = 'example').order_by('title')  
    else:
        facts = ChanceFact.objects.filter(fact_type = 'example', title__icontains = search).order_by('title')  
    form = FilterFactsForm(initial={'search': search})
    dyk=spuriousFact(NumberFact,3)
    promote = choice(["book", "book", "sponsor","donate","click"])
    return render(request, 'blog/chancefact_list.html', {'fact_type': 'examples', 'form': form, 'facts':facts, 'quote': choose_quote('n'), "dyk":dyk, "promote":promote})



def chance(request):
    params = request.GET
    permlink = getParamDefault(params, "fact", None)
    if permlink:
        chanceFact = get_object_or_404(ChanceFact, permlink=permlink)
        form_style = chanceFact.page_type
    else:
        form_style = getParamDefault(params, "form_style", "smp")
    if form_style == 'smp':
        return chance_std(request)
    if form_style == 'adv':
        return chance_std(request)
    if form_style == 'sng':
        return chance_single(request)
    if form_style == 'scr':
        return chance_screen(request)
    
def chance_smp(request):
    params = request.GET
    user_agent = parse(request.META["HTTP_USER_AGENT"])
    case = SimpleChanceCase()
    return chance_base(request, params, user_agent, case, case.form_style, case.form)

def chance_single(request):
    params = request.GET
    user_agent = parse(request.META["HTTP_USER_AGENT"])
    case = SingleChanceCase()
    case.set_params(params)
    return chance_base(request, params, user_agent, case, case.form_style, case.form)

def chance_screen(request):
    params = request.GET
    user_agent = parse(request.META["HTTP_USER_AGENT"])
    case = ScreenChanceCase()
    return chance_base(request, params, user_agent, case, case.form_style, case.form)

def chance_base(request, params, user_agent, case, form_style, xform):
    aspect_default = 0.5 if (user_agent.is_mobile or user_agent.is_tablet) else 2
    aspect = float(getParamDefault(params, "aspect", aspect_default))
    case.set_params(params)
    items = case.items
    outcome_text = getParamDefault(params, "outcome_text", case.outcome_text)
    palette_name = case.palette
    description = "What are the chances of this?"
    permlink = getParamDefault(params, "fact", None)
    if permlink:
        chanceFact = get_object_or_404(ChanceFact, permlink=permlink)
        case.probability = chanceFact.probability
        if '|' in case.probability:
            case.probability, case.sensitivity, case.specificity = (case.probability.split('|')+["0.9", "0.9"])[:3]
        else:
            case.sensitivity = getParamDefault(params, "probability_a", getParamDefault(params, "number", "0.9"))
            case.specificity = getParamDefault(params, "probability_b", getParamDefault(params, "number", "0.9"))

        case.outcome_text = chanceFact.outcome_text
        items = ' '. join([str(chanceFact.exposed_items), chanceFact.item_text])
        case.items = items
        outcome_text = chanceFact.outcome_text
        description = chanceFact.title
    split_i = items.split(' ')
    item_num =int(split_i[0])
    item_text = ' '.join(split_i[1:])
    caseform = case.prepare_form()

    trial_probability = case.build_probability()
    outcome_text = outcome_text.replace(",", "|")
    probs = [parse_probability(pstr) for pstr in trial_probability.split('|')]
    print("probs", probs)
    classes = len(probs)
    if classes == 1:
        hitnames = [outcome_text]
    else:
        hitnames = outcome_text.split("|") if "|" in outcome_text else [' '.join(pair) for pair in zip([outcome_text] * classes, [str(i+1) for i in range(classes)])]

    paramsets = zip(trial_probability.split('|'), probs, hitnames, [item_num]*classes)
    summaries = [get_single_prob_summary(paramset) for paramset in paramsets]
    print("summaries", summaries)
    seed = randint(1,1000000)    
    exposure = item_num
    trial_repetitions = int(0.999+sqrt(exposure / aspect))
    trial_items = int(0.999+exposure / trial_repetitions)
    single_trial = {
        "items": trial_items,
        "item_text": item_text,
        "repetitions": trial_repetitions,
        "repetition_text": 'rows',
        "exposure": exposure,
        "repeat_mode": "repeats",
        "probability": trial_probability,
        "hits_text": outcome_text,
        "seed": seed,
    }
    trial_outcomes = do_trial(single_trial, params, seed = seed, include_none = False)
    for level, trial_outcome in trial_outcomes.items():
        trial_outcome["hit_name"] = "None" if level == 0 else hitnames[level-1]
        trial_outcome["hits"] = trial_outcome['hits']
        trial_outcome["exposure"] = single_trial['exposure']
        trial_outcome["hit_percentage"]= 100 * trial_outcome["hits"] / trial_outcome["exposure"]
        trial_outcome["expected_hits"]= 0 if level == 0 else summaries[level-1]['hits']
        trial_outcome["expected_percentage"]= 0 if level == 0 else summaries[level-1]['equivalents']['percentage']
    promote = choice(["watcot-book"])
    dyk = spuriousFact(NumberFact,3)
    return render(request, 'blog/chance_single.html', {'description': description, 
        'form': caseform, 'form_style': form_style, 'palette_name': palette_name,
        'params': params, 'summaries': summaries, 'trial':single_trial, 'trial_outcomes': [outcome for level, outcome in trial_outcomes.items()], 'quote': choose_quote('s'), "dyk":dyk, "promote":promote})
 
def chance_std(request):
    params = request.GET
    form_style = getParamDefault(params, "form_style", "smp")
    adv_form = ChanceForm()
    exposed_items = getParamDefault(params, "exposed_items", "100")
    item_text = getParamDefault(params, "item_text", "items")
    exposed_repetitions = getParamDefault(params, "exposed_repetitions", "100")
    repetitions = getParamDefault(params, "repetitions", "100 repetitions")
    repetition_text = getParamDefault(params, "repetition_text", "times")
    smp_form = SimpleChanceForm()
    items = getParamDefault(params, "items", "100 items")

    #chance_function = getParamDefault(params, "chance_function", "[constant(probability)]")
    probability = getParamDefault(params, "probability", getParamDefault(params, "number", "0.1"))
    outcome_text = getParamDefault(params, "outcome_text", "hits")
    repeat_mode = getParamDefault(params, "repeat_mode", "repeats")
    palette_name = getParamDefault(params, "palette_name", "default")
    target = getParamDefault(params, "calc_target", "hits")
    description = "What are the chances of this?"
    permlink = getParamDefault(params, "fact", None)
    if permlink:
        chanceFact = get_object_or_404(ChanceFact, permlink=permlink)
        probability = chanceFact.probability
        items = ' '. join([str(chanceFact.exposed_items), chanceFact.item_text])
        repetitions = ' '. join([str(chanceFact.exposed_repetitions), chanceFact.repetition_text])
        outcome_text = chanceFact.outcome_text
        repeat_mode = chanceFact.repeat_mode
        description = chanceFact.title

    split_i = items.split(' ')
    exposed_items =int(split_i[0])
    item_text = ' '.join(split_i[1:])
    split_r = repetitions.split(' ')
    exposed_repetitions =int(split_r[0])
    repetition_text = ' '.join(split_r[1:])

    adv_form.fields["probability"].initial = probability
    adv_form.fields["probability"].label = "Chances?"
    adv_form.fields["items"].initial = items
    adv_form.fields["items"].label = "Columns?"
    adv_form.fields["repetitions"].initial = repetitions
    adv_form.fields["repetitions"].label = "Rows?"
    adv_form.fields["repeat_mode"].initial = repeat_mode
    adv_form.fields["repeat_mode"].label = "repeats or removes?"
    adv_form.fields["palette_name"].initial = palette_name
    adv_form.fields["palette_name"].label = "Palette"
    adv_form.fields["outcome_text"].initial = outcome_text
    adv_form.fields["outcome_text"].label = "Outcomes?"
    adv_form.fields["form_style"].initial = 'adv'
    adv_form.fields['form_style'].widget = forms.HiddenInput()
    
    smp_form.fields["probability"].initial = probability
    smp_form.fields["probability"].label = "Chances?"
    smp_form.fields["items"].initial = items
    smp_form.fields["items"].label = "Columns?"
    smp_form.fields["repetitions"].initial = repetitions
    smp_form.fields["repetitions"].label = "Rows?"
    smp_form.fields["outcome_text"].initial = outcome_text
    smp_form.fields["outcome_text"].label = "Outcomes?"
    smp_form.fields["form_style"].initial = 'smp'
    smp_form.fields['form_style'].widget = forms.HiddenInput()

    probability=probability.replace(",", "|")
    outcome_text =outcome_text.replace(",", "|")
    probs = [parse_probability(pstr) for pstr in probability.split('|')]
    classes = len(probs)
    if classes == 1:
        hitnames = [outcome_text]
    else:
        hitnames = outcome_text.split("|") if "|" in outcome_text else [' '.join(pair) for pair in zip([outcome_text] * classes, [str(i+1) for i in range(classes)])]

    items = int(exposed_items)
    repetitions = int(exposed_repetitions)
    paramsets = zip(probability.split('|'), probs, hitnames, [items]*classes, [repetitions] * classes, [repeat_mode] * classes)

    summaries = [get_prob_summary(paramset) for paramset in paramsets]
    for summry in summaries:
        summry['palette_name'] = palette_name
    seed = randint(1,1000000)    
    trial = {
        "items": items,
        "item_text": item_text,
        "repetitions": repetitions,
        "repetition_text": repetition_text,
        "exposure": items * repetitions,
        "probability": probability,
        "repeat_mode": repeat_mode,
        "hits_text": outcome_text,
        "seed": seed,
    }
    trial_outcomes = do_trial(trial, params, repeat_mode=repeat_mode, seed = seed, include_none = False)
    for level, trial_outcome in trial_outcomes.items():
        trial_outcome["hit_name"] = "None" if level == 0 else hitnames[level-1]
        trial_outcome["item_hits"] = list(trial_outcome['x_hits'].values())
        trial_outcome["repetition_hits"] = list(trial_outcome['y_hits'].values())
        item_distribution = distribution(trial_outcome["item_hits"])
        trial_outcome["item_hits_distribution"]=[(k,v) for k,v in item_distribution.items()]
        trial_outcome["item_hits_summary"]=summary(item_distribution)
        repetition_distribution = distribution(trial_outcome["repetition_hits"])
        trial_outcome["repetition_hits_distribution"]=[(k,v) for k,v in repetition_distribution.items()]
        trial_outcome["repetition_hits_summary"]=summary(repetition_distribution)
        trial_outcome["exposure"] = trial['exposure']
        trial_outcome["hit_percentage"]= 100 * trial_outcome["hits"] / trial_outcome["exposure"]
        trial_outcome["expected_hits"]= 0 if level == 0 else summaries[level-1]['hits']
        trial_outcome["expected_percentage"]= 0 if level == 0 else summaries[level-1]['equivalents']['percentage']
    promote = choice(["watcot-book"])
    dyk = spuriousFact(NumberFact,3)
    return render(request, 'blog/chance.html', {'description': description, 
        'adv_form': adv_form, 'smp_form': smp_form, 'form_style': form_style,
        'params': params, 'summaries': summaries, 'trial':trial, 'trial_outcomes': [outcome for level, outcome in trial_outcomes.items()], 'quote': choose_quote('s'), "dyk":dyk, "promote":promote})



def basegrid(request):
    params = request.GET
    width = int(getParamDefault(params, "width", "20"))
    depth = int(getParamDefault(params, "depth", "1"))
    aspect = float(getParamDefault(params, "aspect", "10"))
    exposed = width * depth
    hits = int(getParamDefault(params, "hits", "5"))
    palette = get_palette(getParamDefault(params, "palette_name", "default"))
    invert = getParamDefault(params, "invert", "F")
    xy = getParamDefault(params, "xy", "F")
    surface = draw_count_grid(width, depth, hits, exposed, aspect=aspect, palette=palette, invert = invert.upper().find("T")>=0, xy = xy.upper().find("T")>=0)
    response = HttpResponse(content_type="image/png")
    surface.write_to_png(response)
    return response

def grid(request):
    stacked = 0
    params = request.GET
    width = int(getParamDefault(params, "width", "20"))
    aspect = float(getParamDefault(params, "aspect", "10"))
    depth = int(getParamDefault(params, "depth", "1"))
    exposed = int(getParamDefault(params, "exposed", width*depth))
    hits = int(getParamDefault(params, "hits", "5"))
    colour = int(getParamDefault(params, "colour", "0"))
    frame_aspect = aspect
    '''
    if hits > 0 :
        while (hits / exposed) < 0.00099:
            print(exposed, hits, width, depth)
            if exposed == (exposed // 1000) *1000:
                width = width // 1000
                exposed = exposed // 1000
                stacked += 1
            else:
                width = width // 100
                exposed = exposed // 100
                hits = hits * 10
                stacked += 1
    '''
    if hits > 0:
        print(hits, exposed)
        if (hits / exposed) < 1/1001.0:
            aspect = 1
            width = 10
            depth = 10
            this_exp = exposed
            next_exp = exposed / (width * depth) 
            while (hits / this_exp) < 1/101.0:
                stacked +=1
                this_exp = next_exp
                next_exp = this_exp / (width * depth) 
            print(hits, exposed, this_exp)
            hits = round(hits * round(this_exp) / this_exp)
            exposed = round(this_exp)
            #hits = round(hits * 1000 / this_exp)
            #exposed = 1000
            print(hits, exposed)
            fraction = Fraction(hits, exposed).limit_denominator(100)   
            hits = fraction.numerator
            exposed = fraction.denominator
            #print(hits, exposed)
            
            #odds = odds2(hits/exposed)
            #hits = odds[1]
            #exposed = odds[0]+odds[1]

        print(hits, exposed)


    palette = get_palette(getParamDefault(params, "palette_name", "default"))
    invert = getParamDefault(params, "invert", "F")
    xy = getParamDefault(params, "xy", "F")
    cutoff = 100
    if stacked == 0:
        cutoff = 100
        if exposed > cutoff and depth == 1:
            depth = int((exposed+cutoff - 1) / cutoff)
            width = int(exposed / depth +0.999)
    else:
        cutoff = 10
        if True:
        #if exposed > cutoff:
            depth = int((exposed+cutoff - 1) // cutoff)
            width = int(exposed / depth +0.999)
        print(hits, exposed, cutoff, depth, width)
    surface = draw_count_grid(width, depth, hits, exposed, aspect=aspect, frame_aspect=frame_aspect, palette=palette, invert = invert.upper().find("T")>=0, xy = xy.upper().find("T")>=0, stacked=stacked, colour=colour)
    response = HttpResponse(content_type="image/png")
    surface.write_to_png(response)
    return response

def gridchance(request):
    params = request.GET
    width = int(getParamDefault(params, "width", "20"))
    depth = int(getParamDefault(params, "depth", "10"))
    exposure = int(getParamDefault(params, "exposure", str(width * depth)))
    repeat_mode = getParamDefault(params, "repeat_mode", "repeats")
    display = getParamDefault(params, "display", "default")
    palette = get_palette(getParamDefault(params, "palette_name", "default"))
    top_down_param = getParamDefault(params, "top_down", "false")
    top_down = top_down_param.lower()[0] == "t"
    try:
        seed = int(getParamDefault(params, "seed", None))
    except:
        seed = None
    probability = getParamDefault(params, "probability", "0.1")
    level_counts, grid = compute_chance_grid(width, depth, exposure, probability, params, repeat_mode=repeat_mode, seed=seed)
    if display == 'collect_lower':
        grid = collect_lower(grid)
    if display == 'collect_left':
        grid = collect_left(grid)
    if display == 'sort_lower':
        grid = collect_lower(grid, sort=True)
    if display == 'sort_left':
        grid = collect_left(grid, sort=True)
    if display == 'collect_all':
        grid = collect_all(grid, sort=True)
    if display == 'collect_corner':
        grid = collect_corner(grid, sort=True)
    #count, count_items, count_repetitions, grid = compute_chance_grid(width, depth, probability, params, repeat_mode = repeat_mode, seed=seed)
    surface = draw_chance_grid(grid, width, depth, palette=palette, top_down = top_down)
    response = HttpResponse(content_type="image/png")
    surface.write_to_png(response)
    return response

def gridlegend(request):
    params = request.GET
    hit_type = int(getParamDefault(params, "hit_type", 1))
    palette = get_palette(getParamDefault(params, "palette_name", "default"))
    surface = draw_grid_legend(hit_type, palette=palette)
    response = HttpResponse(content_type="image/png")
    surface.write_to_png(response)
    return response
