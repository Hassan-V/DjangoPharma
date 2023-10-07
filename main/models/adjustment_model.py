from django.db import models
from django.contrib.auth.models import User  # Assuming you're using the built-in User model
from .product_model import Product

class Adjustment(models.Model):
    product = models.ForeignKey(Product, default=1, on_delete=models.SET_DEFAULT)
    ADJUSTMENT_TYPES = (
        ('percentage', 'Percentage'),
        ('fixed_amount', 'Fixed Amount'),
    )
    adjustment_type = models.CharField(max_length=20, choices=ADJUSTMENT_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    administrator = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT)
    date_time = models.DateTimeField()

    def __str__(self):
        return f"Adjustment for {self.product.chemical_name}"
