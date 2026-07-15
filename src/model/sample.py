from dataclasses import dataclass


@dataclass
class Sample:
    sample_id: str
    name: str
    avg_production_time: int
    yield_rate: float
    inventory: int = 0


class SampleRepository:
    def __init__(self):
        self._samples = []

    def register(self, sample_id: str, name: str, avg_production_time: int, yield_rate: float) -> Sample:
        sample = Sample(sample_id, name, avg_production_time, yield_rate)
        self._samples.append(sample)
        return sample

    def list_all(self):
        return list(self._samples)
