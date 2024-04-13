from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'bg-gray-200 rounded-lg p-2 focus:outline-none focus:ring focus:border-blue-500 w-full'})

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user