from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import config
import link_gui_backend
from seating_layouts import create_pairs_layout


EXAMPLE_CONFIG = Path(__file__).resolve().parents[1] / "example_files" / "config.yaml"


def test_registry_path_uses_default_config_root(tmp_path):
    cfg = config.default_config(tmp_path)

    assert link_gui_backend._registry_path(cfg) == tmp_path / "seatingplans.json"


def test_registry_path_uses_configured_extra(tmp_path):
    cfg = config.default_config(tmp_path)
    configured = tmp_path / "custom.json"
    cfg.extras["seatingplans_registry_path"] = str(configured)

    assert link_gui_backend._registry_path(cfg) == configured


def test_find_plan_and_latest_plan():
    plans = [
        {"course": "1ma1df01", "date": "2026-04-01"},
        {"course": "1ma1df01", "date": "2026-04-03"},
        {"course": "2ma2dfb01", "date": "2026-04-02"},
    ]

    assert link_gui_backend._find_plan(plans, "1ma1df01", "2026-04-01") == plans[0]
    assert link_gui_backend._find_plan(plans, "1ma1df01", "2026-04-05") is None
    assert link_gui_backend._latest_plan(plans, "1ma1df01") == plans[1]
    assert link_gui_backend._latest_plan(plans, "missing") is None


def test_desk_layout_bounds_and_default_gui_places():
    desks = create_pairs_layout(4, 3)

    gui_places = link_gui_backend._gui_places_for_desks("pairs_4x3", desks)
    bounds = link_gui_backend._desk_layout_bounds(gui_places.values())

    assert gui_places["R1D1"] == (0, 0)
    assert gui_places["R4D6"] == (7, 6)
    assert bounds == (8, 7)


def test_gui_places_for_non_default_layout_uses_desk_coordinates():
    desks = [SimpleNamespace(desk_id="A1", x=2.5, y=3.5)]

    gui_places = link_gui_backend._gui_places_for_desks("rows_custom", desks)

    assert gui_places == {"A1": (2.5, 3.5)}


def test_save_seating_state_ignores_empty_names_and_missing_ids():
    seating_state = {
        "registry_file": Path("registry.json"),
        "date": "2026-04-07",
        "layout_name": "pairs_4x3",
        "desks": ["layout-desk"],
        "mode": "manual",
    }
    desks = [
        SimpleNamespace(desk_id="A1", name="Alice"),
        SimpleNamespace(desk_id="A2", name=""),
        SimpleNamespace(name="NoId"),
    ]

    with patch("link_gui_backend.seating_history.save_generated_plan") as save_generated_plan:
        link_gui_backend.save_seating_state(str(EXAMPLE_CONFIG), "1ma1df01", seating_state, desks)

    save_generated_plan.assert_called_once_with(
        registry_file=Path("registry.json"),
        course="1ma1df01",
        date="2026-04-07",
        layout_name="pairs_4x3",
        desks=["layout-desk"],
        assignments={"A1": "Alice"},
        mode="manual",
    )


def test_load_students_returns_codes_and_given_names():
    students_list, class_path = link_gui_backend.load_students(str(EXAMPLE_CONFIG), "1ma1df01")

    assert students_list[:2] == ["EINSTEIN Albert, Albert", "CRAMER Gabriel, Gabs"]
    assert class_path.name == "1ma1df01.txt"


def test_add_and_delete_courses_in_files(tmp_path):
    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        "\n".join(
            [
                "courses:",
                "- 1ma1df01",
                "courses_path: .",
                "config_path: .",
                "comments_path: comments.txt",
                "exam_path: .",
                "report_student_path: report_outline_student.tex",
                "report_skeleton_path: report_skeleton.tex",
            ]
        )
    )

    new_courses = link_gui_backend.add_courses_in_files(str(config_file), "2ma2dfb01", ["1ma1df01"])
    assert new_courses == ["1ma1df01", "2ma2dfb01"]
    assert (tmp_path / "2ma2dfb01.txt").read_text() == "StudentID, StudentName"

    link_gui_backend.delete_course_in_files(str(config_file), "1ma1df01")
    cfg = config.load(str(config_file))
    assert cfg.courses == ["2ma2dfb01"]


def test_build_reports_and_calculate_averages_open_outputs():
    with patch("link_gui_backend.linkComments.create_report", return_value="report.pdf"), patch(
        "link_gui_backend.open_file"
    ) as open_file:
        link_gui_backend.build_reports("config.yaml")
    open_file.assert_called_once_with("report.pdf")

    with patch("link_gui_backend.analyseNotes.dump_all", return_value="averages.xlsx"), patch(
        "link_gui_backend.open_file"
    ) as open_file:
        link_gui_backend.calculate_averages("config.yaml")
    open_file.assert_called_once_with("averages.xlsx")
