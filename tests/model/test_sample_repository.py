import pytest

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


def test_search_by_name_returns_matching_samples():
    repo = SampleRepository()
    repo.register(sample_id="S-001", name="실리콘 웨이퍼-8인치", avg_production_time=30, yield_rate=0.9)
    repo.register(sample_id="S-002", name="SiC 파워기판-6인치", avg_production_time=45, yield_rate=0.8)

    results = repo.search_by_name("웨이퍼")

    assert len(results) == 1
    assert results[0].sample_id == "S-001"


def test_search_by_name_returns_empty_when_no_match():
    repo = SampleRepository()
    repo.register(sample_id="S-001", name="실리콘 웨이퍼-8인치", avg_production_time=30, yield_rate=0.9)

    assert repo.search_by_name("존재하지않는이름") == []


def test_find_by_id_returns_matching_sample():
    repo = SampleRepository()
    repo.register(sample_id="S-001", name="실리콘 웨이퍼-8인치", avg_production_time=30, yield_rate=0.9)

    found = repo.find_by_id("S-001")

    assert found.sample_id == "S-001"


def test_find_by_id_returns_none_when_not_found():
    repo = SampleRepository()

    assert repo.find_by_id("UNKNOWN") is None


@pytest.mark.parametrize("yield_rate", [0, -0.1, 1.5])
def test_register_raises_for_out_of_range_yield_rate(yield_rate):
    repo = SampleRepository()

    with pytest.raises(ValueError):
        repo.register(sample_id="S-001", name="실리콘 웨이퍼-8인치", avg_production_time=30, yield_rate=yield_rate)
