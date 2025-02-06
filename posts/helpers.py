from django.db.models import Count

def sort_queries(posts, sort_by, type):
    posts = posts.annotate(upvotes_count=Count(type))
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


def user_interaction_state(user):
    from .models import Save, Upvote
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