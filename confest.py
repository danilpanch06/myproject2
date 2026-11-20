"""Настройка путей pytest: корень проекта добавляется в sys.path.

Благодаря этому пакет num_series импортируется как обычно,
где бы ни находилась папка tests.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
