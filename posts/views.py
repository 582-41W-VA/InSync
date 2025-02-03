from django.shortcuts import render, get_object_or_404, redirect
from .helpers import build_search_query, user_interaction_state, main_sort_queries
from .models import Post, Comment, Save, Upvote, Flag
from .forms import PostForm, MediaForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def home(request):
    posts = Post.objects.all()
    if request.user.is_authenticated:
        interaction = user_interaction_state(request.user)
    else:
        interaction = {}
    context = { "posts": posts, 'interaction': interaction }
    return render(request, "posts/home.html", context)


@login_required
def create_post(request):
    if request.method == "POST":
        post_form = PostForm(request.POST)
        media_form = MediaForm(request.POST, request.FILES)
        if post_form.is_valid() and media_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            media = media_form.save(commit=False)
            media.post = post
            media.save()
            post_form.save_m2m()
            return redirect('posts:post_detail', post_id=post.id)
    else:
        post_form = PostForm()
        media_form = MediaForm()
    context = { 'post_form': post_form, 'media_form': media_form, 'action': 'Create' }
    return render(request, 'posts/create_post.html', context)


@login_required
def toggle_upvote(request, object, object_id):
    if object == 'post':
        post = get_object_or_404(Post, id=object_id)
        upvote = Upvote.objects.filter(user=request.user, post=post).first()
    elif object == 'comment':
        comment = get_object_or_404(Comment, id=object_id)
        upvote = Upvote.objects.filter(user=request.user, comment=comment).first()
    else:
        return HttpResponse(status=400)
    if upvote:
        upvote.delete()
    else:
        if object == 'post':
            Upvote.objects.create(user=request.user, post=post)
        elif object == 'comment':
            Upvote.objects.create(user=request.user, comment=comment)
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def toggle_save(request, object, object_id):
    if object == 'post':
        post = get_object_or_404(Post, id=object_id)
        save = Save.objects.filter(user=request.user, post=post).first()
    elif object == 'comment':
        comment = get_object_or_404(Comment, id=object_id)
        save = Save.objects.filter(user=request.user, comment=comment).first()  
    else:
        return HttpResponse(status=400)
    if save:
        save.delete() 
    else:
        if object == 'post':
            Save.objects.create(user=request.user, post=post)
        elif object == 'comment':
            Save.objects.create(user=request.user, comment=comment)  
    return redirect(request.META.get('HTTP_REFERER', 'home')) 


@login_required
def search_result(request):
    query = request.GET.get('query')
    user_id = request.GET.get('user_id')
    sort_by = request.GET.get('sort', 'newest')

    params = build_search_query(query)
    posts = Post.objects.filter(params)   

    posts = main_sort_queries(posts, sort_by)
    context = {'posts': posts, 'query': query, 'user_id': user_id, 'sort_by': sort_by }
    return render(request, 'posts/search_result.html', context)