"""Тесты скользящих средних: SMA, центрированное MA, EMA."""
import math

import pytest

from num_series.moving_average import (
    simple_moving_average,
    centered_moving_average,
    exponential_moving_average,
)


class TestSimpleMovingAverage:
    def test_control_point_from_task(self):
        # Контрольная точка из методички
        assert simple_moving_average([1, 2, 3, 4, 5], 3) == pytest.approx([2.0, 3.0, 4.0])

    def test_window_greater_than_n_raises(self):
        with pytest.raises(ValueError):
            simple_moving_average([1, 2], 3)

    def test_window_zero_raises(self):
        with pytest.raises(ValueError):
            simple_moving_average([1, 2, 3], 0)

    def test_window_negative_raises(self):
        with pytest.raises(ValueError):
            simple_moving_average([1, 2, 3], -1)

    def test_window_not_int_raises(self):
        with pytest.raises(ValueError):
            simple_moving_average([1, 2, 3], 2.5)

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            simple_moving_average([], 1)

    def test_window_1_equals_source(self):
        data = [3.5, -1.0, 42.0, 0.25]
        assert simple_moving_average(data, 1) == data

    def test_window_n_equals_mean(self):
        data = [1.0, 2.0, 3.0, 4.0]
        result = simple_moving_average(data, len(data))
        assert len(result) == 1
        assert result[0] == pytest.approx(2.5)

    def test_result_length(self):
        data = list(range(50))
        for w in (1, 3, 7, 50):
            assert len(simple_moving_average(data, w)) == len(data) - w + 1

    def test_matches_naive_implementation(self):
        """Проверка против «наивной» реализации (это не O(n), но верной)."""
        data = [math.sin(i / 3.0) for i in range(40)]
        w = 5
        expected = [sum(data[i:i + w]) / w for i in range(len(data) - w + 1)]
        assert simple_moving_average(data, w) == pytest.approx(expected)


class TestCenteredMovingAverage:
    def test_control_point(self):
        # Среднее окна [1,2,3] ставится на центральную точку (2)
        assert centered_moving_average([1, 2, 3, 4, 5], 3) == pytest.approx([2.0, 3.0, 4.0])

    def test_window_5(self):
        assert centered_moving_average([1, 2, 3, 4, 5], 5) == pytest.approx([3.0])

    def test_even_window_raises(self):
        with pytest.raises(ValueError):
            centered_moving_average([1, 2, 3, 4, 5], 4)

    def test_result_length(self):
        data = list(range(30))
        for w in (3, 5, 9, 29):
            assert len(centered_moving_average(data, w)) == len(data) - w + 1

    def test_matches_naive_implementation(self):
        data = [i ** 2 % 17 for i in range(25)]
        w = 7
        half = w // 2
        expected = [
            sum(data[i - half:i + half + 1]) / w
            for i in range(half, len(data) - half)
        ]
        assert centered_moving_average(data, w) == pytest.approx(expected)

    def test_window_greater_than_n_raises(self):
        with pytest.raises(ValueError):
            centered_moving_average([1, 2], 3)


class TestExponentialMovingAverage:
    def test_first_value_is_first_element(self):
        assert exponential_moving_average([5.0, 1.0, 2.0], 0.5)[0] == pytest.approx(5.0)

    def test_formula(self):
        data = [1, 2, 3, 4]
        ema = exponential_moving_average(data, 0.5)
        assert ema == pytest.approx([1.0, 1.5, 2.25, 3.125])

    def test_alpha_1_equals_source(self):
        data = [3.0, 1.0, 4.0]
        assert exponential_moving_average(data, 1.0) == data

    def test_alpha_zero_raises(self):
        with pytest.raises(ValueError):
            exponential_moving_average([1.0, 2.0], 0.0)

    def test_alpha_negative_raises(self):
        with pytest.raises(ValueError):
            exponential_moving_average([1.0, 2.0], -0.1)

    def test_alpha_greater_than_one_raises(self):
        with pytest.raises(ValueError):
            exponential_moving_average([1.0, 2.0], 1.5)

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            exponential_moving_average([], 0.5)
