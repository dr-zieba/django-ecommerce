from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse

from .models import (
    Brand,
    Category,
    Product,
    ProductLine,
    ProductImage,
    AttributeValue,
    Attribute,
    ProductType,
)


class EditLineInLine:
    def edit(self, instance):
        url = reverse(
            f"admin:{instance._meta.app_label}_{instance._meta.model_name}_change",
            args=[instance.pk],
        )

        if instance.pk:
            link = mark_safe(f'<a href="{url}">edit</a>')
            return link
        else:
            return ""


class ProductInLine(EditLineInLine, admin.TabularInline):
    model = ProductLine
    readonly_fields = ("edit",)


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductInLine]


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class AttributeValueInLine(admin.TabularInline):
    # model specified as below due AttributeValue do not have FK to ProductLine model
    # used name of relation field
    model = AttributeValue.product_line_attribute_value.through


class ProductLineAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
        AttributeValueInLine,
    ]


class AttributeInLine(admin.TabularInline):
    model = Attribute.product_type_attribute.through


class ProductTypeInLine(admin.ModelAdmin):
    inlines = [
        AttributeInLine,
    ]


# Register your models here.
admin.site.register(ProductLine, ProductLineAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(ProductType, ProductTypeInLine)
