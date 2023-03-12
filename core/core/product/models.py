from django.db import models

# Library to store indented data efectivly
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=100)
    # field to store relation between categories
    # on_delete=models.PROTECT: prevents from delete if child exists
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = TreeForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name
