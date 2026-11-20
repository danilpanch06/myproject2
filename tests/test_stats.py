"""Тесты базовой статистики."""
import pytest

from num_series.stats import mean, median, spread, summarize


class TestMean:
    def test_basic(self):
        assert mean([1, 2, 3, 4]) == pytest.approx(2.5)

    def test_single_element(self):
        assert mean([7]) == pytest.approx(7.0)

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            mean([])


class TestMedian:
    def test_odd_count(self):
        assert median([3, 1, 2]) == pytest.approx(2.0)

    def test_even_count(self):
        assert median([4, 1, 3, 2]) == pytest.approx(2.5)

    def test_robust_to_outlier(self):
        # Один выброс почти не влияет на медиану
        assert median([1, 2, 3, 4, 100]) == pytest.approx(3.0)

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            median([])


class TestSpread:
    def test_basic(self):
        assert spread([1, 5, 3]) == pytest.approx(4.0)

    def test_constant_row(self):
        assert spread([2.5, 2.5, 2.5]) == pytest.approx(0.0)

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            spread([])


class TestSummarize:
    def test_keys(self):
        data = [1.0, 2.0, 3.0]
        stats = summarize(data)
        assert set(stats) == {"count", "mean", "median", "spread", "min", "max"}

    def test_values(self):
        stats = summarize([1.0, 2.0, 3.0])
        assert stats["count"] == 3
        assert stats["mean"] == pytest.approx(2.0)
        assert stats["median"] == pytest.approx(2.0)
        assert stats["spread"] == pytest.approx(2.0)
        assert stats["min"] == pytest.approx(1.0)
        assert stats["max"] == pytest.approx(3.0)

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            summarize([])
