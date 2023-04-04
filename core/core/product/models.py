from django.core.exceptions import ValidationError
from django.db import models

# Library to store indented data efectivly
from mptt.models import MPTTModel, TreeForeignKey
from .fields import OrderField


class ActiveFilter(models.QuerySet):
    def is_active(self):
        return self.filter(is_active=True)


class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    # field to store relation between categories
    # on_delete=models.PROTECT: prevents from delete if child exists
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = TreeForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, blank=True
    )
    is_active = models.BooleanField(default=False)

    objects = ActiveFilter().as_manager()

    def __str__(self):
        return self.name


class ProductLine(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=5)
    sku = models.CharField(max_length=100)
    stock = models.IntegerField()
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_line"
    )
    is_active = models.BooleanField(default=False)
    order = OrderField(unique_for_field="product", blank=True)

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        queryset = ProductLine.objects.filter(product=self.product)
        for obj in queryset:
            if obj.id != self.id and obj.order == self.order:
                raise ValidationError("Order value must be uique")

    def __str__(self):
        return self.sku
