from django.shortcuts import render, redirect
from main.forms.CustomUserCreationForm import CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

# Create your views here.
def homepage(request):
    return render(request, 'main_hompage.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user= form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New User Created, Welcome {username}!")
            login(request, user)

            return redirect("main:HomePage")
        
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
    else:
        form = CustomUserCreationForm()  # Create an instance of the form

    return render(request, 'main_register.html', {'form': form})