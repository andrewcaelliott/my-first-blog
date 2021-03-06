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
from .chance_utils import compute_chance_grid
from .grid_utils import draw_chance_grid, draw_count_grid, get_palette
from .watcot_views import watcot_home, article as watcot_article
from .utils import getParamDefault

contexts = ["nitn", "ftlon", "ggb", "lmk"]
titles = [""]


def itabn_home(request):
    freeForm = FreeForm()
    freeForm.fields["number"].label="Is this a big number?"
    widgets = []
    for section in ["news", "passion", "education", "landmark"]:
        widget = buildSection(section)
        widgets += [widget]
    dyk=spuriousFact(NumberFact,3)  
    promote = choice(["book", "book2", "book3","book4","book5"])
    return render(request, 'blog/home.html', {'widgets':sample(widgets,3), 'freeForm':freeForm, 'quote': choose_quote('n'), "dyk":dyk, "promote":promote})

def home(request):
    host =request.build_absolute_uri()
    if host.find('chance')>=0:
        return watcot_home(request)
    return itabn_home(request)


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

def homealt(request):
    freeForm = FreeForm()
    widgets = []
    stories = {}
    stories["news"]=storySelection("news")
    stories["passion"]=storySelection("passion")
    stories["education"]=storySelection("education")
    stories["landmark"]=storySelection("landmark")
    return render(request, 'blog/home-alt.html', {'widgets':random.sample(widgets,3), 'freeForm':freeForm, 'quote': choose_quote('n'), 'stories':stories})

def blog(category, request):
    params = request.GET

    try:
       topstory = params["topstory"]
    except :
        topstory = None
    stories=tumblrSelection(category, topstory)
    titles = {
        "news":"Numbers In The News", 
        "passion":"For the Love of Numbers", 
        "education":"Getting to Grips with Big", 
        "landmark":"Landmark Numbers",
        "chance":"The Uncertain World"
    }
    subtitles = {
        "news":"Some notable numbers we have spotted recently", 
        "passion":"A number-led selection of writings for the truly geeky among us ...", 
        "education":"How to stop worrying and learn to love big numbers", 
        "landmark":"Prominent and memorable numbers show the way like landmarks on the horizon",
        "chance":"Chance would be a fine thing"
    }
    if category == "chance":
        template = "blog/watcot_blog.html"
    else:
        template = "blog/blog2.html"
    dyk = spuriousFact(NumberFact,3)
    promote = choice(["book", "book", "sponsor","donate","click"])
    return render(request, template, {'quote': choose_quote('n'), 'stories':stories, 'blog_title':titles[category], 'blog_subtitle':subtitles[category], "dyk":dyk, "promote":promote})

def blog_flton(request):
    return blog("passion", request)

def blog_nitn(request):
    return blog("news", request)

def blog_ggb(request):
    return blog("education", request)

def blog_lmk(request):
    return blog("landmark", request)

def blog_tuw(request):
    return blog("chance", request)


def article(article_name, request):
    host =request.build_absolute_uri()
    if host.find('chance')>=0:
        return watcot_article(article_name, request)
    return itabn_article(article_name, request)


def itabn_article(article_name, request):
    content=get_article(article_name)
    dyk=spuriousFact(NumberFact,3)
#    promote = choice(["sponsor","donate"])
#    return render(request, 'blog/article.html', {'quote': choose_quote('n'), 'article_title':title, 'article_subtitle':subtitle, "content": content, "dyk":dyk})
    return render(request, 'blog/article.html', {'quote': choose_quote('n'), "content": content, "dyk":dyk})



def article_sponsor(request):
    return article("ITABN-Sponsors.md", request)

def article_badlink(request):
    host =request.build_absolute_uri()
    if host.find('chance') >= 0:
        return article("WATCOT-Bad-Link.md", request)
    return article("ITABN-Bad-Link.md", request)

def article_gen(request, article_name):
    article_name = article_name+".md"
    return article(article_name, request)


