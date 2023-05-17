import factory

from ..product.models import (
    Attribute,
    AttributeValue,
    Category,
    Product,
    ProductLine,
    ProductImage,
    ProductType,
    ProductTypeAttribute,
)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda x: f"Test-Category_{x}")
    slug = factory.Sequence(lambda x: f"Test-SLUG_{x}")


class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductType

    name = "test_name"


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f"Product_name_{n}")
    pid = factory.Sequence(lambda n: f"000_{n}")
    description = factory.Sequence(lambda n: f"Product_description_{n}")
    is_digital = False
    category = factory.SubFactory(CategoryFactory)
    # product_type = factory.SubFactory(ProductTypeFactory)
    is_active = True
    product_type = factory.SubFactory(ProductTypeFactory)


class ProductLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLine

    price = 100
    sku = "111"
    stock = 5
    product = factory.SubFactory(ProductFactory)
    is_active = False
    weight = 100.00
    product_type = factory.SubFactory(ProductTypeFactory)

    @factory.post_generation
    def attribute_value(self, created, extraced, **kwargs):
        if not created or not extraced:
            return
        self.attribute_value.add(*extraced)


class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductType

    name = factory.Sequence(lambda n: f"Product type {n}")

    @factory.post_generation
    def attribute(self, created, extracted, **kwargs):
        if not created or not extracted:
            return
        self.attribute.add(*extracted)


class AttributeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Attribute

    name = "test_attribute"
    description = "test_description"


class ProductTypeAttributeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductTypeAttribute

    product_type = factory.SubFactory(ProductTypeFactory)
    attribute = factory.SubFactory(AttributeFactory)


class ProductImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductImage

    alternative_text = "test"
    url = "https://test.com/test.jpg"
    product_line = factory.SubFactory(ProductLineFactory)
    order = 1


class AttributeValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AttributeValue

    attribute_value = "test_attr_val"
    attribute = factory.SubFactory(AttributeFactory)
