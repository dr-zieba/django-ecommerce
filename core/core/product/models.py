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
    slug = models.SlugField(max_length=255)

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


class Attribute(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    attribute_value = models.CharField(max_length=100)
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name="attribute_value"
    )

    def __str__(self):
        return f"{self.attribute}{self.attribute_value}"


class ProductLine(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=5)
    sku = models.CharField(max_length=100)
    stock = models.IntegerField()
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_line"
    )
    is_active = models.BooleanField(default=False)
    attribute_value = models.ManyToManyField(
        AttributeValue,
        through="ProductLineAttributeValues",
        related_name="product_line_attribute_value",
    )
    product_type = models.ForeignKey(
        "ProductType", on_delete=models.PROTECT, related_name="product_type"
    )
    order = OrderField(unique_for_field="product", blank=True)

    def clean(self):
        queryset = ProductLine.objects.filter(product=self.product)
        for obj in queryset:
            if obj.id != self.id and obj.order == self.order:
                raise ValidationError("Order value must be uique")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductLine, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.sku)


class ProductLineAttributeValues(models.Model):
    attribute_value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
        related_name="attribute_value_product_line",
    )
    product_line = models.ForeignKey(
        ProductLine,
        on_delete=models.CASCADE,
        related_name="product_line_attribute_value",
    )

    class Meta:
        unique_together = ("attribute_value", "product_line")


class ProductImage(models.Model):
    alternative_text = models.CharField(max_length=255)
    url = models.ImageField(upload_to=None)
    product_line = models.ForeignKey(
        ProductLine, on_delete=models.CASCADE, related_name="product_image"
    )
    order = OrderField(unique_for_field="product_line", blank=True)

    def clean(self):
        queryset = ProductImage.objects.filter(product_line=self.product_line)
        for obj in queryset:
            if obj.id != self.id and obj.order == self.order:
                raise ValidationError("Order value must be uique")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductImage, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.url)


class ProductType(models.Model):
    name = models.CharField(max_length=100)
    attribute = models.ManyToManyField(
        Attribute, through="ProductTypeAttribute", related_name="product_type_attribute"
    )

    def __str__(self):
        return self.name


class ProductTypeAttribute(models.Model):
    product_type = models.ForeignKey(
        ProductType, on_delete=models.CASCADE, related_name="product_type_attribute"
    )
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name="attribute_product_type"
    )

    class Meta:
        unique_together = ("product_type", "attribute")
