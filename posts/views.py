from django.shortcuts import render, get_object_or_404, redirect
from .helpers import user_interaction_state, sort_queries
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from django.template.loader import render_to_string
from .models import Post, Comment, Save, Upvote, Flag, Tag
from django.http import HttpResponse, JsonResponse
from .forms import PostForm, MediaForm
from django.http import HttpResponse
from django.contrib import messages


def home(request):
    posts = Post.objects.all()
    context = { "posts": posts }
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
            messages.success(request, "You have created a post")
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

        return JsonResponse(
            {
                'is_added': False, 
                'message': 'Unliked',
                'action': 'upvote', 
                'upvotes': upvotes 
            }
        )
    else:
        if object == 'post':
            Upvote.objects.create(user=request.user, post=post) 
            upvotes = post.upvote_count()  
        elif object == 'comment':
            Upvote.objects.create(user=request.user, comment=comment)  
            upvotes = comment.upvote_count() 

    return JsonResponse(
        {
            'is_added': True, 
            'message': 'Liked',
            'action': 'upvote', 
            'upvotes': upvotes 
        }
    )


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
            return
        if flag:
            flag.reason = reason
            flag.save()
            return JsonResponse(
                {
                    'message': 'Flag updated successfully', 
                    'action': 'flag'
                }
            )
        else:
            if object == 'post':
                flag = Flag.objects.create(
                    user=request.user, 
                    post=post, 
                    reason=reason
                )
            elif object == 'comment':
                flag = Flag.objects.create(
                    user=request.user, 
                    comment=comment, 
                    reason=reason
                )
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
        return JsonResponse(
            { 
                'is_added': False, 
                'message': 'Unsaved', 
                'action': 'save'
            }
        )
    else:
        if object == 'post':
            Save.objects.create(user=request.user, post=post)
        elif object == 'comment':
            Save.objects.create(user=request.user, comment=comment)  
    return JsonResponse(
        { 
            'is_added': True, 
            'message': 'Saved', 
            'action': 'save' 
        }
    )


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    sort_by = request.GET.get('sort', 'upvotes')
    top_level_comments = post.comments.filter(parent__isnull=True)
    sorted_comments = sort_queries(top_level_comments, sort_by, 'comment_upvotes')

    context = {
        "post": post,
        "comments": sorted_comments,
        'sort_by': sort_by
    }

    return render(request, "posts/post_detail.html", context)

def create_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if not request.user.is_authenticated:
        return JsonResponse({'redirect': '/account/login/'}, status=401)

    parent_comment_id = request.POST.get('parent_comment_id')
    parent_comment = None
    if parent_comment_id:
        parent_comment = get_object_or_404(Comment, id=parent_comment_id)

    text = request.POST.get('comment_text')
    if not text or text.strip() == '':
        return JsonResponse(status=400)

    comment = Comment.objects.create(
        post=post,
        user=request.user,
        parent=parent_comment,
        text=text
    )

    comment_html = render_to_string('partials/comment.html', 
        { 
            'comment': comment, 
            'user': request.user,
            'csrf_token': get_token(request),
        }
    )

    messages.success(request, 'Comment Posted!')
    flash_message_html = render_to_string('partials/flash_message.html', 
        {
            'messages': messages.get_messages(request),
        }
    )
    
    return JsonResponse(
        {
            'flash_message_html': flash_message_html,
            'comment_html': comment_html,
            'comment_id': comment.id,
            'action': 'create'
        }
    )


def edit_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if not request.user.is_authenticated:
        return JsonResponse({'redirect': '/account/login/'}, status=401)

    comment_id = request.POST.get('comment_id')
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    new_text = request.POST.get('edit_comment_text')

    if not new_text or new_text.strip() == '':
        return JsonResponse({'error': 'New comment is required.'}, status=400)

    comment.text = new_text
    comment.save()

    interaction = user_interaction_state(request.user)
    comment_html = render_to_string('partials/comment.html', 
        { 
            'comment': comment,  
            'user': request.user,
            'csrf_token': get_token(request),
            'interaction': interaction,
        }
    )

    messages.success(request, 'Comment Edited!')
    flash_message_html = render_to_string('partials/flash_message.html', 
        {
            'messages': messages.get_messages(request),
        }
    )

    return JsonResponse(
        {
            'flash_message_html': flash_message_html,
            'comment_html': comment_html,
            'comment_id': comment.id,
            'action': 'edit'
        }
    )


