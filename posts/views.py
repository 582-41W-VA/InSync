from django.shortcuts import render, get_object_or_404, redirect
from .helpers import user_interaction_state, post_sort, comment_sort, searchQuery
from .models import Post, Comment, Save, Upvote, Flag
from .forms import PostForm, MediaForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponse, JsonResponse


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


def toggle_upvote(request, object, object_id):
    if not request.user.is_authenticated:
        return JsonResponse({'redirect': '/account/login/'}, status=401)
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
        if object == 'post':
            upvotes = post.upvote_count() 
        elif object == 'comment':
            upvotes = comment.upvote_count() 
        return JsonResponse({
            'is_added': False, 'message': 'Upvote Removed',
            'action': 'upvote', 'upvotes': upvotes 
        })
    
    if object == 'post':
        Upvote.objects.create(user=request.user, post=post) 
        upvotes = post.upvote_count()  
    elif object == 'comment':
        Upvote.objects.create(user=request.user, comment=comment)  
        upvotes = comment.upvote_count()  
    return JsonResponse({
        'is_added': True, 'message': 'Upvoted',
        'action': 'upvote', 'upvotes': upvotes 
    })


def flag(request, object, object_id):
    if not request.user.is_authenticated:
        return JsonResponse({'redirect': '/account/login/'}, status=401)
    if object == 'post':
        post = get_object_or_404(Post, id=object_id)
        flag = Flag.objects.filter(user=request.user, post=post).first()
    elif object == 'comment':
        comment = get_object_or_404(Comment, id=object_id)
        flag = Flag.objects.filter(user=request.user, comment=comment).first()
    else:
        return JsonResponse(status=400)
    
    if request.method == 'POST':
        reason = request.POST.get('reason')
        if not reason:
            return JsonResponse({'message': 'Please select a reason.'}, status=400)
        if flag:
            flag.reason = reason
            flag.save()
            return JsonResponse({'message': 'Flag updated successfully', 'action': 'flag'})
        else:
            if object == 'post':
                flag = Flag.objects.create(user=request.user, post=post, reason=reason)
            elif object == 'comment':
                flag = Flag.objects.create(user=request.user, comment=comment, reason=reason)
            return JsonResponse({'message': 'Flagged successfully', 'action': 'flag'})
        
    return JsonResponse({'error': 'Invalid request method'}, status=405)


def toggle_save(request, object, object_id):
    if not request.user.is_authenticated:
        return JsonResponse({'redirect': '/account/login/'}, status=401)
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
        return JsonResponse({ 'is_added': False, 'message': 'Unsaved', 'action': 'save' })
    else:
        if object == 'post':
            Save.objects.create(user=request.user, post=post)
        elif object == 'comment':
            Save.objects.create(user=request.user, comment=comment)  
    return JsonResponse({ 'is_added': True, 'message': 'Saved', 'action': 'save' })


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    sort_by = request.GET.get('sort', 'newest')
    top_level_comments = post.comments.filter(parent__isnull=True)
    sorted_comments = comment_sort(top_level_comments, sort_by)
    interaction = user_interaction_state(request.user)

    context = {
        "post": post,
        "comments": sorted_comments,
        'interaction': interaction,
        'sort_by': sort_by
    }

    return render(request, "posts/post_detail.html", context)


@login_required
def search_result(request):
    query = request.GET.get('query')
    user_id = request.GET.get('user_id')
    sort_by = request.GET.get('sort', 'newest')
    name = request.GET.get('name')
    url = request.GET.get('url', 'all')
    posts, comments = searchQuery(query, Post, Comment, url, sort_by, request, user_id)

    context = {
        'posts': posts, 
        'comments': comments, 
        'query': query, 
        'url': url, 
        'user_id': user_id, 
        'name': name, 
        'sort_by': sort_by 
    }   

    return render(request, 'posts/search_result.html', context)