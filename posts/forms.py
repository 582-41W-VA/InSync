from django import forms
from .models import Post, Media

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'url', 'tags'] 
        widgets = {
            'tags': forms.CheckboxSelectMultiple,
        }


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['media'] 

    def clean_media(self):
        media = self.cleaned_data.get('media')
        valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov', '.webm'}
        if media and not any(media.name.lower().endswith(ext) for ext in valid_extensions):
            raise forms.ValidationError("File type not supported")
        return media