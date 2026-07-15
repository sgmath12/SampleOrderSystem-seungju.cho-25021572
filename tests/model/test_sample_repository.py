from model.sample import SampleRepository


def test_register_sample_appears_in_list():
    repo = SampleRepository()

    repo.register(
        sample_id="S-001",
        name="실리콘 웨이퍼-8인치",
        avg_production_time=30,
        yield_rate=0.9,
    )

    samples = repo.list_all()
    assert len(samples) == 1
    registered = samples[0]
    assert registered.sample_id == "S-001"
    assert registered.name == "실리콘 웨이퍼-8인치"
    assert registered.avg_production_time == 30
    assert registered.yield_rate == 0.9


def test_registered_sample_starts_with_zero_inventory():
    repo = SampleRepository()

    repo.register(
        sample_id="S-002",
        name="SiC 파워기판-6인치",
        avg_production_time=45,
        yield_rate=0.8,
    )

    registered = repo.list_all()[0]
    assert registered.inventory == 0


def test_list_all_returns_empty_when_nothing_registered():
    repo = SampleRepository()

    assert repo.list_all() == []