def ratio(request):
    params = request.GET
    try:
        measure = params["measure"]
    except:
        measure ="extent"
    try:
        ratio_str = params["number"].replace("to",":")
        if ratio_str.find(":")>=0:
            ratio_num, ratio_den = ratio_str.split(":")
            ratio = num(ratio_num)/num(ratio_den)
        else:
            ratio = num(ratio_str)
            ratio_str = ratio_str + " : 1"
    except:
        ratio, ratio_str = choice([(1, "1 : 1"), (2, "2 : 1"), (5, "5 : 1"),  (10, "10 : 1"), (100, "100 : 1"), (1000, '1000 : 1')])
        #ratio = 1000
        #ratio_str = '1000 : 1'
    freeForm = FreeForm()
    freeForm.fields["number"].label="Ratio"
    freeForm.fields["number"].initial=ratio_str
    ratio_pairs = facts_matching_ratio(NumberFact, measure, ratio, 5, tolerance = 0.02)
    dyk=spuriousFact(NumberFact,3)
    promote = choice(["book", "book", "sponsor","donate","click"])
    return render(request, 'blog/ratio.html', {'form': freeForm, 'ratio_str': ratio_str, 'ratio':ratio, 'ratio_pairs':ratio_pairs, 'quote': choose_quote('n'), "dyk":dyk, "promote":promote})

def make_spec(bestComparisons, comparison, measure):
    fact_slugs=[]
    for fact in bestComparisons:
        fact_slugs = fact_slugs+[slugify(fact.title)]
    return ",".join([measure, comparison]+fact_slugs)

def quiz_from_spec(seed, spec):
    spec_list= spec.split(",")
    measure = spec_list[0]
    comparison = spec_list[1]
    option_slugs = spec_list[2:6]
    if len(option_slugs)>0:
        options = []
        for slug in option_slugs:
            options = options+[get_object_or_404(NumberFact, permlink=slug)]
    else:
        rf, options = options_from_seed(seed, measure)

    quiz = {"options":options, "comparison":comparison, "measure":measure}
    quiz["seed"] = seed
    return quiz

def options_from_seed(seed, measure):
    rf = randomFact(NumberFact, measure, rseed=seed)
    bestComparisons, tolerance, score  = numberFactsLikeThis(NumberFact, rf, rseed=seed) 
    while len(bestComparisons)<4:
        seed = randint(0,10000000)
        rf = randomFact(NumberFact, measure, rseed=seed)
        bestComparisons, tolerance, score  = numberFactsLikeThis(NumberFact, rf, rseed=seed) 
    return rf, bestComparisons

def quiz_from_seed(seed, params):
    quiz={}
    set_seed(seed)    
    askbiggest = randint(0,1)==0
    if askbiggest:
        quiz["comparison"]="biggest"
    else:
        quiz["comparison"] = "smallest"
    try:
        measure=params.get("measure")
    except (AttributeError,TypeError):
        measure=None
    if measure==None or measure == "random":
        measure=choice(["extent", "count", "amount!", "duration", "mass", "speed"])

    quiz["measure"]=measure
    quiz["seed"] = seed
    rf, bestComparisons = options_from_seed(seed, measure)
    quiz["hint"] = rf.render
    quiz["options"]=bestComparisons
    return quiz
    

