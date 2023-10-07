from django.shortcuts import render, redirect
from main.forms.CustomUserCreationForm import CustomUserCreationForm
from main.forms.CustomAuthenticationForm import CustomAuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

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


def logout_request(request):
    messages.info(request, f"Logged Out Successfully")
    logout(request)

    return redirect("main:HomePage")

def login_request(request):
    if request.user.is_authenticated:
        return redirect("main:HomePage")
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']

            password = form.cleaned_data['password']

            user = authenticate(request=request, username=username, password=password)


            if user is not None:
                login(request, user)
                messages.info(request, f"Logged In Successfully, Welcome Back {username}!")

                return redirect("main:HomePage")
        
            else:
                messages.error(request, f"Invalid Username or Password")

        else:
            messages.error(request, f"Invalid Username or Password")


    else:
        form = CustomAuthenticationForm()
        return render(request, "main_login.html", {"form": form})


def dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            # Staff or superuser, allow access to the dashboard
            return render(request, 'main_dashboard.html')
        else:
            # Authenticated but not staff, you can handle this case, e.g., show an error message or redirect
            return error_page(request,"Invalid User Permissions!")
    else:
        # Not authenticated, redirect to login
        return redirect("main:HomePage")
        
        
def error_page(request, data):
    return render(request,"main_error.html", context={"data": data})