import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from core.product.models import Category, Product, ProductLine

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

    def test_name_max_lengh(self, category_factory):
        name = "X" * 256
        obj = category_factory(name=name)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_slug_max_leght(self, category_factory):
        name = "x" * 256
        obj = category_factory(name=name)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_unique_name(self, category_factory):
        category_factory(name="test")
        with pytest.raises(IntegrityError):
            category_factory(name="test")

    def test_unique_slug(self, category_factory):
        category_factory(slug="test")
        with pytest.raises(IntegrityError):
            category_factory(slug="test")

    def test_is_active(self, category_factory):
        obj = category_factory()
        assert obj.is_active == False

    def test_parent_directory_on_delete_protection(self, category_factory):
        obj1 = category_factory()
        category_factory(parent=obj1)
        with pytest.raises(IntegrityError):
            obj1.delete()

    def test_parent_null(self, category_factory):
        obj = category_factory()
        assert obj.parent is None

    def test_return_only_active_category(self, category_factory):
        obj1 = category_factory(is_active=True)
        obj2 = category_factory(is_active=False)
        qs = Category.objects.is_active().count()
        assert qs == 1

    def test_return_with_default_object_menager(self, category_factory):
        obj1 = category_factory(is_active=True)
        obj2 = category_factory(is_active=False)
        qs = Category.objects.all().count()
        assert qs == 2


class TestProductModel:
    def test_str_method(self, product_factory):
        # Arrange
        obj = product_factory(name="test_product")
        # Assert
        assert obj.__str__() == "test_product"

    def test_product_type_protection(self, product_factory, product_type_factory):
        obj1 = product_type_factory()
        obj2 = product_factory(product_type=obj1)
        with pytest.raises(IntegrityError):
            obj1.delete()

    def test_product_name_max_length(self, product_factory):
        name = "A" * 256
        obj = product_factory(name=name)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_product_slug_max_length(self, product_factory):
        slug = "A" * 256
        obj = product_factory(slug=slug)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_product_pid_max_length(self, product_factory):
        pid = 100 * 256
        obj = product_factory(pid=pid)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_product_is_digital(self, product_factory):
        obj = product_factory()
        assert obj.is_digital == False

    def test_delete_category(self, product_factory, category_factory):
        obj1 = category_factory()
        obj2 = product_factory(category=obj1)
        with pytest.raises(IntegrityError):
            obj1.delete()

    def test_return_only_active_true(self, product_factory):
        obj1 = product_factory(is_active=True)
        obj2 = product_factory(is_active=False)
        qs = Product.objects.is_active().count()
        assert qs == 1


class TestProductLine:
    def test_str_method(self, product_line_factory, attribute_value_factory):
        attr = attribute_value_factory(attribute_value="test")
        obj = product_line_factory.create(sku="111", attribute_value=(attr,))
        assert obj.__str__() == "111"

    def test_product_type_protection(self, product_line_factory, product_type_factory):
        obj1 = product_type_factory()
        obj2 = product_line_factory(product_type=obj1)
        with pytest.raises(IntegrityError):
            obj1.delete()

    def test_duplicate_order_values(self, product_line_factory, product_factory):
        obj = product_factory()
        product_line_factory(order=1, product=obj)
        with pytest.raises(ValidationError):
            product_line_factory(order=1, product=obj)

    def test_price_decimal_places(self, product_line_factory):
        price = 1.0092
        with pytest.raises(ValidationError):
            product_line_factory(price=price)

    def test_price_max_digits(self, product_line_factory):
        price = 99999.99
        with pytest.raises(ValidationError):
            product_line_factory(price=price)

    def test_sku_max_legth(self, product_line_factory):
        sku = "x" * 101
        with pytest.raises(ValidationError):
            product_line_factory(sku=sku)

    def test_if_is_active_false(self, product_line_factory):
        obj = product_line_factory()
        assert obj.is_active == False

    def test_product_protect(self, product_line_factory, product_factory):
        obj = product_factory()
        obj2 = product_line_factory(product=obj)
        with pytest.raises(IntegrityError):
            obj.delete()

    def test_is_active_objects_manager(self, product_line_factory):
        obj1 = product_line_factory(is_active=True)
        obj2 = product_line_factory(is_active=False)
        qs = ProductLine.objects.is_active().count()
        assert qs == 1


class TestProductImage:
    def test_str_method(self, product_image_factory, product_line_factory):
        prod_line = product_line_factory(sku="test_sku")
        obj = product_image_factory(product_line=prod_line)
        assert obj.__str__() == "test_sku"

    def test_alternative_text_max_lenght(self, product_image_factory):
        alternative_text = "a" * 256
        with pytest.raises(ValidationError):
            product_image_factory(alternative_text=alternative_text)

    def test_order_uniqe_number(self, product_image_factory, product_line_factory):
        obj = product_line_factory()
        product_image_factory(order=1, product_line=obj)
        with pytest.raises(ValidationError):
            product_image_factory(order=1, product_line=obj).clean()


class TestProductType:
    def test_str_method(self, product_type_factory, attribute_factory):
        test = attribute_factory(name="test")
        obj = product_type_factory.create(name="test_type", attribute=(test,))
        assert obj.__str__() == "test_type"

    def test_name_max_length(self, product_type_factory):
        name = "a" * 101
        obj = product_type_factory(name=name)
        with pytest.raises(ValidationError):
            obj.full_clean()


class TestAttribute:
    def test_str_method(self, attribute_factory):
        obj = attribute_factory(name="test_attr")
        assert obj.__str__() == "test_attr"

    def test_name_max_length(self, attribute_factory):
        name = "a" * 101
        obj = attribute_factory(name=name)
        with pytest.raises(ValidationError):
            obj.full_clean()


class TestAttributeValue:
    def test_str_method(self, attribute_value_factory, attribute_factory):
        obj_a = attribute_factory(name="test_attr")
        obj_b = attribute_value_factory(attribute_value="test_val", attribute=obj_a)
        assert obj_b.__str__() == "test_attr-test_val"

    def test_attribute_value_max_length(self, attribute_value_factory):
        attribute_value = "a" * 101
        obj = attribute_value_factory(attribute_value=attribute_value)
        with pytest.raises(ValidationError):
            obj.full_clean()
