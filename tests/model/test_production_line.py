import pytest

from model.order import Order
from model.production_line import ProductionLine
from model.sample import Sample


def _sample(yield_rate=0.8, avg_production_time=10, inventory=0):
    return Sample(
        sample_id="S-001",
        name="SiC 파워기판-6인치",
        avg_production_time=avg_production_time,
        yield_rate=yield_rate,
        inventory=inventory,
    )


def _order(quantity=16):
    return Order(order_id=1, sample_id="S-001", customer="삼성전자", quantity=quantity, status="PRODUCING")


def test_enqueue_adds_job_to_pending_queue():
    line = ProductionLine()

    line.enqueue(_order(), _sample(), shortfall=16)

    assert len(line.list_pending()) == 1


def test_list_pending_preserves_fifo_order():
    line = ProductionLine()
    first_order = _order(quantity=16)
    second_order = Order(order_id=2, sample_id="S-001", customer="SK하이닉스", quantity=30, status="PRODUCING")

    line.enqueue(first_order, _sample(), shortfall=16)
    line.enqueue(second_order, _sample(), shortfall=30)

    pending = line.list_pending()
    assert pending[0].order is first_order
    assert pending[1].order is second_order


def test_complete_next_adds_only_surplus_to_inventory():
    line = ProductionLine()
    sample = _sample(yield_rate=0.8, inventory=0)
    line.enqueue(_order(quantity=16), sample, shortfall=16)

    line.complete_next()

    assert sample.inventory == 4


def test_complete_next_sets_order_status_confirmed():
    line = ProductionLine()
    order = _order(quantity=16)
    line.enqueue(order, _sample(), shortfall=16)

    line.complete_next()

    assert order.status == "CONFIRMED"


def test_complete_next_removes_job_from_pending_queue():
    line = ProductionLine()
    first_order = _order(quantity=16)
    second_order = Order(order_id=2, sample_id="S-001", customer="SK하이닉스", quantity=30, status="PRODUCING")
    line.enqueue(first_order, _sample(), shortfall=16)
    line.enqueue(second_order, _sample(), shortfall=30)

    line.complete_next()

    pending = line.list_pending()
    assert len(pending) == 1
    assert pending[0].order is second_order


def test_enqueue_computes_actual_quantity_immediately():
    line = ProductionLine()

    line.enqueue(_order(quantity=16), _sample(yield_rate=0.8), shortfall=16)

    job = line.list_pending()[0]
    assert job.actual_quantity == 20


def test_enqueue_computes_production_time_immediately():
    line = ProductionLine()

    line.enqueue(_order(quantity=16), _sample(yield_rate=0.8, avg_production_time=10), shortfall=16)

    job = line.list_pending()[0]
    assert job.production_time == 200


def test_complete_next_raises_when_queue_empty():
    line = ProductionLine()

    with pytest.raises(ValueError):
        line.complete_next()
