from controller.order_controller import OrderController
from model.order import OrderRepository
from model.production_line import ProductionLine
from model.sample import SampleRepository


class FakeOrderView:
    def __init__(self, placement=None, selection_number=None, decision=None):
        self._placement = placement
        self._selection_number = selection_number
        self._decision = decision
        self.shown_samples = None
        self.shown_numbered_orders = None
        self.release_confirmation = None
        self.messages = []

    def read_order_placement(self):
        return self._placement

    def show_samples(self, samples):
        self.shown_samples = samples

    def show_orders_numbered(self, orders):
        self.shown_numbered_orders = orders

    def read_selection_number(self):
        return self._selection_number

    def read_menu_choice(self):
        return self._decision

    def show_release_confirmation(self, order):
        self.release_confirmation = order

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


def test_place_order_shows_registered_samples_before_reading_input():
    sample_repository = _sample_repository_with_stock()
    order_repository = OrderRepository()
    production_line = ProductionLine()
    view = FakeOrderView(placement=("S-001", "삼성전자", 10))
    controller = OrderController(order_repository, sample_repository, production_line, view)

    controller.place_order()

    assert view.shown_samples == sample_repository.list_all()


def test_place_order_aborts_when_no_samples_registered():
    sample_repository = SampleRepository()
    order_repository = OrderRepository()
    production_line = ProductionLine()
    view = FakeOrderView(placement=("S-001", "삼성전자", 10))
    controller = OrderController(order_repository, sample_repository, production_line, view)

    controller.place_order()

    assert order_repository.list_all() == []
    assert "등록된 시료가 없습니다" in view.messages[0]


def test_review_order_shows_list_before_asking_decision():
    sample_repository = _sample_repository_with_stock(inventory=100)
    order_repository = OrderRepository()
    production_line = ProductionLine()
    order = order_repository.create(sample_repository, sample_id="S-001", customer="삼성전자", quantity=10)
    view = FakeOrderView(selection_number=1, decision="1")
    controller = OrderController(order_repository, sample_repository, production_line, view)

    controller.review_order()

    assert view.shown_numbered_orders == [order]


def test_review_order_approves_when_decision_is_1():
    sample_repository = _sample_repository_with_stock(inventory=100)
    order_repository = OrderRepository()
    production_line = ProductionLine()
    order = order_repository.create(sample_repository, sample_id="S-001", customer="삼성전자", quantity=10)
    view = FakeOrderView(selection_number=1, decision="1")
    controller = OrderController(order_repository, sample_repository, production_line, view)

    controller.review_order()

    assert order.status == "CONFIRMED"


def test_review_order_rejects_when_decision_is_2():
    sample_repository = _sample_repository_with_stock()
    order_repository = OrderRepository()
    production_line = ProductionLine()
    order = order_repository.create(sample_repository, sample_id="S-001", customer="삼성전자", quantity=10)
    view = FakeOrderView(selection_number=1, decision="2")
    controller = OrderController(order_repository, sample_repository, production_line, view)

    controller.review_order()

    assert order.status == "REJECTED"


def test_review_order_leaves_order_reserved_when_decision_is_cancelled():
    sample_repository = _sample_repository_with_stock()
    order_repository = OrderRepository()
    production_line = ProductionLine()
    order = order_repository.create(sample_repository, sample_id="S-001", customer="삼성전자", quantity=10)
    view = FakeOrderView(selection_number=1, decision="0")
    controller = OrderController(order_repository, sample_repository, production_line, view)

    controller.review_order()

    assert order.status == "RESERVED"


def test_release_order_selects_by_number_and_delegates_to_order_repository():
    sample_repository = _sample_repository_with_stock()
    order_repository = OrderRepository()
    production_line = ProductionLine()
    order = order_repository.create(sample_repository, sample_id="S-001", customer="삼성전자", quantity=10)
    order_repository.approve(order.order_id, sample_repository)
    view = FakeOrderView(selection_number=1)
    controller = OrderController(order_repository, sample_repository, production_line, view)

    controller.release_order()

    assert order.status == "RELEASE"
    assert view.release_confirmation is order


def test_review_order_shows_message_when_no_reserved_orders():
    sample_repository = _sample_repository_with_stock()
    order_repository = OrderRepository()
    production_line = ProductionLine()
    view = FakeOrderView()
    controller = OrderController(order_repository, sample_repository, production_line, view)

    controller.review_order()

    assert "없습니다" in view.messages[0]


def test_review_order_shows_message_for_out_of_range_selection():
    sample_repository = _sample_repository_with_stock(inventory=100)
    order_repository = OrderRepository()
    production_line = ProductionLine()
    order_repository.create(sample_repository, sample_id="S-001", customer="삼성전자", quantity=10)
    view = FakeOrderView(selection_number=99)
    controller = OrderController(order_repository, sample_repository, production_line, view)

    controller.review_order()

    assert "잘못된 번호" in view.messages[0]
