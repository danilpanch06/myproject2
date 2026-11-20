"""Тесты генераторов числовых рядов."""
import math

import pytest

from num_series.generator import random_series, sine_series, trend_series


class TestRandomSeries:
    def test_length(self):
        assert len(random_series(17, seed=1)) == 17

    def test_values_in_bounds(self):
        data = random_series(1000, low=-5.0, high=5.0, seed=2)
        assert all(-5.0 <= x <= 5.0 for x in data)

    def test_reproducible_with_seed(self):
        assert random_series(50, seed=7) == random_series(50, seed=7)

    def test_different_seeds_give_different_rows(self):
        assert random_series(50, seed=1) != random_series(50, seed=2)

    def test_n_zero_raises(self):
        with pytest.raises(ValueError):
            random_series(0)

    def test_n_negative_raises(self):
        with pytest.raises(ValueError):
            random_series(-3)

    def test_n_float_raises(self):
        with pytest.raises(ValueError):
            random_series(10.5)

    def test_low_ge_high_raises(self):
        with pytest.raises(ValueError):
            random_series(10, low=5, high=5)


class TestSineSeries:
    def test_exact_formula_without_noise(self):
        n = 20
        data = sine_series(n, amplitude=3.0, frequency=1.0, noise=0.0)
        expected = [3.0 * math.sin(2 * math.pi * i / n) for i in range(n)]
        assert data == pytest.approx(expected)

    def test_reproducible_with_noise_and_seed(self):
        assert sine_series(30, noise=1.0, seed=5) == sine_series(30, noise=1.0, seed=5)

    def test_noise_zero_means_deterministic(self):
        a = sine_series(10, noise=0.0, seed=None)
        b = sine_series(10, noise=0.0, seed=None)
        assert a == b

    def test_n_zero_raises(self):
        with pytest.raises(ValueError):
            sine_series(0)


class TestTrendSeries:
    def test_linear_without_noise(self):
        data = trend_series(5, start=2.0, step=0.5, noise=0.0)
        assert data == pytest.approx([2.0, 2.5, 3.0, 3.5, 4.0])

    def test_reproducible_with_noise_and_seed(self):
        assert trend_series(20, noise=0.5, seed=3) == trend_series(20, noise=0.5, seed=3)

    def test_n_zero_raises(self):
        with pytest.raises(ValueError):
            trend_series(0)
