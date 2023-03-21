import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient
from core.tests import factories

register(factories.CategoryFactory)
register(factories.BrandFactory)
register(factories.ProductFactory)

@pytest.fixture
def api_client():
    return APIClient