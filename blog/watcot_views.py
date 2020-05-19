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
from .config import quip_lists,quotes
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
from .chance_utils import compute_chance_grid
from .grid_utils import draw_chance_grid, draw_count_grid, get_palette
from .utils import getParamDefault

contexts = ["nitn", "ftlon", "ggb", "lmk"]
titles = [""]

def watcot_home(request):
    freeForm = FreeForm()
    freeForm.fields["number"].label="What are the chances of that?"
    widgets = []
    for section in ["news", "passion", "education", "landmark"]:
        widget = buildSection(section)
        widgets += [widget]
    dyk=spuriousFact(NumberFact,3)  
    promote = choice(["watcot-book"])
    return render(request, 'blog/watcot_home.html', {'widgets':sample(widgets,3), 'freeForm':freeForm, 'quote': choice(quotes), "dyk":dyk, "promote":promote})

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
#    return render(request, 'blog/article.html', {'quote': choice(quotes), 'article_title':title, 'article_subtitle':subtitle, "content": content, "dyk":dyk})
    return render(request, 'blog/watcot_article.html', {'quote': choice(quotes), "content": content, "dyk":dyk})

def chance(request):
    params = request.GET
    adv_form = ChanceForm()
    exposed_items = getParamDefault(params, "exposed_items", "100")
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

    chance_function = getParamDefault(params, "chance_function", "[constant(probability)]")
    probability = getParamDefault(params, "probability", getParamDefault(params, "number", "0.1"))
    outcome_text = getParamDefault(params, "outcome_text", "hits")
    repeat_mode = getParamDefault(params, "repeat_mode", "repeats")
    palette_name = getParamDefault(params, "palette", "default")
    target = getParamDefault(params, "calc_target", "hits")
    description = "this"
    permlink = getParamDefault(params, "fact", None)
    if permlink:
        chanceFact = get_object_or_404(ChanceFact, permlink=permlink)
        probability = chanceFact.probability
        exposed_items = chanceFact.exposed_items
        item_text = chanceFact.item_text
        exposed_repetitions = chanceFact.exposed_repetitions
        repetition_text = chanceFact.repetition_text
        outcome_text = chanceFact.outcome_text
        repeat_mode = chanceFact.repeat_mode
        description = chanceFact.title

    adv_form.fields["probability"].initial = probability
    adv_form.fields["probability"].label = "Chance"
    adv_form.fields["chance_function"].initial = chance_function
    adv_form.fields["chance_function"].label = "Advanced"
    adv_form.fields["exposed_items"].initial = exposed_items
    adv_form.fields["exposed_items"].label = "How many things?"
    adv_form.fields["item_text"].initial = item_text
    adv_form.fields["item_text"].label = "What things are they?"
    adv_form.fields["exposed_repetitions"].initial = exposed_repetitions
    adv_form.fields["exposed_repetitions"].label = "Repeated how many times?"
    adv_form.fields["repetition_text"].initial = repetition_text
    adv_form.fields["repetition_text"].label = "Times are called?"
    adv_form.fields["repeat_mode"].initial = repeat_mode
    adv_form.fields["repeat_mode"].label = "repeats for "+item_text+" or removes?"
    adv_form.fields["palette_name"].initial = palette_name
    adv_form.fields["palette_name"].label = "Palette"
    adv_form.fields["outcome_text"].initial = outcome_text
    adv_form.fields["outcome_text"].label = "Hits are called?"
    
    smp_form.fields["probability"].initial = probability
    smp_form.fields["probability"].label = "Chance"
    smp_form.fields["items"].initial = items
    smp_form.fields["items"].label = "How many things?"
    smp_form.fields["repetitions"].initial = repetitions
    smp_form.fields["repetitions"].label = "Repeated how many times?"

    prob = parse_probability(probability)
    items = int(exposed_items)
    repetitions = int(exposed_repetitions)

