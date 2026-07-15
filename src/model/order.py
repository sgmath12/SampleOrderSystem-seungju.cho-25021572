from dataclasses import dataclass
from datetime import datetime


@dataclass
class Order:
    order_id: str
    sample_id: str
    customer: str
    quantity: int
    status: str = "RESERVED"


class OrderRepository:
    def __init__(self, clock=datetime.now):
        self._orders = []
        self._sequence_by_date = {}
        self._clock = clock

    def create(self, sample_repository, sample_id: str, customer: str, quantity: int) -> Order:
        if quantity <= 0:
            raise ValueError(f"주문 수량은 1 이상이어야 합니다: {quantity}")
        if sample_repository.find_by_id(sample_id) is None:
            raise ValueError(f"등록되지 않은 시료입니다: {sample_id}")

        date_str = self._clock().strftime("%Y%m%d")
        sequence = self._sequence_by_date.get(date_str, 0) + 1
        self._sequence_by_date[date_str] = sequence
        order_id = f"ORD-{date_str}-{sequence:04d}"
        order = Order(order_id, sample_id, customer, quantity)
        self._orders.append(order)
        return order

    def list_all(self):
        return list(self._orders)

    def list_reserved(self):
        return [order for order in self._orders if order.status == "RESERVED"]

    def list_confirmed(self):
        return [order for order in self._orders if order.status == "CONFIRMED"]

    def approve(self, order_id: str, sample_repository, production_line=None) -> None:
        order = self._find_by_id(order_id)
        if order.status != "RESERVED":
            raise ValueError(f"RESERVED 상태의 주문만 승인/거절할 수 있습니다: {order.status}")
        sample = sample_repository.find_by_id(order.sample_id)
        if sample.inventory >= order.quantity:
            sample.inventory -= order.quantity
            order.status = "CONFIRMED"
        else:
            order.status = "PRODUCING"
            shortfall = order.quantity - sample.inventory
            sample.inventory = 0
            if production_line is not None:
                production_line.enqueue(order, sample, shortfall)

    def reject(self, order_id: str) -> None:
        order = self._find_by_id(order_id)
        if order.status != "RESERVED":
            raise ValueError(f"RESERVED 상태의 주문만 승인/거절할 수 있습니다: {order.status}")
        order.status = "REJECTED"

    def release(self, order_id: str) -> None:
        order = self._find_by_id(order_id)
        if order.status != "CONFIRMED":
            raise ValueError(f"CONFIRMED 상태의 주문만 출고할 수 있습니다: {order.status}")
        order.status = "RELEASE"

    def _find_by_id(self, order_id: str) -> Order:
        order = next((order for order in self._orders if order.order_id == order_id), None)
        if order is None:
            raise ValueError(f"존재하지 않는 주문입니다: {order_id}")
        return order
