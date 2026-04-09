from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from . models import Post,Comment,Tag,Categories
from django.db.models import Q 
from django.core.paginator import Paginator

# Create your views here.

def post_list(request):
    # category, tag, searching, pagination -> post dekhate hobe
    categoryQ = request.GET.get('category')
    tagQ = request.GET.get('tag')
    searchQ = request.GET.get('q')

    posts = Post.objects.all()

    if categoryQ:
        posts = posts.filter(category__name = categoryQ)
    if tagQ:
        posts = posts.filter(tag__name = tagQ)
    if searchQ:
        posts = posts.filter(
            Q(titile_icontains = searchQ)
            | Q(content_icontains = searchQ)
            | Q(tag__name__icontains = searchQ)
            | Q(category__name__icontains = searchQ)

        ).distinct()

    #using pagination
    paginator = Paginator(posts, 2) # per page 2
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context ={ 
        "page_obj" : page_obj,
        "categories" : Categories.objects.all(),
        "tags" : Tag.objects.all(),
        'search_query' : searchQ,
        'category_query' : categoryQ,
        'tag_query' : tagQ,
     }
    return render(request, '' , context)
