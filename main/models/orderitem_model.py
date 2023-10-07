from django.db import models
from .product_model import Product
from .order_model import Order

class OrderItem(models.Model):
    product = models.ForeignKey(Product, default=1, on_delete=models.SET_DEFAULT)
    order = models.ForeignKey(Order, default=1, on_delete=models.SET_DEFAULT)
    quantity = models.PositiveIntegerField()
    subtotal_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.chemical_name} in Order {self.order.id}"
