from django.contrib import admin
from .models import Post, Comment, Tag, Upvote, Flag, Media, Save

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'created_at', 'updated_at', 'text', 'upvote_count')
    list_filter = ('created_at',)
    search_fields = ('text', 'user', 'text',)

class FlagAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'comment', 'reason', 'flagged_at')
    list_filter = ('flagged_at',)
    search_fields = ('reason', 'user')

class UpvoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'comment', 'upvoted_at')
    list_filter = ('upvoted_at',)
    search_fields = ('user__username', 'post__title', 'comment__text')

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'created_at', 'updated_at', 'upvote_count', 'top_level_comments_count', 'total_comments')
    list_filter = ('tags', 'created_at',)
    search_fields = ('title', 'content')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Flag, FlagAdmin)
admin.site.register(Upvote, UpvoteAdmin)
admin.site.register(Tag)
admin.site.register(Media)
admin.site.register(Save)