"""Технологические расчёты сушки: масса воды, время сушки, классификация."""
import math

from constants import TAU_FAST_LIMIT, TAU_NORMAL_LIMIT


def water_mass(m: float, w1: float, w2: float) -> float:
    """Вычисляет массу удаляемой воды.

    Args:
        m: масса влажного материала, кг.
        w1: начальная влажность, %.
        w2: конечная влажность, %.

    Returns:
        Масса удаляемой воды, кг.
    """
    return m * (w1 - w2) / (100 - w2)


def drying_time(k: float, w1: float, w2: float) -> float:
    """Вычисляет время сушки.

    Args:
        k: коэффициент скорости сушки, 1/ч.
        w1: начальная влажность, %.
        w2: конечная влажность, %.

    Returns:
        Время сушки, ч.
    """
    return (1 / k) * math.log(w1 / w2)


def drying_class(tau: float) -> str:
    """Классифицирует процесс по времени сушки.

    Args:
        tau: время сушки, ч.

    Returns:
        Название класса: быстрая / нормальная / длительная сушка.
    """
    if tau < TAU_FAST_LIMIT:
        return "быстрая сушка"
    elif tau <= TAU_NORMAL_LIMIT:
        return "нормальная сушка"
    else:
        return "длительная сушка"
