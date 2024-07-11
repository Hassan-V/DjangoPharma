from django.contrib import admin
from tinymce.widgets import TinyMCE
from django.db import models
# Register your models here.

from .models import Adjustment, Order, Discount, OrderItem, Product, Cart, CartItem

class ItemAdmin(admin.ModelAdmin):
    form_field_overrides = {
        models.TextField: {"widget":TinyMCE()}
    }

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Product)
admin.site.register(Adjustment)
admin.site.register(Discount)
admin.site.register(Cart)
admin.site.register(CartItem)
#Shto Më shumë 