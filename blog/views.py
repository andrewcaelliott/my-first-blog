from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
from .models import Post
from .models import NumberFact
from .models import NumberQuery
from .forms import PostForm 
from .forms import FactForm 
from .forms import QueryForm 
from .forms import ConvertForm 

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

LENGTH_UNIT_CHOICES= (
        ('km', 'kilometer'),
        ('m', 'meter'),
        ('cm', 'centimeter'),
        ('mm', 'millimeter'),
        ('mi', 'mile'),
        ('yd', 'yard'),
        ('ft', 'foot'),
        ('in', 'inch'),
    )

COUNT_UNIT_CHOICES= (
        ('i', 'item'),
    )

AMOUNT_UNIT_CHOICES= (
        ('USD', 'USD'),
    )

TIME_UNIT_CHOICES= (
        ('year', 'year'),
        ('month', 'month'),
        ('week', 'week'),
        ('day', 'day'),
        ('hour', 'hour'),
        ('minute', 'minute'),
        ('second', 'second'),
    )
    

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')  
    return render(request, 'blog/post_list.html', {'posts':posts})

def fact_list(request):
    facts = NumberFact.objects.filter().order_by('text')  
    return render(request, 'blog/fact_list.html', {'facts':facts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

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
    return render(request, 'blog/post_edit.html', {'form': form})    

def fact_detail(request, pk):
    fact = get_object_or_404(NumberFact, pk=pk)
    return render(request, 'blog/fact_detail.html', {'fact': fact})

def fact_new(request):
    if request.method == "POST":
        form = FactForm(request.POST)
        if form.is_valid():
            fact = form.save(commit=False)
            fact.value=num(fact.number)
            fact.scale=0
            fact.save()
            return redirect('fact_detail', pk=fact.pk)
    else:   
        form = FactForm()
    return render(request, 'blog/fact_edit.html', {'form': form})   

def itabn(request):
    extentForm = QueryForm(initial={'measure': 'e'})
    extentForm.fields['unit'].choices=LENGTH_UNIT_CHOICES
    countForm = QueryForm(initial={'measure': 'c'})
    countForm.fields['unit'].choices=COUNT_UNIT_CHOICES
    amountForm = QueryForm(initial={'measure': 'a'})
    amountForm.fields['unit'].choices=AMOUNT_UNIT_CHOICES
    durationForm = QueryForm(initial={'measure': 'd'})
    durationForm.fields['unit'].choices=TIME_UNIT_CHOICES
    widgets = [
        {"title":"How Big?","glyph":"glyphicon glyphicon-resize-horizontal","form":extentForm},
        {"title":"How Many?","glyph":"glyphicon glyphicon-th","form":countForm},
        {"title":"How Much?","glyph":"glyphicon glyphicon-usd","form":amountForm},
        {"title":"How Long?","glyph":"glyphicon glyphicon-time","form":durationForm}]
    return render(request, 'blog/itabn.html', {'widgets':widgets})


def query_answer(request):
    query = QueryForm(request.POST)
    numberQuery = NumberQuery(number=query["number"].value(), multiple=query["multiple"].value(), unit=query["unit"].value())
    answer = {"quip":"Here's your query_answer"}
    references=[]
    if query["measure"].value()=="e":
        query.fields['unit'].choices=LENGTH_UNIT_CHOICES
        answer = {"quip":"It's a long, long way to ..."}
        references = [
            ('Length of trip from the Earth to the Sun','{times:20.2f} times the distance from the Earth to the Sun','1 / {fraction:20.0f} of the distance from the Earth to the Sun'),
            ('Length of trip from the Earth to the Moon','{times:20.2f} times the distance from the Earth to the Moon','1 / {fraction:20.0f} of the distance from the Earth to the Moon'),
            ('Length of trip around the equator','{times:20.2f} times the distance around the equator','1 / {fraction:20.0f} of the distance around the equator'),
            ('Length of trip from London to New York','{times:20.2f} times the distance from London to New York','1 / {fraction:20.0f} of the distance from London to New York'),
            ('Length of trip from London to Edinburgh','{times:20.2f} times the distance from London to Edinburgh','1 / {fraction:20.0f} of the distance from London to Edinburgh'),
            ('Length of a football pitch','{times:20.2f} football pitches end to end','1 / {fraction:20.0f} as long as a football pitch'),
            ('Length of a London bus','{times:20.2f} London buses end to end','1 / {fraction:20.0f} as long as a London bus'),
            ('Length of an iPhone 6',"{times:20.2f} iPhone 6's end to end",'1 / {fraction:20.0f} as long as an iPhone 6'),
        ]
    elif query["measure"].value()=="c":
        query.fields['unit'].choices=COUNT_UNIT_CHOICES
        answer = {"quip":"Let me count ..."}
        references = [
            ('Population of World','{times:20.2f} for every person in the world','One for every {fraction:20.0f} people in the world'),
            ('Population of China','{times:20.2f} for every person in China','One for every {fraction:20.0f} people in China'),
            ('Population of United States','{times:20.2f} for every person in the USA','One for every {fraction:20.0f} people in the USA'),
            ('Population of United Kingdom','{times:20.2f} for every person in the UK','One for every {fraction:20.0f} people in the UK'),
        ]
    elif query["measure"].value()=="a":
        answer = {"quip":"There's more to life than money"}
        query.fields['unit'].choices=AMOUNT_UNIT_CHOICES
        references = [
            ('GDP of United States','{times:20.2f} times the USA GDP','{percent:20.2f} percent of the USA GDP','1 /{fraction:20.0f} of the USA GDP'),
            ('GDP of United Kingdom','{times:20.2f} times the UK GDP','{percent:20.2f} percent of the UK GDP','1 /{fraction:20.0f} of the UK GDP'),
        ] 
    elif query["measure"].value()=="d":
        answer = {"quip":"How many years can a mountain exist?"}
        query.fields['unit'].choices=TIME_UNIT_CHOICES
        references = [
            ('age of the universe','{times:20.2f} times the age of the universe','{percent:20.2f} percent of the age of the universe','1 /{fraction:20.0f} of the age of the universe'),
            ('first modern humans','{times:20.2f} times the period since the emergence of the first modern humans','{percent:20.2f} percent of the time since the emergence of the first modern humans','1 /{fraction:20.0f} of the time since the emergence of the first modern humans'),
            ('building of Great Wall of China','{times:20.2f} times the period since the building of the Great Wall of China','{percent:20.2f} percent of the time since the building of the Great Wall of China','1 /{fraction:20.0f} of the time since the building of the Great Wall of China'),
            ('lifespan of Galapagos giant tortoise','{times:20.2f} times the lifespan of a Galapagos giant tortoise','{percent:20.2f} percent of the lifespan of a Galapagos giant tortoise','1 /{fraction:20.0f} of the lifespan of a Galapagos giant tortoise'),
            ('human generation','{times:20.2f} human generations','{percent:20.2f} percent of a human generation','1 /{fraction:20.0f} of a human generation'),
            ('lifespan of rat','{times:20.2f} times the lifespan of a rat','{percent:20.2f} percent of the lifespan of a rat','1 /{fraction:20.0f} of the lifespan of a rat'),
        ] 
    answer["comparisons"] = numberQuery.getComparisons(references)
    return render(request, 'blog/query_answer.html', {'query': query, 'answer':answer})   

def convert(request):
    extentForm = ConvertForm(initial={'measure': 'e'})
    extentForm.fields['unit'].choices=LENGTH_UNIT_CHOICES
    extentForm.fields['target_unit'].choices=LENGTH_UNIT_CHOICES
    durationForm = ConvertForm(initial={'measure': 'd'})
    durationForm.fields['unit'].choices=TIME_UNIT_CHOICES
    durationForm.fields['target_unit'].choices=TIME_UNIT_CHOICES
    widgets = [
        {"title":"Convert Length","glyph":"glyphicon glyphicon-resize-horizontal","form":extentForm},
        {"title":"Convert Time","glyph":"glyphicon glyphicon-time","form":durationForm},
        ]
    return render(request, 'blog/convert.html', {'widgets':widgets})


def conversion_answer(request):
    conversion = ConvertForm(request.POST)
    numberQuery = NumberQuery(number=conversion["number"].value(), multiple=conversion["multiple"].value(), unit=conversion["unit"].value(), target_unit=conversion["target_unit"].value())


    answer = {"quip":"Here's your conversion answer"}
    conversion_targets=[]
    if conversion["measure"].value()=="e":
        answer = {"quip":"The long and winding road ..."}
        conversion_targets = [
            (numberQuery.target_unit),
            ('kilometer'),
            ('metre'),
            ('millimeter'),
            ('mile'),
            ('yard'),
            ('foot'),
            ('inch'),
        ]
    elif conversion["measure"].value()=="d":
        answer = {"quip":"How long has it been ..."}
        conversion_targets = [
            (numberQuery.target_unit),
            ('year'),
            ('month'),
            ('fortnight'),
            ('week'),
            ('day'),
            ('hour'),
            ('minute'),
            ('second'),
        ]
    conversions = numberQuery.getConversions(conversion_targets)
    answer["requestedConversion"] = conversions[0]
    answer["otherConversions"] = conversions[1:]
    return render(request, 'blog/conversion_answer.html', {'conversion': conversion, 'answer':answer})   