def quiz(request):
    params = request.POST
    if len(params)==0:
        params = request.GET
    abs_uri = request.build_absolute_uri()            
    protocol, uri = abs_uri.split("://")
    site = protocol+"://"+uri.split("/")[0]+"/"
    try:
        cycle=params.get("cycle")
    except (AttributeError,TypeError):
        cycle="initial"
    try:
        force_reveal=params.get("reveal")=="true"
    except (AttributeError,TypeError):
        force_reveal=False
    try:
        saveas=params.get("saveas")
    except (AttributeError,TypeError):
        saveas=None

    try:
        seed=num(params.get("seed"))
    except (AttributeError,TypeError):
        set_seed()
        seed = randint(0,10000000)
    if seed == None:
        set_seed()
        seed = randint(0,10000000)


    try:
        spec=request.GET.get("spec")
        if spec==None:
            spec=params.get("spec")
        quiz = quiz_from_spec(seed, spec)
    except (AttributeError):
        spec = None
    if spec == None:
        quiz = quiz_from_seed(seed, params)
        
    spec = make_spec(quiz["options"], quiz["comparison"], quiz["measure"])

    measure = quiz["measure"]
    if quiz["comparison"]=="biggest":
        if measure.find("extent")>=0:
            quiz["question"]="Which of these is the biggest?"
        elif measure.find("count")>=0:
            quiz["question"]="Which of these is the most numerous?"
        elif measure.find("amount")>=0:
            quiz["question"]="Which of these is the greatest amount?"
        elif measure.find("duration")>=0:
            quiz["question"]="Which of these is the longest period of time?"
        elif measure.find("volume")>=0:
            quiz["question"]="Which of these has the greatest volume?"
        elif measure.find("area")>=0:
            quiz["question"]="Which of these has the greatest area?"
        elif measure.find("speed")>=0:
            quiz["question"]="Which of these is the fastest?"
        elif measure.find("energy")>=0:
            quiz["question"]="Which of these has the most energy?"
        elif measure.find("mass")>=0:
            quiz["question"]="Which of these has the greatest mass?"
        else:
            quiz["question"]="Which of these is biggest?"
    else:
        if measure.find("extent")>=0:
            quiz["question"]="Which of these is the smallest?"
        elif measure.find("count")>=0:
            quiz["question"]="Which of these is the least numerous?"
        elif measure.find("amount")>=0:
            quiz["question"]="Which of these is the smallest amount?"
        elif measure.find("duration")>=0:
            quiz["question"]="Which of these has the shortest period of time?"
        elif measure.find("volume")>=0:
            quiz["question"]="Which of these has the smallest volume?"
        elif measure.find("area")>=0:
            quiz["question"]="Which of these has the least area?"
        elif measure=="duration":
            quiz["question"]="Which of these is the shortest period of time?"
        elif measure.find("speed")>=0:
            quiz["question"]="Which of these is the slowest?"
        elif measure.find("energy")>=0:
            quiz["question"]="Which of these has the least energy?"
        elif measure.find("mass")>=0:
            quiz["question"]="Which of these has the least mass?"
        else:
            quiz["question"]="Which of these is smallest?"
    permalink = site+"quiz/?spec="+spec
    if force_reveal:
        permalink+="&reveal=true"
    if saveas:
        poke_link(permalink, saveas)
    quiz["spec"]=spec
    if quiz["comparison"]=="biggest":
        answer = biggestNumberFact(quiz["options"])
    else: 
        answer = smallestNumberFact(quiz["options"])
    quiz["answer"]=answer.title
    if request.method == "POST":
        response = request.POST
        if response.get("option")==quiz["answer"] and cycle=="answered":
            quiz["assessment"] = str(response.get("option"))+" is the correct answer: Well done!"
            #quiz["question"]=""
            reveal = []
            for option in quiz["options"]:
                reveal.append({"title":option.render_folk, "link":option.link})
            quiz["options"]=reveal
            quiz["cycle"]="correct"
        elif cycle=="answered":
            quiz["assessment"] = str(response.get("option"))+" is not correct. Try again."
    if request.method == "GET":
        if force_reveal:
            reveal = []
            for option in quiz["options"]:
                reveal.append({"title":option.render_folk, "link":option.link})
            quiz["assessment"] = quiz["answer"]+" is the correct answer."
            quiz["options"]=reveal
            quiz["cycle"]="correct"

    else:   
        pass
#        form = FactForm()
 #   return render(request, 'blog/fact_edit.html', {'form': form})   
    dyk=spuriousFact(NumberFact,3,measure=quiz["measure"])
    promote = choice(["book", "book", "sponsor","donate","click"])
    return render(request, 'blog/quiz.html', {'quiz':quiz, 'permalink':permalink, 'quote': choose_quote('n'), "dyk":dyk, "promote":promote})

