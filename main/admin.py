from django.contrib import admin
from .models.item_model import Item
from .models.inventory_model import Inventory
from tinymce.widgets import TinyMCE
from django.db import models
# Register your models here.

class ItemAdmin(admin.ModelAdmin):
    form_field_overrides = {
        models.TextField: {"widget":TinyMCE()}
    }

admin.site.register(Item)
admin.site.register(Inventory)