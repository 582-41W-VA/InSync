from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=255, blank=True, null=True)
    profile_image = models.FileField(upload_to='', blank=True, null=True)
    job_title = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'Profile user: {self.user.username}'
    
    def first_profile_image(self):
        return self.profile_image if self.profile_image else None