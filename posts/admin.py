from django.contrib import admin
from .models import Post, Comment, Tag, Upvote, Flag, Media, Save
from django.db.models import Count

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'upvote_count', 'flag_count', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at',)
    search_fields = ('text', 'user')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(upvote_count=Count('comment_upvotes'))
        return queryset

    def upvote_count(self, obj):
        return obj.upvote_count
    upvote_count.admin_order_field = 'upvote_count'

class FlagAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'comment', 'reason', 'flagged_at')
    list_filter = ('flagged_at', 'reason')
    search_fields = ('reason', 'user')

class UpvoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'comment', 'upvoted_at')
    list_filter = ('upvoted_at',)
    search_fields = ('user__username', 'post__title', 'comment__text')

class SaveAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'comment', 'saved_at')
    list_filter = ('saved_at',)
    search_fields = ('user__username', 'post__title', 'comment__text')

class MediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'post',)
    list_filter = ()
    search_fields = ('user__username', 'post__title')

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'comment_count', 'upvote_count', 'flag_count', 'created_at', 'updated_at',)
    list_filter = ('tags', 'created_at',)
    search_fields = ('title', 'content')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            comment_count=Count('comments')
        )
        return queryset

    def comment_count(self, obj):
        return obj.comment_count  
    comment_count.admin_order_field = 'comment_count' 

admin.site.register(Comment, CommentAdmin)
admin.site.register(Upvote, UpvoteAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Flag, FlagAdmin)
admin.site.register(Save, SaveAdmin)
admin.site.register(Tag)

