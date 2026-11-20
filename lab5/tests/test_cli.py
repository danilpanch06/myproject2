"""Тесты CLI (argparse + коды выхода)."""
import io
from contextlib import redirect_stdout, redirect_stderr

import pytest

from main import build_parser, main


class TestParser:
    def test_defaults(self):
        args = build_parser().parse_args([])
        assert args.kind == "sine"
        assert args.n == 20
        assert args.window == 3
        assert args.alpha == pytest.approx(0.3)
        assert args.seed == 42

    def test_custom_values(self):
        args = build_parser().parse_args(
            ["--kind", "trend", "--n", "50", "--window", "5",
             "--alpha", "0.8", "--seed", "7"]
        )
        assert args.kind == "trend"
        assert args.n == 50
        assert args.window == 5
        assert args.alpha == pytest.approx(0.8)
        assert args.seed == 7

    def test_invalid_kind_rejected(self):
        with pytest.raises(SystemExit):
            build_parser().parse_args(["--kind", "waves"])


def _run_main(argv):
    """Запускает main() и возвращает (код_выхода, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = main(argv)
    return code, out.getvalue(), err.getvalue()


class TestMain:
    def test_valid_run_returns_zero(self):
        code, out, err = _run_main(
            ["--kind", "sine", "--n", "10", "--window", "3", "--seed", "1"]
        )
        assert code == 0
        assert "Исходный ряд" in out
        assert "SMA" in out
        assert "EMA" in out

    def test_window_greater_than_n_returns_one(self):
        code, out, err = _run_main(["--kind", "sine", "--n", "5", "--window", "10"])
        assert code == 1
        assert "Ошибка" in err

    def test_even_window_prints_no_centered(self):
        code, out, err = _run_main(["--kind", "sine", "--n", "10", "--window", "4"])
        assert code == 0
        assert "Центрированное MA" not in out

    def test_odd_window_prints_centered(self):
        code, out, err = _run_main(["--kind", "sine", "--n", "10", "--window", "3"])
        assert code == 0
        assert "Центрированное MA" in out

    def test_output_reproducible_with_same_seed(self):
        first = _run_main(["--kind", "random", "--n", "15", "--seed", "9"])
        second = _run_main(["--kind", "random", "--n", "15", "--seed", "9"])
        assert first[0] == second[0] == 0
        assert first[1] == second[1]
