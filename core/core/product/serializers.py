from rest_framework import serializers
from .models import (
    Brand,
    Category,
    Product,
    ProductLine,
    ProductImage,
    Attribute,
    AttributeValue,
    ProductType,
)


class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="name")

    class Meta:
        model = Category
        fields = ["category_name"]


class BrandSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source="name")

    class Meta:
        model = Brand
        fields = ["brand_name"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ("id", "product_line")


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ("name",)


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(many=False)

    class Meta:
        model = AttributeValue
        fields = ("attribute", "attribute_value")


class ProductLineSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)
    attribute_value = AttributeValueSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = ("price", "sku", "stock", "order", "product_image", "attribute_value")


class ProductSerializer(serializers.ModelSerializer):
    brand_name = serializers.ReadOnlyField(source="brand.name")
    category_name = serializers.ReadOnlyField(source="category.name")
    product_line = ProductLineSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            "name",
            "slug",
            "description",
            "brand_name",
            "category_name",
            "product_line",
        )
