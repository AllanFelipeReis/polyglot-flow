import pytest
from consumer import process_order


@pytest.mark.asyncio
async def test_high_value_order_should_alert_risk(capsys):
    # Arrange
    order = {"orderId": 1, "amount": 6000, "customerEmail": "suspect@test.com"}

    # Act
    await process_order(order)

    # Assert
    captured = capsys.readouterr()
    assert "ALTO RISCO" in captured.out
    assert "Pedido #1" in captured.out


@pytest.mark.asyncio
async def test_low_value_order_should_approve(capsys):
    # Arrange
    order = {"orderId": 2, "amount": 100, "customerEmail": "good@test.com"}

    # Act
    await process_order(order)

    # Assert
    captured = capsys.readouterr()
    assert "aprovado" in captured.out