def itabn(request):
    freeForm = FreeForm()
    freeForm.fields["number"].label="Is this a big number?"
    extentForm = QueryForm(initial={'measure': 'e'})
    extentForm.fields['unit'].choices=unit_choice_lists['e']
    extentForm.fields['measure'].widget = forms.HiddenInput()
    countForm = QueryForm(initial={'measure': 'c'})
    countForm.fields['unit'].choices=unit_choice_lists['c']
    countForm.fields['measure'].widget = forms.HiddenInput()
    amountForm = QueryForm(initial={'measure': 'a'})
    amountForm.fields['unit'].choices=unit_choice_lists['a']
    amountForm.fields['measure'].widget = forms.HiddenInput()
    durationForm = QueryForm(initial={'measure': 'd'})
    durationForm.fields['unit'].choices=unit_choice_lists['d']
    durationForm.fields['measure'].widget = forms.HiddenInput()
    massForm = QueryForm(initial={'measure': 'm'})
    massForm.fields['unit'].choices=unit_choice_lists['m']
    massForm.fields['measure'].widget = forms.HiddenInput()
    widgets = [
        {"title":"How Big?","glyph":"glyphicon glyphicon-resize-horizontal","form":extentForm},
        {"title":"How Many?","glyph":"glyphicon glyphicon-th","form":countForm},
        {"title":"How Much?","glyph":"glyphicon glyphicon-usd","form":amountForm},
        {"title":"How Long?","glyph":"glyphicon glyphicon-time","form":durationForm},
        {"title":"How Heavy?","glyph":"glyphicon glyphicon-briefcase","form":massForm}]
    dyk=spuriousFact(NumberFact,3)
    promote = choice(["book", "book", "sponsor","donate","click"])
    return render(request, 'blog/itabn.html', {'widgets':widgets, 'freeForm':freeForm, 'quote': choose_quote('n'), "dyk":dyk, "promote":promote})

def query_answer(request, numberQuery, numberFact):
    query =  QueryForm(instance=numberQuery)
#    query.fields['magnitude'].value=numberQuery.magnitude
    query.fields['measure'].widget = forms.HiddenInput()

#    query =  FreeForm(request.GET)
#    magnitude, multiple, unit, measure = parseBigNumber(query["number"].value())
#    mag2, unit2 = convertToDefaultBase(magnitude, unit)
#    numberFact = make_number2(NumberFact, str(mag2), multiple, "Your number", measure, str(unit2))

    measure = numberQuery.measure
    answer = {"quip":choice(quip_lists[measure])}
    multiple = numberQuery.multiple
    if (multiple=='?'):
        answer["easteregg"]=numberQuery.unit
    query.fields['unit'].choices=unit_choice_lists[measure]
    references = reference_lists[measure]
    answer["comparisons"] = numberQuery.getComparisons(references)
    answer["closeMatches"] = numberQuery.getCloseMatches()
    answer["brackets"] = numberQuery.getBrackets()
    for match in answer["closeMatches"]:
        if match["text"] == answer["brackets"]["above"]:
            answer["closeMatches"].remove(match)
        if match["text"] == answer["brackets"]["below"]:
            answer["closeMatches"].remove(match)
