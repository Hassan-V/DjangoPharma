from functools import wraps
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from central.forms.CustomUserCreationForm import CustomUserCreationForm
from central.forms.CustomAuthenticationForm import CustomAuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST  # Add this line
from .models import Cart, CartItem, Product

# Create your views here.
def homepage(request):
    return render(request, 'main_hompage.html')


def staff_or_superuser_required(view_func):
    @login_required
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return error_page(request, "Invalid User Permissions!")
    return _wrapped_view

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user= form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New User Created, Welcome {username}!")
            login(request, user)
            return redirect("central:HomePage")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
            # Add this line to return a response when the form is not valid
            return render(request, 'main_register.html', {'form': form})
    else:
        form = CustomUserCreationForm()  # Create an instance of the form
        return render(request, 'main_register.html', {'form': form})


def logout_request(request):
    messages.info(request, f"Logged Out Successfully")
    logout(request)

    return redirect("central:HomePage")

def login_request(request):
    if request.user.is_authenticated:
        return redirect("central:HomePage")
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request=request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.info(request, f"Logged In Successfully, Welcome Back {username}!")
                return redirect("central:HomePage")
            else:
                messages.error(request, f"Invalid Username or Password")
        else:
            messages.error(request, f"Invalid Username or Password")

        return render(request, "main_login.html", {"form": form})

    else:
        form = CustomAuthenticationForm()
        return render(request, "main_login.html", {"form": form})

@staff_or_superuser_required
def staff_dashboard(request):
    return render(request, 'main_dashboard.html')

@staff_or_superuser_required
def staff_products(request):
    return render(request, 'main_product.html')

@staff_or_superuser_required
def staff_orders(request):
    return render(request, 'main_order.html')
        
def error_page(request, data):
    return render(request,"main_error.html", context={"data": data})

def products(request):
    products = Product.objects.all() 
    return render(request, 'main_products.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'main_product_details.html', {'product': product})

def cart_detail(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = request.session.get('cart_id', None)
        if cart_id:
            cart, created = Cart.objects.get_or_create(id=cart_id)
        else:
            cart = None  # No cart available
    if cart:
        items = CartItem.objects.filter(cart=cart)
    else:
        items = []
    return render(request, 'main_cart.html', {'cart_items': items})


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = request.session.get('cart_id', None)
        if cart_id:
            cart, _ = Cart.objects.get_or_create(id=cart_id)
        else:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
    return cart

@require_POST
def add_to_cart_view(request, product_id, quantity=1):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    try:
        quantity = int(quantity)
    except ValueError:
        return JsonResponse({'status': 'error', 'message': 'Invalid quantity'})

    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    return JsonResponse({'status': 'success'})

@require_POST
def remove_from_cart(request, product_id):
    cart = get_or_create_cart(request)

    if cart:
        CartItem.objects.filter(cart=cart, product_id=product_id).delete()
        print('Product removed from cart')
    print('Product removed from cart')

    return JsonResponse({'status': 'success'})

@require_POST
def update_cart_item_quantity_view(request, product_id):
    try:
        data = json.loads(request.body)
        quantity = int(data.get('quantity', 1))
    except ValueError:
        return JsonResponse({'status': 'error', 'message': 'Invalid quantity'})
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'})

    cart = get_or_create_cart(request)

    if cart:
        cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
        if cart_item:
            cart_item.quantity = quantity
            cart_item.save()
            # Calculate the new total price using the total_price property
            new_total_price = cart_item.total_price
            # Return the new total price in the JsonResponse
            return JsonResponse({'status': 'success', 'new_total_price': str(new_total_price)})
        else:
            return JsonResponse({'status': 'error', 'message': 'Cart item not found'})

    return JsonResponse({'status': 'error', 'message': 'Cart not found'})