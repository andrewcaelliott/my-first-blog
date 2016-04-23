from json import loads
from random import choice,seed as set_seed,randint
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
from django.http import JsonResponse
from django import forms
from .models import Post
from .models import NumberFact
from .models import NumberQuery
from .utils import numberFactsLikeThis,biggestNumberFact, smallestNumberFact,spuriousFact,neatFacts
from .forms import PostForm 
from .forms import FactForm 
from .forms import QueryForm 
from .forms import FreeForm 
from .forms import ConvertForm 
from .convert import convertToDefaultBase 
from .convert import convertToUnit 
from .config import reference_lists
from .config import unit_choice_lists
from .config import quip_lists,quotes
from .config import conversion_target_lists
from .config import conversion_quip_lists
from .utils import num
from .utils import parseBigNumber, randomFact
from .dummycontent import storySelection
from .tumblr import tumblrSelection


def home(request):
    freeForm = FreeForm()
    freeForm.fields["number"].label="Is this a big number?"
    widgets = []
    stories = {}
    stories["news"]=tumblrSelection("news")
    stories["passion"]=tumblrSelection("passion")
    stories["education"]=tumblrSelection("education")
    stories["landmark"]=tumblrSelection("landmark")
    dyk=spuriousFact(NumberFact)
    return render(request, 'blog/home.html', {'widgets':widgets, 'freeForm':freeForm, 'quote': choice(quotes), 'stories':stories, "dyk":dyk})

def homealt(request):
    freeForm = FreeForm()
    widgets = []
    stories = {}
    stories["news"]=storySelection("news")
    stories["passion"]=storySelection("passion")
    stories["education"]=storySelection("education")
    stories["landmark"]=storySelection("landmark")
    return render(request, 'blog/home-alt.html', {'widgets':widgets, 'freeForm':freeForm, 'quote': choice(quotes), 'stories':stories})

def blog(category, request):
    stories=tumblrSelection(category)
    titles = {
        "news":"Numbers In The News", 
        "passion":"For the Love of Numbers", 
        "education":"Know Your Numbers", 
        "landmark":"Landmark Numbers"
    }
    subtitles = {
        "news":"Some notable numbers we have spotted recently", 
        "passion":"A number-led selection of writings for the truly geeky among us ...", 
        "education":"A little more knowledge is never a dangerous thing ...", 
        "landmark":"Like beacons in a landscape, prominent numbers offer guidance"
    }
    dyk=spuriousFact(NumberFact)
    return render(request, 'blog/blog.html', {'quote': choice(quotes), 'stories':stories, 'blog_title':titles[category], 'blog_subtitle':subtitles[category], "dyk":dyk})

def blog_flton(request):
    return blog("passion", request)

def blog_nitn(request):
    return blog("news", request)

def blog_ggb(request):
    return blog("education", request)

def blog_lmk(request):
    return blog("landmark", request)

def quiz(request):
    params = request.POST
    try:
        seed=num(params.get("seed"))
    except (AttributeError,TypeError):
        seed = randint(0,10000000)
    if seed == None:
        seed = randint(0,10000000)

    set_seed(seed)    
    try:
        cycle=params.get("cycle")
    except (AttributeError,TypeError):
        cycle="initial"


    try:
        measure=params.get("measure")
    except (AttributeError,TypeError):
        measure=choice(["extent", "count", "amount", "duration", "mass"])
    if measure==None or measure == "random":
        measure=choice(["extent", "count", "amount", "duration", "mass"])

    quiz={}
    askbiggest = randint(0,1)==0
    if askbiggest:
        if measure=="extent":
            quiz["question"]="Which of these is the biggest?"
        elif measure=="count":
            quiz["question"]="Which of these is the most numerous?"
        elif measure=="amount":
            quiz["question"]="Which of these is the greatest amount?"
        elif measure=="duration":
            quiz["question"]="Which of these is the longest period of time?"
        else:
            quiz["question"]="Which of these has the greatest mass?"
    else:
        if measure=="extent":
            quiz["question"]="Which of these is the smallest?"
        elif measure=="count":
            quiz["question"]="Which of these is the least numerous?"
        elif measure=="amount":
            quiz["question"]="Which of these is the smallest amount?"
        elif measure=="duration":
            quiz["question"]="Which of these is the shortest period of time?"
        else:
            quiz["question"]="Which of these has the least mass?"
    quiz["measure"]=measure
    quiz["seed"] = seed
    rf = randomFact(NumberFact, measure, rseed=seed)
    bestComparisons, tolerance, score  = numberFactsLikeThis(NumberFact, rf, rseed=seed) 
    while len(bestComparisons)<4:
        seed = randint(0,10000000)
        rf = randomFact(NumberFact, measure, rseed=seed)
        bestComparisons, tolerance, score  = numberFactsLikeThis(NumberFact, rf, rseed=seed) 
    quiz["hint"] = rf.render
    quiz["options"]=bestComparisons
    if askbiggest:
        answer = biggestNumberFact(bestComparisons)
    else: 
        answer = smallestNumberFact(bestComparisons)
    quiz["answer"]=answer.title
    if request.method == "POST":
        response = request.POST
        if response.get("option")==quiz["answer"] and cycle=="answered":
            quiz["assessment"] = str(response.get("option"))+" is the correct answer: Well done!"
            #quiz["question"]=""
            reveal = []
            for option in bestComparisons:
                reveal.append({"title":option.render_folk, "link":option.link})
            quiz["options"]=reveal
            quiz["cycle"]="correct"
        elif cycle=="answered":
            quiz["assessment"] = str(response.get("option"))+" is not correct. Try again."
    else:   
        pass