#    question = numberQuery.render.replace("million","m").replace("billion","bn").replace("trillion","tn").replace("thousand","k").replace(" - "," ").replace(" i","")
    question = numberQuery.render.replace(" - "," ").replace("imperial","Imperial").replace(" i","").replace(" 10^","*10^")
    if (multiple=='?'):
        print("?",numberQuery.unit)
        if numberQuery.unit.find("?")>=0:
            easteregg={"question":numberQuery.unit}
        else:
            easteregg={"question":numberQuery.unit+"?"}
        print("?",easteregg)
        if numberQuery.unit.lower().find("graham")>=0:
            easteregg["answer"]="Graham's Number is a very big number indeed, way bigger than any context or comparison this site can offer."
        elif numberQuery.unit.lower().find("infinity")>=0:
            easteregg["answer"]="Sorry, this site does not (yet) deal in infinities. Check back later!"
        elif numberQuery.unit.lower().find("overflow")>=0:
            easteregg["question"] = numberQuery.unit.replace("_","").replace("overflow","")
            easteregg["answer"]="That IS a big number. In fact so big that I have nothing to compare it to. Sorry!"
        elif numberQuery.unit.lower().find("aleph")>=0:
            easteregg["answer"]="Sorry, this site does not (yet) deal in infinities. Check back later!"
        elif numberQuery.unit.lower().find("uncount")>=0:
            easteregg["answer"]="Sorry, this site does not (yet) deal in infinities. Check back later!"
        elif numberQuery.unit.lower().find("googleplex")>=0:
            easteregg["answer"]="Googleplex is the headquarters of Google. A googolplex, on the other hand, is 10^googol = 10 ^ (10^100), a very big number, bigger than any context or comparison this site can offer."
        elif numberQuery.unit.lower().find("googolplex")>=0:
            easteregg["answer"]="A googolplex is 10^googol = 10 ^ (10^100), a very big number, bigger than any context or comparison this site can offer."
        elif numberQuery.unit.lower().find("google")>=0:
            easteregg["answer"]="Google is a large technology company. A googol, on the other hand, is 10^100, a big number indeed."
        elif numberQuery.unit.lower().find("googol")>=0:
            easteregg["answer"]="A googol is 10^100, a big number indeed."
        elif numberQuery.unit.lower().find("illion")>=0:
            easteregg["answer"]="That ("+numberQuery.unit+") is very likely an indefinite hyperbolic numeral. That's big, but no one knows quite how big."
        else:
            easteregg["answer"]="I'm sorry, you have me stumped with that one."            
        answer["easteregg"]=easteregg
    #question = question.replace(" times ", " x ").replace(" the ", " ").replace(" distance ", " dist ")
    neat = neatFacts(NumberFact, numberFact)
    dyk=spuriousFact(NumberFact,3)
    promote = choice(["book", "book", "sponsor","donate","click"])
    numberFact.normalise()
    return render(request, 'blog/itabn_answer.html', {'query': query, 'question': question[3:]+"\n", 'answer':answer, 'neat':neat,'basefact': numberFact,'quote': choose_quote('n'), "dyk":dyk, "promote":promote})   

def query_answer_post(request):
    query =  QueryForm(request.POST)
    numberQuery = NumberQuery(magnitude=query["magnitude"].value(), multiple=query["multiple"].value(), unit=query["unit"].value(), measure=query["measure"].value())
    return query_answer(request,numberQuery)

def query_answer_get(request):
    query =  QueryForm(request.GET)
    numberQuery = NumberQuery(magnitude=query["magnitude"].value(), multiple=query["multiple"].value(), unit=query["unit"].value(), measure=query["measure"].value())
    #magnitude, multiple, unit, measure = parseBigNumber(query["number"].value())
    mag2, unit2 = convertToDefaultBase(numberQuery.magnitude, numberQuery.unit)
    numberFact = make_number2(NumberFact, str(mag2), numberQuery.multiple, "Your number", numberQuery.measure, str(unit2))
    return query_answer(request, numberQuery, numberFact)

def query_compare(request):
    query =  FreeForm(request.GET)
    magnitude, multiple, unit, measure = parseBigNumber(query["number"].value())
    print("number >>", query["number"].value())
    numberQuery = NumberQuery(magnitude=magnitude, multiple=multiple, unit=unit, measure=measure)
    mag2, unit2 = convertToDefaultBase(magnitude, unit)
    numberFact = make_number2(NumberFact, str(mag2), multiple, "Your number", measure, str(unit2))
    return query_answer(request, numberQuery, numberFact)

def query_compare2(request):
    query =  FreeForm(request.GET)
    magnitude, multiple, unit, measure = parseBigNumber(query["number"].value())
    mag2, unit2 = convertToDefaultBase(magnitude, unit)
    numberFact = make_number2(NumberFact, str(mag2), multiple, "Your number", measure, str(unit2))
    #numberFact = NumberFact(magnitude=magnitude, multiple=multiple, unit=unit, measure=measure)
    return query_answer2(request, numberFact)

