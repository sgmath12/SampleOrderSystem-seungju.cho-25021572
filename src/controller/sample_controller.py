class SampleController:
    def __init__(self, sample_repository, view):
        self.sample_repository = sample_repository
        self.view = view

    def register_sample(self):
        sample_id, name, avg_production_time, yield_rate = self.view.read_sample_registration()
        self.sample_repository.register(sample_id, name, avg_production_time, yield_rate)
        self.view.show_message(f"시료 등록 완료: {sample_id}")

    def list_samples(self):
        self.view.show_samples(self.sample_repository.list_all())

    def search_samples(self):
        keyword = self.view.read_search_keyword()
        self.view.show_samples(self.sample_repository.search_by_name(keyword))
