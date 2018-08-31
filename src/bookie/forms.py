from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    siteName = forms.CharField(max_length=30, required=False, help_text='This is the sitename users will use to log into your site, it can be anything')
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'siteName', 'password1', 'password2', )