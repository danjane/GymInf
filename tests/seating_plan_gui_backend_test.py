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