def query_api(request):
        
    magnitude=params.get("magnitude")
    if magnitude==None:
        return JsonResponse({"success":"false", "message":"'magnitude' parameter missing"})
    unit=params.get("unit")
    if unit==None:
        return JsonResponse({"success":"false", "message":"'unit' parameter missing"})
    multiple=params.get("multiple")
    if multiple==None:
        return JsonResponse({"success":"false", "message":"'multiple' parameter missing"})
    measure=params.get("measure")
    if measure==None:
        return JsonResponse({"success":"false", "message":"'measure' parameter missing"})
    numberQuery = NumberQuery(magnitude=magnitude, multiple=multiple, unit=unit, measure=measure)
    references = reference_lists[measure]
    answer = {"quip":choice(quip_lists[measure])}
    answer["comparisons"] = numberQuery.getComparisons(references)
    return JsonResponse({
        'magnitude':str(magnitude), 
        'unit':str(unit), 
        'measure':str(measure), 
        'multiple':str(multiple), 
        'answer': answer, 
        })

def country(request):
    params = request.GET
    try:
        qnumber = params["number"]
    except:
        qnumber = None
    try:
        location = params["location"]
    except:
        location = "GB"
    freeForm = FreeFormCountry(initial = {"number":qnumber, "location": location})
    freeForm.fields["number"].label="Is this a big number?"
    freeForm.fields["location"].label=""
    dyk=spuriousFact(NumberFact,3)
    promote = choice(["book", "book", "sponsor","donate","click"])
    country = resolve_country_code(location)
    country_ask, country_list = summarise_country_list(NumberQuery, NumberFact, location, qnumber)
    panels = []
    for item in country_list:
        if item[0] == "Is That A Big Number?":
            panels+=[{"title":item[0], "facts":item[1:], "featured":True}]
        else:
            panels+=[{"title":item[0], "facts":item[1:]}]
    return render(request, 'blog/country.html', {
        'ask':country_ask, 'panels': panels, 'country_code':location, 'country':country, 
        'widgets':{}, 'freeForm':freeForm, 'quote': choose_quote('n'), "dyk":dyk, "promote":promote
        })

def stat(request, stat):
    params = request.GET
    dyk=spuriousFact(NumberFact,3)
    promote = choice(["book", "book", "sponsor","donate","click"])
    stats = get_stat(NumberFact, stat)
    statgroup, statname = stat.split(".")
    stats.reverse()
    maxval = max(map(lambda k: k[1].value*10**k[1].scale, stats))
    minval = min(map(lambda k: k[1].value*10**k[1].scale, stats))
    displaystats = list(map(lambda k:(resolve_country_code(k[0]), round(100*(k[1].value*10**k[1].scale-minval)/(maxval-minval),1), k[1].render_number), stats))
    return render(request, 'blog/stat.html', {
        #'ask':country_ask, 'panels': panels, 'country_code':location, 'country':country, 
        'widgets':{}, 'quote': choose_quote('n'), "dyk":dyk, "promote":promote, "stats":displaystats, "statname":statname,
        })



def convert(request):
    extentForm = ConvertForm(initial={'measure': 'ex'})
    extentForm.fields['unit'].choices=unit_choice_lists['ex']
    extentForm.fields['target_unit'].choices=unit_choice_lists['ex']
    extentForm.fields['measure'].widget = forms.HiddenInput()
    amountForm = ConvertForm(initial={'measure': 'am'})
    amountForm.fields['unit'].choices=unit_choice_lists['am']
    amountForm.fields['target_unit'].choices=unit_choice_lists['am']
    amountForm.fields['measure'].widget = forms.HiddenInput()
    durationForm = ConvertForm(initial={'measure': 'du'})
    durationForm.fields['unit'].choices=unit_choice_lists['du']
    durationForm.fields['target_unit'].choices=unit_choice_lists['du']
    durationForm.fields['measure'].widget = forms.HiddenInput()
    massForm = ConvertForm(initial={'measure': 'ma'})
    massForm.fields['unit'].choices=unit_choice_lists['ma']
    massForm.fields['target_unit'].choices=unit_choice_lists['ma']
    massForm.fields['measure'].widget = forms.HiddenInput()
    capacityForm = ConvertForm(initial={'measure': 'ca'})
    capacityForm.fields['unit'].choices=unit_choice_lists['ca']
    capacityForm.fields['target_unit'].choices=unit_choice_lists['ca']
    capacityForm.fields['measure'].widget = forms.HiddenInput()
    widgets = [
            {"title":"Convert Length","glyph":"glyphicon glyphicon-resize-horizontal","form":extentForm},
            {"title":"Convert Amount","glyph":"glyphicon glyphicon-usd","form":amountForm},
            {"title":"Convert Time","glyph":"glyphicon glyphicon-time","form":durationForm},
            {"title":"Convert Mass","glyph":"glyphicon glyphicon-briefcase","form":massForm},
            {"title":"Convert Capacity","glyph":"glyphicon glyphicon-briefcase","form":capacityForm},
        ]
    dyk=spuriousFact(NumberFact,3)
    promote = choice(["book", "book", "sponsor","donate","click"])
    return render(request, 'blog/convert.html', {'widgets':widgets, 'quote': choose_quote('n'), "dyk":dyk})

