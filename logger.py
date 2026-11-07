"""Журнал ошибок ввода: хранит записи в памяти и дублирует их в файл."""
import datetime

from constants import LOG_FILE

_entries: list[str] = []


def log_error(message: str) -> None:
    """Добавляет запись в журнал и дописывает её в файл LOG_FILE.

    Args:
        message: текст сообщения об ошибке.
    """
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record = f"[{stamp}] {message}"
    _entries.append(record)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(record + "\n")
    except OSError:
        pass  # файл недоступен — программа не должна падать


def get_entries() -> list[str]:
    """Возвращает копию журнала в памяти."""
    return list(_entries)


def clear() -> None:
    """Очищает журнал (используется в тестах)."""
    _entries.clear()