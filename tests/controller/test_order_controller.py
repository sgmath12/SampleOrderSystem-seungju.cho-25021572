from controller.order_controller import OrderController
from model.order import OrderRepository
from model.production_line import ProductionLine
from model.sample import SampleRepository


class FakeOrderView:
    def __init__(self, placement=None, order_id=None):
        self._placement = placement
        self._order_id = order_id
        self.shown_orders = None
        self.messages = []

    def read_order_placement(self):
        return self._placement

    def read_order_id(self):
        return self._order_id

    def show_orders(self, orders):
        self.shown_orders = orders

    def show_message(self, message):
        self.messages.append(message)


def _sample_repository_with_stock(inventory=100):
    repo = SampleRepository()
    repo.register(sample_id="S-001", name="실리콘 웨이퍼-8인치", avg_production_time=30, yield_rate=0.9)
    repo.find_by_id("S-001").inventory = inventory
    return repo


def test_place_order_creates_reserved_order():
    sample_repository = _sample_repository_with_stock()
    order_repository = OrderRepository()
    production_line = ProductionLine()
    view = FakeOrderView(placement=("S-001", "삼성전자", 10))
    controller = OrderController(order_repository, sample_repository, production_line, view)

    controller.place_order()

    orders = order_repository.list_all()
    assert len(orders) == 1
    assert orders[0].sample_id == "S-001"
    assert orders[0].customer == "삼성전자"
    assert orders[0].quantity == 10
    assert orders[0].status == "RESERVED"


def test_approve_order_delegates_to_order_repository():
    sample_repository = _sample_repository_with_stock(inventory=100)
    order_repository = OrderRepository()
    production_line = ProductionLine()
    order = order_repository.create(sample_repository, sample_id="S-001", customer="삼성전자", quantity=10)
    view = FakeOrderView(order_id=order.order_id)
    controller = OrderController(order_repository, sample_repository, production_line, view)

    controller.approve_order()

    assert order.status == "CONFIRMED"


def test_reject_order_delegates_to_order_repository():
    sample_repository = _sample_repository_with_stock()
    order_repository = OrderRepository()
    production_line = ProductionLine()
    order = order_repository.create(sample_repository, sample_id="S-001", customer="삼성전자", quantity=10)
    view = FakeOrderView(order_id=order.order_id)
    controller = OrderController(order_repository, sample_repository, production_line, view)

    controller.reject_order()

    assert order.status == "REJECTED"


def test_release_order_delegates_to_order_repository():
    sample_repository = _sample_repository_with_stock()
    order_repository = OrderRepository()
    production_line = ProductionLine()
    order = order_repository.create(sample_repository, sample_id="S-001", customer="삼성전자", quantity=10)
    order_repository.approve(order.order_id, sample_repository)
    view = FakeOrderView(order_id=order.order_id)
    controller = OrderController(order_repository, sample_repository, production_line, view)

    controller.release_order()

    assert order.status == "RELEASE"
