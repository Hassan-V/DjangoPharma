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
from django.urls import path, include
from . import views

app_name = "main"

urlpatterns = [
    path('',views.homepage, name = "HomePage"),
    path('register/',views.register ,name = "Register"),
    path('logout/',views.logout_request ,name = "Logout"),
    path('login/',views.login_request ,name = "Login"),
    path('dashboard/',views.dashboard ,name = "Dashboard"),
    path('products/',views.products ,name = "Products"),
    path('orders/',views.dashboard ,name = "Orders"),
]
handler404 = 'main.views.error_page'