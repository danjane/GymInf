from pathlib import Path
from types import SimpleNamespace
import importlib


EXAMPLE_CONFIG = Path(__file__).resolve().parents[1] / "example_files" / "config.yaml"


def test_load_plan_returns_shared_seating_state():
    seating_plan_gui_backend = importlib.import_module("seating_plan_gui_backend")

    state = seating_plan_gui_backend.load_plan(str(EXAMPLE_CONFIG), "1ma1df01")

    assert state["layout_name"] == "pairs_4x3"
    assert "assignments" in state
    assert "date" in state
    assert "registry_file" in state


def test_save_plan_persists_assignments(monkeypatch):
    seating_plan_gui_backend = importlib.import_module("seating_plan_gui_backend")

    calls = {}

    monkeypatch.setattr(
        seating_plan_gui_backend,
        "save_seating_state",
        lambda cfg_path, course, seating_state, desks: calls.update(
            {
                "cfg_path": cfg_path,
                "course": course,
                "seating_state": seating_state,
                "desks": desks,
            }
        ),
    )

    desks = [SimpleNamespace(desk_id="R1D1", name="Albert")]
    seating_state = {"date": "2026-04-20", "layout_name": "pairs_4x3"}
    seating_plan_gui_backend.save_plan(str(EXAMPLE_CONFIG), "1ma1df01", seating_state, desks)

    assert calls["cfg_path"] == str(EXAMPLE_CONFIG)
    assert calls["course"] == "1ma1df01"
    assert calls["desks"] == desks


def test_dump_plan_pdf_exports_current_date(monkeypatch):
    seating_plan_gui_backend = importlib.import_module("seating_plan_gui_backend")

    calls = {}

    monkeypatch.setattr(
        seating_plan_gui_backend.seating_history,
        "create_pdf_for_date",
        lambda registry_file, course, date, skeleton_path, output_directory, create_if_missing=False: calls.update(
            {
                "registry_file": registry_file,
                "course": course,
                "date": date,
                "skeleton_path": skeleton_path,
                "output_directory": output_directory,
                "create_if_missing": create_if_missing,
            }
        )
        or Path("plan.pdf"),
    )

    seating_state = {
        "registry_file": Path("seatingplans.json"),
        "date": "2026-04-20",
    }

    output = seating_plan_gui_backend.dump_plan_pdf(
        str(EXAMPLE_CONFIG),
        "1ma1df01",
        seating_state,
    )

    assert output == Path("plan.pdf")
    assert calls["course"] == "1ma1df01"
    assert calls["date"] == "2026-04-20"


def test_randomize_plan_reassigns_students(monkeypatch):
    seating_plan_gui_backend = importlib.import_module("seating_plan_gui_backend")

    seating_state = {
        "desks": [
            SimpleNamespace(desk_id="R1D1"),
            SimpleNamespace(desk_id="R1D2"),
        ],
        "assignments": {"R1D1": "Albert", "R1D2": "Gabs"},
    }

    monkeypatch.setattr(
        seating_plan_gui_backend,
        "arrange_students",
        lambda students, mode, seed=None: ["Gabs", "Albert"],
    )

    assignments = seating_plan_gui_backend.randomize_plan(
        str(EXAMPLE_CONFIG),
        "1ma1df01",
        seating_state,
        seed=7,
    )

    assert assignments == {"R1D1": "Gabs", "R1D2": "Albert"}


def test_alphabetic_plan_uses_class_list_ordering():
    seating_plan_gui_backend = importlib.import_module("seating_plan_gui_backend")

    seating_state = {
        "desks": [
            SimpleNamespace(desk_id="R1D1"),
            SimpleNamespace(desk_id="R1D2"),
            SimpleNamespace(desk_id="R1D3"),
            SimpleNamespace(desk_id="R1D4"),
        ],
        "assignments": {},
    }

    assignments = seating_plan_gui_backend.alphabetic_plan(
        str(EXAMPLE_CONFIG),
        "1ma1df01",
        seating_state,
    )

    assert assignments == {
        "R1D1": "Gabs",
        "R1D2": "Marie",
        "R1D3": "Albert",
        "R1D4": "Dick",
    }


def test_alphabetic_plan_starts_at_front_left_and_leaves_empty_desks_at_back():
    seating_plan_gui_backend = importlib.import_module("seating_plan_gui_backend")

    seating_state = {
        "desks": [
            SimpleNamespace(desk_id="back_left"),
            SimpleNamespace(desk_id="front_left"),
            SimpleNamespace(desk_id="front_right"),
            SimpleNamespace(desk_id="back_right"),
        ],
        "gui_places": {
            "back_left": (0, 0),
            "front_left": (0, 6),
            "front_right": (1, 6),
            "back_right": (1, 0),
        },
        "assignments": {},
    }

    assignments = seating_plan_gui_backend.alphabetic_plan(
        str(EXAMPLE_CONFIG),
        "1ma1df01",
        seating_state,
    )

    assert assignments["front_left"] == "Gabs"
    assert assignments["front_right"] == "Marie"
    assert assignments["back_left"] == "Albert"
    assert assignments["back_right"] == "Dick"


def test_randomize_plan_moves_empty_desks_to_back(monkeypatch):
    seating_plan_gui_backend = importlib.import_module("seating_plan_gui_backend")

    seating_state = {
        "desks": [
            SimpleNamespace(desk_id="back_left"),
            SimpleNamespace(desk_id="front_left"),
            SimpleNamespace(desk_id="front_right"),
        ],
        "gui_places": {
            "back_left": (0, 0),
            "front_left": (0, 6),
            "front_right": (1, 6),
        },
        "assignments": {"back_left": "Albert", "front_left": "Gabs", "front_right": ""},
    }

    monkeypatch.setattr(
        seating_plan_gui_backend,
        "arrange_students",
        lambda students, mode, seed=None: ["Albert", "Gabs"],
    )

    assignments = seating_plan_gui_backend.randomize_plan(
        str(EXAMPLE_CONFIG),
        "1ma1df01",
        seating_state,
        seed=3,
    )

    assert assignments["front_left"] == "Albert"
    assert assignments["front_right"] == "Gabs"
    assert assignments["back_left"] == ""
