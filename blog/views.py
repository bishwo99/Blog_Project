from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from . models import Post,Comment,Tag,Categories
from django.db.models import Q 
from django.core.paginator import Paginator
from . forms import CommentForm,PostForm

# Create your views here.
def profile(request,id):
    post = get_object_or_404

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
            Q(title__icontains = searchQ)
            | Q(content__icontains = searchQ)
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
    return render(request, 'blog/post_list.html' , context)

def post_details(request,id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False) #Database e save hobena
            comment.post = post 
            comment.author = request.user
            comment.save() #Ekhon database e save hobe
            return redirect('post_details', id = post.id)
    else:
        comment_form = CommentForm()
    comments = post.comment_set.all()
    is_liked = post.liked_user.filter(id = request.user.id).exists()
    like_count = post.liked_user.count()

    context = {
        'post' : post,
        'categories' : Categories.objects.all(),
        'tag' : Tag.objects.all(),
        'comments' : comments,
        'comment_form': comment_form,
        'is_liked' : is_liked,
        'like_count' : like_count, 
    }
    post.view_count += 1
    post.save()

    return render(request, 'blog/post_details.html', context)


def liked_post(request,id):
    post = get_object_or_404(Post, id=id)

    if post.liked_user.filter(id = request.user.id):
        post.liked_user.remove(request.user)
    else:
        post.liked_user.add(request.user)
    return redirect('liked_post', id = post.id) 


def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    
    return render(request, 'blog/post_create.html', {'form' : form})

def post_update(request,id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = PostForm(request.POST,instance=post)
        form.save()
        return redirect('post_details', id = post.id)
    else:
        form = PostForm()
    return render(request, 'blog/post_create.html', {'form' : form})

def post_delete(request,id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect('post_list')


        