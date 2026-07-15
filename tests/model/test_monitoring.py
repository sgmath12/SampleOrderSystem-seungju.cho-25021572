from model.monitoring import (
    count_orders_by_status,
    inventory_status,
    reserved_quantity_for_sample,
)
from model.order import Order


def _order(order_id, sample_id, quantity, status):
    return Order(order_id=order_id, sample_id=sample_id, customer="고객", quantity=quantity, status=status)


def test_count_orders_by_status_excludes_rejected():
    orders = [
        _order(1, "S-001", 10, "RESERVED"),
        _order(2, "S-001", 10, "REJECTED"),
    ]

    counts = count_orders_by_status(orders)

    assert "REJECTED" not in counts


def test_count_orders_by_status_counts_each_status():
    orders = [
        _order(1, "S-001", 10, "RESERVED"),
        _order(2, "S-001", 10, "RESERVED"),
        _order(3, "S-001", 10, "CONFIRMED"),
    ]

    counts = count_orders_by_status(orders)

    assert counts == {"RESERVED": 2, "CONFIRMED": 1}


def test_reserved_quantity_for_sample_sums_matching_reserved_orders():
    orders = [
        _order(1, "S-001", 10, "RESERVED"),
        _order(2, "S-001", 20, "RESERVED"),
        _order(3, "S-001", 100, "CONFIRMED"),
        _order(4, "S-002", 999, "RESERVED"),
    ]

    total = reserved_quantity_for_sample(orders, "S-001")

    assert total == 30


def test_inventory_status_is_exhausted_when_zero():
    assert inventory_status(inventory=0, reserved_quantity=10) == "고갈"


def test_inventory_status_is_short_when_less_than_reserved():
    assert inventory_status(inventory=5, reserved_quantity=10) == "부족"


def test_inventory_status_is_sufficient_when_greater_or_equal():
    assert inventory_status(inventory=10, reserved_quantity=10) == "여유"
