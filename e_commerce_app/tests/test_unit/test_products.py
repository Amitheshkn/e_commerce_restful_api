from unittest.mock import patch, MagicMock
from e_commerce_app.api.products.actions import ProductActions
from e_commerce_app.schemas.products_schema import ProductCreate


def test_create_product():
    mock_adapter = MagicMock()
    mock_adapter.insert_doc.return_value = "mocked_product_id"

    with patch("e_commerce.db.adapters.MongoAdapter", return_value=mock_adapter):
        service = ProductActions()

        product_data = ProductCreate(
            name="Test Product",
            description="Test Description",
            price=100.0,
            stock=10
        )
        result = service.create_product(product_data)

        assert result.id == "mocked_product_id"
        assert result.name == "Test Product"
        assert result.price == 100.0
        mock_adapter.insert_doc.assert_called_once_with(product_data.dict())


def test_get_product():
    mock_adapter = MagicMock()
    mock_adapter.find_doc.return_value = {
        "_id": "mocked_id", "name": "Test Product", "description": "Test Description", "price": 100.0, "stock": 10
    }

    with patch("e_commerce.db.adapters.MongoAdapter", return_value=mock_adapter):
        service = ProductActions()
        result = service.get_all_products()

        # Assertions
        assert result[0].id == "mocked_id"
        assert result[0].name == "Test Product"
        mock_adapter.find_doc.assert_called_once_with({"_id": "mocked_id"})