def delete_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if not request.user.is_authenticated:
        return JsonResponse({'redirect': '/account/login/'}, status=401)

    comment_id = request.POST.get('comment_id')
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    comment.delete()

    messages.success(request, 'Comment Deleted!')
    flash_message_html = render_to_string('partials/flash_message.html', 
        {
            'messages': messages.get_messages(request),
        }
    )

    return JsonResponse(
        {
            'flash_message_html': flash_message_html,
            'comment_id': comment_id,
            'action': 'delete'
        }
    )

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        media_form = MediaForm(request.POST, request.FILES, instance=post.first_media())
        if post_form.is_valid() and media_form.is_valid():
            new_media = request.FILES.get('media') 
            old_media = post.media_post.first()
            if new_media and old_media:
                old_media.media.delete()
                old_media.delete()  
            post_form.save() 
            media_form.save()  
            messages.success(request, 'Post Edited')
            return redirect('posts:post_detail', post_id=post.id)
    else:
        post_form = PostForm(instance=post)
        media_form = MediaForm(instance=post.first_media())
    
    context = {
        'post_form': post_form,
        'media_form': media_form,
        'action': 'Edit',
        'post': post
    }
    
    return render(request, 'posts/edit_post.html', context)



@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        post.delete() 
        messages.success(request, 'Post Deleted')
        return redirect('posts:home')  
    return render(request, 'posts/delete_post.html', { 'post': post })


@login_required
def search_result(request):
    query = request.GET.get('query')
    sort_by = request.GET.get('sort', 'upvotes')
    posts = Post.search(query, sort_by=sort_by) 
    comments = Comment.search(query, sort_by=sort_by)
  
    context = {
        'posts': posts, 
        'comments': comments, 
        'query': query, 
        'sort_by': sort_by, 
    }
    return render(request, 'posts/search_result.html', context)


@login_required
def all_posts(request, user_id):
    posts = Post.objects.filter(user__id=user_id)
    total_posts = posts.count()
    sort_by = request.GET.get('sort', 'upvotes')
    sorted_posts = sort_queries(posts, sort_by, 'post_upvotes')
    context = {
        'posts': sorted_posts, 
        'total_posts': total_posts, 
        'sort_by': sort_by 
    }
    return render(request, 'posts/all_posts.html', context)


@login_required
def saved_posts(request):
    posts = Post.objects.filter(save__user=request.user)
    total_saved_posts = posts.count()
    sort_by = request.GET.get('sort', 'upvotes')
    sorted_posts = sort_queries(posts, sort_by, 'post_upvotes')
    context = {
        'posts': sorted_posts, 
        'total_saved_posts': total_saved_posts, 
        'sort_by': sort_by  
    }
    return render(request, 'posts/saved_posts.html', context)


@login_required
def liked_posts(request):
    posts = Post.objects.filter(post_upvotes__user=request.user)
    total_liked_posts = posts.count()
    sort_by = request.GET.get('sort', 'upvotes')
    sorted_posts = sort_queries(posts, sort_by, 'post_upvotes')
    context = { 
        'posts': sorted_posts, 
        'total_liked_posts': total_liked_posts, 
        'sort_by': sort_by 
    }
    return render(request, 'posts/liked_posts.html', context)


@login_required
def saved_comments(request):
    comments = Comment.objects.filter(save__user=request.user)
    total_saved_comments = comments.count()
    sort_by = request.GET.get('sort', 'upvotes')
    sorted_comments = sort_queries(comments, sort_by, 'comment_upvotes')

    context = {
        'comments': sorted_comments, 
        'total_saved_comments': total_saved_comments,
        'sort_by': sort_by,
    }
    return render(request, 'posts/saved_comments.html', context)


@login_required
def liked_comments(request):
    comments = Comment.objects.filter(comment_upvotes__user=request.user)
    total_likes = comments.count()
    sort_by = request.GET.get('sort', 'upvotes')
    sorted_comments = sort_queries(comments, sort_by, 'comment_upvotes')

    context = {
        'comments': sorted_comments, 
        'total_likes': total_likes,
        'sort_by': sort_by,
    }
    return render(request, 'posts/liked_comments.html', context)


@login_required
def category(request, tag_id):
    category = get_object_or_404(Tag, id=tag_id)
    posts =  category.post_tag.all()
    total_posts = posts.count()
    context = { "category": category, "posts": posts, 'total_posts': total_posts }
    return render(request, "posts/category.html", context)