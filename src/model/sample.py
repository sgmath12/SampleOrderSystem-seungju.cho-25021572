from dataclasses import dataclass


@dataclass
class Sample:
    sample_id: str
    name: str
    avg_production_time: float
    yield_rate: float
    inventory: int = 0


class SampleRepository:
    def __init__(self):
        self._samples = []

    def register(self, sample_id: str, name: str, avg_production_time: float, yield_rate: float) -> Sample:
        if not (0 < yield_rate <= 1):
            raise ValueError(f"수율은 0보다 크고 1 이하여야 합니다: {yield_rate}")
        sample = Sample(sample_id, name, avg_production_time, yield_rate)
        self._samples.append(sample)
        return sample

    def list_all(self):
        return list(self._samples)

    def search_by_name(self, keyword: str):
        return [sample for sample in self._samples if keyword in sample.name]

    def find_by_id(self, sample_id: str):
        return next((sample for sample in self._samples if sample.sample_id == sample_id), None)
