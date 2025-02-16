from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile
from django.db.models import Count
from posts.models import Post, Comment

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'comment_count', 'is_staff', 'date_joined',)
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'date_joined')
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(comment_count=Count('comment_user'))
        return queryset
    
    def comment_count(self, obj):
        return obj.comment_count
    comment_count.admin_order_field = 'comment_count' 

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'job_title', 'profile_image')
    list_filter = ('job_title',)
    search_fields = ('user__username', 'email', 'job_title')

    def profile_image_display(self, obj):
        if obj.profile_image:
            return f'<img src="{obj.profile_image.url}" width="50" height="50" />'
        return 'No image'
    profile_image_display.allow_tags = True 
    profile_image_display.short_description = 'Profile Image'

    list_editable = ('email', 'job_title') 

admin.site.register(Profile, ProfileAdmin)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
