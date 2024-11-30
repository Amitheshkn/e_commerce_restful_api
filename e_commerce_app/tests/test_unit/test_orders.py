from unittest.mock import MagicMock, patch
from e_commerce_app.api.orders.actions import OrderActions
from e_commerce_app.schemas.orders_schema import OrderCreate


def test_create_order_success():
    mock_product_adapter = MagicMock()
    mock_order_adapter = MagicMock()

    mock_product_adapter.find_doc.side_effect = [
        {"_id": "product_id_1", "price": 50.0, "stock": 5},
        {"_id": "product_id_2", "price": 100.0, "stock": 10},
    ]
    mock_product_adapter.update_doc.return_value = True

    # Mock order insertion
    mock_order_adapter.insert_doc.return_value = "mocked_order_id"

    with patch("e_commerce.db.adapters.MongoAdapter", side_effect=[mock_product_adapter, mock_order_adapter]):
        order_service = OrderActions()

        # Test data
        order_data = OrderCreate(
            products=[
                {"product_id": "product_id_1", "quantity": 2},
                {"product_id": "product_id_2", "quantity": 1},
            ]
        )

        result = order_service.create_order(order_data)

        assert result.id == "mocked_order_id"
        assert result.status == "completed"
        assert result.total_price == 200.0
        mock_product_adapter.find_doc.assert_any_call({"_id": "product_id_1"})
        mock_product_adapter.find_doc.assert_any_call({"_id": "product_id_2"})
        mock_product_adapter.update_doc.assert_any_call(
            {"_id": "product_id_1"}, {"$inc": {"stock": -2}}
        )
        mock_product_adapter.update_doc.assert_any_call(
            {"_id": "product_id_2"}, {"$inc": {"stock": -1}}
        )
        mock_order_adapter.insert_doc.assert_called_once()


def test_create_order_insufficient_stock():
    mock_product_adapter = MagicMock()
    mock_order_adapter = MagicMock()

    mock_product_adapter.find_doc.return_value = {"_id": "product_id_1", "price": 50.0, "stock": 1}

    # Patch the MongoAdapter to use the mocks
    with patch("e_commerce.db.adapters.MongoAdapter", side_effect=[mock_product_adapter, mock_order_adapter]):
        order_service = OrderActions()

        order_data = OrderCreate(
            products=[
                {"product_id": "product_id_1", "quantity": 3},
            ]
        )

        try:
            order_service.create_order(order_data)
        except ValueError as e:
            assert str(e) == "Insufficient stock for product_id: product_id_1"
        mock_product_adapter.find_doc.assert_called_once_with({"_id": "product_id_1"})
