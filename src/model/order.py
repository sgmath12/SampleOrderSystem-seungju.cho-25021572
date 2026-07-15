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
        known_sample_ids = {sample.sample_id for sample in sample_repository.list_all()}
        if sample_id not in known_sample_ids:
            raise ValueError(f"등록되지 않은 시료입니다: {sample_id}")

        order = Order(self._next_id, sample_id, customer, quantity)
        self._orders.append(order)
        self._next_id += 1
        return order

    def list_all(self):
        return list(self._orders)
