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


class ProductionLine:
    def __init__(self):
        self._queue = deque()

    def enqueue(self, order: Order, sample: Sample, shortfall: int) -> None:
        self._queue.append(ProductionJob(order, sample, shortfall))

    def list_pending(self):
        return list(self._queue)

    def complete_next(self) -> None:
        job = self._queue.popleft()
        actual_quantity = math.ceil(job.shortfall / job.sample.yield_rate)
        job.sample.inventory += actual_quantity
        job.order.status = "CONFIRMED"
