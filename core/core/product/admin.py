from django.contrib import admin
from .models import Brand, Category, Product, ProductLine


class ProductInLine(admin.TabularInline):
    model = ProductLine


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductInLine]


# Register your models here.
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(ProductLine)
