from django import forms
from .models import Post, Media

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'url', 'tags'] 
        widgets = {
            'tags': forms.CheckboxSelectMultiple(attrs={'class': 'custom-checkbox'}),
            'title': forms.TextInput(attrs={'placeholder': 'Enter the title of the post'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write your content here'}),
            'url': forms.URLInput(attrs={'placeholder': 'Optional URL for the post'}),
        }


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['media'] 

    def clean_media(self):
        media = self.cleaned_data.get('media')
        valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', 'avif', 'webp', '.mp4', '.mov', '.webm'}
        if media and not any(media.name.lower().endswith(ext) for ext in valid_extensions):
            raise forms.ValidationError("File type not supported")
        return media