from django.contrib import admin
from .models import Post, Comment, Tag, Upvote, Flag, Media, Save

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Upvote)
admin.site.register(Flag)
admin.site.register(Media)
admin.site.register(Save)