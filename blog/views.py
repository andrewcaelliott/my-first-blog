from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
from .models import Post
from .models import NumberFact
from .forms import PostForm 
from .forms import FactForm 

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


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