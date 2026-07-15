from model.monitoring import count_orders_by_status, inventory_status, reserved_quantity_for_sample


class MonitoringController:
    def __init__(self, sample_repository, order_repository, view):
        self.sample_repository = sample_repository
        self.order_repository = order_repository
        self.view = view

    def show_order_counts(self):
        counts = count_orders_by_status(self.order_repository.list_all())
        self.view.show_order_counts(counts)

    def show_inventory_status(self):
        orders = self.order_repository.list_all()
        statuses = [
            (sample, inventory_status(sample.inventory, reserved_quantity_for_sample(orders, sample.sample_id)))
            for sample in self.sample_repository.list_all()
        ]
        self.view.show_inventory_status(statuses)

    def system_summary(self):
        samples = self.sample_repository.list_all()
        return {
            "sample_count": len(samples),
            "total_inventory": sum(sample.inventory for sample in samples),
            "order_count": len(self.order_repository.list_all()),
        }
