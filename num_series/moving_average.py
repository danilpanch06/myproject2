"""Скользящие средние: SMA, центрированное MA, EMA.

Все реализации работают за O(n) по времени и не используют numpy.
"""
from __future__ import annotations

from typing import List, Sequence


def _ensure_not_empty(data: Sequence[float]) -> None:
    if not data:
        raise ValueError("Ряд пуст: расчёт скользящей средней невозможен")


def check_window(window: int, n: int) -> None:
    """Валидация окна: целое >= 1 и не больше длины ряда."""
    if not isinstance(window, int) or isinstance(window, bool):
        raise ValueError(f"window должен быть целым, получено: {window!r}")
    if window < 1:
        raise ValueError(f"window должен быть >= 1, получено: {window}")
    if window > n:
        raise ValueError(f"window ({window}) больше длины ряда ({n})")


def simple_moving_average(data: Sequence[float], window: int) -> List[float]:
    """SMA через бегущую сумму. O(n) по времени, O(window) по памяти.

    Длина результата: len(data) - window + 1.
    """
    _ensure_not_empty(data)
    n = len(data)
    check_window(window, n)

    running = sum(data[:window])
    result = [running / window]
    for i in range(window, n):
        running += data[i] - data[i - window]
        result.append(running / window)
    return result


def centered_moving_average(data: Sequence[float], window: int) -> List[float]:
    """Центрированное MA для нечётного окна.

    Значение i считается по data[i - half : i + half + 1],
    где half = window // 2, то есть выровнено по центру окна.
    Длина результата: len(data) - window + 1.
    """
    _ensure_not_empty(data)
    n = len(data)
    check_window(window, n)
    if window % 2 == 0:
        raise ValueError(
            f"centered_moving_average требует нечётного окна, получено: {window}"
        )

    half = window // 2
    running = sum(data[:window])
    result = [running / window]
    for i in range(window, n):
        running += data[i] - data[i - window]
        result.append(running / window)
    return result


def exponential_moving_average(data: Sequence[float], alpha: float) -> List[float]:
    """EMA с коэффициентом сглаживания alpha из (0, 1].

    EMA[0] = data[0]
    EMA[i] = alpha * data[i] + (1 - alpha) * EMA[i-1]
    """
    _ensure_not_empty(data)
    if not (isinstance(alpha, (int, float)) and not isinstance(alpha, bool)):
        raise ValueError(f"alpha должна быть числом, получено: {alpha!r}")
    if not (0 < alpha <= 1):
        raise ValueError(f"alpha должна быть в (0, 1], получено: {alpha}")

    result = [float(data[0])]
    for x in data[1:]:
        result.append(alpha * x + (1 - alpha) * result[-1])
    return result