#    form.fields["calc_target"].initial = target
    if (target == 'hits'):
        if repeat_mode == "repeats":
            calc_hits = prob * items * repetitions
            calc_hits_item = prob * repetitions
            calc_wait = 1 / prob
        else:
            calc_wait = 1 / prob
            calc_hits = -1
            survival_prob = (1 - prob) ** repetitions
            calc_hits_item = (1 - survival_prob) * items

    fraction = Fraction(prob).limit_denominator(10000)
    odds_raw = odds2(prob, tolerance = 0.0005)
    odds_fraction = (odds_raw[1], (odds_raw[0] + odds_raw[1]))
    percentage = prob * 100
    seed = randint(1,1000000)    
    equivalents = {
        "supplied": probability,
        "probability": prob,
        "percentage": percentage,
        "fraction": fraction,
        "odds": odds_raw,
    }
    trial = {
        "items": items,
        "item_text": item_text,
        "repetitions": repetitions,
        "repetition_text": repetition_text,
        "exposure": items * repetitions,
        "probability": prob,
        "repeat_mode": repeat_mode,
        "calc_hits": calc_hits,
        "hits_text": outcome_text,
        "hit_wait": calc_wait,
        "seed": seed,
        "probability_model":"chance_function="+chance_function,
        "chance_function":chance_function,
    }
    print(trial)
    dyk = spuriousFact(NumberFact,3)
    trial["hits"], trial["item_hits"], trial["repetition_hits"] = do_trial(trial, params, repeat_mode=repeat_mode, seed = seed)
    trial["item_hits_distribution"]=distribution(trial["item_hits"])
    trial["item_hits_summary"]=summary(trial["item_hits_distribution"])
    trial["repetition_hits_distribution"]=distribution(trial["repetition_hits"])
    trial["repetition_hits_summary"]=summary(trial["repetition_hits_distribution"])
    trial["hit_percentage"]= 100 * trial["hits"] / trial["exposure"]
    promote = choice(["watcot-book"])
    return render(request, 'blog/chance.html', {'description': description, 
        'adv_form': adv_form, 'smp_form': smp_form, 'params': params, 'equivalents': equivalents, 'fraction': fraction, 'odds_fraction': odds_fraction, 'hits_item':calc_hits_item, 'trial':trial, 'quote': choice(quotes), "dyk":dyk, "promote":promote})



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
    params = request.GET
    width = int(getParamDefault(params, "width", "20"))
    aspect = float(getParamDefault(params, "aspect", "10"))
    depth = int(getParamDefault(params, "depth", "1"))
    exposed = int(getParamDefault(params, "exposed", width*depth))
    hits = int(getParamDefault(params, "hits", "5"))
    palette = get_palette(getParamDefault(params, "palette_name", "default"))
    invert = getParamDefault(params, "invert", "F")
    xy = getParamDefault(params, "xy", "F")
    cutoff = 100
    if exposed > cutoff and depth == 1:
        depth = int((exposed+cutoff - 1) / cutoff)
        width = int(exposed / depth +0.99)
    surface = draw_count_grid(width, depth, hits, exposed, aspect=aspect, palette=palette, invert = invert.upper().find("T")>=0, xy = xy.upper().find("T")>=0)
    response = HttpResponse(content_type="image/png")
    surface.write_to_png(response)
    return response

def gridchance(request):
    params = request.GET
    width = int(getParamDefault(params, "width", "20"))
    depth = int(getParamDefault(params, "depth", "10"))
    repeat_mode = getParamDefault(params, "repeat_mode", "repeats")
    palette = get_palette(getParamDefault(params, "palette_name", "default"))
    top_down_param = getParamDefault(params, "top_down", "false")
    top_down = top_down_param.lower()[0] == "t"
    try:
        seed = int(getParamDefault(params, "seed", None))
    except:
        seed = None
    probability = num(getParamDefault(params, "probability", "0.1"))
    count, count_items, count_repetitions, grid = compute_chance_grid(width, depth, probability, params, repeat_mode = repeat_mode, seed=seed)
    surface = draw_chance_grid(grid, width, depth, palette=palette, top_down = top_down)
    response = HttpResponse(content_type="image/png")
    surface.write_to_png(response)
    return response