#        form = FactForm()
 #   return render(request, 'blog/fact_edit.html', {'form': form})   
    dyk=spuriousFact(NumberFact)
    return render(request, 'blog/quiz.html', {'quiz':quiz, 'quote': choice(quotes), "dyk":dyk})

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
    dyk=spuriousFact(NumberFact)
    return render(request, 'blog/itabn.html', {'widgets':widgets, 'freeForm':freeForm, 'quote': choice(quotes), "dyk":dyk})

def query_answer(request, numberQuery):
    query =  QueryForm(instance=numberQuery)
#    query.fields['magnitude'].value=numberQuery.magnitude
    query.fields['measure'].widget = forms.HiddenInput()
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
    question = numberQuery.render.replace(" - "," ").replace(" i","").replace(" 10^","*10^")
    if (multiple=='?'):
        easteregg={"question":numberQuery.unit}
        if numberQuery.unit.lower().find("graham")>=0:
            easteregg["answer"]="Graham's Number is a very big number indeed, way bigger than any context or comparison this site can offer."
        elif numberQuery.unit.lower().find("infinity")>=0:
            easteregg["answer"]="Sorry, this site does not (yet) deal in infinities. Check back later!"
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
        else:
            easteregg["answer"]="I'm sorry, you have me stumped with that one."            
        answer["easteregg"]=easteregg
    #question = question.replace(" times ", " x ").replace(" the ", " ").replace(" distance ", " dist ")
    dyk=spuriousFact(NumberFact)
    return render(request, 'blog/itabn_answer.html', {'query': query, 'question': question[3:]+"\n", 'answer':answer, 'quote': choice(quotes), "dyk":dyk})   

def query_answer_post(request):
    query =  QueryForm(request.POST)
    numberQuery = NumberQuery(magnitude=query["magnitude"].value(), multiple=query["multiple"].value(), unit=query["unit"].value(), measure=query["measure"].value())
    return query_answer(request,numberQuery)

def query_answer_get(request):
    query =  QueryForm(request.GET)
    numberQuery = NumberQuery(magnitude=query["magnitude"].value(), multiple=query["multiple"].value(), unit=query["unit"].value(), measure=query["measure"].value())
    return query_answer(request, numberQuery)

def query_compare(request):
    query =  FreeForm(request.GET)
    magnitude, multiple, unit, measure = parseBigNumber(query["number"].value())
    numberQuery = NumberQuery(magnitude=magnitude, multiple=multiple, unit=unit, measure=measure)
    return query_answer(request, numberQuery)

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

def convert(request):
    extentForm = ConvertForm(initial={'measure': 'e'})
    extentForm.fields['unit'].choices=unit_choice_lists['e']
    extentForm.fields['target_unit'].choices=unit_choice_lists['e']
    extentForm.fields['measure'].widget = forms.HiddenInput()
    amountForm = ConvertForm(initial={'measure': 'a'})
    amountForm.fields['unit'].choices=unit_choice_lists['a']
    amountForm.fields['target_unit'].choices=unit_choice_lists['a']
    amountForm.fields['measure'].widget = forms.HiddenInput()
    durationForm = ConvertForm(initial={'measure': 'd'})
    durationForm.fields['unit'].choices=unit_choice_lists['d']
    durationForm.fields['target_unit'].choices=unit_choice_lists['d']
    durationForm.fields['measure'].widget = forms.HiddenInput()
    massForm = ConvertForm(initial={'measure': 'm'})
    massForm.fields['unit'].choices=unit_choice_lists['m']
    massForm.fields['target_unit'].choices=unit_choice_lists['m']
    massForm.fields['measure'].widget = forms.HiddenInput()
    widgets = [
            {"title":"Convert Length","glyph":"glyphicon glyphicon-resize-horizontal","form":extentForm},
            {"title":"Convert Amount","glyph":"glyphicon glyphicon-usd","form":amountForm},
            {"title":"Convert Time","glyph":"glyphicon glyphicon-time","form":durationForm},
            {"title":"Convert Mass","glyph":"glyphicon glyphicon-briefcase","form":massForm},
        ]
    dyk=spuriousFact(NumberFact)
    return render(request, 'blog/convert.html', {'widgets':widgets, 'quote': choice(quotes), "dyk":dyk})

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
    dyk=spuriousFact(NumberFact)
    return render(request, 'blog/conversion_answer.html', {'conversion': conversion, 'answer':answer, 'quote': choice(quotes), "dyk":dyk})   

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
    dyk=spuriousFact(NumberFact)
    return render(request, 'blog/post_list.html', {'posts':posts, "dyk":dyk})

def fact_list(request):
    facts = NumberFact.objects.filter().order_by('text')  
    dyk=spuriousFact(NumberFact)
    return render(request, 'blog/fact_list.html', {'facts':facts, "dyk":dyk})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    dyk=spuriousFact(NumberFact)
    return render(request, 'blog/post_detail.html', {'post': post, "dyk":dyk})

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
    dyk=spuriousFact(NumberFact)
    return render(request, 'blog/post_edit.html', {'form': form, "dyk":dyk})    

def fact_detail(request, pk):
    fact = get_object_or_404(NumberFact, pk=pk)
    if fact.text.rfind("http")>=0:
        reflink=fact.text
    else:
        reflink="http://www.google.com/?q="+fact.title
    dyk=spuriousFact(NumberFact)
    neat = neatFacts(NumberFact, fact)
    return render(request, 'blog/fact_detail.html', {'fact': fact, 'reflink':reflink, 'quote': choice(quotes), "dyk":dyk, "neat":neat})

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
    dyk=spuriousFact(NumberFact)
    return render(request, 'blog/fact_edit.html', {'form': form, "dyk":dyk})   
