import factory

from ..product.models import Category, Brand, Product, ProductLine, ProductImage


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda x: f"Category_{x}")


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.Sequence(lambda x: f"Brand_{x}")


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = "test_product"
    description = "test_description"
    is_digital = True
    brand = factory.SubFactory(BrandFactory)
    category = factory.SubFactory(CategoryFactory)
    is_active = True


class ProductLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLine

    price = 100
    sku = "111"
    stock = 5
    product = factory.SubFactory(ProductFactory)
    is_active = True


class ProductImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductImage

    alternative_text = "test"
    url = "https://test.com/test.jpg"
    product_line = factory.SubFactory(ProductLineFactory)
    order = 1
