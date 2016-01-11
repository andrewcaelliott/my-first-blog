from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
from .models import Post
from .models import NumberFact
from .models import NumberQuery
from .forms import PostForm 
from .forms import FactForm 
from .forms import QueryForm 

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


def itabn(request):
    extentForm = QueryForm(initial={'measure': 'e'})
    countForm = QueryForm(initial={'measure': 'c'})
    amountForm = QueryForm(initial={'measure': 'a'})
    durationForm = QueryForm(initial={'measure': 'd'})
    widgets = [
        {"title":"How Big?","glyph":"glyphicon glyphicon-resize-horizontal","form":extentForm},
        {"title":"How Many?","glyph":"glyphicon glyphicon-th","form":countForm},
        {"title":"How Much?","glyph":"glyphicon glyphicon-usd","form":amountForm},
        {"title":"How Long?","glyph":"glyphicon glyphicon-time","form":durationForm}]
    return render(request, 'blog/itabn.html', {'widgets':widgets})

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

def query_answer(request):
    query = QueryForm(request.POST)
    numberQuery = NumberQuery(number=query["number"].value(), multiple=query["multiple"].value(), unit=query["unit"].value())

    answer = {"quip":"Isn't this jolly?"}
    references=[]
    if query["measure"].value()=="e":
        references = [
            ('Length of a London bus','{times:20.2f} London buses end to end','1 / {fraction:20.0f} as long as a London bus'),
        ]
    elif query["measure"].value()=="c":
        references = [
            ('Population of World','{times:20.2f} for every person in the world','One for every {fraction:20.0f} people in the world'),
            ('Population of China','{times:20.2f} for every person in China','One for every {fraction:20.0f} people in China'),
            ('Population of United States','{times:20.2f} for every person in the USA','One for every {fraction:20.0f} people in the USA'),
            ('Population of United Kingdom','{times:20.2f} for every person in the UK','One for every {fraction:20.0f} people in the UK'),
        ]
    elif query["measure"].value()=="a":
        references = [
            ('GDP of United States','{times:20.2f} times the USA GDP','{percent:20.2f} percent of the USA GDP','A 1 /{fraction:20.0f} fraction of the USA GDP'),
            ('GDP of United Kingdom','{times:20.2f} times the UK GDP','{percent:20.2f} percent of the UK GDP','A 1 /{fraction:20.0f} fraction of the UK GDP'),
        ] 
    answer["comparisons"] = numberQuery.getComparisons(references)
    return render(request, 'blog/query_answer.html', {'query': query, 'answer':answer})   

