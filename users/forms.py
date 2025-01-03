from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Tag

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class UserTagForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text="Enter tags separated by commas (e.g., Python, Django, AI)"
    )

    class Meta:
        model = CustomUser
        fields = ['bio', 'tags']

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
    