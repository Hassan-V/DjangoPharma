from django.db import models
from django.contrib.auth.models import User  # Assuming you're using the built-in User model
from .customer_model import Customer

class Order(models.Model):
    customer = models.ForeignKey(Customer, default=1, on_delete=models.SET_DEFAULT)
    date_time = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20)  # You can use choices for status options

    def __str__(self):
        return f"Order {self.id} by {self.customer.name}"
