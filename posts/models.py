from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from .helpers import sort_queries
from django.db.models import Q


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return f"{self.name}"


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = CKEditor5Field('Text', config_name='extends')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    tags = models.ManyToManyField(Tag, related_name='post_tag')
    url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    @classmethod
    def search(cls, query, sort_by='-upvotes_count'):
        query_conditions = Q(title__icontains=query) | Q(content__icontains=query) | Q(tags__name__icontains=query)
        posts = cls.objects.filter(query_conditions)
        return sort_queries(posts, sort_by, 'post_upvotes')

    def upvote_count(self):
        return self.post_upvotes.count()
    
    def first_media(self):
        return self.media_post.first()
    
    def top_level_comments_count(self):
        return self.comments.filter(parent=None).count()
    
    def total_comments(self):
        return self.comments.count()
    
    def __str__(self):
        return self.title
    
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)  
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies') 
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    @classmethod
    def search(cls, query, sort_by='-upvotes_count'):
        comments = cls.objects.filter(text__icontains=query)
        return sort_queries(comments, sort_by, 'comment_upvotes')

    def __str__(self):
        return f"Comment by {self.user} in Post: {self.post.title}"

    def upvote_count(self):
        return self.comment_upvotes.count()
    
    
class Media(models.Model):
    post = models.ForeignKey(Post, null=True, blank=True, related_name="media_post", on_delete=models.CASCADE) 
    media = models.FileField(upload_to='', null=True, blank=True)
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Media Post: {self.post}, ID: {self.post.id}, user: {self.post.user}"
    
    def is_video(self):
        if self.media:
            return self.media.name.lower().endswith(
                ('.mp4', '.mov', '.webm')
            )
        return False


class Upvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="post_upvotes", null=True, blank=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name="comment_upvotes", null=True, blank=True, on_delete=models.CASCADE)
    upvoted_at = models.DateTimeField(default=timezone.now)

    unique_together = (
        ('user', 'post'),
        ('user', 'comment'),
    ) 

    def __str__(self):
        return f"Upvote by {self.user} for {'Post' if self.post else 'Comment'} ID {self.post.id if self.post else self.comment.id}"


class Save(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, null=True, blank=True, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(default=timezone.now)

    unique_together = (
        ('user', 'post'),
        ('user', 'comment'),
    ) 

    def __str__(self):
        return f"Saved by {self.user} for {'Post' if self.post else 'Comment'} ID {self.post.id if self.post else self.comment.id}"


class Flag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, null=True, blank=True, on_delete=models.CASCADE)
    reason = models.TextField()
    flagged_at = models.DateTimeField(default=timezone.now)

    unique_together = (
        ('user', 'post'),
        ('user', 'comment'),
    ) 

    def __str__(self):
        return f"Flagged by {self.user} for {'Post' if self.post else 'Comment'} ID {self.post.id if self.post else self.comment.id}"