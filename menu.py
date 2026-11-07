"""Меню выбора материала и маршрутизация через match-case."""
from constants import K_WOOD, K_CERAMIC, K_GRAIN
from logger import log_error


def show_menu() -> None:
    """Выводит пункты меню на экран."""
    print("\n=== Расчёт времени сушки влажного материала ===")
    print("1 — древесина   (k = 0.008 1/ч)")
    print("2 — керамика    (k = 0.004 1/ч)")
    print("3 — зерно       (k = 0.012 1/ч)")
    print("0 — выход")


def select_mode() -> float | None:
    """Циклически запрашивает пункт меню; маршрутизация — только match-case.

    Returns:
        Коэффициент k выбранного материала или None при выходе.
    """
    while True:
        choice = input("Выберите режим (0 — выход): ").strip()
        match choice:
            case "1":
                return K_WOOD
            case "2":
                return K_CERAMIC
            case "3":
                return K_GRAIN
            case "0":
                return None
            case _:
                print("Ошибка: нет такого пункта меню")
                log_error(f"Неверный пункт меню: {choice}")


def mode_name(k: float) -> str:
    """Возвращает название материала по коэффициенту k (match-case).

    Args:
        k: коэффициент скорости сушки.

    Returns:
        Название материала.
    """
    match k:
        case 0.008:
            return "древесина"
        case 0.004:
            return "керамика"
        case 0.012:
            return "зерно"
        case _:
            return "неизвестный материал"
