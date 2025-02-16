from .helpers import user_interaction_state

def add_user_interaction(request):
    if request.user.is_authenticated:
        return {'interaction': user_interaction_state(request.user)}
    return {'interaction': None}