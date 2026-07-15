from controller.sample_controller import SampleController
from model.sample import SampleRepository


class FakeSampleView:
    def __init__(self, registration=None, search_keyword=None):
        self._registration = registration
        self._search_keyword = search_keyword
        self.shown_samples = None
        self.messages = []

    def read_sample_registration(self):
        return self._registration

    def read_search_keyword(self):
        return self._search_keyword

    def show_samples(self, samples):
        self.shown_samples = samples

    def show_message(self, message):
        self.messages.append(message)


def test_register_reads_input_and_registers_sample():
    repository = SampleRepository()
    view = FakeSampleView(registration=("S-001", "실리콘 웨이퍼-8인치", 30, 0.9))
    controller = SampleController(repository, view)

    controller.register_sample()

    registered = repository.list_all()
    assert len(registered) == 1
    assert registered[0].sample_id == "S-001"
    assert registered[0].name == "실리콘 웨이퍼-8인치"
    assert registered[0].avg_production_time == 30
    assert registered[0].yield_rate == 0.9


def test_list_shows_all_registered_samples():
    repository = SampleRepository()
    repository.register(sample_id="S-001", name="실리콘 웨이퍼-8인치", avg_production_time=30, yield_rate=0.9)
    view = FakeSampleView()
    controller = SampleController(repository, view)

    controller.list_samples()

    assert view.shown_samples == repository.list_all()


def test_search_shows_matching_samples():
    repository = SampleRepository()
    repository.register(sample_id="S-001", name="실리콘 웨이퍼-8인치", avg_production_time=30, yield_rate=0.9)
    repository.register(sample_id="S-002", name="SiC 파워기판-6인치", avg_production_time=45, yield_rate=0.8)
    view = FakeSampleView(search_keyword="웨이퍼")
    controller = SampleController(repository, view)

    controller.search_samples()

    assert view.shown_samples == repository.search_by_name("웨이퍼")
