from django.db import models

class Inventory(models.Model):
    name = models.CharField(max_length=255)  # You can provide a name for the inventory.
    items = models.ManyToManyField('Item')

    # Add other fields as needed

    def __str__(self):
        return self.name  # You can customize this based on your requirements.


    class Meta:
        verbose_name_plural = 'Inventories'