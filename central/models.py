from datetime import date
from decimal import Decimal
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from docserver import settings

User = get_user_model()

class Discount(models.Model):
    DISCOUNT_TYPES = (
        ('percentage', 'Percentage'),
        ('fixed_amount', 'Fixed Amount'),
    )
    discount_type : str = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    amount : float = models.DecimalField(max_digits=10, decimal_places=2)
    applicability: bool = models.BooleanField()  # Define the applicability logic
    start_date : date = models.DateField()
    end_date : date = models.DateField()

    def apply(self, amount):
        if not isinstance(amount, Decimal):
            raise ValidationError({
                'amount': _('Amount should be a decimal number.')
            })
        if self.discount_type == 'percentage':
            return amount * (1 - self.amount / 100)
        else:  # self.discount_type == 'fixed_amount'
            return max(0, amount - self.amount)

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError({
                'end_date': _('End date should be after start date.')
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_discount_type_display()} {self.amount}%"
    
class Product(models.Model):
    CATEGORY_CHOICES = (
        ('tablet', 'Tablet'),
        ('syrup', 'Syrup'),
        ('injection', 'Injection'),
        ('miscellaneous', 'Miscellaneous'),
    )

    company_name = models.CharField(max_length=255)
    chemical_name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    expiry_date = models.DateField()
    manufacturer = models.CharField(max_length=255)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='product_images/')

    def clean(self):
        if self.price and self.price < 0:
            raise ValidationError({
                'price': _('Price should be a positive number.')
            })
        if self.expiry_date and self.expiry_date < date.today():
            raise ValidationError({
                'expiry_date': _('Expiry date should be in the future.')
            })
        if self.quantity and self.quantity < 1:
            raise ValidationError({
                'quantity': _('Quantity should be at least 1.')
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.chemical_name
    

class Order(models.Model):
    STATUS_CHOICES = (
        ('cart', 'Cart'),
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='cart')
    discounts = models.ManyToManyField(Discount, related_name='orders')

    def calculate_subtotal(self):
        return sum(item.subtotal_price for item in self.items.all())

    def calculate_total_price(self):
        subtotal = self.calculate_subtotal()
        for discount in self.discounts.all():
            if discount.applicability:
                subtotal = discount.apply(subtotal)
        total_price = subtotal * (1 + self.tax_rate / 100)
        return total_price

    def clean(self):
        self.total_price = self.calculate_total_price()
        if self.total_price < 0:
            raise ValidationError({'total_price': _('Total price should be a positive number.')})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} by {self.customer.name if self.customer else 'Anonymous'}"
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL, related_name='items')
    quantity = models.PositiveIntegerField()

    @property
    def subtotal_price(self):
        return self.quantity * self.product.price 

    def clean(self):
        if self.quantity and self.quantity < 1:
            raise ValidationError({
                'quantity': _('Quantity should be at least 1.')
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.chemical_name} in Order {self.order.id}"
    
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
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=255, null=True, blank=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    @property
    def total_price(self):
        return self.quantity * self.product.price