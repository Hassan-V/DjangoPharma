from django.db import models

class Discount(models.Model):
    DISCOUNT_TYPES = (
        ('percentage', 'Percentage'),
        ('fixed_amount', 'Fixed Amount'),
    )
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    applicability = models.CharField(max_length=255)  # Define the applicability logic
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.get_discount_type_display()} {self.amount}%"
