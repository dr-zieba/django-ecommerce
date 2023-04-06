import pytest
import json

pytestmark = pytest.mark.django_db


class TestCategoryEndpoint:
    endpoint = "/api/category/"

    def test_category_get(self, category_factory, api_client):
        category_factory.create_batch(4)
        respons = api_client().get(self.endpoint)
        assert respons.status_code == 200
        assert len(json.loads(respons.content)) == 4


class TestBrandEndpoint:
    endpoint = "/api/brand/"

    def test_brand_get(self, brand_factory, api_client):
        brand_factory.create_batch(4)
        response = api_client().get(self.endpoint)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 4


class TestProductEndpoint:
    endpoint = "/api/product/"

    def test_get_all_products(self, product_factory, api_client):
        product_factory.create_batch(4)
        response = api_client().get(self.endpoint)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 4

    def test_get_product_by_name(self, product_factory, api_client):
        obj = product_factory(slug="test_product")
        response = api_client().get(f"{self.endpoint}{obj.slug}/")
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    def test_get_products_by_category_name(
        self, category_factory, product_factory, api_client
    ):
        obj = category_factory(slug="test_category")
        product_factory(category=obj)
        response = api_client().get(f"{self.endpoint}category/{obj.slug}/")
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1
