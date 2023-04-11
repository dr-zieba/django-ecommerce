from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse

from .models import Brand, Category, Product, ProductLine, ProductImage


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


class ProductLineAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
    ]


# Register your models here.
admin.site.register(ProductLine, ProductLineAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Brand)
admin.site.register(Category)
