import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient
from core.tests import factories

register(factories.CategoryFactory)
register(factories.ProductFactory)
register(factories.ProductLineFactory)
register(factories.ProductImageFactory)
register(factories.ProductTypeFactory)
register(factories.AttributeFactory)
register(factories.AttributeValueFactory)


@pytest.fixture
def api_client():
    return APIClient
