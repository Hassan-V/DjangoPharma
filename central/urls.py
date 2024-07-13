"""
URL configuration for docserver project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = "central"

urlpatterns = [
    path('', views.homepage, name="HomePage"),
    path('register/', views.register, name="Register"),
    path('logout/', views.logout_request, name="Logout"),
    path('login/', views.login_request, name="Login"),
    path('contact/', views.contact_request, name="Contact"),
    path('products/', views.products, name="Product-Listing"),
    path('product/<int:product_id>/', views.product_detail, name="Product_Detail"),
    path('cart/', views.cart_detail, name="view-cart"),
    path('cart/add/<int:product_id>/', views.add_to_cart_view, name='add-to-cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('update_cart_item_quantity/<int:product_id>/', views.update_cart_item_quantity_view, name='update_cart_item_quantity'),
    #path('staff-dashboard/', views.staff_dashboard, name="Staff-Dashboard"),
    #path('staff-products/', views.staff_products, name="Staff-Products"),
    #path('staff-orders/', views.staff_orders, name="Staff-Orders"),
]
handler404 = 'central.views.error_page'