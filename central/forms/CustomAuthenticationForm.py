from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'bg-gray-200 rounded-lg p-2 focus:outline-none focus:ring focus:border-blue-500 w-full'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'bg-gray-200 rounded-lg p-2 focus:outline-none focus:ring focus:border-blue-500 w-full'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize labels or help text if needed
        self.fields['username'].label = 'Username or Email'
