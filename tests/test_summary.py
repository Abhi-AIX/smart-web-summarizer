from types import SimpleNamespace
import pytest
from web_scraper import ArticleSummary, CheckSummary, RecordCost, Summarize
from pydantic import ValidationError

def test_checksummary_valid_ok_count():
    result = ArticleSummary(status="ok", points=["a", "b", "c"], summary=["d", "e", "f"])
    assert CheckSummary(result) is True

def test_checksummary_valid_maximum_count():
    result_maximum = ArticleSummary(
        status="ok",
        points=["1", "2", "3", "4", "5"],
        summary=["a", "b", "c", "d", "e"],
    )
    assert CheckSummary(result_maximum) is True

def test_checksummary_too_few_points_summary():
    result_few = ArticleSummary(status="ok", points=["a", "b"], summary=["c"])
    assert CheckSummary(result_few) is None

def test_checksummary_too_many_points_summary():
    result_many = ArticleSummary(
        status="ok",
        points=["1", "2", "3", "4", "5", "6"],
        summary=["a", "b", "c", "d", "e", "f"],
    )
    assert CheckSummary(result_many) is None

def test_checksummary_not_enough_info_empty():
    result_empty = ArticleSummary(status="not_enough_info", points=[], summary=[])
    assert CheckSummary(result_empty) is False

def test_checksummary_not_enough_info_none():
    with pytest.raises(ValidationError):
        ArticleSummary(status="not_enough_info", points=None, summary=None)

def test_checksummary_not_enough_info_has_points():
    result_has_points = ArticleSummary(status="not_enough_info", points=["something"], summary=[])
    assert CheckSummary(result_has_points) is None

def test_checksummary_not_enough_info_has_summary():
    result_has_summary = ArticleSummary(status="not_enough_info", points=[], summary=["something"])
    assert CheckSummary(result_has_summary) is None

def test_checksummary_points_summary_not_lists():
    with pytest.raises(ValidationError):
        ArticleSummary(status="ok", points="notalist", summary="notalist")

def test_unknown_status_is_rejected():
    with pytest.raises(ValidationError):
        ArticleSummary(status="bad_status", points=[], summary=[])

def test_record_cost_returns_zero_for_missing_cost():
    assert RecordCost(None) == 0

def test_record_cost_returns_none_for_zero_cost():
    data = {"cost": 0.0}
    assert RecordCost(data) is None

def test_record_cost_returns_cost_simple():
    import types

    mock_usage = types.SimpleNamespace(
        input_tokens_details=types.SimpleNamespace(
            cached_tokens=0,
            cache_write_tokens=0
        ),
        output_tokens=0
    )

    # The RecordCost should return 0 for this mocked usage
    assert RecordCost(mock_usage) == 0

def test_record_cost_handles_string_cost():
    data = {"cost": "1.25"}
    assert RecordCost(data) == 1.25

def test_record_cost_raises_on_invalid_cost_type():
    data = {"cost": {"not": "a number"}}
    import pytest
    with pytest.raises((TypeError, ValueError)):
        RecordCost(data)

def test_empty_url_returns_broken_link():
    result = Summarize("")
    assert result.outcome == "broken_link"