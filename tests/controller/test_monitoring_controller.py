from controller.monitoring_controller import MonitoringController
from model.order import OrderRepository
from model.sample import SampleRepository


class FakeMonitoringView:
    def __init__(self):
        self.shown_counts = None
        self.shown_inventory_status = None

    def show_order_counts(self, counts):
        self.shown_counts = counts

    def show_inventory_status(self, statuses):
        self.shown_inventory_status = statuses


def test_show_order_counts_displays_status_counts():
    sample_repository = SampleRepository()
    sample_repository.register(sample_id="S-001", name="실리콘 웨이퍼-8인치", avg_production_time=30, yield_rate=0.9)
    order_repository = OrderRepository()
    order_repository.create(sample_repository, sample_id="S-001", customer="삼성전자", quantity=10)
    view = FakeMonitoringView()
    controller = MonitoringController(sample_repository, order_repository, view)

    controller.show_order_counts()

    assert view.shown_counts == {"RESERVED": 1}


def test_show_inventory_status_displays_per_sample_status():
    sample_repository = SampleRepository()
    sample_repository.register(sample_id="S-001", name="실리콘 웨이퍼-8인치", avg_production_time=30, yield_rate=0.9)
    order_repository = OrderRepository()
    order_repository.create(sample_repository, sample_id="S-001", customer="삼성전자", quantity=10)
    view = FakeMonitoringView()
    controller = MonitoringController(sample_repository, order_repository, view)

    controller.show_inventory_status()

    sample = sample_repository.find_by_id("S-001")
    assert view.shown_inventory_status == [(sample, "고갈")]
