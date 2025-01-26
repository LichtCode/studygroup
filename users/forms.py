from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Tag

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):        
        """
        Initializes the form with Bootstrap classes for all fields.

        This method is needed to define the form's appearance because the
        `AuthenticationForm` class does not provide a way to customize the
        form's appearance through its Meta class.
        """
        super().__init__(*args, **kwargs)
        # Add the Bootstrap class to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        """
        Initializes the UserRegistrationForm form.

        Adds the Bootstrap 'form-control' class to all fields to style the form inputs.
        """
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'bio', 'tags', 'contact_phone', 'location', 'tags']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
                
        """
        Saves the form data to the database.

        If `commit` is `True`, calls the parent class's `save` method to save the user
        instance to the database. Then, it takes the tags from the form data, splits them
        by comma, and creates each tag if it doesn't exist. If the tag exists, it adds the
        existing tag to the user's tags.

        If `commit` is `False`, the user instance is not saved to the database and the
        tags are not added.

        Returns the user instance, regardless of whether `commit` is `True` or `False`.
        """

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
    