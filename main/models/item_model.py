from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    #category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    acquiry_date = models.DateField()
    expiration_date = models.DateField()
    #supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)

    # Add other fields as needed

    def __str__(self):
        return self.name


    class Meta:
        verbose_name_plural = 'Items'