from django.contrib import admin
from tinymce.widgets import TinyMCE
from django.db import models
# Register your models here.

from .models.adjustment_model import Adjustment
from .models.order_model import Order
from .models.customer_model import Customer
from .models.discount_model import Discount
from .models.orderitem_model import OrderItem
from .models.product_model import Product

class ItemAdmin(admin.ModelAdmin):
    form_field_overrides = {
        models.TextField: {"widget":TinyMCE()}
    }

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Product)
admin.site.register(Adjustment)
admin.site.register(Discount)