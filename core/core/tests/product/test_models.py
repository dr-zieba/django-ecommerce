import pytest
from django.core.exceptions import ValidationError

pytestmark = pytest.mark.django_db

"""
    Factories are registered in factory.py
    To use factory class reference is in lowercase with _ as word separator eq.
    CategoryFactory -> category_factory
"""


class TestCategoryModel:
    def test_str_method(self, category_factory):
        # Arrange
        obj = category_factory(name="test_category")
        # Assert
        assert obj.__str__() == "test_category"


class TestBrandModel:
    def test_str_method(self, brand_factory):
        # Arrange
        obj = brand_factory(name="test_brand")
        # Assert
        assert obj.__str__() == "test_brand"


class TestProductModel:
    def test_str_method(self, product_factory):
        # Arrange
        obj = product_factory(name="test_product")
        # Assert
        assert obj.__str__() == "test_product"


class TestProductLine:
    def test_str_method(self, product_line_factory):
        obj = product_line_factory(sku="111")
        assert obj.__str__() == "111"

    def test_duplicate_order_values(self, product_line_factory, product_factory):
        obj = product_factory()
        product_line_factory(order=1, product=obj)
        with pytest.raises(ValidationError):
            product_line_factory(order=1, product=obj)


class TestProductImage:
    def test_str_method(self, product_image_factory):
        obj = product_image_factory()
        assert obj.__str__() == "https://test.com/test.jpg"
