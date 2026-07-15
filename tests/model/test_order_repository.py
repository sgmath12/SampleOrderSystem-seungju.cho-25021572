import pytest

from model.order import OrderRepository
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