def conversion_answer(request, conversion):
    conversion.fields['measure'].widget = forms.HiddenInput()
    numberQuery = NumberQuery(magnitude=conversion["magnitude"].value(), multiple=conversion["multiple"].value(), unit=conversion["unit"].value(), target_unit=conversion["target_unit"].value(), measure=conversion["measure"].value())
    measure = conversion["measure"].value()
    answer = {"quip":choice(conversion_quip_lists[measure])}
    conversion.fields['unit'].choices=unit_choice_lists[measure]
    conversion.fields['target_unit'].choices=unit_choice_lists[measure]
    conversion_targets = [(numberQuery.target_unit),] + conversion_target_lists[measure]
    conversions = numberQuery.getConversions(conversion_targets)
    answer["requestedConversion"] = conversions[0]
    answer["otherConversions"] = conversions[1:]
    dyk=spuriousFact(NumberFact,4,measure=measure)
    promote = choice(["sponsor","donate"])
    return render(request, 'blog/conversion_answer.html', {'conversion': conversion, 'answer':answer, 'quote': choose_quote('n'), "dyk":dyk, "promote":promote})   

def conversion_answer_post(request):
    return conversion_answer(request, ConvertForm(request.POST))

def conversion_answer_get(request):
    return conversion_answer(request, ConvertForm(request.GET))

def conversion_base(request):
    params = request.GET
    magnitude=params.get("magnitude")
    if magnitude==None:
        return JsonResponse({"success":"false", "message":"'magnitude' parameter missing"})
    unit=params.get("unit")
    if unit==None:
        return JsonResponse({"success":"false", "message":"'unit' parameter missing"})
    base_magnitude, base_unit = convertToDefaultBase(magnitude, unit)
    return JsonResponse({
        'source_magnitude':str(magnitude), 
        'source_unit':str(unit), 
        'base_magnitude':str(base_magnitude), 
        'base_unit':str(base_unit), 
        'rendered': " ".join([str(base_magnitude), str(base_unit)]), 
        })

def conversion_unit(request):
    params = request.GET
    magnitude=params.get("magnitude")
    if magnitude==None:
        return JsonResponse({"success":"false", "message":"'magnitude' parameter missing"})
    unit=params.get("unit")
    if unit==None:
        return JsonResponse({"success":"false", "message":"'unit' parameter missing"})
    target_unit=params.get("target_unit")
    if target_unit==None:
        return JsonResponse({"success":"false", "message":"'target_unit' parameter missing"})
    target_magnitude, target_unit = convertToUnit(num(magnitude), unit, target_unit)
    return JsonResponse({
        'source_magnitude':str(magnitude), 
        'source_unit':str(unit), 
        'target_magnitude':str(target_magnitude), 
        'target_unit':str(target_unit), 
        'rendered': " ".join([str(magnitude), str(unit),'=',str(target_magnitude), str(target_unit)]), 
        })

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')  
    dyk=spuriousFact(NumberFact,3)
    promote = choice(["book", "book", "sponsor","donate","click"])
    return render(request, 'blog/post_list.html', {'posts':posts, "dyk":dyk})

