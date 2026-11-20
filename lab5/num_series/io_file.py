"""Чтение числовых рядов из простых текстовых файлов.

Поддерживаемые форматы:
    .txt — по одному числу на строку (пустые строки и #-комментарии пропускаются)
    .csv — числа через запятую / точку с запятой / пробел / табуляцию
           (первая строка, начинающаяся с "value" или "x", считается заголовком)
"""
from __future__ import annotations
import re
from pathlib import Path
from typing import List, Union

PathLike = Union[str, Path]
_SEPARATORS = re.compile(r"[,;\s]+")


def load_series_txt(path: PathLike) -> List[float]:
    """Читает числа из .txt — по одному на строку."""
    file_path = Path(path)
    if not file_path.exists():
        raise ValueError(f"Файл не найден: {file_path}")

    result: List[float] = []
    try:
        with file_path.open("r", encoding="utf-8") as f:
            for lineno, raw in enumerate(f, start=1):
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                try:
                    result.append(float(line))
                except ValueError as err:
                    raise ValueError(
                        f"{file_path}:{lineno}: '{line}' не является числом"
                    ) from err
    except OSError as err:
        raise ValueError(f"Не удалось прочитать файл {file_path}: {err}") from err

    if not result:
        raise ValueError(f"Файл {file_path} не содержит чисел")
    return result


def load_series_csv(path: PathLike) -> List[float]:
    """Читает числа из .csv — через разделитель, возможно, с заголовком."""
    file_path = Path(path)
    if not file_path.exists():
        raise ValueError(f"Файл не найден: {file_path}")

    result: List[float] = []
    try:
        with file_path.open("r", encoding="utf-8") as f:
            for lineno, raw in enumerate(f, start=1):
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                tokens = [t for t in _SEPARATORS.split(line) if t]
                if not tokens:
                    continue
                # Пропускаем заголовок: первая строка, где первое поле не число
                try:
                    values = [float(t) for t in tokens]
                except ValueError:
                    if lineno == 1:
                        continue  # считаем это заголовком
                    raise ValueError(
                        f"{file_path}:{lineno}: строка '{line}' содержит "
                        f"нечисловые значения"
                    )
                result.extend(values)
    except OSError as err:
        raise ValueError(f"Не удалось прочитать файл {file_path}: {err}") from err

    if not result:
        raise ValueError(f"Файл {file_path} не содержит чисел")
    return result


def load_series_auto(path: PathLike) -> List[float]:
    """Автоматически выбирает парсер по расширению.

    .json       → load_series_json
    .txt, .dat  → load_series_txt
    .csv, .tsv  → load_series_csv
    иначе       → пробует csv, при ошибке — txt
    """
    from .io_json import load_series_json

    suffix = Path(path).suffix.lower()
    if suffix == ".json":
        return load_series_json(path)
    if suffix in {".txt", ".dat"}:
        return load_series_txt(path)
    if suffix in {".csv", ".tsv"}:
        return load_series_csv(path)
    try:
        return load_series_csv(path)
    except ValueError:
        return load_series_txt(path)
import sys
from typing import List


def read_numbers(source: str) -> List[float]:
    """Читает ряд из текстового файла: одно число в строке.

    source == "-" — читать из stdin.
    Пустые строки пропускаются.
    Нечисловая строка -> ValueError с указанием файла и номера строки.
    """
    if source == "-":
        lines = sys.stdin.read().splitlines()
        origin = "stdin"
    else:
        with open(source, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        origin = source

    data: List[float] = []
    for lineno, raw in enumerate(lines, start=1):
        text = raw.strip()
        if not text:
            continue
        try:
            data.append(float(text.replace(",", ".")))
        except ValueError:
            raise ValueError(
                f"{origin}: строка {lineno} — не числовое значение: {text!r}"
            ) from None
    return data
