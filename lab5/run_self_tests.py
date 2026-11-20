"""Автопроверка проекта без pytest.

Запуск:
    python run_self_tests.py

Скрипт находит все функции test_* в tests/*.py, запускает их и печатает
сводку. Если настоящей библиотеки pytest нет, используется встроенная
мини-заглушка (pytest.approx, pytest.raises) — этого достаточно,
так как тесты проекта не зависят от фикстур.
"""
from __future__ import annotations

import contextlib
import importlib
import inspect
import math
import sys
import traceback
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

TESTS_DIR = PROJECT_ROOT / "tests"


def _install_pytest_shim() -> None:
    """Мини-заглушка pytest для запуска без установленной библиотеки."""

    class _Approx:
        """Аналог pytest.approx — сравнение чисел с допуском."""

        def __init__(self, expected: Any, rel: float = 1e-6, abs: float = 1e-12):
            self.expected = expected
            self.rel = rel
            self.abs = abs

        def _equal(self, a: Any, b: Any) -> bool:
            if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
                return len(a) == len(b) and all(
                    self._equal(x, y) for x, y in zip(a, b)
                )
            try:
                return math.isclose(float(a), float(b),
                                    rel_tol=self.rel, abs_tol=self.abs)
            except (TypeError, ValueError):
                return a == b

        def __eq__(self, other: Any) -> bool:
            return self._equal(other, self.expected)

        def __req__(self, other: Any) -> bool:
            return self._equal(other, self.expected)

        def __repr__(self) -> str:
            return f"approx({self.expected!r})"

    def approx(expected: Any, rel: float = 1e-6, abs: float = 1e-12) -> _Approx:
        return _Approx(expected, rel=rel, abs=abs)

    class _RaisesCtx:
        """Контекстный менеджер: ожидаем, что блок возбудит исключение."""

        def __init__(self, exc_type: type):
            self.exc_type = exc_type
            self.value = None

        def __enter__(self):
            return self

        def __exit__(self, exc_type_, exc_val, tb):
            if exc_type_ is None:
                raise AssertionError(
                    f"Ожидалось исключение {self.exc_type.__name__}, "
                    f"но ничего не возбуждено"
                )
            if not issubclass(exc_type_, self.exc_type):
                return False
            self.value = exc_val
            return True

    def raises(exc_type: type) -> _RaisesCtx:
        return _RaisesCtx(exc_type)

    shim = ModuleType("pytest")
    shim.approx = approx
    shim.raises = raises
    shim.mark = type("M", (), {"parametrize": lambda *a, **k: (lambda f: f)})
    sys.modules.setdefault("pytest", shim)


def _collect_test_functions(module: ModuleType) -> List[Tuple[str, Callable]]:
    """Собирает тесты: функции test_* и методы test_* в классах Test*."""
    found: List[Tuple[str, Callable]] = []
    for name, obj in vars(module).items():
        if name.startswith("test_") and inspect.isfunction(obj):
            found.append((name, obj))
        elif name.startswith("Test") and inspect.isclass(obj):
            for meth_name, meth in vars(obj).items():
                if meth_name.startswith("test_") and callable(meth):
                    # Привязываем метод к пустому экземпляру (у тестовых
                    # классов нет состояния и __init__)
                    instance = object.__new__(obj)
                    found.append(
                        (f"{name}::{meth_name}", meth.__get__(instance, obj))
                    )
    return found


def main() -> int:
    _install_pytest_shim()

    test_modules = sorted(
        p.stem for p in TESTS_DIR.glob("test_*.py") if p.is_file()
    )
    if not test_modules:
        print(f"В {TESTS_DIR} не найдено файлов test_*.py")
        return 1

    passed: List[str] = []
    failed: List[Tuple[str, str]] = []
    errors: List[Tuple[str, str]] = []

    for mod_name in test_modules:
        module = importlib.import_module(f"tests.{mod_name}")
        for func_name, func in _collect_test_functions(module):
            full_name = f"{mod_name}.{func_name}"
            try:
                func()
            except AssertionError as err:
                failed.append((full_name, str(err) or "assertion failed"))
            except Exception as err:  # noqa: BLE001 — собираем все ошибки
                errors.append((full_name, f"{type(err).__name__}: {err}"))
            else:
                passed.append(full_name)

    total = len(passed) + len(failed) + len(errors)
    print("=" * 60)
    print(f"Автопроверка num_series: {total} проверок")
    print("-" * 60)
    for name in passed:
        print(f"  [ OK ] {name}")
    for name, msg in failed:
        print(f"  [FAIL] {name} — {msg}")
    for name, msg in errors:
        print(f"  [ERR ] {name} — {msg}")
    print("-" * 60)
    print(f"Итог: пройдено {len(passed)}, провалено {len(failed)}, "
          f"ошибок {len(errors)}")
    print("=" * 60)
    return 0 if not failed and not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
