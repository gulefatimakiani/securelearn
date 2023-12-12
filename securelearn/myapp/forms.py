
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import tutorial, registeredusers, comment

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import EmailValidator, MinLengthValidator, RegexValidator


#Form for a new user registration
class CreateUserForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[
            MinLengthValidator(limit_value=4, message="Username must be at least 4 characters long."),
            RegexValidator(
                regex='^[a-zA-Z0-9]+$',
                message='Username must contain only alphanumeric characters.',
                code='invalid_username'
            ),
        ]
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        validators=[
            EmailValidator(message="Enter a valid email address."),
        ]
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=[
            MinLengthValidator(limit_value=8, message="Password must be at least 8 characters long."),
        ]
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=[
            MinLengthValidator(limit_value=8, message="Password must be at least 8 characters long."),
        ]
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


#login form
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


#form for add a new comment
class comment_form(forms.ModelForm):
    class Meta:
        model = comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }

#form for add new tutorial
class tutorial_form(forms.ModelForm):
    class Meta:
        model = tutorial
        fields = ['title', 'category','slug','description', 'content', 'author', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}), 
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            
        }

#Form for rating system
class RatingForm(forms.Form):
    rating = forms.ChoiceField(choices=[(1, '★'), (2, '★★'), (3, '★★★'), (4, '★★★★'), (5, '★★★★★')], widget=forms.RadioSelect)
    tutorial_slug = forms.CharField(widget=forms.HiddenInput())

