from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Tag

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['bio', 'tags', 'contact_phone', 'location']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        tag_names = self.cleaned_data['tags']
        if commit:
            user.save()
            # Split tags by comma and create them if they don't exist
            if tag_names:
                tag_list = [name.strip() for name in tag_names.split(',')]
                for tag_name in tag_list:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    user.tags.add(tag)
        return user
    