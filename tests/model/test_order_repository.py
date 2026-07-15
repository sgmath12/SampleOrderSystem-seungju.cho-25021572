import pytest

from model.order import OrderRepository
from model.production_line import ProductionLine
from model.sample import SampleRepository


def _repo_with_registered_sample(sample_id="S-001"):
    sample_repository = SampleRepository()
    sample_repository.register(
        sample_id=sample_id,
        name="실리콘 웨이퍼-8인치",
        avg_production_time=30,
        yield_rate=0.9,
    )
    return sample_repository


def test_create_order_is_reserved_with_given_fields():
    sample_repository = _repo_with_registered_sample()
    order_repository = OrderRepository()

    order = order_repository.create(
        sample_repository, sample_id="S-001", customer="삼성전자", quantity=100
    )

    assert order.sample_id == "S-001"
    assert order.customer == "삼성전자"
    assert order.quantity == 100
    assert order.status == "RESERVED"


def test_create_order_assigns_incrementing_order_id():
    sample_repository = _repo_with_registered_sample()
    order_repository = OrderRepository()

    first = order_repository.create(
        sample_repository, sample_id="S-001", customer="삼성전자", quantity=100
    )
    second = order_repository.create(
        sample_repository, sample_id="S-001", customer="SK하이닉스", quantity=50
    )

    assert second.order_id != first.order_id


def test_create_order_raises_for_unregistered_sample():
    sample_repository = SampleRepository()
    order_repository = OrderRepository()

    with pytest.raises(ValueError):
        order_repository.create(
            sample_repository, sample_id="UNKNOWN", customer="삼성전자", quantity=100
        )


def test_list_all_returns_created_orders():
    sample_repository = _repo_with_registered_sample()
    order_repository = OrderRepository()

    order_repository.create(
        sample_repository, sample_id="S-001", customer="삼성전자", quantity=100
    )
    order_repository.create(
        sample_repository, sample_id="S-001", customer="SK하이닉스", quantity=50
    )

    orders = order_repository.list_all()
    assert len(orders) == 2


def test_approve_confirms_order_and_deducts_inventory_when_sufficient():
    sample_repository = _repo_with_registered_sample()
    sample_repository.find_by_id("S-001").inventory = 100
    order_repository = OrderRepository()
    order = order_repository.create(
        sample_repository, sample_id="S-001", customer="삼성전자", quantity=60
    )

    order_repository.approve(order.order_id, sample_repository)

    assert order.status == "CONFIRMED"
    assert sample_repository.find_by_id("S-001").inventory == 40


def test_approve_sets_producing_and_keeps_inventory_when_insufficient():
    sample_repository = _repo_with_registered_sample()
    sample_repository.find_by_id("S-001").inventory = 10
    order_repository = OrderRepository()
    order = order_repository.create(
        sample_repository, sample_id="S-001", customer="삼성전자", quantity=60
    )

    order_repository.approve(order.order_id, sample_repository)

    assert order.status == "PRODUCING"
    assert sample_repository.find_by_id("S-001").inventory == 10


def test_reject_sets_status_to_rejected():
    sample_repository = _repo_with_registered_sample()
    order_repository = OrderRepository()
    order = order_repository.create(
        sample_repository, sample_id="S-001", customer="삼성전자", quantity=60
    )

    order_repository.reject(order.order_id)

    assert order.status == "REJECTED"


def test_list_reserved_returns_only_reserved_orders():
    sample_repository = _repo_with_registered_sample()
    sample_repository.find_by_id("S-001").inventory = 100
    order_repository = OrderRepository()
    confirmed = order_repository.create(
        sample_repository, sample_id="S-001", customer="삼성전자", quantity=10
    )
    still_reserved = order_repository.create(
        sample_repository, sample_id="S-001", customer="SK하이닉스", quantity=10
    )
    order_repository.approve(confirmed.order_id, sample_repository)

    reserved = order_repository.list_reserved()

    assert reserved == [still_reserved]


def test_approve_enqueues_job_to_production_line_when_insufficient():
    sample_repository = _repo_with_registered_sample()
    sample_repository.find_by_id("S-001").inventory = 10
    order_repository = OrderRepository()
    production_line = ProductionLine()
    order = order_repository.create(
        sample_repository, sample_id="S-001", customer="삼성전자", quantity=60
    )

    order_repository.approve(order.order_id, sample_repository, production_line)

    pending = production_line.list_pending()
    assert len(pending) == 1
    assert pending[0].order is order
    assert pending[0].shortfall == 50


def test_approve_does_not_enqueue_when_inventory_sufficient():
    sample_repository = _repo_with_registered_sample()
    sample_repository.find_by_id("S-001").inventory = 100
    order_repository = OrderRepository()
    production_line = ProductionLine()
    order = order_repository.create(
        sample_repository, sample_id="S-001", customer="삼성전자", quantity=60
    )

    order_repository.approve(order.order_id, sample_repository, production_line)

    assert production_line.list_pending() == []
