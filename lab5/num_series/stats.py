"""Базовая статистика: среднее, медиана, размах (без numpy и statistics)."""
from __future__ import annotations

from typing import Dict, Sequence


def _ensure_not_empty(data: Sequence[float]) -> None:
    if not data:
        raise ValueError("Ряд пуст: расчёт статистики невозможен")


def mean(data: Sequence[float]) -> float:
    """Среднее арифметическое."""
    _ensure_not_empty(data)
    return sum(data) / len(data)


def median(data: Sequence[float]) -> float:
    """Медиана (устойчива к выбросам)."""
    _ensure_not_empty(data)
    s = sorted(data)
    k = len(s) // 2
    if len(s) % 2:
        return float(s[k])
    return (s[k - 1] + s[k]) / 2.0


def spread(data: Sequence[float]) -> float:
    """Размах ряда: max - min."""
    _ensure_not_empty(data)
    return float(max(data) - min(data))


def summarize(data: Sequence[float]) -> Dict[str, float]:
    """Сводный отчёт: count, mean, median, spread, min, max."""
    _ensure_not_empty(data)
    return {
        "count": len(data),
        "mean": mean(data),
        "median": median(data),
        "spread": spread(data),
        "min": float(min(data)),
        "max": float(max(data)),
    }
from typing import Optional, Sequence


def coefficient_of_variation(data):
    """CV = stdev / |mean|. При mean == 0 возвращает None (вариант 10)."""
    if not data:
        raise ValueError("Ряд пуст: CV не определён")
    m = mean(data)
    if m == 0:
        return None
    return abs(stdev(data) / m)


def stdev(data):
    """Выборочное стандартное отклонение (знаменатель n - 1)."""
    n = len(data)
    if n < 2:
        raise ValueError("stdev требует минимум двух значений")
    m = sum(data) / n
    return (sum((x - m) ** 2 for x in data) / (n - 1)) ** 0.5

