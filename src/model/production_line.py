import math
import time
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
    started_at: float


class ProductionLine:
    def __init__(self, clock=time.time):
        self._queue = deque()
        self._clock = clock

    def enqueue(self, order: Order, sample: Sample, shortfall: int) -> None:
        actual_quantity = math.ceil(shortfall / sample.yield_rate)
        production_time = sample.avg_production_time * actual_quantity
        started_at = self._clock()
        self._queue.append(
            ProductionJob(order, sample, shortfall, actual_quantity, production_time, started_at)
        )

    def list_pending(self):
        return list(self._queue)

    def complete_next(self) -> None:
        if not self._queue:
            raise ValueError("대기 중인 생산 작업이 없습니다.")
        job = self._queue.popleft()
        surplus = job.actual_quantity - job.shortfall
        job.sample.inventory += surplus
        job.order.status = "CONFIRMED"


def progress_percent(job: ProductionJob, now: float) -> float:
    total_seconds = job.production_time * 60
    if total_seconds <= 0:
        return 100.0
    elapsed = now - job.started_at
    return max(0.0, min(100.0, elapsed / total_seconds * 100))


def estimated_completion_at(job: ProductionJob) -> float:
    return job.started_at + job.production_time * 60
