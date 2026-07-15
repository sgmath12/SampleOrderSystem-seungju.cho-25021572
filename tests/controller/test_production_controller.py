from controller.production_controller import ProductionController
from model.order import Order
from model.production_line import ProductionLine
from model.sample import Sample


class FakeProductionView:
    def __init__(self):
        self.shown_jobs = None
        self.messages = []

    def show_production_jobs(self, jobs):
        self.shown_jobs = jobs

    def show_message(self, message):
        self.messages.append(message)


def _sample():
    return Sample(sample_id="S-001", name="SiC 파워기판-6인치", avg_production_time=10, yield_rate=0.8, inventory=0)


def _order():
    return Order(order_id=1, sample_id="S-001", customer="삼성전자", quantity=16, status="PRODUCING")


def test_show_pending_displays_queued_jobs():
    production_line = ProductionLine()
    production_line.enqueue(_order(), _sample(), shortfall=16)
    view = FakeProductionView()
    controller = ProductionController(production_line, view)

    controller.show_pending()

    assert view.shown_jobs == production_line.list_pending()


def test_complete_next_advances_production_queue():
    production_line = ProductionLine()
    order = _order()
    production_line.enqueue(order, _sample(), shortfall=16)
    view = FakeProductionView()
    controller = ProductionController(production_line, view)

    controller.complete_next()

    assert order.status == "CONFIRMED"
    assert production_line.list_pending() == []


def test_count_pending_returns_number_of_queued_jobs():
    production_line = ProductionLine()
    production_line.enqueue(_order(), _sample(), shortfall=16)
    view = FakeProductionView()
    controller = ProductionController(production_line, view)

    assert controller.count_pending() == 1
