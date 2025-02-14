from django import forms
from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email', 'job_title']

class ProfileImage(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image']

    def clean_profile_image(self):
        image = self.cleaned_data.get('profile_image')
        if image:
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            if image and not any(image.name.lower().endswith(ext) for ext in valid_extensions):
                raise forms.ValidationError("File type not supported")
        return image