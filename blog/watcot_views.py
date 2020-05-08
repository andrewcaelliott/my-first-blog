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
from .forms import ChanceForm 
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
from .chance_utils import fillcolours, drawgrid, odds2, do_trial,parse_probability, distribution,summary
from .chance_utils import compute_chance_grid,draw_chance_grid,draw_count_grid

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

