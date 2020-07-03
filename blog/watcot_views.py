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
from .forms import ChanceForm, SimpleChanceForm 
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
from .chance_utils import compute_chance_grid, get_prob_summary, collect_lower, collect_left, collect_all, collect_corner
from .grid_utils import draw_chance_grid, draw_count_grid, get_palette
from .utils import getParamDefault

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

def chance(request):
    params = request.GET
    adv_form = ChanceForm()
    exposed_items = getParamDefault(params, "exposed_items", "100")
    form_style = getParamDefault(params, "form_style", "smp")
    item_text = getParamDefault(params, "item_text", "items")
    exposed_repetitions = getParamDefault(params, "exposed_repetitions", "100")
    repetition_text = getParamDefault(params, "repetition_text", "times")
    smp_form = SimpleChanceForm()
    items = getParamDefault(params, "items", "100 items")
    split_i = items.split(' ')
    exposed_items =int(split_i[0])
    item_text = ' '.join(split_i[1:])
    repetitions = getParamDefault(params, "repetitions", "100 repetitions")
    split_r = repetitions.split(' ')
    exposed_repetitions =int(split_r[0])
    repetition_text = ' '.join(split_r[1:])

    #chance_function = getParamDefault(params, "chance_function", "[constant(probability)]")
    probability = getParamDefault(params, "probability", getParamDefault(params, "number", "0.1"))
    outcome_text = getParamDefault(params, "outcome_text", "hits")
    repeat_mode = getParamDefault(params, "repeat_mode", "repeats")
    palette_name = getParamDefault(params, "palette_name", "default")
    target = getParamDefault(params, "calc_target", "hits")
    description = "this"
    permlink = getParamDefault(params, "fact", None)
    if permlink:
        chanceFact = get_object_or_404(ChanceFact, permlink=permlink)
        probability = chanceFact.probability
        items = ' '. join([str(chanceFact.exposed_items), chanceFact.item_text])
        repetitions = ' '. join([str(chanceFact.exposed_repetitions), chanceFact.repetition_text])
        outcome_text = chanceFact.outcome_text
        repeat_mode = chanceFact.repeat_mode
        description = chanceFact.title

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

    probs = [parse_probability(pstr) for pstr in probability.split('|')]
    classes = len(probs)
    hitnames = outcome_text.split("|") if "|" in outcome_text else [outcome_text] * classes

    items = int(exposed_items)
    repetitions = int(exposed_repetitions)
    paramsets = zip(probability.split('|'), probs, hitnames, [items]*classes, [repetitions] * classes, [repeat_mode] * classes)

    summaries = [get_prob_summary(paramset) for paramset in paramsets]
    summarised = summaries[0]
    seed = randint(1,1000000)    
    trial = {
        "items": items,
        "item_text": item_text,
        "repetitions": repetitions,
        "repetition_text": repetition_text,
        "exposure": items * repetitions,
        "probability": probability,
        "repeat_mode": repeat_mode,
        #"calc_hits": calc_hits,
        "hits_text": outcome_text,
        #"hit_wait": calc_wait,
        "seed": seed,
        #"probability_model":"chance_function="+chance_function,
        #"chance_function":chance_function,
    }
    dyk = spuriousFact(NumberFact,3)
    trial_outcomes = do_trial(trial, params, repeat_mode=repeat_mode, seed = seed, include_none = False)
    for level, trial_outcome in trial_outcomes.items():
        trial_outcome["hit_name"] = "None" if level == 0 else hitnames[level-1]
        trial_outcome["item_hits"] = trial_outcome['x_hits'].values()
        trial_outcome["repetition_hits"] = trial_outcome['y_hits'].values()
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
    if hits > 0 :
        print("adjusting")
        while (hits / exposed) < 0.0009:
            if exposed == (exposed // 1000) *1000:
                width = width // 1000
                exposed = exposed // 1000
                stacked += 1
            else:
                width = width // 100
                exposed = exposed // 100
                hits = hits * 10
                stacked += 1

    palette = get_palette(getParamDefault(params, "palette_name", "default"))
    invert = getParamDefault(params, "invert", "F")
    xy = getParamDefault(params, "xy", "F")
    cutoff = 100
    if exposed > cutoff and depth == 1:
        depth = int((exposed+cutoff - 1) / cutoff)
        width = int(exposed / depth +0.99)
    surface = draw_count_grid(width, depth, hits, exposed, aspect=aspect, palette=palette, invert = invert.upper().find("T")>=0, xy = xy.upper().find("T")>=0, stacked=stacked, colour=colour)
    response = HttpResponse(content_type="image/png")
    surface.write_to_png(response)
    return response

def gridchance(request):
    params = request.GET
    width = int(getParamDefault(params, "width", "20"))
    depth = int(getParamDefault(params, "depth", "10"))
    repeat_mode = getParamDefault(params, "repeat_mode", "repeats")
    display = getParamDefault(params, "display", "default")
    palette = get_palette(getParamDefault(params, "palette_name", "default"))
    top_down_param = getParamDefault(params, "top_down", "false")
    top_down = top_down_param.lower()[0] == "t"
    top_down_param = getParamDefault(params, "top_down", "false")
    try:
        seed = int(getParamDefault(params, "seed", None))
    except:
        seed = None
    probability = getParamDefault(params, "probability", "0.1")
    level_counts, grid = compute_chance_grid(width, depth, probability, params, repeat_mode = repeat_mode, seed=seed)
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

