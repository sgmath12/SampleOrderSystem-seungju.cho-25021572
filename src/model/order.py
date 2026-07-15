from dataclasses import dataclass


@dataclass
class Order:
    order_id: int
    sample_id: str
    customer: str
    quantity: int
    status: str = "RESERVED"


class OrderRepository:
    def __init__(self):
        self._orders = []
        self._next_id = 1

    def create(self, sample_repository, sample_id: str, customer: str, quantity: int) -> Order:
        if sample_repository.find_by_id(sample_id) is None:
            raise ValueError(f"등록되지 않은 시료입니다: {sample_id}")

        order = Order(self._next_id, sample_id, customer, quantity)
        self._orders.append(order)
        self._next_id += 1
        return order

    def list_all(self):
        return list(self._orders)

    def list_reserved(self):
        return [order for order in self._orders if order.status == "RESERVED"]

    def approve(self, order_id: int, sample_repository, production_line=None) -> None:
        order = self._find_by_id(order_id)
        sample = sample_repository.find_by_id(order.sample_id)
        if sample.inventory >= order.quantity:
            sample.inventory -= order.quantity
            order.status = "CONFIRMED"
        else:
            order.status = "PRODUCING"
            if production_line is not None:
                shortfall = order.quantity - sample.inventory
                production_line.enqueue(order, sample, shortfall)

    def reject(self, order_id: int) -> None:
        order = self._find_by_id(order_id)
        order.status = "REJECTED"

    def _find_by_id(self, order_id: int) -> Order:
        return next(order for order in self._orders if order.order_id == order_id)
