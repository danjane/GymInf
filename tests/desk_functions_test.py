import pytest
from pathlib import Path

import desk_functions


EXAMPLE_FILES = Path(__file__).resolve().parents[1] / "example_files"


def test_standard_pairs_layout_returns_expected_grid():
    layout = desk_functions.standard_pairs_layout(6, 4)

    assert len(layout) == 24
    assert layout[:6] == [(0, 0), (1, 0), (3, 0), (4, 0), (6, 0), (7, 0)]
    assert layout[-6:] == [(0, 6), (1, 6), (3, 6), (4, 6), (6, 6), (7, 6)]


def test_load_basic_seating_plan_from_file_pads_with_empties():
    seating_plan = desk_functions.load_basic_seating_plan_from_file(
        str(EXAMPLE_FILES / "1ma1df01.txt")
    )

    assert len(seating_plan) == 24
    assert list(seating_plan.values())[:20] == ["empty"] * 20
    assert list(seating_plan.values())[-4:] == ["Dick", "Marie", "Gabs", "Albert"]


def test_load_basic_seating_plan_raises_for_more_than_24_students(tmp_path):
    class_file = tmp_path / "large_class.txt"
    class_file.write_text(
        "\n".join([f"SURNAME{i} Given{i}, Given{i}" for i in range(25)])
    )

    with pytest.raises(NotImplementedError):
        desk_functions.load_basic_seating_plan_from_file(str(class_file))
