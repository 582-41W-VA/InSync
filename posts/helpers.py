from django.db.models import Q, Count
from .models import Save, Upvote


def main_sort_queries(posts, sort_by):
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


def build_search_query(query):
    return Q(
        title__icontains=query) | Q(
        user__username__icontains=query) | Q(
        tags__name__icontains=query
    )


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