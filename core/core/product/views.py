from django.db import connection
from django.db.models import Prefetch
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from .models import Category, Product, ProductLine, ProductImage
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductCategorySerializer,
)
from django.db import models

# Create your views here.


class CategoryView(viewsets.ViewSet):
    queryset = Category.objects.all().is_active()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)


# class BrandView(viewsets.ViewSet):
#     queryset = Brand.objects.all()
#
#     @extend_schema(responses=BrandSerializer)
#     def list(self, request):
#         serializer = BrandSerializer(self.queryset, many=True)
#         return Response(serializer.data)


class ProductView(viewsets.ViewSet):
    queryset = Product.objects.all()
    lookup_field = "slug"

    def retrieve(self, request, slug=None):
        serializer = ProductSerializer(
            self.queryset.filter(slug=slug)
            .prefetch_related(Prefetch("attribute_value__attribute"))
            .prefetch_related(Prefetch("product_line__product_image"))
            .prefetch_related(Prefetch("product_line__attribute_value__attribute")),
            many=True,
        )
        return Response(serializer.data)

    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=["get"],
        detail=False,
        url_path=r"category/(?P<slug>\S+)",
        url_name="all",
    )
    def list_product_by_category(self, request, slug=None):
        """Viewset of products filtered by category name"""
        serializer = ProductCategorySerializer(
            self.queryset.filter(category__slug=slug)
            .prefetch_related(
                Prefetch("product_line", queryset=ProductLine.objects.order_by("order"))
            )
            .prefetch_related(
                Prefetch(
                    "product_line__product_image",
                    queryset=ProductImage.objects.filter(order=1),
                )
            ),
            many=True,
        )
        return Response(serializer.data)
