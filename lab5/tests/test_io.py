import json

import pytest

from num_series.io_json import save_series_json, load_series_json
from num_series.io_file import load_series_txt, load_series_csv, load_series_auto


def test_save_and_load_json(tmp_path):
    path = tmp_path / "s.json"
    save_series_json([1.0, 2.0, 3.0], path, meta={"kind": "sine"})
    data = load_series_json(path)
    assert data == [1.0, 2.0, 3.0]


def test_load_json_with_meta(tmp_path):
    path = tmp_path / "s.json"
    save_series_json([1.0, 2.0], path, meta={"kind": "sine", "seed": 42})
    data, meta = load_series_json(path, with_meta=True)
    assert meta["kind"] == "sine"
    assert meta["n"] == 2
    assert "created" in meta


def test_load_json_bare_list(tmp_path):
    path = tmp_path / "bare.json"
    path.write_text("[1, 2.5, -3]", encoding="utf-8")
    assert load_series_json(path) == [1.0, 2.5, -3.0]


def test_load_json_missing_data(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text('{"meta": {}}', encoding="utf-8")
    with pytest.raises(ValueError):
        load_series_json(path)


def test_load_json_not_found(tmp_path):
    with pytest.raises(ValueError):
        load_series_json(tmp_path / "nope.json")


def test_save_empty_raises(tmp_path):
    with pytest.raises(ValueError):
        save_series_json([], tmp_path / "s.json")


def test_load_txt(tmp_path):
    path = tmp_path / "s.txt"
    path.write_text("# комментарий\n1.5\n2\n\n3.5\n", encoding="utf-8")
    assert load_series_txt(path) == [1.5, 2.0, 3.5]


def test_load_txt_not_number(tmp_path):
    path = tmp_path / "s.txt"
    path.write_text("abc\n", encoding="utf-8")
    with pytest.raises(ValueError):
        load_series_txt(path)


def test_load_csv_with_header(tmp_path):
    path = tmp_path / "s.csv"
    path.write_text("value;price\n1;10\n2.5;20\n", encoding="utf-8")
    assert load_series_csv(path) == [1.0, 10.0, 2.5, 20.0]


def test_load_auto_json(tmp_path):
    path = tmp_path / "s.json"
    save_series_json([4.0, 5.0], path)
    assert load_series_auto(path) == [4.0, 5.0]

    import io
import sys as _sys

from num_series.io_file import read_numbers
from num_series.stats import coefficient_of_variation, mean, stdev


def test_read_numbers_ok(tmp_path):
    p = tmp_path / "nums.txt"
    p.write_text("1.5\n2\n-3\n\n4\n", encoding="utf-8")
    assert read_numbers(str(p)) == [1.5, 2.0, -3.0, 4.0]


def test_read_numbers_bad_line(tmp_path):
    p = tmp_path / "bad.txt"
    p.write_text("1\nabc\n3\n", encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        read_numbers(str(p))
    assert "строка 2" in str(exc.value)


def test_read_numbers_stdin(monkeypatch):
    monkeypatch.setattr(_sys, "stdin", io.StringIO("1\n2.5\n"))
    assert read_numbers("-") == [1.0, 2.5]


def test_cv_matches_manual():
    data = [1.0, 2.0, 3.0, 4.0, 5.0]
    expected = abs(stdev(data) / mean(data))
    assert coefficient_of_variation(data) == pytest.approx(expected)


def test_cv_zero_mean_returns_none():
    assert coefficient_of_variation([-1.0, 1.0]) is None

