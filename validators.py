"""Валидация ввода: проверка типа, диапазона и циклический ввод до корректного значения.

В этом модуле запрещён match-case — только if-elif-else и try/except.
"""
from constants import M_MIN, M_MAX, W1_MIN, W1_MAX, W2_MIN, W2_MAX, T_MIN, T_MAX
from logger import log_error


def validate_range(value: float, low: float, high: float) -> tuple[bool, str]:
    """Проверяет попадание значения в диапазон [low, high].

    Args:
        value: проверяемое число.
        low: нижняя граница диапазона.
        high: верхняя граница диапазона.

    Returns:
        Кортеж (True, "") при успехе или (False, сообщение) при ошибке.
    """
    if value < low:
        return False, f"значение {value} меньше допустимого ({low})"
    elif value > high:
        return False, f"значение {value} больше допустимого ({high})"
    else:
        return True, ""


def input_number(prompt: str, low: float, high: float) -> float:
    """Циклически запрашивает число: проверка типа через try/except, границ — через validate_range.

    Args:
        prompt: текст приглашения к вводу.
        low: нижняя граница диапазона.
        high: верхняя граница диапазона.

    Returns:
        Корректное значение типа float.
    """
    is_valid = False
    value = 0.0
    while not is_valid:
        raw = input(prompt)
        try:
            value = float(raw)
        except ValueError:
            msg = f"Ошибка: '{raw}' не является числом"
            print(msg)
            log_error(f"Некорректный ввод: {raw!r} (ожидалось число)")
            continue
        ok, msg = validate_range(value, low, high)
        if ok:
            is_valid = True
        else:
            print(f"Ошибка: {msg}")
            log_error(f"Вне диапазона: {value} (допустимо {low}…{high})")
    return value


def input_mass() -> float:
    """Обёртка: ввод массы материала, кг."""
    return input_number(f"Введите массу материала m (кг, {M_MIN}…{M_MAX}): ", M_MIN, M_MAX)


def input_w1() -> float:
    """Обёртка: ввод начальной влажности, %."""
    return input_number(f"Введите начальную влажность w1 (%, {W1_MIN}…{W1_MAX}): ", W1_MIN, W1_MAX)


def input_w2(w1: float) -> float:
    """Ввод конечной влажности в цикле, пока не выполнится 0 < w2 < w1.

    Args:
        w1: начальная влажность, %.

    Returns:
        Корректная конечная влажность, %.
    """
    while True:
        value = input_number(f"Введите конечную влажность w2 (%, {W2_MIN}…{W2_MAX}): ", W2_MIN, W2_MAX)
        if value <= 0:
            print("Ошибка: конечная влажность должна быть больше 0 (иначе ln(w1/w2) не определён)")
            log_error(f"w2 = {value} недопустимо: требуется w2 > 0")
        elif value >= w1:
            print(f"Ошибка: конечная влажность должна быть меньше начальной ({w1})")
            log_error(f"w2 = {value} >= w1 = {w1}")
        else:
            return value


def input_temperature() -> float:
    """Обёртка: ввод температуры сушильного агента, °C."""
    return input_number(f"Введите температуру сушильного агента (°C, {T_MIN}…{T_MAX}): ", T_MIN, T_MAX)
