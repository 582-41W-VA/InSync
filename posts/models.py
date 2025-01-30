from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return f"{self.name}"

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    tags = models.ManyToManyField(Tag, related_name='post_tag')
    url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    
    def upvote_count(self):
        return self.post_upvotes.count()
    
    def first_media(self):
        return self.media_post.first()
    
    def top_level_comments_count(self):
        return self.comments.filter(parent=None).count()
    
    def __str__(self):
        return self.title