def fact_list(request):
    params = request.GET
    try: 
        search = params["search"]
    except:
        search = None
    if search == None:
        facts = NumberFact.objects.filter().order_by('title')  
    else:
        facts = NumberFact.objects.filter(title__icontains = search).order_by('title')  
    form = FilterFactsForm(initial={'search': search})
    dyk=spuriousFact(NumberFact,3)
    promote = choice(["book", "book", "sponsor","donate","click"])
    return render(request, 'blog/fact_list.html', {'form': form, 'facts':facts, 'quote': choose_quote('n'), "dyk":dyk, "promote":promote})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    dyk=spuriousFact(NumberFact,3)
    promote = choice(["book", "book", "sponsor","donate","click"])
    return render(request, 'blog/post_detail.html', {'post': post, "dyk":dyk, "promote":promote})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:   
        form = PostForm()
    dyk=spuriousFact(NumberFact,3)
    promote = choice(["book", "book", "sponsor","donate","click"])
    return render(request, 'blog/post_edit.html', {'form': form, "dyk":dyk, "promote":promote})    

def query_answer2(request, fact):
    reflink=""
    ##fact=
    dyk=spuriousFact(NumberFact,3)
    promote = choice(["book", "book", "sponsor","donate","click"])
    neat = neatFacts(NumberFact, fact)
    permlink = fact.permlink
    return render(request, 'blog/fact_detail.html', {'fact': fact, 'reflink':reflink, 'quote': choose_quote('n'), "dyk":dyk, "neat":neat, "pl":permlink, "promote":promote})

def fact_detail(request, permlink):
    fact = get_object_or_404(NumberFact, permlink=permlink)
    if fact.text.rfind("http")>=0:
        reflink=fact.text
    else:
        reflink="http://www.google.com/?q="+fact.title
    dyk=spuriousFact(NumberFact,3)
    promote = choice(["book", "book", "sponsor","donate","click"])
    print("}}}", fact.render_folk_long, fact.measure)
    neat = neatFacts(NumberFact, fact)
    permlink = fact.permlink
    return render(request, 'blog/fact_detail.html', {'fact': fact, 'reflink':reflink, 'quote': choose_quote('n'), "dyk":dyk, "neat":neat, "pl":permlink, "promote":promote})

def fact_asunit(request, permlink):
    fact = get_object_or_404(NumberFact, permlink=permlink)
    print(fact)
    if fact.text.rfind("http")>=0:
        reflink=fact.text
    else:
        reflink="http://www.google.com/?q="+fact.title
    dyk=spuriousFact(NumberFact,3)
    promote = choice(["book", "book", "sponsor","donate","click"])
    neat = neatFacts(NumberFact, fact)
    permlink = fact.permlink
    return render(request, 'blog/fact_as_unit.html', {'fact': fact, 'reflink':reflink, 'quote': choose_quote('n'), "dyk":dyk, "neat":neat, "pl":permlink, "promote":promote})

def fact_new(request):
    if request.method == "POST":
        form = FactForm(request.POST)
        if form.is_valid():
            fact = form.save(commit=False)
            fact.value=num(fact.magnitude)
            fact.scale=0
            fact.save()
            return redirect('fact_detail', pk=fact.pk)
    else:   
        form = FactForm()
    dyk=spuriousFact(NumberFact,3)
    promote = choice(["book", "book", "sponsor","donate","click"])
    return render(request, 'blog/fact_edit.html', {'form': form, "dyk":dyk, "promote":promote})   

def link_redirect(request, link):
    return HttpResponseRedirect(resolve_link(link))

def links_save(request):
    filename = save_links()
    return JsonResponse({"links saved":filename})

def comparison(request):
    params = request.GET
    try: 
        measure = params["measure"]
    except:
        measure = None
    fact = spuriousFact(NumberFact,3, measure=measure)
    dyk = render_to_string('blog/dyk.html', {"dyk":fact})
    return JsonResponse({"dyk":dyk})

def quote(request):
    params = request.GET
    print(params)
    tag = request.GET.get("tag", 'n')
    print("tag %s" % tag)
    quotation = choose_quote(tag)
    quote = render_to_string('blog/quote.html', {"quote":quotation})
    return JsonResponse({"quote":quote})




