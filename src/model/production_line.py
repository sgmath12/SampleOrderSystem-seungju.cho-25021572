import math
from collections import deque
from dataclasses import dataclass

from model.order import Order
from model.sample import Sample


@dataclass
class ProductionJob:
    order: Order
    sample: Sample
    shortfall: int
    actual_quantity: int
    production_time: float


class ProductionLine:
    def __init__(self):
        self._queue = deque()

    def enqueue(self, order: Order, sample: Sample, shortfall: int) -> None:
        actual_quantity = math.ceil(shortfall / sample.yield_rate)
        production_time = sample.avg_production_time * actual_quantity
        self._queue.append(ProductionJob(order, sample, shortfall, actual_quantity, production_time))

    def list_pending(self):
        return list(self._queue)

    def complete_next(self) -> None:
        job = self._queue.popleft()
        job.sample.inventory += job.actual_quantity
        job.order.status = "CONFIRMED"
