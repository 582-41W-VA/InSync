from django.db.models import Q, Count
from .models import Save, Upvote


def post_sort(posts, sort_by):
    posts = posts.annotate(upvotes_count=Count('post_upvotes'))
    if sort_by == "newest":
        posts = posts.order_by("-created_at")  
    elif sort_by == "oldest":
        posts = posts.order_by("created_at")
    elif sort_by == "upvotes":
        posts = posts.order_by("-upvotes_count")
    elif sort_by == "-upvotes":
        posts = posts.order_by("upvotes_count")
    else:
        posts = posts.order_by("-upvotes_count")
    return posts


def comment_sort(comment, sort_by):
    comment = comment.annotate(upvotes_count=Count('comment_upvotes'))
    if sort_by == "newest":
        comment = comment.order_by("-created_at")  
    elif sort_by == "oldest":
        comment = comment.order_by("created_at")
    elif sort_by == "upvotes":
        comment = comment.order_by("-upvotes_count")
    elif sort_by == "-upvotes":
        comment = comment.order_by("upvotes_count")
    else:
        comment = comment.order_by("-upvotes_count")
    return comment


def build_search_query(query, model):
    query_conditions = Q(user__username__icontains=query)
    if model == 'post':
        query_conditions |= Q(title__icontains=query) | Q(tags__name__icontains=query)
    elif model == 'comment':
        query_conditions |= Q(text__icontains=query)
    return query_conditions


def searchQuery(query, Post, Comment, url, sort_by, request, user_id):
    if not query:
        posts = Post.objects.none()
        comments = Comment.objects.none()
    else:
        posts_query = build_search_query(query, model='post')
        comments_query = build_search_query(query, model='comment')
       
        if url == 'saved_posts':
            posts = Post.objects.filter(save__user=request.user).filter(posts_query)
        elif url == 'user_posts' and user_id:
            posts = Post.objects.filter(user__id=user_id).filter(posts_query)
        elif url == 'user_upvoted_posts':
            posts = Post.objects.filter(post_upvotes__user=request.user).filter(posts_query)
        else:
            posts = Post.objects.filter(posts_query)
            
        if url == 'saved_comments':
            comments = Comment.objects.filter(save__user=request.user).filter(comments_query)
        elif url == 'liked_comments':
            comments = Comment.objects.filter(comment_upvotes__user=request.user).filter(comments_query)  
        else:
            comments = Comment.objects.filter(comments_query)   
    posts = post_sort(posts, sort_by)
    comments = comment_sort(comments, sort_by)
    return posts, comments


def user_interaction_state(user):
    interactions = {
        'posts': {
            'saved': Save.objects.filter(user=user).values_list('post', flat=True),
            'upvoted': Upvote.objects.filter(user=user).values_list('post', flat=True),
        },
        'comments': {
            'saved': Save.objects.filter(user=user).values_list('comment', flat=True),
            'upvoted': Upvote.objects.filter(user=user).values_list('comment', flat=True),
        }
    }
    return interactions