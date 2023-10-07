from django.db import models

class Product(models.Model):
    company_name = models.CharField(max_length=255)
    chemical_name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    expiry_date = models.DateField()
    manufacturer = models.CharField(max_length=255)
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.chemical_name
